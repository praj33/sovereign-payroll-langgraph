from calendar import monthrange
import pandas as pd
from .state import PayrollState


# =================================================
# LOAD BIOMETRIC DATA (DAY 2)
# =================================================
def load_biometric(state: PayrollState) -> PayrollState:
    path = state.get("biometric_path")

    if not path:
        state.setdefault("errors", []).append("Biometric path not provided")
        return state

    try:
        df = pd.read_excel(path)
        df.columns = [str(c).strip().lower() for c in df.columns]

        base_cols = {"employeeid", "employeename", "dept"}
        day_cols = [c for c in df.columns if c.startswith("day")]

        if not base_cols.issubset(df.columns):
            state.setdefault("errors", []).append(
                f"Missing base columns: {base_cols - set(df.columns)}"
            )
            return state

        if not day_cols:
            state.setdefault("errors", []).append("No Day columns found")
            return state

        df = df[list(base_cols) + day_cols]
        state["biometric_df"] = df

        state.setdefault("warnings", []).append(
            f"Biometric loaded with {len(day_cols)} day columns"
        )

    except Exception as e:
        state.setdefault("errors", []).append(f"Biometric load failed: {e}")

    return state


# =================================================
# LOAD TIMESHEET DATA (DAY 2)
# =================================================
def load_timesheet(state: PayrollState) -> PayrollState:
    path = state.get("timesheet_path")

    if not path:
        state.setdefault("errors", []).append("Timesheet path not provided")
        return state

    try:
        df = pd.read_excel(path)
        df.columns = [str(c).strip().lower() for c in df.columns]

        required = {"employeeid", "date", "expected_hours"}
        missing = required - set(df.columns)

        if missing:
            state.setdefault("errors", []).append(
                f"Timesheet missing columns: {missing}"
            )
            return state

        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

        invalid = df["date"].isna().sum()
        if invalid > 0:
            state.setdefault("warnings", []).append(
                f"{invalid} invalid timesheet dates"
            )

        state["timesheet_df"] = df

    except Exception as e:
        state.setdefault("errors", []).append(f"Timesheet load failed: {e}")

    return state


# =================================================
# PROCESS ATTENDANCE (DAY 3)
# =================================================
def process_attendance(state: PayrollState) -> PayrollState:
    biometric_df = state.get("biometric_df")
    timesheet_df = state.get("timesheet_df")

    if biometric_df is None or timesheet_df is None:
        state.setdefault("errors", []).append(
            "Missing biometric or timesheet before attendance processing"
        )
        return state

    records = []

    expected_map = {
        (r["employeeid"], r["date"]): r["expected_hours"]
        for _, r in timesheet_df.iterrows()
    }

    base_date = timesheet_df["date"].iloc[0]
    year, month = base_date.year, base_date.month
    last_day = monthrange(year, month)[1]

    for _, row in biometric_df.iterrows():
        emp_id = row["employeeid"]

        for col in biometric_df.columns:
            if not col.startswith("day"):
                continue

            day_num = int(col.replace("day", ""))

            if day_num < 1 or day_num > last_day:
                continue

            current_date = base_date.replace(day=day_num)
            cell = str(row[col]).strip()
            anomaly = False

            if cell == "" or cell.lower() == "nan":
                in_time = None
                out_time = None
                actual_hours = 0
                status = "ABSENT"

            else:
                times = cell.split()
                if len(times) < 2:
                    in_time = None
                    out_time = None
                    actual_hours = 0
                    status = "ANOMALY"
                    anomaly = True
                else:
                    in_time = times[0]
                    out_time = times[-1]
                    t1 = pd.to_datetime(in_time)
                    t2 = pd.to_datetime(out_time)
                    actual_hours = round((t2 - t1).seconds / 3600, 2)
                    status = "PRESENT"

            expected_hours = expected_map.get((emp_id, current_date), 8)

            records.append({
                "employeeid": emp_id,
                "date": current_date,
                "in_time": in_time,
                "out_time": out_time,
                "actual_hours": actual_hours,
                "expected_hours": expected_hours,
                "status": status,
                "anomaly": anomaly,
            })

    state["attendance_df"] = pd.DataFrame(records)
    return state


# =================================================
# CALCULATE SALARY (DAY 4)
# =================================================
def calculate_salary(state: PayrollState) -> PayrollState:
    print(">>> calculate_salary NODE EXECUTED <<<")

    attendance_df = state.get("attendance_df")
    salary_path = state.get("salary_master_path")

    if attendance_df is None:
        state.setdefault("errors", []).append("Attendance data missing")
        return state

    if not salary_path:
        state.setdefault("errors", []).append("Salary master path not provided")
        return state

    try:
        salary_df = pd.read_excel(salary_path)
        salary_df.columns = [c.lower().strip() for c in salary_df.columns]

        if not {"employeeid", "monthly_salary"}.issubset(salary_df.columns):
            state.setdefault("errors", []).append(
                "Salary master missing required columns"
            )
            return state

        summary = (
            attendance_df
            .groupby("employeeid")
            .agg(
                present_days=("status", lambda x: (x == "PRESENT").sum()),
                absent_days=("status", lambda x: (x != "PRESENT").sum()),
            )
            .reset_index()
        )

        summary["total_days"] = summary["present_days"] + summary["absent_days"]

        payroll_df = summary.merge(
            salary_df,
            on="employeeid",
            how="left"
        )

        payroll_df["payable_salary"] = (
            payroll_df["monthly_salary"]
            * payroll_df["present_days"]
            / payroll_df["total_days"]
        ).round(2)

        state["payroll_df"] = payroll_df

    except Exception as e:
        state.setdefault("errors", []).append(
            f"Salary calculation failed: {e}"
        )

    return state


# =================================================
# DAY 5 PLACEHOLDERS
# =================================================
import os
from datetime import datetime

def export_excel(state: PayrollState) -> PayrollState:
    attendance_df = state.get("attendance_df")
    payroll_df = state.get("payroll_df")

    if attendance_df is None or payroll_df is None:
        state.setdefault("errors", []).append(
            "Missing data for Excel export"
        )
        return state

    try:
        os.makedirs("output", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"output/payroll_output_{timestamp}.xlsx"

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            attendance_df.to_excel(
                writer,
                sheet_name="Attendance",
                index=False
            )
            payroll_df.to_excel(
                writer,
                sheet_name="Payroll",
                index=False
            )

        state["output_path"] = output_path

    except Exception as e:
        state.setdefault("errors", []).append(
            f"Excel export failed: {e}"
        )

    return state



def attach_sovereign_meta(state: PayrollState) -> PayrollState:
    errors = state.get("errors", [])
    warnings = state.get("warnings", [])

    readiness = 100

    if errors:
        readiness -= 50
    if warnings:
        readiness -= 10

    readiness = max(readiness, 0)

    sovereign_meta = {
        "module": "Sovereign Payroll Engine",
        "version": "v1.0",
        "status": "READY" if readiness >= 80 else "NEEDS_REVIEW",
        "readiness_percent": readiness,
        "errors_count": len(errors),
        "warnings_count": len(warnings),
        "notes": "LangGraph payroll pipeline executed successfully"
    }

    state["sovereign_meta"] = sovereign_meta
    return state

from sovereign_core.evaluator import evaluate_payroll_state


def attach_sovereign_meta(state: PayrollState) -> PayrollState:
    """
    Final Sovereign evaluation node.
    Attaches readiness score, checks, and review notes.
    """
    sovereign_meta = evaluate_payroll_state(state)
    state["sovereign_meta"] = sovereign_meta
    return state


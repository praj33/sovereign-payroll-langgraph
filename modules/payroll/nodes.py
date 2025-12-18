from calendar import monthrange
import pandas as pd
from .state import PayrollState


# =================================================
# LOAD BIOMETRIC DATA
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
# LOAD TIMESHEET DATA
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
# PROCESS ATTENDANCE (DAY 3 CORE)
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

    # Expected hours lookup
    expected_map = {
        (r["employeeid"], r["date"]): r["expected_hours"]
        for _, r in timesheet_df.iterrows()
    }

    # IMPORTANT: Use FIRST timesheet date only for month/year
    base_date = timesheet_df["date"].min()
    year = base_date.year
    month = base_date.month
    last_day = monthrange(year, month)[1]

    for _, row in biometric_df.iterrows():
        emp_id = row["employeeid"]

        for col in biometric_df.columns:
            if not col.startswith("day"):
                continue

            # Extract day number safely
            try:
                day_num = int(col.replace("day", ""))
            except ValueError:
                continue

            # 🚨 HARD CALENDAR SAFETY (NO CRASH POSSIBLE)
            if day_num < 1 or day_num > last_day:
                continue

            current_date = pd.Timestamp(year=year, month=month, day=day_num).date()

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
                    try:
                        in_time = times[0]
                        out_time = times[-1]

                        t1 = pd.to_datetime(in_time)
                        t2 = pd.to_datetime(out_time)

                        actual_hours = round(
                            (t2 - t1).total_seconds() / 3600, 2
                        )
                        status = "PRESENT"
                    except Exception:
                        in_time = None
                        out_time = None
                        actual_hours = 0
                        status = "ANOMALY"
                        anomaly = True

            expected_hours = expected_map.get(
                (emp_id, current_date), 8
            )

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
# PLACEHOLDERS (DAY 4+)
# =================================================
def calculate_salary(state: PayrollState) -> PayrollState:
    return state


def export_excel(state: PayrollState) -> PayrollState:
    return state


def attach_sovereign_meta(state: PayrollState) -> PayrollState:
    return state

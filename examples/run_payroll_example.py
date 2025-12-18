import sys
import os

# -------------------------------------------------
# Ensure project root is on PYTHONPATH
# -------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)

from modules.payroll.graph import build_payroll_graph


def main():
    print("\n========== PAYROLL PIPELINE START ==========\n")

    # -------------------------------------------------
    # Build LangGraph Payroll App
    # -------------------------------------------------
    app = build_payroll_graph()

    # -------------------------------------------------
    # Initial State (INPUTS)
    # -------------------------------------------------
    state = {
        "biometric_path": "examples/biometric.xlsx",
        "timesheet_path": "examples/timesheet.xlsx",
        "salary_master_path": "examples/salary_master.xlsx",
        "warnings": [],
        "errors": [],
    }

    # -------------------------------------------------
    # Execute Payroll Graph
    # -------------------------------------------------
    result = app.invoke(state)

    print("\n========== PAYROLL RUN RESULT ==========\n")

    # -------------------------------------------------
    # Errors & Warnings
    # -------------------------------------------------
    print("Errors:")
    if result.get("errors"):
        for e in result["errors"]:
            print(" -", e)
    else:
        print(" - None")

    print("\nWarnings:")
    if result.get("warnings"):
        for w in result["warnings"]:
            print(" -", w)
    else:
        print(" - None")

    # -------------------------------------------------
    # Data Summary
    # -------------------------------------------------
    print("\nData Summary:")
    if "biometric_df" in result:
        print(" - Biometric rows:", len(result["biometric_df"]))
    if "timesheet_df" in result:
        print(" - Timesheet rows:", len(result["timesheet_df"]))
    if "attendance_df" in result:
        print(" - Attendance rows:", len(result["attendance_df"]))
    if "payroll_df" in result:
        print(" - Payroll rows:", len(result["payroll_df"]))

    # -------------------------------------------------
    # Output File
    # -------------------------------------------------
    if "output_path" in result:
        print("\nOutput File:")
        print(" -", result["output_path"])

    # -------------------------------------------------
    # Sovereign Metadata (FINAL PROOF)
    # -------------------------------------------------
    if "sovereign_meta" in result:
        print("\n========== SOVEREIGN META ==========\n")
        for key, value in result["sovereign_meta"].items():
            print(f"{key}: {value}")

    print("\n========== PAYROLL PIPELINE END ==========\n")


if __name__ == "__main__":
    main()

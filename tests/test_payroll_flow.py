import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from modules.payroll.graph import build_payroll_graph


def test_full_payroll_flow():
    app = build_payroll_graph()

    state = {
        "biometric_path": "examples/biometric.xlsx",
        "timesheet_path": "examples/timesheet.xlsx",
        "salary_master_path": "examples/salary_master.xlsx",
        "warnings": [],
        "errors": [],
    }

    result = app.invoke(state)

    assert "attendance_df" in result
    assert "payroll_df" in result
    assert "sovereign_meta" in result

    assert not result["attendance_df"].empty
    assert not result["payroll_df"].empty

    meta = result["sovereign_meta"]
    assert meta["readiness_percent"] >= 80

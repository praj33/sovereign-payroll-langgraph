from typing import Dict
from .schema import default_sovereign_meta


def evaluate_payroll_state(state: Dict) -> Dict:
    """
    Evaluates final payroll pipeline state and produces Sovereign metadata.
    """
    meta = default_sovereign_meta()
    checks = []
    score = 0

    # -------------------------------
    # CHECK 1: Inputs loaded
    # -------------------------------
    if "biometric_df" in state and "timesheet_df" in state:
        checks.append({
            "check": "inputs_loaded",
            "status": "PASS",
            "points": 20,
        })
        score += 20
    else:
        checks.append({
            "check": "inputs_loaded",
            "status": "FAIL",
            "points": 0,
        })

    # -------------------------------
    # CHECK 2: Attendance processed
    # -------------------------------
    if "attendance_df" in state and not state["attendance_df"].empty:
        checks.append({
            "check": "attendance_processed",
            "status": "PASS",
            "points": 20,
        })
        score += 20
    else:
        checks.append({
            "check": "attendance_processed",
            "status": "FAIL",
            "points": 0,
        })

    # -------------------------------
    # CHECK 3: Salary calculated
    # -------------------------------
    if "payroll_df" in state and not state["payroll_df"].empty:
        checks.append({
            "check": "salary_calculated",
            "status": "PASS",
            "points": 25,
        })
        score += 25
    else:
        checks.append({
            "check": "salary_calculated",
            "status": "FAIL",
            "points": 0,
        })

    # -------------------------------
    # CHECK 4: Excel output generated
    # -------------------------------
    if "output_path" in state:
        checks.append({
            "check": "excel_exported",
            "status": "PASS",
            "points": 20,
        })
        score += 20
    else:
        checks.append({
            "check": "excel_exported",
            "status": "FAIL",
            "points": 0,
        })

    # -------------------------------
    # CHECK 5: Error-free execution
    # -------------------------------
    errors = state.get("errors", [])
    if not errors:
        checks.append({
            "check": "no_runtime_errors",
            "status": "PASS",
            "points": 15,
        })
        score += 15
    else:
        checks.append({
            "check": "no_runtime_errors",
            "status": "FAIL",
            "points": 0,
            "details": errors,
        })

    # -------------------------------
    # Finalize meta
    # -------------------------------
    meta["checks"] = checks
    meta["score"] = score
    meta["readiness_percent"] = score

    # Human-readable notes
    if score == 100:
        meta["review_notes"].append("Pipeline is fully Sovereign-ready.")
    elif score >= 80:
        meta["review_notes"].append("Pipeline is production-capable with minor gaps.")
    else:
        meta["review_notes"].append("Pipeline requires further stabilization.")

    return meta

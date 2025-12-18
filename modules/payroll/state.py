from typing import TypedDict
import pandas as pd


class PayrollState(TypedDict, total=False):
    # Input paths
    biometric_path: str
    timesheet_path: str
    salary_master_path: str

    # DataFrames
    biometric_df: pd.DataFrame
    timesheet_df: pd.DataFrame
    attendance_df: pd.DataFrame
    payroll_df: pd.DataFrame

    # Outputs
    output_path: str
    sovereign_meta: dict

    # Diagnostics
    warnings: list
    errors: list

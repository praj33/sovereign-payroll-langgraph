# 🏛️ Sovereign Payroll Automation — LangGraph Engine (v1.0)

A production-aligned payroll automation system built using **LangGraph + Python**, fully migrated from n8n and integrated with the **Sovereign Core evaluation layer**.

This engine processes biometric attendance and timesheet data, calculates attendance and salary, exports Excel payroll reports, and automatically generates **Sovereign readiness metadata** with scores and review notes.

---

## 🎯 Project Objective

The objective of this project is to design and deliver an **end-to-end payroll processing module** that:

- Removes dependency on external workflow tools (n8n)
- Uses graph-based orchestration with LangGraph
- Produces deterministic, auditable payroll outputs
- Automatically evaluates readiness using Sovereign Core standards
- Is ready for enterprise integration and future orchestration layers

---

## ✅ Key Features

- Fully migrated from n8n to **LangGraph**
- State-driven payroll workflow
- Biometric + timesheet ingestion
- Daily attendance normalization
- Salary proration logic
- Excel export with timestamp
- Automated Sovereign evaluation (score + readiness)
- End-to-end test coverage
- Clean, scalable project structure

---

## 🧠 High-Level Architecture

The system is built around a **LangGraph state machine** that orchestrates payroll processing through sequential nodes:

1. **Load Biometric Data**: Ingests biometric attendance data from Excel files.
2. **Load Timesheet Data**: Ingests timesheet data from Excel files.
3. **Process Attendance**: Normalizes and merges biometric and timesheet data into daily attendance records.
4. **Calculate Salary**: Applies proration logic based on attendance to compute salaries.
5. **Export Excel**: Generates timestamped Excel payroll reports.
6. **Attach Sovereign Meta**: Evaluates the pipeline state using Sovereign Core standards and attaches readiness metadata.

The state is managed via `PayrollState` (TypedDict), ensuring type safety and auditability throughout the flow.

### Project Structure

```
sovereign-payroll-langgraph/
├── modules/payroll/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── graph.py           # LangGraph orchestration
│   ├── nodes.py           # Individual processing nodes
│   └── state.py           # State definitions
├── sovereign_core/
│   ├── __init__.py
│   ├── evaluator.py       # Readiness evaluation logic
│   └── schema.py          # Metadata schemas
├── examples/
│   └── run_payroll_example.py  # Usage example
├── tests/
│   └── test_payroll_flow.py    # End-to-end tests
├── output/                # Generated payroll reports
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 📘 Documentation

This section explains how to run the system, required file formats, internal node responsibilities, and known limitations.

---

## ▶️ Run Instructions

### 1. Create and activate virtual environment
```bash
python -m venv venv
Windows

bash
Copy code
venv\Scripts\activate
macOS / Linux

bash
Copy code
source venv/bin/activate
2. Install dependencies
bash
Copy code
pip install -r requirements.txt
3. Run payroll pipeline
bash
Copy code
python examples/run_payroll_example.py
📄 File Formats
biometric.xlsx
Used for raw biometric attendance.

Required Columns

employeeid

employeename

dept

Day1 … Day31

Cell Interpretation

09:41 17:21 → PRESENT

Empty cell → ABSENT

Partial or invalid value → ANOMALY

timesheet.xlsx
Defines expected daily working hours.

Required Columns

employeeid

date (YYYY-MM-DD)

expected_hours (typically 8)

salary_master.xlsx
Defines monthly salary per employee.

Required Columns

employeeid

monthly_salary

🧩 LangGraph Node Descriptions
Node Name	Description
load_biometric	Loads and validates biometric attendance data
load_timesheet	Loads and validates timesheet data
process_attendance	Converts biometric logs into daily attendance records
calculate_salary	Computes prorated salary based on attendance
export_excel	Generates Excel payroll report
attach_sovereign_meta	Attaches Sovereign readiness evaluation

Each node processes a shared LangGraph state and passes validated outputs to the next stage.

📊 Output Artifacts
Excel Output
Generated at:

bash
Copy code
output/payroll_output_YYYYMMDD_HHMMSS.xlsx
Includes:

Attendance sheet

Payroll sheet

Sovereign Metadata (Console Output)
json
Copy code
{
  "engine": "sovereign-payroll-langgraph",
  "version": "1.0.0",
  "score": 100,
  "readiness_percent": 100,
  "checks": [
    {"check": "inputs_loaded", "status": "PASS"},
    {"check": "attendance_processed", "status": "PASS"},
    {"check": "salary_calculated", "status": "PASS"},
    {"check": "excel_exported", "status": "PASS"},
    {"check": "no_runtime_errors", "status": "PASS"}
  ],
  "review_notes": [
    "Pipeline is fully Sovereign-ready."
  ]
}
🧪 Testing
Run all tests:

bash
Copy code
pytest tests/
Tests validate:

End-to-end graph execution

Attendance generation

Salary calculation

Sovereign metadata attachment

⚠️ Known Limitations
Overtime and half-day rules are not implemented in v1.0

Leave management is not included

Salary calculation is prorated by presence days only

No database persistence (file-based processing)

Designed for batch execution, not real-time streaming

These limitations are intentional and can be extended in future versions.

🔐 Sovereign Compliance
This system is:

Deterministic

Auditable

State-driven

Workflow-orchestrated

Independent of external automation tools

Production-aligned

📌 Final Status
Engine: LangGraph + Python

Version: v1.0

Readiness: 100%

Status: ✅ Submission Ready

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 📞 Support

For questions or issues, please open an issue on the GitHub repository or contact the development team.



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

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd sovereign-payroll-langgraph
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare input data**: Place your biometric, timesheet, and salary master Excel files in the `examples/` directory or update paths accordingly.

---

## 📖 Usage

### Basic Example

Run the payroll pipeline with sample data:

```python
from modules.payroll.graph import build_payroll_graph

# Build the graph
app = build_payroll_graph()

# Define initial state with input paths
state = {
    "biometric_path": "examples/biometric.xlsx",
    "timesheet_path": "examples/timesheet.xlsx",
    "salary_master_path": "examples/salary_master.xlsx",
    "warnings": [],
    "errors": [],
}

# Execute the pipeline
result = app.invoke(state)

# Check results
print("Errors:", result.get("errors", []))
print("Output file:", result.get("output_path"))
print("Sovereign score:", result["sovereign_meta"]["readiness_percent"])
```

### Command Line

Execute the example script:

```bash
python examples/run_payroll_example.py
```

This will process sample data and display a summary including errors, warnings, data counts, output path, and Sovereign readiness metadata.

---

## 🧪 Testing

Run the test suite to validate the payroll flow:

```bash
python -m pytest tests/ -v
```

The tests verify end-to-end functionality, ensuring data processing, salary calculation, Excel export, and Sovereign evaluation work correctly.

---

## 📊 Sovereign Core Integration

The system integrates with **Sovereign Core** for automated readiness evaluation. After processing, the pipeline generates metadata including:

- **Readiness Score**: Percentage (0-100) based on successful completion of key checks.
- **Detailed Checks**: Pass/fail status for inputs, processing, calculation, export, and error handling.
- **Review Notes**: Human-readable feedback on pipeline health.

Example metadata output:
```json
{
  "readiness_percent": 100,
  "score": 100,
  "checks": [
    {"check": "inputs_loaded", "status": "PASS", "points": 20},
    {"check": "attendance_processed", "status": "PASS", "points": 20},
    {"check": "salary_calculated", "status": "PASS", "points": 25},
    {"check": "excel_exported", "status": "PASS", "points": 20},
    {"check": "no_runtime_errors", "status": "PASS", "points": 15}
  ],
  "review_notes": ["Pipeline is fully Sovereign-ready."]
}
```

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make changes and add tests.
4. Run tests: `python -m pytest tests/`.
5. Commit changes: `git commit -am 'Add your feature'`.
6. Push to branch: `git push origin feature/your-feature`.
7. Submit a pull request.

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 📞 Support

For questions or issues, please open an issue on the GitHub repository or contact the development team.



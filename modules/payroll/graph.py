from langgraph.graph import StateGraph, END
from .state import PayrollState
from .nodes import (
    load_biometric,
    load_timesheet,
    process_attendance,
    calculate_salary,
    export_excel,
    attach_sovereign_meta,
)

def build_payroll_graph():
    graph = StateGraph(PayrollState)

    # Register nodes
    graph.add_node("load_biometric", load_biometric)
    graph.add_node("load_timesheet", load_timesheet)
    graph.add_node("process_attendance", process_attendance)
    graph.add_node("calculate_salary", calculate_salary)
    graph.add_node("export_excel", export_excel)
    graph.add_node("attach_sovereign_meta", attach_sovereign_meta)

    # Entry point
    graph.set_entry_point("load_biometric")

    # Execution flow
    graph.add_edge("load_biometric", "load_timesheet")
    graph.add_edge("load_timesheet", "process_attendance")
    graph.add_edge("process_attendance", "calculate_salary")
    graph.add_edge("calculate_salary", "export_excel")
    graph.add_edge("export_excel", "attach_sovereign_meta")
    graph.add_edge("attach_sovereign_meta", END)

    return graph.compile()

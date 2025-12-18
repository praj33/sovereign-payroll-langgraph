from typing import Dict, List


def default_sovereign_meta() -> Dict:
    """
    Canonical Sovereign metadata schema.
    This is the final evaluation artifact of the pipeline.
    """
    return {
        "engine": "sovereign-payroll-langgraph",
        "version": "1.0.0",

        # Evaluation results
        "checks": [],            # List of individual checks
        "score": 0,              # Total score (0–100)
        "readiness_percent": 0,  # Same as score, explicit for clarity

        # Human-readable feedback
        "review_notes": [],
    }

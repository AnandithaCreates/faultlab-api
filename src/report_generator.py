"""Structured report generation for FaultLab Person-2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPORT_FILENAME = "faultlab_report.json"


def generate_report(
    results: list[dict[str, Any]], score_data: dict[str, Any]
) -> dict[str, Any]:
    """Build and persist a JSON report for a reliability run.

    Args:
        results: Per-test validation records.
        score_data: Aggregate metrics returned by the scoring engine.

    Returns:
        The report payload written to disk.
    """

    tests_run = len(results)
    tests_passed = sum(1 for result in results if bool(result.get("passed")))
    tests_failed = tests_run - tests_passed

    # Group failure types so evaluators can quickly see which categories are
    # dominating a run without inspecting every individual test result.
    failure_breakdown: dict[str, int] = {}
    for result in results:
        failure_type = result.get("failure_type")
        if failure_type:
            failure_breakdown[failure_type] = failure_breakdown.get(failure_type, 0) + 1

    report = {
        "project": "FaultLab",
        "tests_run": tests_run,
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "reliability_score": float(score_data.get("RDI", 0.0)),
        "metrics": score_data,
        "failure_breakdown": failure_breakdown,
    }

    # Persisting a stable JSON artifact makes CI output and downstream
    # integrations easy for Person-1 or reporting systems to consume.
    report_path = Path(REPORT_FILENAME)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

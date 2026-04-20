"""Structured reporting helpers for Person-2 integration."""

from __future__ import annotations

from typing import Any


def generate_report(results: list[dict[str, Any]], score: float) -> dict[str, Any]:
    """Build a compact summary report from execution results."""

    safe_results = results if isinstance(results, list) else []
    total_tests = len(safe_results)
    passed = sum(
        1 for result in safe_results if isinstance(result, dict) and bool(result.get("passed"))
    )
    failed = max(total_tests - passed, 0)
    safe_score = round(float(score), 2) if isinstance(score, (int, float)) else 0.0

    if total_tests == 0:
        summary = "No test results were provided for scoring."
    elif failed == 0:
        summary = "All recorded tests passed successfully."
    elif passed == 0:
        summary = "All recorded tests failed validation."
    else:
        summary = f"{passed} of {total_tests} tests passed."

    return {
        "total_tests": total_tests,
        "passed": passed,
        "failed": failed,
        "score": safe_score,
        "summary": summary,
    }

"""Reliability scoring engine for FaultLab Person-2."""

from __future__ import annotations

from typing import Any


def compute_rdi(results: list[dict[str, Any]]) -> dict[str, float]:
    """Compute the Reliability Diagnostic Index (RDI).

    The score intentionally blends functional correctness and failure rejection.
    That means an API is rewarded for both serving valid traffic correctly and
    rejecting invalid traffic consistently.

    Args:
        results: Aggregated validation records from a test run.

    Returns:
        Individual metric components and the final RDI score.
    """

    valid_results = [result for result in results if result.get("failure_type") is None]
    failure_results = [result for result in results if result.get("failure_type") is not None]

    total_valid_requests = len(valid_results)
    total_failure_tests = len(failure_results)

    successful_valid_requests = sum(
        1 for result in valid_results if bool(result.get("passed"))
    )
    correctly_rejected_failures = sum(
        1 for result in failure_results if bool(result.get("passed"))
    )

    # FCS captures whether legitimate requests keep working under test.
    functional_correctness_score = _safe_divide(
        successful_valid_requests, total_valid_requests
    )
    # FRS captures whether malformed requests are blocked as intended.
    fault_rejection_score = _safe_divide(
        correctly_rejected_failures, total_failure_tests
    )
    # FIS and LSS are placeholders for now, but remain explicit so the scoring
    # model is easy to evolve without changing the report contract.
    flow_integrity_score = 1.0
    latency_stability_score = 0.9

    rdi = (
        0.35 * functional_correctness_score
        + 0.35 * fault_rejection_score
        + 0.20 * flow_integrity_score
        + 0.10 * latency_stability_score
    )

    return {
        "FCS": round(functional_correctness_score, 4),
        "FRS": round(fault_rejection_score, 4),
        "FIS": round(flow_integrity_score, 4),
        "LSS": round(latency_stability_score, 4),
        "RDI": round(rdi, 4),
    }


def _safe_divide(numerator: int, denominator: int) -> float:
    """Divide defensively to keep empty result sets from crashing scoring."""

    if denominator == 0:
        return 0.0
    return numerator / denominator

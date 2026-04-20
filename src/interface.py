"""Integration interface for the FaultLab Person-1 execution layer."""

from __future__ import annotations

from typing import Any

from .failure_injector import generate_failures
from .reporter import generate_report
from .scorer import compute_score
from .validator import validate_response


def generate_failure_variants(step: dict[str, Any]) -> list[dict[str, Any]]:
    """Return deterministic failure variants for the provided API step."""

    return generate_failures(step)


def validate_api_response(expected: str, response: dict[str, Any]) -> bool:
    """Validate a response using the existing validator implementation.

    The expected value is interpreted defensively:
    - "success", "valid", "normal" map to a non-failure request
    - any other non-empty string is treated as a failure classification
    """

    normalized_expected = (expected or "").strip().lower()
    failure_type = None if normalized_expected in {"", "success", "valid", "normal", "none"} else expected
    validation_result = validate_response(response if isinstance(response, dict) else {}, failure_type)
    return bool(validation_result.get("passed"))


def compute_reliability_score(results: list[dict[str, Any]]) -> float:
    """Compute the Person-2 compatibility reliability score."""

    return compute_score(results)


def build_test_report(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a compact report for Person-1 consumers."""

    score = compute_reliability_score(results)
    return generate_report(results, score)

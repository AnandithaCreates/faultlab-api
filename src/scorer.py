"""Lightweight scoring engine for Person-2 integration."""

from __future__ import annotations

from typing import Any


def compute_score(results: list[dict[str, Any]]) -> float:
    """Compute the percentage of passed tests.

    Malformed entries are treated as failed rather than raising errors so the
    integration layer remains resilient to partial data.
    """

    if not isinstance(results, list) or not results:
        return 0.0

    total_tests = len(results)
    passed_tests = sum(
        1 for result in results if isinstance(result, dict) and bool(result.get("passed"))
    )
    return round((passed_tests / total_tests) * 100, 2)

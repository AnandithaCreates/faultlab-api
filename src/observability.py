"""Prometheus observability primitives for FaultLab Person-2.

Observability matters in reliability testing because teams need visibility into
how many tests ran, how many failed, and whether latency behavior changed while
faults were injected. These metrics are intentionally minimal and composable.
"""

from __future__ import annotations

from prometheus_client import Counter, Histogram


TESTS_TOTAL = Counter(
    "tests_total",
    "Total number of reliability tests executed.",
)
TESTS_FAILED = Counter(
    "tests_failed",
    "Total number of reliability tests that failed validation.",
)
API_LATENCY_SECONDS = Histogram(
    "api_latency_seconds",
    "Latency distribution of API executions in seconds.",
)


def record_test_result(passed: bool) -> None:
    """Record whether a single validation result passed or failed."""

    TESTS_TOTAL.inc()
    if not passed:
        TESTS_FAILED.inc()


def record_api_latency(latency_seconds: float) -> None:
    """Record the latency of one API execution in seconds."""

    API_LATENCY_SECONDS.observe(latency_seconds)

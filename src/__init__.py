"""FaultLab API package exports."""

from .failure_injector import FAILURE_TYPES, generate_failure_variants
from .observability import (
    API_LATENCY_SECONDS,
    TESTS_FAILED,
    TESTS_TOTAL,
    record_api_latency,
    record_test_result,
)
from .report_generator import REPORT_FILENAME, generate_report
from .scoring_engine import compute_rdi
from .validator import validate_response

__all__ = [
    "API_LATENCY_SECONDS",
    "FAILURE_TYPES",
    "REPORT_FILENAME",
    "TESTS_FAILED",
    "TESTS_TOTAL",
    "compute_rdi",
    "generate_failure_variants",
    "generate_report",
    "record_api_latency",
    "record_test_result",
    "validate_response",
]

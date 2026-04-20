"""Basic tests for FaultLab"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.validator import validate_response


def test_validate_response_accepts_successful_normal_request() -> None:
    """Normal traffic should pass when the API returns a non-error status."""

    result = validate_response({"status_code": 200}, None)

    assert result == {
        "passed": True,
        "reason": "Normal request accepted as expected.",
    }


def test_validate_response_accepts_rejected_failure_request() -> None:
    """Failure-injected traffic should pass validation when rejected by the API."""

    result = validate_response({"status_code": 422}, "invalid_type")

    assert result["passed"] is True
    assert "rejected as expected" in result["reason"]


def test_validate_response_rejects_failure_case_that_succeeds() -> None:
    """A malformed request that succeeds should be flagged as a reliability issue."""

    result = validate_response({"status_code": 200}, "missing_field")

    assert result["passed"] is False

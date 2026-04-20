"""Response validation for FaultLab Person-2.

The validator treats normal traffic and failure-injected traffic differently.
That split is intentional: reliability intelligence needs to confirm both that
healthy requests succeed and that malformed requests are rejected safely.
"""

from __future__ import annotations

from typing import Any


def validate_response(
    response: dict[str, Any], failure_type: str | None
) -> dict[str, Any]:
    """Validate an API response against the expected reliability behavior.

    Args:
        response: Response metadata produced by Person-1 after executing a test.
        failure_type: ``None`` for normal traffic, otherwise the injected
            failure category under evaluation.

    Returns:
        A dictionary indicating whether the behavior matched expectations and
        why the decision was made.
    """

    status_code = int(response.get("status_code", 500))

    if failure_type is None:
        # Normal requests should succeed. A 4xx/5xx means the API rejected
        # healthy traffic and therefore failed the functional correctness check.
        passed = status_code < 400
        reason = (
            "Normal request accepted as expected."
            if passed
            else "Normal request failed unexpectedly."
        )
    else:
        # Failure-injected requests should be rejected. Accepting malformed
        # inputs is a reliability weakness because the API tolerated bad input.
        passed = status_code >= 400
        reason = (
            f"Failure case '{failure_type}' rejected as expected."
            if passed
            else f"Failure case '{failure_type}' was not rejected."
        )

    return {"passed": passed, "reason": reason}

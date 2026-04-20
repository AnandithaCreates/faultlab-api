"""Deterministic failure injection for FaultLab Person-2.

This module mutates a canonical API request definition into predictable failure
variants. Deterministic mutations are important for reliability testing because
they make failures reproducible across CI runs, local debugging sessions, and
cross-team reviews.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


FAILURE_TYPES: tuple[str, ...] = (
    "missing_field",
    "invalid_type",
    "semantic_error",
    "protocol_error",
)


def generate_failure_variants(api_step: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate deterministic failure variants for a single API step.

    The function intentionally mutates only one aspect of the request at a time
    so evaluators can clearly understand why a downstream validation passed or
    failed.

    Args:
        api_step: Canonical API request definition produced by Person-1.

    Returns:
        A list of mutated API request dictionaries. Each variant includes a
        ``failure_type`` field to preserve traceability during execution.
    """

    variants: list[dict[str, Any]] = []
    request_body = api_step.get("json")
    request_headers = api_step.get("headers")

    if isinstance(request_body, dict) and request_body:
        variants.append(_build_missing_field_variant(api_step, request_body))
        variants.append(_build_invalid_type_variant(api_step, request_body))
        variants.append(_build_semantic_error_variant(api_step, request_body))

    if isinstance(request_headers, dict) and request_headers:
        variants.append(_build_protocol_error_variant(api_step))

    return variants


def _build_missing_field_variant(
    api_step: dict[str, Any], request_body: dict[str, Any]
) -> dict[str, Any]:
    """Remove a required-looking field to simulate incomplete client payloads."""

    variant = deepcopy(api_step)
    mutated_body = deepcopy(request_body)

    # Remove the first sorted field so the mutation is stable across runs.
    field_to_remove = sorted(mutated_body)[0]
    mutated_body.pop(field_to_remove, None)

    variant["json"] = mutated_body
    variant["failure_type"] = "missing_field"
    return variant


def _build_invalid_type_variant(
    api_step: dict[str, Any], request_body: dict[str, Any]
) -> dict[str, Any]:
    """Change a value type to simulate schema-level contract violations."""

    variant = deepcopy(api_step)
    mutated_body = deepcopy(request_body)

    # Mutating the first stable field keeps the failure deterministic.
    target_field = sorted(mutated_body)[0]
    mutated_body[target_field] = _coerce_invalid_type(mutated_body[target_field])

    variant["json"] = mutated_body
    variant["failure_type"] = "invalid_type"
    return variant


def _build_semantic_error_variant(
    api_step: dict[str, Any], request_body: dict[str, Any]
) -> dict[str, Any]:
    """Inject a logically invalid value while preserving overall shape."""

    variant = deepcopy(api_step)
    mutated_body = deepcopy(request_body)

    # Semantic errors should keep the schema intact but violate business rules.
    target_field = _find_semantic_target(mutated_body)
    mutated_body[target_field] = _coerce_semantic_error(mutated_body[target_field])

    variant["json"] = mutated_body
    variant["failure_type"] = "semantic_error"
    return variant


def _build_protocol_error_variant(api_step: dict[str, Any]) -> dict[str, Any]:
    """Remove headers to simulate malformed or incomplete HTTP protocol usage."""

    variant = deepcopy(api_step)

    # Clearing headers is a simple way to trigger auth/content-type failures.
    variant["headers"] = {}
    variant["failure_type"] = "protocol_error"
    return variant


def _coerce_invalid_type(value: Any) -> Any:
    """Return a value with a mismatched type for schema rejection testing."""

    if isinstance(value, bool):
        return "not-a-boolean"
    if isinstance(value, int):
        return "not-an-integer"
    if isinstance(value, float):
        return "not-a-float"
    if isinstance(value, list):
        return "not-a-list"
    if isinstance(value, dict):
        return "not-a-dict"
    if isinstance(value, str):
        return 999
    return None


def _find_semantic_target(request_body: dict[str, Any]) -> str:
    """Choose the best field for a business-logic mutation."""

    for key in sorted(request_body):
        value = request_body[key]
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            return key
    return sorted(request_body)[0]


def _coerce_semantic_error(value: Any) -> Any:
    """Return a logically incorrect value without changing the field type."""

    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return -abs(value) if value != 0 else -1
    if isinstance(value, str):
        return ""
    if isinstance(value, list):
        return []
    if isinstance(value, dict):
        return {}
    return None

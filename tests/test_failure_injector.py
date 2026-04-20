"""Lightweight failure injector compatibility test."""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.failure_injector import generate_failures


def test_generate_failures_returns_list() -> None:
    step = {
        "method": "POST",
        "url": "/login",
        "headers": {"Authorization": "Bearer token"},
        "body": {"email": "test@test.com", "password": "123"},
    }

    result = generate_failures(step)

    assert isinstance(result, list)

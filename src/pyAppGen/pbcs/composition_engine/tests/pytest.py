"""Minimal pytest compatibility shim for focused fallback execution."""

from __future__ import annotations

from contextlib import ContextDecorator


class raises(ContextDecorator):
    def __init__(self, expected_exception):
        self.expected_exception = expected_exception
        self.caught = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            raise AssertionError(f"Expected {self.expected_exception.__name__} to be raised")
        if not issubclass(exc_type, self.expected_exception):
            return False
        self.caught = exc
        return True

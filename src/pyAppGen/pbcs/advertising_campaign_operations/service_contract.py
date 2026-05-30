"""Service contract wrapper for the advertising campaign standalone slice."""

from __future__ import annotations

from .services import service_operation_contracts


def build_service_contract() -> dict:
    return service_operation_contracts()

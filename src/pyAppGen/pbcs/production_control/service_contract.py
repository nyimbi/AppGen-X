"""Runtime-backed service evidence for the production_control PBC."""

from __future__ import annotations

from .runtime import production_control_build_service_contract


def build_service_contract() -> dict:
    """Return generated command, eventing, and handler evidence."""
    contract = production_control_build_service_contract()
    return {**contract, "pbc": "production_control", "shared_table_access": False}


SERVICE_CONTRACT = build_service_contract()

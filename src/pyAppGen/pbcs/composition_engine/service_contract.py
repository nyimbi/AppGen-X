"""Service evidence for the composition_engine PBC."""

from __future__ import annotations

from .runtime import composition_engine_build_service_contract

SERVICE_CONTRACT = {
    **composition_engine_build_service_contract(),
    "pbc": "composition_engine",
    "shared_table_access": False,
}


def build_service_contract() -> dict:
    """Return command, query, dependency, and boundary evidence."""
    return dict(SERVICE_CONTRACT)

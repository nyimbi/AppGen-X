"""Generated service evidence for the payroll_engine PBC."""

from __future__ import annotations

from .runtime import payroll_engine_build_service_contract

SERVICE_CONTRACT = {
    **payroll_engine_build_service_contract(),
    "pbc": "payroll_engine",
    "shared_table_access": False,
}


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)

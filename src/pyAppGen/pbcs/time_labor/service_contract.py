"""Generated service evidence for the time_labor PBC."""

from __future__ import annotations

from .runtime import time_labor_build_service_contract

SERVICE_CONTRACT = {
    **time_labor_build_service_contract(),
    "pbc": "time_labor",
    "shared_table_access": False,
}


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)

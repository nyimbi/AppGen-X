"""Generated service evidence for the mrp_engine PBC."""

from __future__ import annotations

from .runtime import mrp_engine_build_service_contract

SERVICE_CONTRACT = {
    **mrp_engine_build_service_contract(),
    "pbc": "mrp_engine",
    "shared_table_access": False,
}


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)

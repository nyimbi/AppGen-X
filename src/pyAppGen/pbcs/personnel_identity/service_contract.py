"""Generated service evidence for the personnel_identity PBC."""

from __future__ import annotations

from .runtime import personnel_identity_build_service_contract

SERVICE_CONTRACT = {
    **personnel_identity_build_service_contract(),
    "pbc": "personnel_identity",
    "shared_table_access": False,
}


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)

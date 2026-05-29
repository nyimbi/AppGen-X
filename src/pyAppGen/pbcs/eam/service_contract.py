"""Generated service evidence for the EAM PBC."""

from __future__ import annotations

from .runtime import eam_build_service_contract


SERVICE_CONTRACT = {
    **eam_build_service_contract(),
    "pbc": "eam",
    "shared_table_access": False,
}


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)

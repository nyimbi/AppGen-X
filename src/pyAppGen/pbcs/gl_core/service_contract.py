"""Generated service evidence for the gl_core PBC."""

from __future__ import annotations

from .runtime import gl_core_build_service_contract

SERVICE_CONTRACT = {
    **gl_core_build_service_contract(),
    "pbc": "gl_core",
    "shared_table_access": False,
}


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)

"""Generated service evidence for the api_gateway_mesh PBC."""

from __future__ import annotations

from .runtime import api_gateway_mesh_build_service_contract

SERVICE_CONTRACT = {
    **api_gateway_mesh_build_service_contract(),
    "pbc": "api_gateway_mesh",
    "shared_table_access": False,
}


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)

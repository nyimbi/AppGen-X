"""Generated service evidence for the workflow_orchestration PBC."""

from __future__ import annotations

from .runtime import workflow_orchestration_build_service_contract


SERVICE_CONTRACT = {
    **workflow_orchestration_build_service_contract(),
    "pbc": "workflow_orchestration",
    "shared_table_access": False,
}


def build_service_contract() -> dict:
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)

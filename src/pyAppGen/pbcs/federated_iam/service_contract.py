"""Generated service evidence for the federated_iam PBC."""

from __future__ import annotations

from . import services
from .runtime import federated_iam_build_service_contract as runtime_service_contract


def build_service_contract() -> dict:
    """Return command, query, eventing, and handler evidence."""
    runtime_contract = runtime_service_contract()
    manifest = services.service_operation_manifest()
    return {
        **runtime_contract,
        "ok": runtime_contract["ok"] and manifest["ok"],
        "pbc": "federated_iam",
        "command_methods": manifest["command_operations"],
        "query_methods": manifest["query_operations"],
        "operation_contracts": manifest["operation_contracts"],
        "shared_table_access": False,
    }


SERVICE_CONTRACT = build_service_contract()

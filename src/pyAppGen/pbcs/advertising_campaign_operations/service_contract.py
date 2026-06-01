"""Service contract wrapper for the advertising campaign standalone slice."""

from __future__ import annotations

from .services import service_operation_contracts
from .services import service_operation_manifest


def build_service_contract() -> dict:
    manifest = service_operation_manifest()
    contracts = service_operation_contracts()
    return {
        **contracts,
        "service_class": manifest["service_class"],
        "command_methods": tuple(manifest["command_operations"]),
        "query_methods": tuple(manifest["query_operations"]),
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": manifest["event_contract"],
        "shared_table_access": False,
    }

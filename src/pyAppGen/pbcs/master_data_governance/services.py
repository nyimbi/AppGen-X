"""Service layer for the standalone master_data_governance slice."""
from __future__ import annotations

from .standalone import MasterDataGovernanceStandaloneService
from .standalone import standalone_service_operation_contracts
from .standalone import standalone_store_smoke_test

PBC_KEY = "master_data_governance"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}


COMMAND_OPERATIONS = tuple(item["operation"] for item in standalone_service_operation_contracts()["contracts"] if item["operation_kind"] == "command")
QUERY_OPERATIONS = tuple(item["operation"] for item in standalone_service_operation_contracts()["contracts"] if item["operation_kind"] == "query")
OWNED_TABLES = standalone_service_operation_contracts()["store_contract"]["table_keys"]


class MasterDataGovernanceService(MasterDataGovernanceStandaloneService):
    """Compatibility facade that now delegates to the standalone service."""



def _operation_contract(operation: str) -> dict:
    contract = next(item for item in standalone_service_operation_contracts()["contracts"] if item["operation"] == operation)
    return {
        "operation": contract["operation"],
        "operation_kind": contract["operation_kind"],
        "owned_tables": (contract["table"],) if contract["operation_kind"] == "command" else (),
        "read_tables": (contract["table"],) if contract["operation_kind"] == "query" else (),
        "emitted_event": contract.get("event_contract") if contract["operation_kind"] == "command" else None,
        "transaction_boundary": contract["transaction_boundary"],
    }



def service_operation_manifest():
    manifest = standalone_service_operation_contracts()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "service_class": "MasterDataGovernanceService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "standalone_service_contract": manifest,
        "side_effects": (),
    }



def service_operation_contracts():
    manifest = standalone_service_operation_contracts()
    contracts = tuple(_operation_contract(item["operation"]) for item in manifest["contracts"])
    return {"ok": manifest["ok"], "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}



def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {"ok": operation in manifest["query_operations"] + manifest["command_operations"], "operation": operation, "operation_kind": kind, "payload": dict(payload or {}), "side_effects": ()}



def smoke_test():
    smoke = standalone_store_smoke_test()
    return {
        "ok": smoke["ok"] and service_operation_contracts()["ok"],
        "smoke": smoke,
        "contracts": service_operation_contracts(),
        "side_effects": (),
    }

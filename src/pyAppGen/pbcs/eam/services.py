"""Command and query service layer for the Enterprise Asset Management PBC."""

from .events import EVENT_CONTRACT
from .runtime import EAM_OWNED_TABLES
from .runtime import eam_build_api_contract
from .runtime import eam_build_service_contract
from .runtime import eam_permissions_contract


_OPERATION_EVENT_MAP = {
    "register_equipment": "EquipmentRegistered",
    "create_maintenance_plan": "MaintenancePlanReleased",
    "record_condition_reading": "ConditionReadingRecorded",
    "record_meter_reading": "MeterReadingRecorded",
    "create_safety_permit": "SafetyPermitApproved",
    "create_work_order": "WorkOrderCreated",
    "schedule_work_order": "WorkOrderScheduled",
    "issue_spare_part": "SparePartUsed",
    "complete_work_order": "MaintenanceCompleted",
}


def _owned_tables() -> tuple[str, ...]:
    return tuple(table if table.startswith("eam_") else f"eam_{table}" for table in EAM_OWNED_TABLES)



def _operation_contracts() -> tuple[dict, ...]:
    api = eam_build_api_contract()
    service = eam_build_service_contract()
    permission_index = eam_permissions_contract()["action_permissions"]
    commands = set(service["command_methods"])
    queries = set(service["query_methods"])
    contracts = []
    for route in api["route_definitions"]:
        operation = route.get("command") or route.get("query")
        operation_kind = "command" if operation in commands else "query"
        contracts.append(
            {
                "operation": operation,
                "operation_kind": operation_kind,
                "method": route["method"],
                "path": f"/api/pbc/eam{route['path']}",
                "permission": permission_index.get(operation, "eam.read" if operation_kind == "query" else "eam.execute"),
                "owned_tables": _owned_tables() if operation_kind == "command" else (),
                "read_tables": () if operation_kind == "command" else _owned_tables(),
                "emitted_event": _OPERATION_EVENT_MAP.get(operation),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": "AppGen-X",
            }
        )
    return tuple(contracts)


OPERATION_CONTRACTS = _operation_contracts()



def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item["operation"] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    governance_commands = tuple(
        item["operation"]
        for item in command_contracts
        if item["operation"] in {"configure_runtime", "set_parameter", "register_rule"}
    )
    eventful_commands = tuple(item for item in command_contracts if item["operation"] not in governance_commands)
    return {
        "ok": len(OPERATION_CONTRACTS) >= 13
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["emitted_event"] for item in eventful_commands)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["emitted_event"] is None for item in query_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": "eam",
        "operations": operations,
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "governance_commands": governance_commands,
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }



def operation_plan(operation_name, payload=None):
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    table_scope = contract["owned_tables"] or contract["read_tables"]
    return {
        "ok": bool(table_scope) and contract["event_contract"] == "AppGen-X",
        "pbc": "eam",
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "side_effects": (),
    }


class EamService:
    """Side-effect-free EAM command/query facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get("operation_kind")
        result = {
            "ok": plan["ok"],
            "pbc": "eam",
            "operation": operation_name,
            "operation_kind": operation_kind,
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }
        if operation_kind == "command":
            event_type = plan.get("emitted_event")
            result.update({"command": operation_name, "read_only": False, "outbox_table": EVENT_CONTRACT["outbox_table"], "emits": (event_type,) if event_type else ()})
        elif operation_kind == "query":
            result.update({"query": operation_name, "read_only": True, "outbox_table": None, "emits": ()})
        return result

    def __getattr__(self, operation_name):
        if operation_name in service_operation_contracts()["operations"]:
            return lambda payload=None: self._execute(operation_name, payload or {})
        raise AttributeError(operation_name)



def service_operation_manifest():
    """Return the executable service operation surface."""
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": "eam",
        "service_class": "EamService",
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }



def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = EamService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = getattr(service, operation)({"smoke": True}) if operation else {"ok": False}
    return {
        "ok": manifest["ok"] and result.get("ok") is True and result.get("operation_contract", {}).get("ok") is True,
        "manifest": manifest,
        "result": result,
        "side_effects": (),
    }

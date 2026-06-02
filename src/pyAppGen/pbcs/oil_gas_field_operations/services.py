"""Service layer for the oil_gas_field_operations PBC."""

from __future__ import annotations

from .agent import oil_gas_field_operations_assistant_preview
from .controls import oil_gas_field_operations_control_center
from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES
from .domain_depth import execute_domain_operation as execute_domain_depth_operation
from .runtime import OIL_GAS_FIELD_OPERATIONS_EMITTED_EVENT_TYPES
from .runtime import oil_gas_field_operations_build_workbench_view
from .standalone import oil_gas_field_operations_standalone_app_contract

PBC_KEY = "oil_gas_field_operations"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(("command_well", "configure_runtime", "set_parameter", "register_rule") + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS))
)
QUERY_OPERATIONS = (
    "query_workbench",
    "query_oil_gas_field_operations_controls",
    "query_oil_gas_field_operations_assistant_preview",
    "query_oil_gas_field_operations_standalone_app",
)
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES


def _operation_contract(name: str, kind: str) -> dict:
    route_table = OWNED_TABLES[0] if kind == "command" else None
    emitted_event = None
    if kind == "command":
        emitted_event = OIL_GAS_FIELD_OPERATIONS_EMITTED_EVENT_TYPES[0]
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            emitted_event = execute_domain_depth_operation(name, {}).get("emitted_event")
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": (route_table,) if route_table else (),
        "read_tables": OWNED_TABLES[:4] if kind == "query" else (),
        "emitted_event": emitted_event,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class OilGasFieldOperationsService:
    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            plan = execute_domain_depth_operation(name, payload)
            return {
                "ok": plan["ok"],
                "operation": name,
                "operation_kind": "command",
                "read_only": False,
                "payload": dict(payload),
                "operation_contract": {
                    "operation": name,
                    "operation_kind": "command",
                    "owned_tables": plan.get("owned_tables", ()),
                    "read_tables": (),
                    "emitted_event": plan.get("emitted_event"),
                    "transaction_boundary": "owned_datastore_plus_outbox",
                },
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": (plan.get("emitted_event"),),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "domain_depth": plan,
                "side_effects": (),
            }
        contract = _operation_contract(name, "command")
        return {
            "ok": True,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (contract["emitted_event"],),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "side_effects": (),
        }

    def _query(self, name, payload):
        if name == "query_workbench":
            result = oil_gas_field_operations_build_workbench_view(payload.get("tenant", "default"))
        elif name == "query_oil_gas_field_operations_controls":
            result = oil_gas_field_operations_control_center(payload.get("state"))
        elif name == "query_oil_gas_field_operations_assistant_preview":
            result = oil_gas_field_operations_assistant_preview(payload)
        elif name == "query_oil_gas_field_operations_standalone_app":
            result = oil_gas_field_operations_standalone_app_contract()
        else:
            result = {"ok": False, "reason": "unknown_query", "query": name, "side_effects": ()}
        contract = _operation_contract(name, "query")
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": contract,
            "result": result,
            "outbox_table": None,
            "emits": (),
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "OilGasFieldOperationsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def operation_plan(operation, payload=None) -> dict:
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = OilGasFieldOperationsService()
    command = getattr(service, "create_well")({"tenant": "tenant-smoke"})
    query = getattr(service, "query_oil_gas_field_operations_controls")({})
    preview = getattr(service, "query_oil_gas_field_operations_assistant_preview")(
        {
            "document_text": "Prepare morning review.",
            "instructions": "Read only.",
            "target_entity": "production_reading",
            "requested_action": "read",
        }
    )
    return {
        "ok": command["ok"] and query["ok"] and preview["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "preview": preview,
        "side_effects": (),
    }

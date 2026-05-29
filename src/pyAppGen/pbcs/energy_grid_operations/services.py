"""Executable service layer for the energy_grid_operations PBC."""

from __future__ import annotations

from . import runtime

PBC_KEY = runtime.PBC_KEY
EVENT_CONTRACT = {
    "contract": "AppGen-X",
    "topic": runtime.ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC,
    "outbox_table": runtime.ENTITY_TO_TABLE["appgen_outbox_event"],
    "inbox_table": runtime.ENTITY_TO_TABLE["appgen_inbox_event"],
    "dead_letter_table": runtime.ENTITY_TO_TABLE["appgen_dead_letter_event"],
    "retry_policy": {"max_attempts": 5, "backoff": "exponential"},
}
_ROUTE_HINTS = {
    "configure_runtime": ("POST", "/api/pbc/energy_grid_operations/runtime/configuration"),
    "set_parameter": ("POST", "/api/pbc/energy_grid_operations/runtime/parameters/preview"),
    "register_rule": ("POST", "/api/pbc/energy_grid_operations/runtime/rules/preview"),
    "receive_event": ("POST", "/api/pbc/energy_grid_operations/events/inbox"),
    "create_grid_asset": ("POST", "/grid-assets"),
    "record_load_forecast": ("POST", "/load-forecasts"),
    "review_switching_order": ("POST", "/switching-orders"),
    "approve_dispatch_instruction": ("POST", "/dispatch-instructions"),
    "simulate_outage_event": ("POST", "/outage-events"),
    "create_reliability_constraint": ("POST", "/api/pbc/energy_grid_operations/reliability-constraints"),
    "record_grid_topology": ("POST", "/api/pbc/energy_grid_operations/topology"),
    "review_energy_grid_operations_policy_rule": ("POST", "/api/pbc/energy_grid_operations/runtime/rules"),
    "approve_energy_grid_operations_runtime_parameter": ("POST", "/api/pbc/energy_grid_operations/runtime/parameters"),
    "simulate_energy_grid_operations_schema_extension": ("POST", "/api/pbc/energy_grid_operations/schema-extensions"),
    "create_energy_grid_operations_control_assertion": ("POST", "/api/pbc/energy_grid_operations/control-assertions"),
    "record_energy_grid_operations_governed_model": ("POST", "/api/pbc/energy_grid_operations/governed-models"),
    "build_workbench_view": ("GET", "/energy-grid-operations-workbench"),
    "query_timeline": ("GET", "/api/pbc/energy_grid_operations/timeline"),
}
_COMMAND_HANDLERS = {
    "configure_runtime": runtime.energy_grid_operations_configure_runtime,
    "set_parameter": runtime.energy_grid_operations_set_parameter,
    "register_rule": runtime.energy_grid_operations_register_rule,
    "receive_event": runtime.energy_grid_operations_receive_event,
    "create_grid_asset": runtime.energy_grid_operations_create_grid_asset,
    "record_load_forecast": runtime.energy_grid_operations_record_load_forecast,
    "review_switching_order": runtime.energy_grid_operations_review_switching_order,
    "approve_dispatch_instruction": runtime.energy_grid_operations_approve_dispatch_instruction,
    "simulate_outage_event": runtime.energy_grid_operations_simulate_outage_event,
    "create_reliability_constraint": runtime.energy_grid_operations_create_reliability_constraint,
    "record_grid_topology": runtime.energy_grid_operations_record_grid_topology,
    "review_energy_grid_operations_policy_rule": runtime.energy_grid_operations_review_energy_grid_operations_policy_rule,
    "approve_energy_grid_operations_runtime_parameter": runtime.energy_grid_operations_approve_energy_grid_operations_runtime_parameter,
    "simulate_energy_grid_operations_schema_extension": runtime.energy_grid_operations_simulate_energy_grid_operations_schema_extension,
    "create_energy_grid_operations_control_assertion": runtime.energy_grid_operations_create_energy_grid_operations_control_assertion,
    "record_energy_grid_operations_governed_model": runtime.energy_grid_operations_record_energy_grid_operations_governed_model,
}
_QUERY_HANDLERS = {
    "build_workbench_view": runtime.energy_grid_operations_build_workbench_view,
    "query_timeline": runtime.energy_grid_operations_query_timeline,
}


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    preview = runtime.energy_grid_operations_operation_preview(operation, payload)
    if not preview["ok"]:
        return preview
    method, path = _ROUTE_HINTS[operation]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": preview["operation_kind"],
        "route": {"method": method, "path": path},
        "permission": preview["permission"],
        "owned_tables": preview.get("owned_tables", ()),
        "read_tables": preview.get("read_tables", ()),
        "emitted_event": preview.get("emitted_event"),
        "event_contract": preview.get("event_contract"),
        "transaction_boundary": preview.get("transaction_boundary", "read_only_projection"),
        "payload_keys": preview.get("payload_keys", ()),
        "side_effects": (),
    }


class EnergyGridOperationsService:
    """In-memory executable service for standalone one-PBC use."""

    def __init__(self, state: dict | None = None):
        self.state = runtime.energy_grid_operations_empty_state() if state is None else state

    def __getattr__(self, name: str):
        if name in _COMMAND_HANDLERS or name in _QUERY_HANDLERS:
            return lambda payload=None, _name=name: self.execute(_name, payload or {})
        raise AttributeError(name)

    def execute(self, operation: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        plan = operation_plan(operation, payload)
        if not plan["ok"]:
            return {"ok": False, "operation": operation, "service_contract": plan, "side_effects": ()}
        if operation in _COMMAND_HANDLERS:
            result = _COMMAND_HANDLERS[operation](self.state, payload)
            if result.get("state") is not None:
                self.state = result["state"]
            return {
                "ok": result["ok"],
                "operation": operation,
                "operation_kind": "command",
                "result": result,
                "service_contract": plan,
                "read_only": False,
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": (result.get("emitted_event"),) if result.get("emitted_event") else (),
                "state": self.state,
                "side_effects": (),
            }
        result = _QUERY_HANDLERS[operation](self.state, payload)
        return {
            "ok": result["ok"],
            "operation": operation,
            "operation_kind": "query",
            "result": result,
            "service_contract": plan,
            "read_only": True,
            "outbox_table": None,
            "emits": (),
            "state": self.state,
            "side_effects": (),
        }

    def query_service_contract(self, payload: dict | None = None) -> dict:
        return {"ok": True, "result": service_operation_manifest(), "payload": dict(payload or {}), "side_effects": ()}

    def close(self) -> None:
        return None


def service_operation_contracts() -> dict:
    contracts = tuple(operation_plan(operation) for operation in _COMMAND_HANDLERS) + tuple(
        operation_plan(operation) for operation in _QUERY_HANDLERS
    )
    return {
        "ok": all(item["ok"] for item in contracts),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in contracts),
        "command_operations": tuple(operation for operation in _COMMAND_HANDLERS),
        "query_operations": tuple(operation for operation in _QUERY_HANDLERS),
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def standalone_service_operation_contracts() -> dict:
    contracts = service_operation_contracts()
    return {
        "format": "appgen.energy-grid-operations-standalone-service-contract.v2",
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "contracts": contracts["contracts"],
        "event_contract": EVENT_CONTRACT,
        "state_model": "in_memory_owned_state",
        "side_effects": (),
    }


def service_operation_manifest() -> dict:
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": "EnergyGridOperationsService",
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = EnergyGridOperationsService()
    created = service.execute(
        "create_grid_asset",
        {
            "asset_id": "asset_service_smoke",
            "tenant": "tenant_service",
            "asset_type": "breaker",
            "asset_name": "Service Smoke Breaker",
            "voltage_kv": 11,
            "substation_id": "sub_service",
            "feeder_id": "feeder_service",
            "normal_state": "closed",
        },
    )
    workbench = service.execute("build_workbench_view", {"tenant": "tenant_service"})
    return {
        "ok": created["ok"] and workbench["ok"] and service_operation_contracts()["ok"],
        "created": created,
        "workbench": workbench,
        "side_effects": (),
    }

"""Service layer for the hotel_revenue_management standalone slice."""

from __future__ import annotations

from . import runtime
from .domain_depth import DOMAIN_OPERATION_LABELS


PBC_KEY = runtime.PBC_KEY
EVENT_CONTRACT = {
    "contract": "AppGen-X",
    "topic": runtime.HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "retry_policy": {"max_attempts": 5, "backoff": "exponential"},
}


_COMMAND_HANDLERS = {
    "configure_runtime": lambda state, payload: runtime.hotel_revenue_management_configure_runtime(state, payload),
    "set_parameter": lambda state, payload: runtime.hotel_revenue_management_set_parameter(
        state, payload.get("name") or payload.get("parameter_key"), payload.get("value", payload.get("parameter_value"))
    ),
    "register_rule": lambda state, payload: runtime.hotel_revenue_management_register_rule(state, payload),
    "register_schema_extension": lambda state, payload: runtime.hotel_revenue_management_register_schema_extension(
        state, payload.get("table") or payload.get("owned_table"), payload.get("fields") or payload.get("extension_fields")
    ),
    "receive_event": lambda state, payload: runtime.hotel_revenue_management_receive_event(state, payload),
    "command_room_type": lambda state, payload: runtime.hotel_revenue_management_command_room_type(state, payload),
    "create_room_type": lambda state, payload: runtime.hotel_revenue_management_create_room_type(state, payload),
    "record_rate_plan": lambda state, payload: runtime.hotel_revenue_management_record_rate_plan(state, payload),
    "review_channel_inventory": lambda state, payload: runtime.hotel_revenue_management_review_channel_inventory(state, payload),
    "approve_demand_forecast": lambda state, payload: runtime.hotel_revenue_management_approve_demand_forecast(state, payload),
    "simulate_overbooking_policy": lambda state, payload: runtime.hotel_revenue_management_simulate_overbooking_policy(state, payload),
    "create_yield_decision": lambda state, payload: runtime.hotel_revenue_management_create_yield_decision(state, payload),
    "record_revenue_snapshot": lambda state, payload: runtime.hotel_revenue_management_record_revenue_snapshot(state, payload),
    "review_hotel_revenue_management_policy_rule": lambda state, payload: runtime.hotel_revenue_management_review_hotel_revenue_management_policy_rule(state, payload),
    "approve_hotel_revenue_management_runtime_parameter": lambda state, payload: runtime.hotel_revenue_management_approve_hotel_revenue_management_runtime_parameter(state, payload),
    "simulate_hotel_revenue_management_schema_extension": lambda state, payload: runtime.hotel_revenue_management_simulate_hotel_revenue_management_schema_extension(state, payload),
    "create_hotel_revenue_management_control_assertion": lambda state, payload: runtime.hotel_revenue_management_create_hotel_revenue_management_control_assertion(state, payload),
    "record_hotel_revenue_management_governed_model": lambda state, payload: runtime.hotel_revenue_management_record_hotel_revenue_management_governed_model(state, payload),
    "operate_hotel_revenue_management_13": lambda state, payload: runtime.hotel_revenue_management_operate_hotel_revenue_management_13(state, payload),
    "operate_hotel_revenue_management_14": lambda state, payload: runtime.hotel_revenue_management_operate_hotel_revenue_management_14(state, payload),
    "operate_hotel_revenue_management_15": lambda state, payload: runtime.hotel_revenue_management_operate_hotel_revenue_management_15(state, payload),
    "operate_hotel_revenue_management_16": lambda state, payload: runtime.hotel_revenue_management_operate_hotel_revenue_management_16(state, payload),
    "operate_hotel_revenue_management_17": lambda state, payload: runtime.hotel_revenue_management_operate_hotel_revenue_management_17(state, payload),
    "operate_hotel_revenue_management_18": lambda state, payload: runtime.hotel_revenue_management_operate_hotel_revenue_management_18(state, payload),
    "run_advanced_assessment": lambda state, payload: runtime.hotel_revenue_management_run_advanced_assessment(state, payload),
    "parse_document_instruction": lambda state, payload: runtime.hotel_revenue_management_parse_document_instruction(
        payload.get("document"), payload.get("instruction")
    ),
}
_QUERY_HANDLERS = {
    "query_workbench": lambda state, payload: runtime.hotel_revenue_management_query_workbench(state, payload),
    "build_workbench_view": lambda state, payload: runtime.hotel_revenue_management_build_workbench_view(
        state, payload.get("tenant", "default")
    ),
}

COMMAND_OPERATIONS = tuple(_COMMAND_HANDLERS)
QUERY_OPERATIONS = tuple(_QUERY_HANDLERS)
OWNED_TABLES = runtime.HOTEL_REVENUE_MANAGEMENT_OWNED_TABLES


def _operation_contract(name: str, kind: str) -> dict:
    target_table = runtime.HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_TABLE.get(name)
    emitted_event = runtime.HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT.get(name)
    route = next(
        (route for route, operation in runtime.HOTEL_REVENUE_MANAGEMENT_ROUTE_TO_OPERATION.items() if operation == name),
        None,
    )
    return {
        "operation": name,
        "label": DOMAIN_OPERATION_LABELS.get(name, name.replace("_", " ")),
        "operation_kind": kind,
        "route": route,
        "permission": f"{PBC_KEY}.operate",
        "owned_tables": (target_table,) if kind == "command" and target_table else (),
        "read_tables": runtime.HOTEL_REVENUE_MANAGEMENT_BUSINESS_TABLES[:3] if kind == "query" else (),
        "emitted_event": emitted_event if kind == "command" else None,
        "event_contract": "AppGen-X",
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class HotelRevenueManagementService:
    """Stateful, side-effect-free service harness for focused package tests."""

    def __init__(self, state: dict | None = None) -> None:
        self.state = runtime.hotel_revenue_management_empty_state() if state is None else state

    def __getattr__(self, name: str):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        result = _COMMAND_HANDLERS[name](self.state, dict(payload or {}))
        if "state" in result:
            self.state = result["state"]
        return {
            **result,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload or {}),
            "operation_contract": _operation_contract(name, "command"),
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (() if result.get("event") is None else (result["event"]["event_type"],)),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        result = _QUERY_HANDLERS[name](self.state, dict(payload or {}))
        return {
            **result,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload or {}),
            "operation_contract": _operation_contract(name, "query"),
            "outbox_table": None,
            "emits": (),
            "transaction_boundary": "read_only_projection",
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "HotelRevenueManagementService",
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


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "operation_contract": _operation_contract(operation, kind) if operation in manifest["query_operations"] + manifest["command_operations"] else None,
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = HotelRevenueManagementService()
    config = service.configure_runtime(
        {
            "database_backend": "postgresql",
            "event_topic": runtime.HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        }
    )
    room = service.command_room_type(
        {
            "tenant": "tenant-smoke",
            "hotel_id": "hotel-smoke",
            "code": "STD",
            "physical_rooms": 8,
            "maintenance_holdback": 1,
            "complimentary_allotment": 0,
            "capacity_adults": 2,
            "capacity_children": 1,
        }
    )
    query = service.query_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": config["ok"] and room["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": room,
        "query": query,
        "side_effects": (),
    }

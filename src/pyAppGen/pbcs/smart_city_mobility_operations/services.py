"""Service layer for the smart_city_mobility_operations PBC."""

from __future__ import annotations

from .domain_depth import (
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_QUERY_SPECS,
    DOMAIN_RECORD_SPECS,
    PBC_KEY,
    execute_domain_operation,
    operation_spec,
    query_spec,
)
from .models import SmartCityMobilityOperationsStandaloneStore

EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
) + tuple(DOMAIN_OPERATIONS)
QUERY_OPERATIONS = tuple(spec["query"] for spec in DOMAIN_QUERY_SPECS)
OWNED_TABLES = DOMAIN_OWNED_TABLES


def _operation_contract(name: str, kind: str) -> dict:
    if kind == "command":
        spec = operation_spec(name)
        if spec is not None:
            return {
                "operation": name,
                "method": "POST",
                "path": spec["path"],
                "permission": spec["permission"],
                "operation_kind": "command",
                "owned_tables": (spec["table"],),
                "read_tables": tuple(),
                "emitted_event": spec["event"],
                "form": spec["form"],
                "wizard": spec["wizard"],
                "transaction_boundary": "owned_datastore_plus_outbox",
            }
    else:
        spec = query_spec(name)
        if spec is not None:
            return {
                "operation": name,
                "method": "GET",
                "path": spec["path"],
                "permission": spec["permission"],
                "operation_kind": "query",
                "owned_tables": (),
                "read_tables": (spec["table"],),
                "emitted_event": None,
                "form": None,
                "wizard": spec["view"],
                "transaction_boundary": "read_only_projection",
            }
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OWNED_TABLES[:2] if kind == "command" else (),
        "read_tables": OWNED_TABLES[:2] if kind == "query" else (),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class SmartCityMobilityOperationsService:
    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name in DOMAIN_OPERATIONS:
            plan = execute_domain_operation(name, payload)
            return {
                "ok": plan["ok"],
                "operation": name,
                "operation_kind": "command",
                "read_only": False,
                "payload": dict(payload),
                "operation_contract": _operation_contract(name, "command"),
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
            "emits": (contract.get("emitted_event"),),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "side_effects": (),
        }

    def _query(self, name, payload):
        contract = _operation_contract(name, "query")
        return {
            "ok": True,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": None,
            "emits": (),
            "side_effects": (),
        }


def service_operation_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "SmartCityMobilityOperationsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts():
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


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


class SmartCityMobilityOperationsStandaloneService:
    """Live package-local service backed by the standalone store."""

    def __init__(self, store: SmartCityMobilityOperationsStandaloneStore | None = None):
        self.store = store or SmartCityMobilityOperationsStandaloneStore()

    def close(self) -> None:
        self.store.close()

    def __getattr__(self, name):
        if name in DOMAIN_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        if name == "receive_event":
            return lambda payload=None: self.store.receive_event(payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        spec = operation_spec(name)
        if spec is None:
            return {"ok": False, "reason": "unknown_operation", "operation": name, "side_effects": ()}
        if name == "preview_governed_instruction":
            result = self.store.preview_governed_instruction(
                payload.get("document", ""),
                payload.get("instruction", ""),
                tenant=payload.get("tenant", "default"),
            )
        else:
            result = self.store.record_domain_item(spec["record_type"], payload)
        return {
            "ok": result.get("ok") is True,
            "operation": name,
            "operation_kind": "command",
            "payload": dict(payload),
            "table": spec["table"],
            "result": result,
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        if name == "build_workbench_view":
            result = self.store.build_workbench(payload.get("tenant", "default"))
        elif name == "build_corridor_snapshot":
            result = self.store.build_corridor_snapshot(payload.get("corridor_id", ""))
        elif name == "build_intersection_detail":
            result = self.store.build_intersection_detail(payload.get("intersection_id", ""))
        elif name == "build_readiness_scorecard":
            result = self.store.build_readiness_scorecard(payload.get("tenant", "default"))
        else:
            return {"ok": False, "reason": "unknown_query", "query": name, "side_effects": ()}
        return {
            "ok": result.get("ok") is True,
            "operation": name,
            "operation_kind": "query",
            "payload": dict(payload),
            "result": result,
            "side_effects": (),
        }


def standalone_service_operation_contracts():
    command_contracts = tuple(
        {
            "method": "POST",
            "path": spec["path"],
            "handler": spec["operation"],
            "operation": spec["operation"],
            "operation_kind": "command",
            "permission": spec["permission"],
            "table": spec["table"],
            "form": spec["form"],
            "wizard": spec["wizard"],
        }
        for spec in DOMAIN_RECORD_SPECS
    )
    query_contracts = tuple(
        {
            "method": "GET",
            "path": spec["path"],
            "handler": spec["query"],
            "operation": spec["query"],
            "operation_kind": "query",
            "permission": spec["permission"],
            "table": spec["table"],
            "form": None,
            "wizard": spec["view"],
        }
        for spec in DOMAIN_QUERY_SPECS
    )
    contracts = command_contracts + query_contracts
    return {
        "format": "appgen.smart-city-mobility-operations-standalone-service.v1",
        "ok": bool(contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def standalone_service_smoke_test():
    service = SmartCityMobilityOperationsStandaloneService()
    try:
        corridor = service.register_corridor(
            {
                "corridor_id": "c_service_smoke",
                "tenant": "tenant_smoke",
                "name": "Downtown Spine",
                "functional_class": "arterial",
                "operating_objective": "transit reliability",
            }
        )
        workbench = service.build_workbench_view({"tenant": "tenant_smoke"})
        return {
            "ok": corridor["ok"] and workbench["ok"] and standalone_service_operation_contracts()["ok"],
            "corridor": corridor,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        service.close()


def smoke_test():
    service = SmartCityMobilityOperationsService()
    command = getattr(service, COMMAND_OPERATIONS[-1])({"tenant": "tenant-smoke"})
    query = getattr(service, QUERY_OPERATIONS[0])({"tenant": "tenant-smoke"})
    return {
        "ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "side_effects": (),
    }

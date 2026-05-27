"""Command and query service layer for the composition_engine PBC."""

from __future__ import annotations

from .runtime import COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
from .runtime import COMPOSITION_ENGINE_RUNTIME_TABLES
from .runtime import composition_engine_build_api_contract
from .runtime import composition_engine_build_service_contract

EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "runtime_profile_visibility": "read_only_platform_metadata",
    "adapter": "appgen_event_adapter",
    "topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
    "inbox_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
    "outbox_table": COMPOSITION_ENGINE_RUNTIME_TABLES[0],
    "inbox_table": COMPOSITION_ENGINE_RUNTIME_TABLES[1],
    "dead_letter_table": COMPOSITION_ENGINE_RUNTIME_TABLES[2],
    "retry_policy": {"name": "composition_engine_default_retry", "max_attempts": 5, "backoff": "exponential"},
    "idempotency": {"key_fields": ("event_type", "event_id", "handler"), "storage": COMPOSITION_ENGINE_RUNTIME_TABLES[1]},
}


def _path_for(route: str) -> tuple[str, str]:
    method, path = route.split(" ", 1)
    return method, f"/api/pbc/composition_engine{path}"


def _operation_contracts() -> tuple[dict, ...]:
    api = composition_engine_build_api_contract()
    fallback_event = tuple(api["events"]["emits"])[0]
    contracts = []
    for route in api["routes"]:
        method, path = _path_for(route["route"])
        operation = route.get("command") or route.get("query")
        operation_kind = "command" if route.get("command") else "query"
        command_tables = tuple(route.get("owned_tables", ())) if operation_kind == "command" else ()
        if operation == "receive_event":
            command_tables = (COMPOSITION_ENGINE_RUNTIME_TABLES[1], COMPOSITION_ENGINE_RUNTIME_TABLES[2])
        contracts.append(
            {
                "operation": operation,
                "operation_kind": operation_kind,
                "method": method,
                "path": path,
                "permission": route["requires_permission"],
                "owned_tables": command_tables,
                "read_tables": tuple(route.get("owned_tables", ())) if operation_kind == "query" else (),
                "emitted_event": (tuple(route.get("emits", ())) or (fallback_event,))[0] if operation_kind == "command" else None,
                "consumed_events": tuple(route.get("consumes", ())),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": "AppGen-X",
            }
        )
    return tuple(contracts)


OPERATION_CONTRACTS = _operation_contracts()


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    service = composition_engine_build_service_contract()
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": service["ok"]
        and bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": "composition_engine",
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "runtime_service": service,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    table_scope = contract["owned_tables"] or contract["read_tables"]
    return {
        "ok": bool(table_scope) and contract["event_contract"] == "AppGen-X",
        "pbc": "composition_engine",
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "consumed_events": contract["consumed_events"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "side_effects": (),
    }


class CompositionEngineService:
    """Side-effect-free command/query facade."""

    def _execute(self, operation_name: str, payload: dict) -> dict:
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get("operation_kind")
        result = {
            "ok": plan["ok"],
            "pbc": "composition_engine",
            "operation": operation_name,
            "operation_kind": operation_kind,
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }
        if operation_kind == "command":
            event_type = plan.get("emitted_event")
            result.update(
                {
                    "command": operation_name,
                    "read_only": False,
                    "outbox_table": EVENT_CONTRACT["outbox_table"],
                    "emits": (event_type,) if event_type else (),
                }
            )
        elif operation_kind == "query":
            result.update({"query": operation_name, "read_only": True, "outbox_table": None, "emits": ()})
        return result

    def __getattr__(self, name: str):
        if name in {item["operation"] for item in OPERATION_CONTRACTS}:
            return lambda payload=None: self._execute(name, payload or {})
        raise AttributeError(name)


def service_operation_manifest() -> dict:
    """Return the executable service operation surface."""
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": "composition_engine",
        "service_class": "CompositionEngineService",
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = CompositionEngineService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = getattr(service, operation)({"smoke": True}) if operation else {"ok": False}
    return {
        "ok": manifest["ok"] and result.get("ok") is True and result.get("operation_contract", {}).get("ok") is True,
        "manifest": manifest,
        "result": result,
        "side_effects": (),
    }

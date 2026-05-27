"""Command and query service layer for the audit_ledger PBC."""

from __future__ import annotations

from .runtime import audit_ledger_build_api_contract
from .runtime import audit_ledger_build_service_contract

EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "adapter": "appgen_event_adapter",
    "topic": "appgen.audit.events",
    "inbox_topic": "appgen.audit.events",
    "outbox_table": "audit_ledger_appgen_outbox_event",
    "inbox_table": "audit_ledger_appgen_inbox_event",
    "dead_letter_table": "audit_ledger_dead_letter_event",
    "retry_policy": {"name": "audit_ledger_default_retry", "max_attempts": 5, "backoff": "exponential"},
    "idempotency": {"key_fields": ("event_type", "event_id", "handler"), "storage": "audit_ledger_appgen_inbox_event"},
}


def _path_for(route: str) -> tuple[str, str]:
    method, path = route.split(" ", 1)
    return method, f"/api/pbc/audit_ledger{path}"


def _operation_contracts() -> tuple[dict, ...]:
    contracts = []
    for route in audit_ledger_build_api_contract()["routes"]:
        method, path = _path_for(route["route"])
        operation = route.get("command") or route.get("query")
        operation_kind = "command" if route.get("command") else "query"
        contracts.append(
            {
                "operation": operation,
                "operation_kind": operation_kind,
                "method": method,
                "path": path,
                "permission": route["requires_permission"],
                "owned_tables": tuple(route.get("owned_tables", ())) if operation_kind == "command" else (),
                "read_tables": tuple(route.get("owned_tables", ())) if operation_kind == "query" else (),
                "emitted_event": tuple(route.get("emits", ()))[0] if route.get("emits") else None,
                "consumed_events": tuple(route.get("consumes", ())),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": "AppGen-X",
            }
        )
    return tuple(contracts)


OPERATION_CONTRACTS = _operation_contracts()


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    service = audit_ledger_build_service_contract()
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": service["ok"]
        and bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": "audit_ledger",
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
        "pbc": "audit_ledger",
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


class AuditLedgerService:
    """Side-effect-free command/query facade."""

    def _execute(self, operation_name: str, payload: dict) -> dict:
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get("operation_kind")
        result = {
            "ok": plan["ok"],
            "pbc": "audit_ledger",
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
        "pbc": "audit_ledger",
        "service_class": "AuditLedgerService",
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
    service = AuditLedgerService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = getattr(service, operation)({"smoke": True}) if operation else {"ok": False}
    return {
        "ok": manifest["ok"] and result.get("ok") is True and result.get("operation_contract", {}).get("ok") is True,
        "manifest": manifest,
        "result": result,
        "side_effects": (),
    }

"""Executable service layer for the gl_core PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from .runtime import gl_core_append_ledger_event
from .runtime import gl_core_build_api_contract
from .runtime import gl_core_build_projection
from .runtime import gl_core_build_service_contract
from .runtime import gl_core_build_workbench_view
from .runtime import gl_core_create_continuous_close_snapshot
from .runtime import gl_core_empty_state
from .runtime import gl_core_generate_audit_proof
from .runtime import gl_core_predict_posting_validation
from .runtime import gl_core_receive_event
from .runtime import gl_core_register_rule
from .runtime import gl_core_suggest_reconciliation

PBC_KEY = "gl_core"


def _route_to_contract(route: dict) -> dict:
    method, path = route["route"].split(" ", 1)
    operation = route.get("command") or route.get("query")
    operation_kind = "command" if route.get("command") else "query"
    owned_tables = tuple(
        table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
        for table in route.get("owned_tables", ())
    )
    is_command = operation_kind == "command"
    if is_command and not owned_tables:
        owned_tables = (EVENT_CONTRACT["inbox_table"],)
    return {
        "operation": operation,
        "operation_kind": operation_kind,
        "method": method,
        "path": f"/api/pbc/{PBC_KEY}{path}",
        "permission": route["requires_permission"],
        "owned_tables": owned_tables if is_command else (),
        "read_tables": () if is_command else owned_tables,
        "emitted_event": (route.get("emits") or (f"{PBC_KEY}.{operation}.executed",))[0] if is_command else None,
        "consumed_event": tuple(route.get("consumes", ())),
        "idempotency_key": route.get("idempotency_key"),
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
    }


OPERATION_CONTRACTS = tuple(_route_to_contract(route) for route in gl_core_build_api_contract()["routes"])


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    runtime_service = gl_core_build_service_contract()
    return {
        "ok": runtime_service["ok"]
        and bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] or item["consumed_event"] for item in command_contracts)
        and all(item["read_tables"] for item in query_contracts),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "runtime_service_contract": runtime_service,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    return {
        "ok": bool(contract["owned_tables"] or contract["read_tables"] or contract["consumed_event"]),
        "pbc": PBC_KEY,
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "consumed_event": contract["consumed_event"],
        "idempotency_key": contract["idempotency_key"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


class GlCoreService:
    """Stateful package-local service facade over the GL runtime."""

    def __init__(self, state: dict | None = None):
        self.state = state or gl_core_empty_state()

    def _apply_command(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "append_ledger_event":
            event_type = payload.get("event_type", "JournalPosted")
            command_payload = dict(payload.get("payload", payload))
            command_payload.pop("event_type", None)
            return gl_core_append_ledger_event(self.state, event_type, command_payload)
        if operation_name == "predict_posting_validation":
            return gl_core_predict_posting_validation(self.state, payload.get("payload", payload))
        if operation_name == "create_continuous_close_snapshot":
            result = gl_core_create_continuous_close_snapshot(self.state, tenant=payload.get("tenant"))
            return {**result, "state": self.state}
        if operation_name == "suggest_reconciliation":
            source_items = tuple(payload.get("source_items", payload.get("items", ())))
            result = gl_core_suggest_reconciliation(self.state, source_items)
            next_state = {
                **self.state,
                "reconciliation_suggestions": tuple(self.state.get("reconciliation_suggestions", ())) + tuple(result.get("suggestions", ())),
            }
            return {**result, "state": next_state}
        if operation_name == "register_rule":
            return gl_core_register_rule(self.state, payload.get("rule", payload))
        if operation_name == "receive_event":
            return gl_core_receive_event(
                self.state,
                payload.get("envelope", payload),
                simulate_failure=payload.get("simulate_failure", False),
            )
        raise ValueError(f"Unsupported GL Core command: {operation_name}")

    def _apply_query(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "build_projection":
            return gl_core_build_projection(self.state, tenant=payload.get("tenant"))
        if operation_name == "generate_audit_proof":
            return gl_core_generate_audit_proof(self.state, disclosure=tuple(payload.get("disclosure", ())))
        if operation_name == "build_workbench_view":
            result = gl_core_build_workbench_view(self.state, tenant=payload.get("tenant"))
            return {"ok": True, **result}
        raise ValueError(f"Unsupported GL Core query: {operation_name}")

    def execute_operation(self, operation_name: str, payload: dict | None = None) -> dict:
        plan = operation_plan(operation_name, payload)
        if not plan["ok"]:
            return plan
        supplied = dict(payload or {})
        if plan["operation_kind"] == "command":
            result = self._apply_command(operation_name, supplied)
            if "state" in result:
                self.state = result["state"]
            return {
                "ok": result.get("ok") is True,
                "pbc": PBC_KEY,
                "operation": operation_name,
                "operation_kind": "command",
                "payload": supplied,
                "operation_contract": plan,
                "transaction_boundary": plan["transaction_boundary"],
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": (plan.get("emitted_event"),) if plan.get("emitted_event") else (),
                "result": result,
                "state": self.state,
                "side_effects": (),
            }
        result = self._apply_query(operation_name, supplied)
        return {
            "ok": result.get("ok") is True,
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": "query",
            "payload": supplied,
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "outbox_table": None,
            "emits": (),
            "result": result,
            "state": self.state,
            "side_effects": (),
        }

    def __getattr__(self, operation_name: str):
        if operation_name in service_operation_contracts()["operations"]:
            return lambda payload=None: self.execute_operation(operation_name, payload or {})
        raise AttributeError(operation_name)


def service_operation_manifest() -> dict:
    """Return the executable service operation surface."""
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": GlCoreService.__name__,
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the stateful service facade without external side effects."""
    service = GlCoreService()
    command = service.execute_operation(
        "append_ledger_event",
        {
            "event_type": "JournalPosted",
            "payload": {
                "tenant": "tenant_service_smoke",
                "lines": (
                    {"account": "cash", "debit": 100.0, "credit": 0.0},
                    {"account": "revenue", "debit": 0.0, "credit": 100.0},
                ),
            },
        },
    )
    query = service.execute_operation("build_workbench_view", {"tenant": "tenant_service_smoke"})
    manifest = service_operation_manifest()
    return {
        "ok": manifest["ok"] and command["ok"] and query["ok"],
        "manifest": manifest,
        "command": command,
        "query": query,
        "side_effects": (),
    }

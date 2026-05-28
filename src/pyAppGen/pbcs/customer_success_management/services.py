"""Service layer for the customer_success_management PBC."""
from __future__ import annotations

from .slice_app import APPGEN_X_TOPIC, PBC_KEY, build_service_contract, build_standalone_app

SERVICE_CONTRACT = build_service_contract()
COMMAND_OPERATIONS = tuple(SERVICE_CONTRACT["command_methods"])
QUERY_OPERATIONS = tuple(SERVICE_CONTRACT["query_methods"])
OWNED_TABLES = tuple(SERVICE_CONTRACT["mutates_only"])
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}


def _operation_contract(name: str, kind: str) -> dict:
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OWNED_TABLES if kind == "command" else (),
        "read_tables": OWNED_TABLES if kind == "query" else (),
        "emitted_event": "AppGen-X" if kind == "command" else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class CustomerSuccessManagementService:
    def __init__(self, database_url: str = ":memory:") -> None:
        self.app = build_standalone_app(database_url=database_url)

    def __getattr__(self, name: str):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        result = self.app.run_operation(name, payload)
        contract = _operation_contract(name, "command")
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": tuple(result.get("event", {}).get("event_type") for _ in [0] if result.get("event")),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "result": result,
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        result = self.app.run_operation(name, payload)
        contract = _operation_contract(name, "query")
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": None,
            "emits": (),
            "result": result,
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "CustomerSuccessManagementService",
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
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = CustomerSuccessManagementService()
    command = getattr(service, COMMAND_OPERATIONS[0])({"database_backend": "sqlite", "event_topic": APPGEN_X_TOPIC})
    account = service.create_success_account(
        {
            "tenant": "tenant-smoke",
            "code": "CS-SERVICE",
            "customer_name": "Service Smoke",
            "segment": "enterprise",
            "lifecycle_stage": "active",
            "owner": "csm-service",
            "renewal_date": "2026-11-30",
        }
    )
    query = service.query_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": command["ok"] and account["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "account": account,
        "query": query,
        "side_effects": (),
    }

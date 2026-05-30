"""Service layer for the student_financial_aid PBC."""
from __future__ import annotations

from .slice_app import (
    COMMAND_METHODS,
    EVENT_TABLES,
    PBC_KEY,
    QUERY_METHODS,
    RUNTIME_TABLES,
    build_release_evidence,
    build_schema_contract,
    build_service_contract,
    build_standalone_app,
)

EVENT_CONTRACT = {
    "outbox_table": EVENT_TABLES[0],
    "inbox_table": EVENT_TABLES[1],
    "dead_letter_table": EVENT_TABLES[2],
    "event_contract": "AppGen-X",
}
OWNED_TABLES = RUNTIME_TABLES


def _operation_contract(name: str, kind: str) -> dict:
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OWNED_TABLES if kind == "command" else (),
        "read_tables": OWNED_TABLES if kind == "query" else (),
        "emitted_event": "StudentFinancialAidUpdated" if kind == "command" else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class StudentFinancialAidService:
    def __init__(self, app=None) -> None:
        self.app = app or build_standalone_app()

    def __getattr__(self, name):
        if name in COMMAND_METHODS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_METHODS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name == "configure_runtime":
            result = self.app.configure_runtime(payload)
        elif name == "set_parameter":
            result = self.app.set_parameter(payload.get("name", "workbench_limit"), payload.get("value"))
        elif name == "register_rule":
            result = self.app.register_rule(payload)
        elif name == "register_schema_extension":
            result = self.app.register_schema_extension(payload.get("table", "aid_application"), payload.get("fields", {}))
        elif name == "receive_event":
            result = self.app.receive_event(payload)
        elif name == "run_advanced_assessment":
            result = self.app.run_advanced_assessment(payload)
        elif name == "parse_document_instruction":
            result = self.app.document_instruction_plan(payload.get("document", ""), payload.get("instruction", ""))
        elif name == "build_schema_contract":
            result = build_schema_contract()
        elif name == "build_service_contract":
            result = build_service_contract()
        elif name == "build_release_evidence":
            result = build_release_evidence()
        else:
            result = self.app.run_operation(name, payload)
        contract = _operation_contract(name, "command")
        event_type = result.get("event_type")
        return {
            "ok": result.get("ok") is True,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (event_type,) if event_type else (),
            "transaction_boundary": contract["transaction_boundary"],
            "result": result,
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        if name == "query_workbench":
            result = self.app.query_workbench(payload.get("tenant", "default"))
        else:
            result = self.app.build_workbench_view(payload.get("tenant", "default"))
        contract = _operation_contract(name, "query")
        return {
            "ok": result.get("ok") is True,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": None,
            "emits": (),
            "transaction_boundary": contract["transaction_boundary"],
            "result": result,
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    contract = build_service_contract()
    return {
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "service_class": "StudentFinancialAidService",
        "command_operations": COMMAND_METHODS,
        "query_operations": QUERY_METHODS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_METHODS) + tuple(_operation_contract(name, "query") for name in QUERY_METHODS)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def operation_plan(operation: str, payload=None) -> dict:
    kind = "query" if operation in QUERY_METHODS else "command"
    return {
        "ok": operation in COMMAND_METHODS + QUERY_METHODS,
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = StudentFinancialAidService()
    command = service.setup_aid_year({"tenant": "tenant-smoke", "aid_year_code": "2026-2027"})
    query = service.query_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "side_effects": (),
    }

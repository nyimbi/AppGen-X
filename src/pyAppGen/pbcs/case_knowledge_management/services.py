"""Service layer for the case_knowledge_management PBC."""

from __future__ import annotations

from .application import create_app
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import QUERY_OPERATIONS
from .models import OWNED_TABLES


PBC_KEY = "case_knowledge_management"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = (
    "command_support_case",
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
    "governed_datastore_crud",
    "run_advanced_assessment",
    "parse_document_instruction",
    *DOMAIN_OPERATIONS,
)
OWNED_TABLES = OWNED_TABLES


def _operation_contract(name: str, kind: str) -> dict:
    command = kind == "command"
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OWNED_TABLES if command else (),
        "read_tables": OWNED_TABLES if not command else (),
        "emitted_event": None if not command else {
            "command_support_case": "CaseCreated",
            "create_support_case": "CaseCreated",
            "assign_case": "CaseAssigned",
            "resolve_case": "CaseResolved",
            "publish_knowledge_article": "KnowledgeArticlePublished",
            "record_case_deflection": "CaseDeflected",
            "recommend_next_best_resolution": "AgentAssistRecommended",
        }.get(name),
        "transaction_boundary": "owned_datastore_plus_outbox" if command else "read_only_projection",
    }


class CaseKnowledgeManagementService:
    def __init__(self, state: dict | None = None) -> None:
        self.app = create_app(state)

    def __getattr__(self, name: str):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name == "command_support_case":
            result = self.app.create_support_case(payload)
        elif name == "parse_document_instruction":
            from .runtime import case_knowledge_management_parse_document_instruction

            result = case_knowledge_management_parse_document_instruction(
                payload.get("document", ""),
                payload.get("instruction", ""),
            )
        else:
            result = self.app.execute_command(name, payload)
        contract = _operation_contract(name, "command")
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (contract["emitted_event"],) if contract["emitted_event"] else (),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "state": result.get("state", self.app.snapshot()),
            "result": result,
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        result = self.app.execute_query(name, payload)
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
            "state": self.app.snapshot(),
            "result": result,
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "CaseKnowledgeManagementService",
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
    supported = operation in manifest["command_operations"] or operation in manifest["query_operations"]
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": supported,
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = CaseKnowledgeManagementService()
    command = service.command_support_case({"tenant": "tenant-smoke", "title": "Smoke"})
    query = service.query_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "side_effects": (),
    }

"""Service layer for the executable healthcare claims adjudication slice."""

from __future__ import annotations

from typing import Any
from typing import Callable

from .events import event_contract_manifest
from .runtime import BUSINESS_TABLES
from .runtime import DOMAIN_OPERATIONS
from .runtime import claims_adjudication_healthcare_approve_benefit_rule
from .runtime import claims_adjudication_healthcare_command_health_claim
from .runtime import claims_adjudication_healthcare_create_appeal
from .runtime import claims_adjudication_healthcare_create_control_assertion
from .runtime import claims_adjudication_healthcare_create_document_instruction
from .runtime import claims_adjudication_healthcare_empty_state
from .runtime import claims_adjudication_healthcare_parse_document_instruction
from .runtime import claims_adjudication_healthcare_query_workbench
from .runtime import claims_adjudication_healthcare_record_claim_line
from .runtime import claims_adjudication_healthcare_record_governed_model
from .runtime import claims_adjudication_healthcare_record_payment_integrity_case
from .runtime import claims_adjudication_healthcare_register_rule
from .runtime import claims_adjudication_healthcare_register_schema_extension
from .runtime import claims_adjudication_healthcare_review_coding_review
from .runtime import claims_adjudication_healthcare_run_advanced_assessment
from .runtime import claims_adjudication_healthcare_set_parameter
from .runtime import claims_adjudication_healthcare_simulate_denial

PBC_KEY = "claims_adjudication_healthcare"
EVENT_CONTRACT = event_contract_manifest()

COMMAND_OPERATIONS = (
    "command_health_claim",
    "create_health_claim",
    "record_claim_line",
    "review_coding_review",
    "approve_benefit_rule",
    "simulate_denial",
    "create_appeal",
    "record_payment_integrity_case",
    "register_rule",
    "set_parameter",
    "register_schema_extension",
    "create_control_assertion",
    "record_governed_model",
    "create_document_instruction",
)
QUERY_OPERATIONS = ("query_workbench", "run_advanced_assessment", "parse_document_instruction")
OWNED_TABLES = BUSINESS_TABLES


def _operation_contract(name: str, kind: str) -> dict[str, Any]:
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OWNED_TABLES if kind == "command" else (),
        "read_tables": OWNED_TABLES if kind == "query" else (),
        "permission": f"{PBC_KEY}.update" if kind == "command" else f"{PBC_KEY}.read",
        "event_contract": "AppGen-X",
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class ClaimsAdjudicationHealthcareService:
    """Stateful in-memory service surface for the PBC."""

    def __init__(self, state: dict[str, Any] | None = None) -> None:
        self.state = claims_adjudication_healthcare_empty_state() if state is None else state
        self._commands: dict[str, Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]] = {
            "command_health_claim": claims_adjudication_healthcare_command_health_claim,
            "create_health_claim": claims_adjudication_healthcare_command_health_claim,
            "record_claim_line": claims_adjudication_healthcare_record_claim_line,
            "review_coding_review": claims_adjudication_healthcare_review_coding_review,
            "approve_benefit_rule": claims_adjudication_healthcare_approve_benefit_rule,
            "simulate_denial": claims_adjudication_healthcare_simulate_denial,
            "create_appeal": claims_adjudication_healthcare_create_appeal,
            "record_payment_integrity_case": claims_adjudication_healthcare_record_payment_integrity_case,
            "register_rule": claims_adjudication_healthcare_register_rule,
            "set_parameter": lambda state, payload: claims_adjudication_healthcare_set_parameter(
                state,
                payload["name"],
                payload["value"],
                tenant=str(payload.get("tenant") or "default"),
            ),
            "register_schema_extension": claims_adjudication_healthcare_register_schema_extension,
            "create_control_assertion": claims_adjudication_healthcare_create_control_assertion,
            "record_governed_model": claims_adjudication_healthcare_record_governed_model,
            "create_document_instruction": claims_adjudication_healthcare_create_document_instruction,
        }
        self._queries: dict[str, Callable[..., dict[str, Any]]] = {
            "query_workbench": claims_adjudication_healthcare_query_workbench,
            "run_advanced_assessment": claims_adjudication_healthcare_run_advanced_assessment,
            "parse_document_instruction": lambda _state, payload: claims_adjudication_healthcare_parse_document_instruction(
                str(payload.get("document") or payload.get("document_name") or ""),
                str(payload.get("instruction") or payload.get("instruction_text") or ""),
            ),
        }

    def __getattr__(self, name: str) -> Callable[[dict[str, Any] | None], dict[str, Any]]:
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        result = self._commands[name](self.state, dict(payload))
        if result.get("state") is not None:
            self.state = result["state"]
        return {
            **result,
            "operation": name,
            "operation_kind": "command",
            "operation_contract": _operation_contract(name, "command"),
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "transaction_boundary": "owned_datastore_plus_outbox",
            "read_only": False,
        }

    def _query(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        result = self._queries[name](self.state, dict(payload))
        return {
            **result,
            "operation": name,
            "operation_kind": "query",
            "operation_contract": _operation_contract(name, "query"),
            "outbox_table": None,
            "transaction_boundary": "read_only_projection",
            "read_only": True,
        }


def service_operation_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "ClaimsAdjudicationHealthcareService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "domain_operations": DOMAIN_OPERATIONS,
        "side_effects": (),
    }


def service_operation_contracts() -> dict[str, Any]:
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


def operation_plan(operation: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    service = ClaimsAdjudicationHealthcareService()
    service.set_parameter({"name": "workbench_limit", "value": 10})
    service.approve_benefit_rule(
        {
            "plan_id": "plan-a",
            "service_code": "99213",
            "description": "Office visit",
            "effective_from": "2026-01-01",
            "effective_to": "2026-12-31",
        }
    )
    claim = service.command_health_claim(
        {
            "claim_number": "SVC-1",
            "member_id": "M-1",
            "provider_id": "P-1",
            "plan_id": "plan-a",
            "received_date": "2026-05-29",
        }
    )
    query = service.query_workbench({"tenant": "default"})
    return {
        "ok": claim["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": claim,
        "query": query,
        "side_effects": (),
    }

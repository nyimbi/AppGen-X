"""Service layer for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from typing import Any, Callable

from .domain_depth import execute_domain_operation
from .runtime import (
    CYBERSECURITY_OPERATIONS_CENTER_CONSUMED_EVENT_TYPES,
    CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES,
    CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC,
    CYBERSECURITY_OPERATIONS_CENTER_RUNTIME_TABLES,
    cybersecurity_operations_center_approve_threat_intel,
    cybersecurity_operations_center_build_case_detail,
    cybersecurity_operations_center_build_workbench_view,
    cybersecurity_operations_center_command_security_alert,
    cybersecurity_operations_center_configure_runtime,
    cybersecurity_operations_center_create_containment_action,
    cybersecurity_operations_center_create_control_assertion,
    cybersecurity_operations_center_empty_state,
    cybersecurity_operations_center_enrich_security_alert,
    cybersecurity_operations_center_generate_handoff_packet,
    cybersecurity_operations_center_parse_document_instruction,
    cybersecurity_operations_center_query_workbench,
    cybersecurity_operations_center_receive_event,
    cybersecurity_operations_center_record_governed_model,
    cybersecurity_operations_center_record_response_evidence,
    cybersecurity_operations_center_record_security_incident,
    cybersecurity_operations_center_register_rule,
    cybersecurity_operations_center_register_schema_extension,
    cybersecurity_operations_center_review_asset_exposure,
    cybersecurity_operations_center_run_advanced_assessment,
    cybersecurity_operations_center_set_parameter,
    cybersecurity_operations_center_simulate_playbook_run,
    cybersecurity_operations_center_suppress_security_alert,
    cybersecurity_operations_center_transition_alert,
)

PBC_KEY = "cybersecurity_operations_center"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
    "event_topic": CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC,
}

COMMAND_HANDLERS: dict[str, Callable[..., dict[str, Any]]] = {
    "configure_runtime": cybersecurity_operations_center_configure_runtime,
    "set_parameter": cybersecurity_operations_center_set_parameter,
    "register_rule": cybersecurity_operations_center_register_rule,
    "register_schema_extension": cybersecurity_operations_center_register_schema_extension,
    "receive_event": cybersecurity_operations_center_receive_event,
    "command_security_alert": cybersecurity_operations_center_command_security_alert,
    "transition_alert": cybersecurity_operations_center_transition_alert,
    "enrich_security_alert": cybersecurity_operations_center_enrich_security_alert,
    "suppress_security_alert": cybersecurity_operations_center_suppress_security_alert,
    "record_security_incident": cybersecurity_operations_center_record_security_incident,
    "review_asset_exposure": cybersecurity_operations_center_review_asset_exposure,
    "approve_threat_intel": cybersecurity_operations_center_approve_threat_intel,
    "simulate_playbook_run": cybersecurity_operations_center_simulate_playbook_run,
    "create_containment_action": cybersecurity_operations_center_create_containment_action,
    "record_response_evidence": cybersecurity_operations_center_record_response_evidence,
    "create_control_assertion": cybersecurity_operations_center_create_control_assertion,
    "record_governed_model": cybersecurity_operations_center_record_governed_model,
}

QUERY_HANDLERS: dict[str, Callable[..., dict[str, Any]]] = {
    "query_workbench": cybersecurity_operations_center_query_workbench,
    "build_workbench_view": cybersecurity_operations_center_build_workbench_view,
    "build_case_detail": cybersecurity_operations_center_build_case_detail,
    "generate_handoff_packet": cybersecurity_operations_center_generate_handoff_packet,
    "run_advanced_assessment": cybersecurity_operations_center_run_advanced_assessment,
    "parse_document_instruction": lambda _state, document, instruction: cybersecurity_operations_center_parse_document_instruction(
        document, instruction
    ),
}

COMMAND_OPERATIONS = tuple(COMMAND_HANDLERS)
QUERY_OPERATIONS = tuple(QUERY_HANDLERS)
OWNED_TABLES = CYBERSECURITY_OPERATIONS_CENTER_RUNTIME_TABLES
SERVICE_TO_DOMAIN_OPERATION = {
    "set_parameter": "approve_runtime_parameter",
    "register_rule": "review_policy_rule",
    "register_schema_extension": "simulate_schema_extension",
    "command_security_alert": "create_security_alert",
    "transition_alert": "triage_security_alert",
    "enrich_security_alert": "enrich_security_alert",
    "suppress_security_alert": "suppress_security_alert",
    "record_security_incident": "record_security_incident",
    "review_asset_exposure": "review_asset_exposure",
    "approve_threat_intel": "approve_threat_intel",
    "simulate_playbook_run": "simulate_playbook_run",
    "create_containment_action": "create_containment_action",
    "record_response_evidence": "record_response_evidence",
    "create_control_assertion": "create_control_assertion",
    "record_governed_model": "record_governed_model",
    "generate_handoff_packet": "generate_handoff_packet",
}


def service_operation_contract(name: str) -> dict[str, Any]:
    kind = "query" if name in QUERY_HANDLERS else "command"
    mapped_operation = SERVICE_TO_DOMAIN_OPERATION.get(name)
    if mapped_operation:
        domain = execute_domain_operation(mapped_operation)
    else:
        domain = {
            "owned_tables": (),
            "read_tables": OWNED_TABLES if kind == "query" else (),
            "emitted_event": None,
            "event_contract": "AppGen-X",
        }
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": domain.get("owned_tables", OWNED_TABLES[:2]) if kind == "command" else (),
        "read_tables": domain.get("read_tables", OWNED_TABLES[:2]) if kind == "query" else (),
        "emitted_event": domain.get("emitted_event") if kind == "command" else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
        "event_contract": "AppGen-X",
    }


class CybersecurityOperationsCenterService:
    def __init__(self, state: dict[str, Any] | None = None) -> None:
        self.state = state or cybersecurity_operations_center_empty_state()

    def __getattr__(self, name: str) -> Callable[..., dict[str, Any]]:
        if name in COMMAND_HANDLERS:
            return lambda *args, _name=name, **kwargs: self._command(_name, *args, **kwargs)
        if name in QUERY_HANDLERS:
            return lambda *args, _name=name, **kwargs: self._query(_name, *args, **kwargs)
        raise AttributeError(name)

    def _command(self, name: str, *args: Any, **kwargs: Any) -> dict[str, Any]:
        result = COMMAND_HANDLERS[name](self.state, *args, **kwargs)
        if "state" in result:
            self.state = result["state"]
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": args[0] if args else kwargs,
            "operation_contract": service_operation_contract(name),
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES,
            "consumes": CYBERSECURITY_OPERATIONS_CENTER_CONSUMED_EVENT_TYPES,
            "event_topic": EVENT_CONTRACT["event_topic"],
            "transaction_boundary": "owned_datastore_plus_outbox",
            "result": result,
            "side_effects": (),
        }

    def _query(self, name: str, *args: Any, **kwargs: Any) -> dict[str, Any]:
        result = QUERY_HANDLERS[name](self.state, *args, **kwargs)
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": args[0] if args else kwargs,
            "operation_contract": service_operation_contract(name),
            "outbox_table": None,
            "emits": (),
            "result": result,
            "side_effects": (),
        }


def service_operation_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "CybersecurityOperationsCenterService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict[str, Any]:
    contracts = tuple(service_operation_contract(name) for name in COMMAND_OPERATIONS) + tuple(
        service_operation_contract(name) for name in QUERY_OPERATIONS
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
    mapped_operation = SERVICE_TO_DOMAIN_OPERATION.get(operation)
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "domain_plan": execute_domain_operation(mapped_operation, payload or {}) if mapped_operation else None,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    service = CybersecurityOperationsCenterService()
    command = service.command_security_alert(
        {
            "tenant": "tenant-smoke",
            "severity": "high",
            "asset_ref": "srv-smoke",
            "principal_ref": "smoke-user",
            "indicator_value": "198.51.100.10",
            "detection_context": {
                "source_event_id": "evt-service",
                "detection_timestamp": "2026-05-29T00:00:00+00:00",
                "detection_rule_id": "sigma-service",
                "evidence_checksum": "sha256:service",
            },
        }
    )
    query = service.query_workbench({"tenant": "tenant-smoke"})
    detail = service.build_case_detail(command["result"]["created"][0]["id"])
    return {
        "ok": command["ok"] and query["ok"] and detail["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "detail": detail,
        "side_effects": (),
    }

"""AI agent and chatbot skill contract for the enterprise_risk_controls PBC."""

from __future__ import annotations

import hashlib
import re

from .controls import enterprise_risk_controls_mutation_preview

PBC_KEY = "enterprise_risk_controls"
AGENT_NAME = "EnterpriseRiskControlsAgent"
_DOCUMENT_ACTIONS = (
    "summarize",
    "extract_risk_facts",
    "validate_against_appetite",
    "draft_crud_plan",
)
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_SKILL_NAMES = (
    f"{PBC_KEY}.task_guidance",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.governed_delete",
    f"{PBC_KEY}.policy_explanation",
    f"{PBC_KEY}.workbench_navigation",
)
_ENTITY_TO_TABLE = {
    "risk_register": "enterprise_risk_controls_risk_register",
    "risk_policy_rule": "enterprise_risk_controls_risk_policy_rule",
    "risk_runtime_parameter": "enterprise_risk_controls_risk_runtime_parameter",
    "control_library": "enterprise_risk_controls_control_library",
    "control_test": "enterprise_risk_controls_control_test",
    "remediation_issue": "enterprise_risk_controls_remediation_issue",
    "audit_evidence_packet": "enterprise_risk_controls_audit_evidence_packet",
}
_ENTITY_TO_PERMISSION = {
    "risk_register": "enterprise_risk_controls.register_risk",
    "risk_policy_rule": "enterprise_risk_controls.configure",
    "risk_runtime_parameter": "enterprise_risk_controls.configure",
    "control_library": "enterprise_risk_controls.manage_controls",
    "control_test": "enterprise_risk_controls.manage_controls",
    "remediation_issue": "enterprise_risk_controls.manage_remediation",
    "audit_evidence_packet": "enterprise_risk_controls.compile_assurance",
}
_ENTITY_TO_EVENT = {
    "risk_register": "RiskRegistered",
    "risk_policy_rule": None,
    "risk_runtime_parameter": None,
    "control_library": "ControlDefined",
    "control_test": "ControlTestScheduled",
    "remediation_issue": "RemediationOpened",
    "audit_evidence_packet": "AssurancePacketGenerated",
}


def _owned_tables() -> tuple[str, ...]:
    return tuple(_ENTITY_TO_TABLE.values())


def _query_operations() -> tuple[str, ...]:
    from .services import service_operation_manifest

    return service_operation_manifest().get("query_operations", ())


def _command_operations() -> tuple[str, ...]:
    from .services import service_operation_manifest

    return service_operation_manifest().get("command_operations", ())


def _infer_entity(document_text: str, instruction_text: str, requested: str | None = None) -> str:
    if requested in _ENTITY_TO_TABLE:
        return requested
    combined = f"{document_text}\n{instruction_text}".lower()
    if "parameter" in combined or "threshold" in combined or "sla" in combined:
        return "risk_runtime_parameter"
    if "policy" in combined or "rule" in combined or "appetite" in combined:
        return "risk_policy_rule"
    if "assurance" in combined or "packet" in combined or "evidence" in combined:
        return "audit_evidence_packet"
    if "remediation" in combined or "issue" in combined:
        return "remediation_issue"
    if "test" in combined:
        return "control_test"
    if "control" in combined:
        return "control_library"
    return "risk_register"


def _infer_action(instruction_text: str, requested: str | None = None) -> str:
    if requested in _CRUD_ACTIONS:
        return requested
    lowered = instruction_text.lower()
    if re.search(r"\b(create|add|open)\b", lowered):
        return "create"
    if re.search(r"\b(update|change|revise|adjust)\b", lowered):
        return "update"
    if re.search(r"\b(delete|remove|drop)\b", lowered):
        return "delete"
    return "read"


def agent_skill_manifest() -> dict:
    return {
        "ok": bool(_SKILL_NAMES) and bool(_owned_tables()) and bool(_query_operations()),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": tuple(
            {
                "name": skill,
                "scope": PBC_KEY,
                "owned_tables": _owned_tables(),
                "allowed_crud_actions": _CRUD_ACTIONS,
                "document_actions": _DOCUMENT_ACTIONS,
                "requires_confirmation_for_mutation": True,
                "uses_appgen_event_contract": True,
                "stream_engine_picker_visible": False,
            }
            for skill in _SKILL_NAMES
        ),
        "query_operations": _query_operations(),
        "command_operations": _command_operations(),
        "side_effects": (),
    }


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_and_instruction_intake",
            "governed_datastore_crud",
            "policy_and_permission_explanation",
            "workbench_navigation",
            "mutation_preview_before_commit",
        ),
        "professional_controls": (
            "citation_required_for_document_facts",
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "audit_event_plan",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document=None, instructions=None, *, target_entity: str | None = None, requested_action: str | None = None) -> dict:
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    entity = _infer_entity(document_text, instruction_text, target_entity)
    action = _infer_action(instruction_text, requested_action)
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}:{entity}:{action}".encode("utf-8")).hexdigest()
    sensitive_fields = ("loss_estimate", "exception_rationale", "evidence_hash") if entity in {"remediation_issue", "audit_evidence_packet"} else ()
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "target_entity": entity,
        "requested_action": action,
        "candidate_table": _ENTITY_TO_TABLE[entity],
        "candidate_permission": _ENTITY_TO_PERMISSION[entity],
        "expected_event": _ENTITY_TO_EVENT[entity],
        "sensitive_fields": sensitive_fields,
        "candidate_operations": _command_operations() + _query_operations(),
        "requires_human_confirmation": action != "read",
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None) -> dict:
    normalized_action = str(action).lower()
    owned_tables = _owned_tables()
    selected_table = table or (owned_tables[0] if owned_tables else None)
    allowed = normalized_action in _CRUD_ACTIONS and selected_table in owned_tables
    entity = next((name for name, candidate in _ENTITY_TO_TABLE.items() if candidate == selected_table), None)
    return {
        "ok": allowed,
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "owned_tables": owned_tables,
        "candidate_operations": _query_operations() if normalized_action == "read" else _command_operations(),
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "permission": _ENTITY_TO_PERMISSION.get(entity),
        "expected_event": _ENTITY_TO_EVENT.get(entity),
        "side_effects": (),
    }


def enterprise_risk_controls_assistant_preview(payload: dict | None = None) -> dict:
    supplied = dict(payload or {})
    plan = document_instruction_plan(
        supplied.get("document_text"),
        supplied.get("instructions"),
        target_entity=supplied.get("target_entity"),
        requested_action=supplied.get("requested_action"),
    )
    crud = datastore_crud_plan(plan["requested_action"], plan["candidate_table"], supplied.get("payload"))
    mutation = enterprise_risk_controls_mutation_preview(plan["requested_action"], plan["candidate_table"], supplied.get("payload"))
    return {
        "ok": plan["ok"] and crud["ok"] and mutation["ok"],
        "pbc": PBC_KEY,
        "target_entity": plan["target_entity"],
        "action": plan["requested_action"],
        "candidate_table": plan["candidate_table"],
        "permission": plan["candidate_permission"],
        "expected_event": plan["expected_event"],
        "document_digest": plan["document_digest"],
        "requires_confirmation": plan["requires_human_confirmation"],
        "sensitive_fields": plan["sensitive_fields"],
        "crud_plan": crud,
        "mutation_preview": mutation,
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    return {
        "ok": skills["ok"] and chatbot["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "dsl_tools": (f"{PBC_KEY}_skills", f"{PBC_KEY}_documents", f"{PBC_KEY}_crud"),
        "skills": tuple(item["name"] for item in skills["skills"]),
        "chatbot": chatbot,
        "side_effects": (),
    }


def smoke_test() -> dict:
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan(
        "A committee memo requests tighter risk appetite coverage.",
        "Update the risk appetite rule for committee review.",
        target_entity="risk_policy_rule",
        requested_action="update",
    )
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan(
        "create",
        table="enterprise_risk_controls_risk_runtime_parameter",
        payload={"name": "high_risk_threshold"},
    )
    preview = enterprise_risk_controls_assistant_preview(
        {
            "document_text": "Critical issues need a 30-day remediation SLA.",
            "instructions": "Update the remediation parameter to 30 days.",
            "target_entity": "risk_runtime_parameter",
            "requested_action": "update",
            "payload": {"name": "critical_remediation_sla_days", "value": 30},
        }
    )
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"] and chatbot["ok"] and document["ok"] and read_plan["ok"] and create_plan["ok"] and preview["ok"] and contribution["ok"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "preview": preview,
        "contribution": contribution,
        "side_effects": (),
    }

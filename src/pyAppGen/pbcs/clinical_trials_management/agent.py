"""AI agent and chatbot skill contract for the clinical_trials_management PBC."""

from __future__ import annotations

import hashlib
import re

from .controls import clinical_trials_management_mutation_preview


PBC_KEY = "clinical_trials_management"
AGENT_NAME = "ClinicalTrialsManagementAgent"
_DOCUMENT_ACTIONS = (
    "summarize_trial_state",
    "extract_protocol_or_subject_facts",
    "draft_safety_or_monitoring_summary",
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
    f"{PBC_KEY}.lock_blocker_explanation",
    f"{PBC_KEY}.workbench_navigation",
)
_ENTITY_TO_TABLE = {
    "trial_protocol": "clinical_trials_management_trial_protocol",
    "study_site": "clinical_trials_management_study_site",
    "subject": "clinical_trials_management_subject",
    "consent_record": "clinical_trials_management_consent_record",
    "visit_schedule": "clinical_trials_management_visit_schedule",
    "adverse_event": "clinical_trials_management_adverse_event",
    "monitoring_finding": "clinical_trials_management_monitoring_finding",
    "policy_rule": "clinical_trials_management_clinical_trials_management_policy_rule",
    "runtime_parameter": "clinical_trials_management_clinical_trials_management_runtime_parameter",
}
_ENTITY_TO_PERMISSION = {
    "trial_protocol": "clinical_trials_management.protocol_admin",
    "study_site": "clinical_trials_management.site_activation",
    "subject": "clinical_trials_management.subject_enrollment",
    "consent_record": "clinical_trials_management.consent_manage",
    "visit_schedule": "clinical_trials_management.visit_manage",
    "adverse_event": "clinical_trials_management.safety_review",
    "monitoring_finding": "clinical_trials_management.monitoring_manage",
    "policy_rule": "clinical_trials_management.configure",
    "runtime_parameter": "clinical_trials_management.configure",
}
_ENTITY_TO_EVENT = {
    "trial_protocol": "ClinicalTrialProtocolRegistered",
    "study_site": "ClinicalTrialSiteActivated",
    "subject": "ClinicalTrialSubjectEnrollmentReviewed",
    "consent_record": "ClinicalTrialConsentRecorded",
    "visit_schedule": "ClinicalTrialVisitScheduled",
    "adverse_event": "ClinicalTrialSeriousAdverseEventReported",
    "monitoring_finding": "ClinicalTrialMonitoringFindingOpened",
    "policy_rule": None,
    "runtime_parameter": None,
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
    if "monitor" in combined:
        return "monitoring_finding"
    if "serious adverse" in combined or "safety" in combined:
        return "adverse_event"
    if "consent" in combined or "re-consent" in combined:
        return "consent_record"
    if "visit" in combined or "window" in combined:
        return "visit_schedule"
    if "site" in combined or "activation" in combined:
        return "study_site"
    if "subject" in combined or "screen" in combined or "enroll" in combined:
        return "subject"
    if "parameter" in combined or "sla" in combined or "threshold" in combined:
        return "runtime_parameter"
    if "rule" in combined or "policy" in combined:
        return "policy_rule"
    return "trial_protocol"


def _infer_action(instruction_text: str, requested: str | None = None) -> str:
    if requested in _CRUD_ACTIONS:
        return requested
    lowered = instruction_text.lower()
    if re.search(r"\b(create|add|open|record)\b", lowered):
        return "create"
    if re.search(r"\b(update|change|revise|amend|close)\b", lowered):
        return "update"
    if re.search(r"\b(delete|remove|drop)\b", lowered):
        return "delete"
    return "read"


def agent_skill_manifest() -> dict:
    """Return the skills this PBC contributes to the composed application assistant."""
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
    """Return the professional help/chatbot surface contract for this PBC."""
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
            "safety_and_lock_blocker_explanation",
            "workbench_navigation",
            "mutation_preview_before_commit",
        ),
        "professional_controls": (
            "citation_required_for_safety_and_monitoring_text",
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "audit_event_plan",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document=None, instructions=None, *, target_entity: str | None = None, requested_action: str | None = None) -> dict:
    """Plan document/instruction handling without mutating state."""
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    entity = _infer_entity(document_text, instruction_text, target_entity)
    action = _infer_action(instruction_text, requested_action)
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}:{entity}:{action}".encode("utf-8")).hexdigest()
    citation_required = entity in {"adverse_event", "monitoring_finding"}
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
        "citation_required": citation_required,
        "candidate_operations": _command_operations() + _query_operations(),
        "requires_human_confirmation": action != "read",
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None) -> dict:
    """Plan governed CRUD against owned tables only."""
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


def clinical_trials_management_assistant_preview(payload: dict | None = None) -> dict:
    """Build a bounded assistant preview for document/instruction CRUD requests."""
    supplied = dict(payload or {})
    plan = document_instruction_plan(
        supplied.get("document_text"),
        supplied.get("instructions"),
        target_entity=supplied.get("target_entity"),
        requested_action=supplied.get("requested_action"),
    )
    crud = datastore_crud_plan(plan["requested_action"], plan["candidate_table"], supplied.get("payload"))
    mutation = clinical_trials_management_mutation_preview(plan["requested_action"], plan["candidate_table"], supplied.get("payload"))
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
        "citation_required": plan["citation_required"],
        "crud_plan": crud,
        "mutation_preview": mutation,
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    """Return the package contribution to the application's single assistant."""
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
    """Exercise guidance, document intake, CRUD planning, and composition contribution."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan(
        "Monitoring memo: source data lag on Visit 4 for subject SUBJ-001.",
        "Update the monitoring finding and keep the remediation owner unchanged.",
        target_entity="monitoring_finding",
        requested_action="update",
    )
    read_plan = datastore_crud_plan("read")
    update_plan = datastore_crud_plan("update", table="clinical_trials_management_monitoring_finding", payload={"status": "resolved"})
    preview = clinical_trials_management_assistant_preview(
        {
            "document_text": "Safety note: grade 3 neutropenia reported within 8 hours.",
            "instructions": "Update the adverse event record and preserve the reporting evidence.",
            "target_entity": "adverse_event",
            "requested_action": "update",
            "payload": {"adverse_event_id": "AE-001", "status": "closed"},
        }
    )
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"] and chatbot["ok"] and document["ok"] and read_plan["ok"] and update_plan["ok"] and preview["ok"] and contribution["ok"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "update_plan": update_plan,
        "preview": preview,
        "contribution": contribution,
        "side_effects": (),
    }

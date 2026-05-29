"""AI agent and chatbot skill contract for the EAM PBC."""

from __future__ import annotations

import hashlib

from .manifest import PBC_MANIFEST
from .runtime import EAM_EVENT_CONTRACT
from .runtime import EAM_REQUIRED_EVENT_TOPIC
from .services import service_operation_contracts


PBC_KEY = "eam"
AGENT_NAME = "EamAgent"
_DOCUMENT_ACTIONS = ("summarize", "extract_fields", "validate_against_rules", "draft_crud_plan")
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


def _owned_tables():
    return tuple(f"{PBC_KEY}_{table}" for table in PBC_MANIFEST.get("tables", ()))


def _query_contracts():
    return tuple(item for item in service_operation_contracts().get("contracts", ()) if item["operation_kind"] == "query")


def _command_contracts():
    return tuple(item for item in service_operation_contracts().get("contracts", ()) if item["operation_kind"] == "command")


def _event_index():
    return {item["operation"]: item.get("emitted_event") for item in _command_contracts()}


def agent_skill_manifest():
    """Return the skills this PBC contributes to the composed application assistant."""
    return {
        "ok": bool(_SKILL_NAMES) and bool(_owned_tables()) and bool(_query_contracts()),
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
        "query_operations": tuple(item["operation"] for item in _query_contracts()),
        "command_operations": tuple(item["operation"] for item in _command_contracts()),
        "side_effects": (),
    }


def chatbot_interface_contract():
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
            "policy_and_permission_explanation",
            "workbench_navigation",
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


def governed_mutation_plan(operation_name, payload=None):
    """Plan one governed mutation with permission, event, and rollback evidence."""
    contract = next((item for item in _command_contracts() if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_command_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation_name,
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "idempotency_key": f"eam:{operation_name}:preview",
        "expected_event": _event_index().get(operation_name),
        "event_contract": EAM_EVENT_CONTRACT,
        "required_event_topic": EAM_REQUIRED_EVENT_TOPIC,
        "payload_keys": tuple(sorted(supplied)),
        "safety_gates": (
            "owned_table_boundary_check",
            "permission_check",
            "rule_evaluation",
            "human_confirmation",
        ),
        "rollback_limits": (
            "append_only_outbox",
            "compensating_action_required_after_publish",
            "no_hard_delete_of_audit_history",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document=None, instructions=None):
    """Plan document/instruction handling without mutating state."""
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    combined = " ".join(part for part in (document_text, instruction_text) if part)
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}".encode("utf-8")).hexdigest()
    detected_terms = tuple(
        term
        for term in ("equipment", "permit", "spare", "vendor", "priority", "work", "meter", "condition")
        if term in combined.lower()
    )
    mutation_candidates = tuple(governed_mutation_plan(item["operation"]) for item in _command_contracts()[:4])
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "detected_terms": detected_terms,
        "candidate_tables": _owned_tables(),
        "candidate_operations": tuple(item["operation"] for item in _command_contracts() + _query_contracts()),
        "mutation_candidates": mutation_candidates,
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None):
    """Plan governed CRUD against owned tables only."""
    normalized_action = str(action).lower()
    owned_tables = _owned_tables()
    selected_table = table or (owned_tables[0] if owned_tables else None)
    allowed = normalized_action in _CRUD_ACTIONS and selected_table in owned_tables
    if normalized_action == "read":
        operation_pool = tuple(item["operation"] for item in _query_contracts())
    elif normalized_action in {"create", "update"}:
        operation_pool = tuple(item["operation"] for item in _command_contracts())
    else:
        operation_pool = ()
    delete_governance = {
        "hard_delete_allowed": False,
        "reason": "audit_history_and_outbox_evidence_must_be_preserved",
    }
    return {
        "ok": allowed and (bool(operation_pool) or normalized_action == "delete"),
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "owned_tables": owned_tables,
        "candidate_operations": operation_pool,
        "requires_confirmation": normalized_action != "read",
        "mutation_supported": normalized_action != "delete",
        "delete_governance": delete_governance if normalized_action == "delete" else None,
        "event_contract": EAM_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def composed_agent_contribution():
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


def smoke_test():
    """Exercise guidance, document intake, CRUD planning, and composition contribution."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan("equipment pump_01 manual", "priority critical work corrective action inspect")
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", payload={"status": "draft"})
    delete_plan = datastore_crud_plan("delete")
    mutation_plan = governed_mutation_plan("register_equipment", {"equipment_id": "PUMP-01"})
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"]
        and chatbot["ok"]
        and document["ok"]
        and read_plan["ok"]
        and create_plan["ok"]
        and delete_plan["ok"]
        and mutation_plan["ok"]
        and contribution["ok"]
        and not create_plan["stream_engine_picker_visible"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "delete_plan": delete_plan,
        "mutation_plan": mutation_plan,
        "contribution": contribution,
        "side_effects": (),
    }

"""AI agent and chatbot skill contract for the ap_automation PBC."""

from __future__ import annotations

import hashlib

from . import services
from .controls import control_contract
from .forms import form_contract
from .manifest import PBC_MANIFEST
from .repository import repository_contract
from .wizards import wizard_contract


PBC_KEY = "ap_automation"
AGENT_NAME = "ApAutomationAgent"
_DOCUMENT_ACTIONS = (
    "summarize",
    "extract_fields",
    "validate_against_rules",
    "draft_crud_plan",
    "prepare_form_submission",
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
    f"{PBC_KEY}.repository_query",
    f"{PBC_KEY}.form_guidance",
    f"{PBC_KEY}.wizard_execution",
    f"{PBC_KEY}.control_interpretation",
)


def _owned_tables():
    return tuple(f"{PBC_KEY}_{table}" for table in PBC_MANIFEST.get("tables", ()))



def _query_operations():
    return services.service_operation_manifest().get("query_operations", ())



def _command_operations():
    return services.service_operation_manifest().get("command_operations", ())



def agent_skill_manifest():
    """Return the skills this PBC contributes to the composed application assistant."""
    forms = form_contract()
    wizards = wizard_contract()
    repository = repository_contract()
    controls = control_contract()
    return {
        "ok": bool(_SKILL_NAMES)
        and bool(_owned_tables())
        and bool(_query_operations())
        and forms["ok"]
        and wizards["ok"]
        and repository["ok"]
        and controls["ok"],
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
        "form_ids": tuple(form["form_id"] for form in forms["forms"]),
        "wizard_ids": tuple(wizard["wizard_id"] for wizard in wizards["wizards"]),
        "control_ids": tuple(control["control_id"] for control in controls["controls"]),
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
            "database_backed_form_guidance",
            "wizard_execution_plans",
            "control_interpretation",
        ),
        "professional_controls": (
            "citation_required_for_document_facts",
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "audit_event_plan",
            "form_submission_preview",
            "wizard_step_preview",
        ),
        "side_effects": (),
    }



def document_instruction_plan(document=None, instructions=None):
    """Plan document/instruction handling without mutating state."""
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}".encode("utf-8")).hexdigest()
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": _owned_tables(),
        "candidate_operations": _command_operations() + _query_operations(),
        "candidate_forms": form_contract()["forms"],
        "candidate_wizards": wizard_contract()["wizards"],
        "requires_human_confirmation": True,
        "side_effects": (),
    }



def datastore_crud_plan(action="read", table=None, payload=None):
    """Plan governed CRUD against owned tables only."""
    normalized_action = str(action).lower()
    owned_tables = _owned_tables()
    selected_table = table or (owned_tables[0] if owned_tables else None)
    allowed = normalized_action in _CRUD_ACTIONS and selected_table in owned_tables
    operation_pool = _query_operations() if normalized_action == "read" else _command_operations()
    return {
        "ok": allowed and bool(operation_pool),
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "owned_tables": owned_tables,
        "candidate_operations": operation_pool,
        "candidate_forms": tuple(form["form_id"] for form in form_contract()["forms"]),
        "candidate_wizards": tuple(wizard["wizard_id"] for wizard in wizard_contract()["wizards"]),
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }



def composed_agent_contribution():
    """Return the package contribution to the application's single assistant."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    execution = services.execution_service_manifest()
    forms = form_contract()
    wizards = wizard_contract()
    repository = repository_contract()
    controls = control_contract()
    return {
        "ok": skills["ok"]
        and chatbot["ok"]
        and execution["ok"]
        and forms["ok"]
        and wizards["ok"]
        and repository["ok"]
        and controls["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "dsl_tools": (
            f"{PBC_KEY}_skills",
            f"{PBC_KEY}_documents",
            f"{PBC_KEY}_crud",
            f"{PBC_KEY}_forms",
            f"{PBC_KEY}_wizards",
            f"{PBC_KEY}_controls",
        ),
        "skills": tuple(item["name"] for item in skills["skills"]),
        "execution_operations": execution["operations"],
        "domain_slices": execution["domain_slices"],
        "forms": tuple(form["form_id"] for form in forms["forms"]),
        "wizards": tuple(wizard["wizard_id"] for wizard in wizards["wizards"]),
        "controls": tuple(control["control_id"] for control in controls["controls"]),
        "chatbot": chatbot,
        "side_effects": (),
    }



def smoke_test():
    """Exercise guidance, document intake, CRUD planning, and composition contribution."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan("sample instruction", "create or update the primary record")
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", payload={"status": "draft"})
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"]
        and chatbot["ok"]
        and document["ok"]
        and read_plan["ok"]
        and create_plan["ok"]
        and contribution["ok"]
        and not create_plan["stream_engine_picker_visible"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "contribution": contribution,
        "side_effects": (),
    }

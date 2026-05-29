"""Assistant surface for airline_operations_control."""

from __future__ import annotations

from .permissions import ACTION_PERMISSIONS
from .runtime import AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES
from .runtime import airline_operations_control_parse_document_instruction


PBC_KEY = "airline_operations_control"
SKILL_NAMESPACE = f"{PBC_KEY}_skills"


def agent_skill_manifest() -> dict:
    skills = (
        {
            "name": f"{PBC_KEY}_guide_user",
            "scope": PBC_KEY,
            "description": "Guide airline OCC users through the one-PBC workbench.",
            "requires_confirmation_for_mutation": False,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_plan_recovery",
            "scope": PBC_KEY,
            "description": "Plan tail, crew, and passenger recovery options before mutation.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_document_instruction_intake",
            "scope": PBC_KEY,
            "description": "Translate OCC notes or operational directives into governed CRUD plans.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_rotation_recovery_preview",
            "scope": PBC_KEY,
            "description": "Preview recovery effects on tail continuity and minimum-turn feasibility.",
            "requires_confirmation_for_mutation": False,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": SKILL_NAMESPACE,
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "rotation_recovery_preview",
            "turn_feasibility_explanation",
            "decision_pack_planning",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document, instruction) -> dict:
    plan = airline_operations_control_parse_document_instruction(document, instruction)
    return {
        "ok": plan["ok"],
        "pbc": PBC_KEY,
        "document_digest": plan["document_digest"],
        "instruction": plan["instruction"],
        "candidate_tables": plan["candidate_tables"],
        "requires_human_confirmation": plan["requires_human_confirmation"],
        "crud_preview": plan["crud_preview"],
        "planning_focus": plan["planning_focus"],
        "side_effects": (),
    }


def datastore_crud_plan(action, table=None, payload=None):
    target = table or AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": action in ("create", "update", "delete"),
        "event_contract": "AppGen-X",
        "required_permission": ACTION_PERMISSIONS.get("manage_flight_leg"),
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": SKILL_NAMESPACE,
        "dsl_tools": (
            SKILL_NAMESPACE,
            f"{PBC_KEY}_crud",
            f"{PBC_KEY}_documents",
            f"{PBC_KEY}_rotation_recovery",
            f"{PBC_KEY}_decision_journal",
        ),
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = agent_skill_manifest()
    contract = chatbot_interface_contract()
    plan = document_instruction_plan("Crew note: hold KQ431 for inbound tail swap", "Create recovery decision")
    crud = datastore_crud_plan("create", table="airline_operations_control_operations_decision")
    rejected = datastore_crud_plan("update", table="foreign_table")
    return {
        "ok": manifest["ok"] and contract["ok"] and plan["ok"] and crud["ok"] and rejected["ok"] is False,
        "manifest": manifest,
        "contract": contract,
        "plan": plan,
        "crud": crud,
        "rejected": rejected,
        "side_effects": (),
    }

"""Assistant surface for the court_case_management PBC."""
from __future__ import annotations

from hashlib import sha256

from .court_operations_app import document_instruction_mutation_plan

PBC_KEY = "court_case_management"
OWNED_TABLES = (
    "court_case_management_court_case",
    "court_case_management_filing",
    "court_case_management_evidence_item",
    "court_case_management_hearing",
    "court_case_management_case_task",
    "court_case_management_docket_entry",
    "court_case_management_party",
    "court_case_management_judgment",
    "court_case_management_court_order",
    "court_case_management_court_case_management_policy_rule",
    "court_case_management_court_case_management_runtime_parameter",
    "court_case_management_court_case_management_schema_extension",
    "court_case_management_court_case_management_control_assertion",
    "court_case_management_court_case_management_governed_model",
    "court_case_management_appgen_outbox_event",
    "court_case_management_appgen_inbox_event",
    "court_case_management_appgen_dead_letter_event",
)


def agent_skill_manifest() -> dict:
    skills = (
        {
            "name": f"{PBC_KEY}_filing_triage",
            "scope": PBC_KEY,
            "description": "Classify filings, flag likely deficiencies, and prepare clerk review actions.",
            "document_actions": ("receive_filing", "register_evidence", "create_task"),
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_hearing_preparation",
            "scope": PBC_KEY,
            "description": "Prepare hearing packets, confirm readiness, and queue hearing follow-up tasks.",
            "document_actions": ("schedule_hearing", "create_task", "register_evidence"),
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_order_follow_up",
            "scope": PBC_KEY,
            "description": "Draft order actions, route signature review, and schedule service tasks.",
            "document_actions": ("draft_order", "sign_and_enter_order", "create_task"),
            "requires_confirmation_for_mutation": True,
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
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "filing_triage",
            "hearing_preparation",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    plan = document_instruction_mutation_plan(document, instruction)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": sha256(str(document).encode("utf-8")).hexdigest(),
        "instruction": instruction,
        "candidate_tables": OWNED_TABLES[:8],
        "requires_human_confirmation": True,
        "assistant_skills": tuple(skill["name"] for skill in agent_skill_manifest()["skills"]),
        "domain_plan": plan,
        "crud_preview": {
            "operation": plan["proposed_action"],
            "table": plan["target_table"],
            "event_contract": "AppGen-X",
        },
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or OWNED_TABLES[0]
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
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": agent_skill_manifest()["ok"] and chatbot_interface_contract()["ok"] and document_instruction_plan("Exhibit A", "log evidence")["ok"] and datastore_crud_plan("create", table="court_case_management_case_task")["ok"] and datastore_crud_plan("update", table="foreign_table")["ok"] is False and composed_agent_contribution()["ok"],
        "side_effects": (),
    }

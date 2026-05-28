"""Agent and chatbot assistance for the case_knowledge_management PBC."""

from __future__ import annotations

from .application import create_app
from .domain_depth import DOMAIN_OPERATIONS
from .models import OWNED_TABLES


PBC_KEY = "case_knowledge_management"
OWNED_TABLES = OWNED_TABLES


def agent_skill_manifest() -> dict:
    base_skills = (
        "case_knowledge_management_guide_user",
        "case_knowledge_management_read_records",
        "case_knowledge_management_create_record",
        "case_knowledge_management_update_record",
    )
    domain_skills = tuple(f"{PBC_KEY}_{operation}" for operation in DOMAIN_OPERATIONS)
    skills = tuple(
        {
            "name": name,
            "scope": PBC_KEY,
            "description": f"{name} for support operations and knowledge work.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for name in base_skills + domain_skills
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
            "grounded_resolution_recommendation",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    app = create_app()
    parsed = {
        "create": f"{PBC_KEY}_support_case",
        "update article": f"{PBC_KEY}_knowledge_article",
        "feedback": f"{PBC_KEY}_article_feedback",
    }
    lowered = f"{document} {instruction}".lower()
    target = next((table for key, table in parsed.items() if key in lowered), f"{PBC_KEY}_support_case")
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "instruction": instruction,
        "document_preview": document[:200],
        "candidate_tables": (target,),
        "requires_human_confirmation": True,
        "crud_preview": {
            "operation": "create",
            "table": target,
            "event_contract": "AppGen-X",
        },
        "workbench_snapshot": app.query_workbench()["metrics"],
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    mutation = action in {"create", "update", "delete"}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": mutation,
        "event_contract": "AppGen-X",
        "owned_boundary": True,
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
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("doc", "create case")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }

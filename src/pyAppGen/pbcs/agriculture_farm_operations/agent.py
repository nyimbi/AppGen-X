"""AI assistant and governed CRUD planning for agriculture_farm_operations."""

from __future__ import annotations

from .runtime import AGRICULTURE_FARM_OPERATIONS_BUSINESS_TABLES, PBC_KEY


def agent_skill_manifest() -> dict:
    skills = (
        {
            "name": f"{PBC_KEY}_agronomist_copilot",
            "scope": PBC_KEY,
            "description": "Summarize field history, planting-window risk, and readiness blockers.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_document_intake",
            "scope": PBC_KEY,
            "description": "Turn agronomy notes into reviewable crop-plan drafts.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_compliance_packet_planner",
            "scope": PBC_KEY,
            "description": "Plan audit-ready evidence packets for fields and seasons.",
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
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "workflow_guidance",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    from .runtime import agriculture_farm_operations_parse_document_instruction

    plan = agriculture_farm_operations_parse_document_instruction(document, instruction, context)
    return {
        "ok": plan["ok"],
        "pbc": PBC_KEY,
        "document_digest": plan["document_digest"],
        "instruction": instruction,
        "candidate_tables": plan["candidate_tables"],
        "requires_human_confirmation": plan["requires_human_confirmation"],
        "crud_preview": {
            "operation": "create",
            "target_table": "agriculture_farm_operations_crop_plan",
            "draft_preview": plan["draft_preview"],
            "event_contract": "AppGen-X",
        },
        "source_plan": plan,
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or AGRICULTURE_FARM_OPERATIONS_BUSINESS_TABLES[0]
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
        "stages": ("validate", "preview", "confirm", "apply", "emit_event"),
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


def standalone_agent_workspace_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "assistant_entrypoint": f"/api/pbc/{PBC_KEY}/assistant",
        "document_entrypoint": f"/api/pbc/{PBC_KEY}/assistant/document-plan",
        "crud_entrypoint": f"/api/pbc/{PBC_KEY}/assistant/crud-plan",
        "governance": {
            "mutation_confirmation_required": True,
            "owned_table_boundary_only": True,
            "event_contract": "AppGen-X",
        },
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("doc", "create")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"]
        and standalone_agent_workspace_contract()["ok"],
        "side_effects": (),
    }

"""Assistant and chatbot skill contracts for defense_readiness_logistics."""

from __future__ import annotations

from hashlib import sha256

from .defense_app import document_instruction_mutation_plan
from .models import OWNED_TABLES, PBC_KEY


SKILL_DEFINITIONS = (
    {
        "name": f"{PBC_KEY}_extract_movement_order",
        "description": "Extract convoy, airlift, or sealift movement drafts with citations and no-write preview.",
        "supported_inputs": ("operations_message", "movement_fragment", "route_change"),
    },
    {
        "name": f"{PBC_KEY}_summarize_maintenance_narrative",
        "description": "Summarize maintenance narratives into readiness-relevant serviceability facts.",
        "supported_inputs": ("maintenance_narrative", "fault_log", "parts_status"),
    },
    {
        "name": f"{PBC_KEY}_propose_shortage_mitigation",
        "description": "Suggest policy-aware shortage mitigations with approved, restricted, and unavailable labels.",
        "supported_inputs": ("stock_snapshot", "requisition_note", "fuel_plan"),
    },
    {
        "name": f"{PBC_KEY}_explain_readiness_posture",
        "description": "Explain readiness blockers with provenance from inspections, supply, assets, and movement records.",
        "supported_inputs": ("readiness_report", "inspection_pack", "deployment_release_bundle"),
    },
)


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def agent_skill_manifest() -> dict:
    skills = tuple(
        {
            **skill,
            "scope": PBC_KEY,
            "requires_confirmation_for_mutation": True,
            "requires_citations": True,
            "classification_aware": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for skill in SKILL_DEFINITIONS
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
            "citation_enforcement",
            "classification_redaction",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    domain_plan = document_instruction_mutation_plan(document, instruction)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document),
        "instruction": instruction,
        "candidate_tables": (domain_plan["target_table"],),
        "requires_human_confirmation": True,
        "requires_citations": True,
        "domain_plan": domain_plan,
        "crud_preview": {
            "operation": domain_plan["proposed_operation"],
            "target_table": domain_plan["target_table"],
            "workflow_id": domain_plan["workflow_id"],
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
        "requires_citations": action in ("create", "update"),
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
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("convoy order", "extract movement") ["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }

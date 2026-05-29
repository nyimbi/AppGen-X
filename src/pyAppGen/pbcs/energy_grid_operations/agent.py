"""Agent metadata for the energy_grid_operations standalone package."""

from __future__ import annotations

from .runtime import ENERGY_GRID_OPERATIONS_OWNED_TABLES, PBC_KEY


def agent_skill_manifest() -> dict:
    skills = (
        {
            "name": f"{PBC_KEY}_guide_operator",
            "description": "Explain switching, dispatch, and outage workflows using package-local evidence.",
            "requires_confirmation_for_mutation": False,
        },
        {
            "name": f"{PBC_KEY}_simulate_switching",
            "description": "Prepare a switching-order preview with hold points and backfeed warnings.",
            "requires_confirmation_for_mutation": True,
        },
        {
            "name": f"{PBC_KEY}_summarize_outage",
            "description": "Summarize outage impact, restoration priority, and recommended operator actions.",
            "requires_confirmation_for_mutation": False,
        },
        {
            "name": f"{PBC_KEY}_governed_crud_preview",
            "description": "Generate owned-table create and update previews that require human confirmation before mutation.",
            "requires_confirmation_for_mutation": True,
        },
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "skills": skills,
        "side_effects": (),
    }


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "switching_simulation_explanation",
            "outage_restoration_summary",
            "governed_datastore_crud",
            "mutation_preview",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    lowered = f"{document} {instruction}".lower()
    if "switch" in lowered:
        candidate_operations = ("review_switching_order", "record_grid_topology")
    elif "outage" in lowered or "restore" in lowered:
        candidate_operations = ("simulate_outage_event", "approve_dispatch_instruction")
    elif "dispatch" in lowered:
        candidate_operations = ("approve_dispatch_instruction",)
    else:
        candidate_operations = ("create_grid_asset", "record_load_forecast")
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": str(abs(hash(document))),
        "instruction": instruction,
        "candidate_operations": candidate_operations,
        "candidate_tables": ENERGY_GRID_OPERATIONS_OWNED_TABLES[:4],
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or ENERGY_GRID_OPERATIONS_OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": action in {"create", "update", "delete"},
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (
            namespace,
            f"{PBC_KEY}_crud",
            f"{PBC_KEY}_documents",
            f"{PBC_KEY}_release_evidence",
        ),
        "side_effects": (),
    }


def standalone_agent_workspace_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "workspace_route": f"/assistant/pbc/{PBC_KEY}",
        "namespace": f"{PBC_KEY}_skills",
        "documents_supported": True,
        "governed_mutations": True,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("switching order", "simulate")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }

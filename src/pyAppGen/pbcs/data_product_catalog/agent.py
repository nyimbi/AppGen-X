"""Agent and chatbot assistance for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import (
    AGENT_SKILL_BLUEPRINTS,
    BUSINESS_TABLES,
    EVENT_CONTRACT,
    FORM_BLUEPRINTS,
    OPERATION_BLUEPRINTS,
    PBC_KEY,
    WIZARD_BLUEPRINTS,
    digest,
    operation_blueprint,
)

OWNED_TABLES = BUSINESS_TABLES


def agent_skill_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "skills": AGENT_SKILL_BLUEPRINTS, "side_effects": ()}


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "stream_engine_picker_visible": False,
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "wizard_guidance",
            "event_plan_preview",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    operation = next(
        (item["name"] for item in OPERATION_BLUEPRINTS if item["name"].split("_", 1)[0] in instruction.lower()),
        "create_data_product",
    )
    spec = operation_blueprint(operation)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": digest((document, instruction)),
        "instruction": instruction,
        "context": dict(context or {}),
        "candidate_tables": OWNED_TABLES[:5],
        "recommended_operation": operation,
        "recommended_form": spec["form_id"],
        "recommended_wizard": spec["wizard_id"],
        "requires_human_confirmation": True,
        "crud_preview": {"operation": "create", "event_contract": EVENT_CONTRACT},
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    mutation = action in ("create", "update", "delete")
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": mutation,
        "event_contract": EVENT_CONTRACT,
        "available_forms": tuple(item["form_id"] for item in FORM_BLUEPRINTS[:3]),
        "available_wizards": tuple(item["wizard_id"] for item in WIZARD_BLUEPRINTS[:3]),
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents", f"{PBC_KEY}_wizards"),
        "side_effects": (),
    }


def smoke_test() -> dict:
    plan = document_instruction_plan("publish customer contract", "publish the contract")
    crud = datastore_crud_plan("create")
    rejected = datastore_crud_plan("update", table="foreign_table")
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and plan["ok"]
        and crud["ok"]
        and rejected["ok"] is False
        and composed_agent_contribution()["ok"],
        "plan": plan,
        "crud": crud,
        "side_effects": (),
    }

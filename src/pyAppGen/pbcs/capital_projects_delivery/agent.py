from __future__ import annotations

from .runtime import (
    CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES,
    capital_projects_delivery_build_agent_help_contract,
    capital_projects_delivery_build_forms_contract,
    capital_projects_delivery_build_wizards_contract,
)

PBC_KEY = "capital_projects_delivery"
OWNED_TABLES = CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES


def agent_skill_manifest():
    forms = capital_projects_delivery_build_forms_contract()
    wizards = capital_projects_delivery_build_wizards_contract()
    skills = tuple(
        {
            "name": name,
            "scope": PBC_KEY,
            "description": f"{name} for {PBC_KEY}",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
            "suggested_forms": tuple(form["name"] for form in forms["forms"]),
            "suggested_wizards": tuple(wizard["name"] for wizard in wizards["wizards"]),
        }
        for name in (
            f"{PBC_KEY}_guide_user",
            f"{PBC_KEY}_read_records",
            f"{PBC_KEY}_create_record",
            f"{PBC_KEY}_update_record",
            f"{PBC_KEY}_prepare_gate_review",
        )
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract():
    help_contract = capital_projects_delivery_build_agent_help_contract()
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
            "gate_approval_assistance",
        ),
        "help_contract": help_contract,
        "side_effects": (),
    }


def document_instruction_plan(document, instruction):
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": str(abs(hash(document))),
        "instruction": instruction,
        "candidate_tables": OWNED_TABLES[:3],
        "candidate_forms": tuple(
            form["name"] for form in capital_projects_delivery_build_forms_contract()["forms"]
        ),
        "candidate_wizards": tuple(
            wizard["name"] for wizard in capital_projects_delivery_build_wizards_contract()["wizards"]
        ),
        "requires_human_confirmation": True,
        "crud_preview": {"operation": "create", "event_contract": "AppGen-X"},
        "side_effects": (),
    }


def datastore_crud_plan(action, table=None, payload=None):
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


def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "assistant_help": capital_projects_delivery_build_agent_help_contract(),
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("doc", "create")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }

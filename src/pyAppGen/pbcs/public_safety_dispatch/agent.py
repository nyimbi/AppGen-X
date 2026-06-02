from __future__ import annotations

from .standalone import PBC_KEY, build_agent_contract, build_standalone_app

OWNED_TABLES = tuple(build_standalone_app().verify_owned_table_boundary(()).get("owned_tables", ()))


def agent_skill_manifest() -> dict:
    contract = build_agent_contract()
    skills = tuple({
        **skill,
        "scope": PBC_KEY,
        "requires_confirmation_for_mutation": True,
        "uses_appgen_event_contract": True,
        "stream_engine_picker_visible": False,
    } for skill in contract["skills"])
    return {
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "skills": skills,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def chatbot_interface_contract() -> dict:
    contract = build_agent_contract()
    return {
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "entrypoint": contract["entrypoint"],
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "capabilities": contract["capabilities"],
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    return build_standalone_app().document_instruction_plan(document, instruction)


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    plan = build_standalone_app().datastore_crud_plan(action, target, payload)
    if plan.get("ok") is True:
        plan["event_contract"] = "AppGen-X"
    return plan


def composed_agent_contribution() -> dict:
    contract = build_agent_contract()
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace,) + tuple(skill["name"] for skill in contract["skills"]),
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": agent_skill_manifest()["ok"] and chatbot_interface_contract()["ok"] and document_instruction_plan("incident note", "summarize")["ok"] and datastore_crud_plan("create")["ok"] and datastore_crud_plan("update", table="foreign_table")["ok"] is False and composed_agent_contribution()["ok"],
        "side_effects": (),
    }

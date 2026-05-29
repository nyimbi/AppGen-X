from __future__ import annotations

from .standalone import AGENT_SKILLS, OWNED_TABLES, PBC_KEY, build_agent_contract, build_datastore_crud_plan, build_document_instruction_plan


def agent_skill_manifest():
    contract = build_agent_contract()
    return {"ok": True, "pbc": PBC_KEY, "skills": contract["skills"], "side_effects": ()}


def chatbot_interface_contract():
    contract = build_agent_contract()
    return {"ok": True, "pbc": PBC_KEY, "entrypoint": contract["entrypoint"], "single_agent_contribution": contract["single_agent_contribution"], "capabilities": contract["capabilities"], "side_effects": ()}


def document_instruction_plan(document, instruction):
    return build_document_instruction_plan(document, instruction)


def datastore_crud_plan(action, table=None, payload=None):
    return build_datastore_crud_plan(action, table=table, payload=payload)


def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    return {"ok": True, "pbc": PBC_KEY, "single_agent_skill_namespace": namespace, "dsl_tools": tuple(skill["name"] for skill in AGENT_SKILLS) + (f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"), "owned_tables": OWNED_TABLES, "side_effects": ()}


def smoke_test():
    return {"ok": agent_skill_manifest()["ok"] and chatbot_interface_contract()["ok"] and document_instruction_plan("permit package", "check permit conflict") ["ok"] and datastore_crud_plan("create")["ok"] and datastore_crud_plan("update", table="foreign_table")["ok"] is False and composed_agent_contribution()["ok"], "side_effects": ()}

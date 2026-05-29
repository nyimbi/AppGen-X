"""Agent and chatbot assistance for the contract_lifecycle PBC."""

from .app_surface import document_instruction_contract_lifecycle_plan, single_pbc_contract_lifecycle_app_contract
from .application import (
    OWNED_TABLES,
    agent_skill_manifest as _agent_skill_manifest,
    chatbot_interface_contract as _chatbot_interface_contract,
    composed_agent_contribution as _composed_agent_contribution,
    datastore_crud_plan as _datastore_crud_plan,
    document_instruction_plan as _document_instruction_plan,
)

PBC_KEY = "contract_lifecycle"
OWNED_TABLES = OWNED_TABLES


def agent_skill_manifest():
    return _agent_skill_manifest()


def chatbot_interface_contract():
    return _chatbot_interface_contract()


def document_instruction_plan(document, instruction):
    return document_instruction_contract_lifecycle_plan(document, instruction)


def datastore_crud_plan(action, table=None, payload=None):
    return _datastore_crud_plan(action, table=table, payload=payload)


def composed_agent_contribution():
    contribution = _composed_agent_contribution()
    return {
        **contribution,
        "single_agent_skill_namespace": contribution.get("single_agent_skill_namespace", "contract_lifecycle_skills"),
        "stream_engine_picker_visible": False,
        "standalone_app": single_pbc_contract_lifecycle_app_contract(),
    }


def smoke_test():
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("renewal notice", "create renewal reminder")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }

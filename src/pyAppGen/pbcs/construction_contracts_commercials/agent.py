from __future__ import annotations

from .core import (
    agent_skill_manifest as _agent_skill_manifest,
    chatbot_interface_contract as _chatbot_interface_contract,
    composed_agent_contribution as _composed_agent_contribution,
    datastore_crud_plan as _datastore_crud_plan,
    document_instruction_plan as _document_instruction_plan,
)


def agent_skill_manifest():
    """Return the PBC skills contributed to the single composed assistant."""
    return _agent_skill_manifest()


def chatbot_interface_contract():
    """Return the construction commercial assistant interface contract."""
    return _chatbot_interface_contract()


def document_instruction_plan(document, instruction):
    """Plan document-driven construction commercial CRUD without side effects."""
    return _document_instruction_plan(document, instruction)


def datastore_crud_plan(action, table=None, payload=None):
    """Plan governed CRUD against construction-commercial owned tables only."""
    return _datastore_crud_plan(action, table=table, payload=payload)


def composed_agent_contribution():
    """Return the skills namespace contributed to the composed application agent."""
    contribution = _composed_agent_contribution()
    return {
        **contribution,
        "single_agent_skill_namespace": contribution.get(
            "single_agent_skill_namespace",
            "construction_contracts_commercials_skills",
        ),
        "stream_engine_picker_visible": False,
    }


def standalone_agent_workspace_contract():
    """Return the assistant surface exposed by the one-PBC standalone app."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    contribution = composed_agent_contribution()
    return {
        "format": "appgen.construction-contracts-commercials-standalone-agent.v1",
        "ok": skills["ok"] and chatbot["ok"] and contribution["ok"],
        "pbc": "construction_contracts_commercials",
        "skills": skills.get("skills", ()),
        "chatbot": chatbot,
        "single_agent_skill_namespace": contribution["single_agent_skill_namespace"],
        "document_instruction_intake": True,
        "governed_datastore_crud": True,
        "requires_confirmation_for_mutation": True,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("pay application valuation", "create pay application preview")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }

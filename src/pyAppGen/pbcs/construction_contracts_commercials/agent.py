from __future__ import annotations

from .core import (
    agent_skill_manifest as _agent_skill_manifest,
    chatbot_interface_contract as _chatbot_interface_contract,
    composed_agent_contribution as _composed_agent_contribution,
    datastore_crud_plan as _datastore_crud_plan,
    document_instruction_plan as _document_instruction_plan,
)
from .models import standalone_model_contract
from . import routes
from . import services
from .ui import (
    construction_contracts_commercials_form_contracts,
    construction_contracts_commercials_wizard_contracts,
)


PBC_KEY = "construction_contracts_commercials"


def _standalone_operations():
    return services.standalone_service_operation_contracts().get("contracts", ())


def _standalone_tables():
    return tuple(standalone_model_contract().get("table_keys", ()))


def standalone_agent_workspace_contract():
    form_manifest = construction_contracts_commercials_form_contracts()
    wizard_manifest = construction_contracts_commercials_wizard_contracts()
    route_manifest = routes.standalone_route_contracts()
    return {
        "format": "appgen.construction-contracts-commercials-standalone-agent-workspace.v1",
        "ok": form_manifest["ok"] and wizard_manifest["ok"] and route_manifest["ok"],
        "pbc": PBC_KEY,
        "forms": tuple(item["key"] for item in form_manifest["contracts"]),
        "wizards": tuple(item["key"] for item in wizard_manifest["contracts"]),
        "routes": route_manifest["routes"],
        "tables": _standalone_tables(),
        "side_effects": (),
    }


def agent_skill_manifest():
    """Return the PBC skills contributed to the single composed assistant."""
    manifest = _agent_skill_manifest()
    return {
        **manifest,
        "standalone_tables": _standalone_tables(),
        "standalone_workspace": standalone_agent_workspace_contract(),
    }


def chatbot_interface_contract():
    """Return the construction commercial assistant interface contract."""
    contract = _chatbot_interface_contract()
    return {
        **contract,
        "standalone_workspace": standalone_agent_workspace_contract(),
    }


def document_instruction_plan(document, instruction):
    """Plan document-driven construction commercial CRUD without side effects."""
    plan = _document_instruction_plan(document, instruction)
    combined = f"{document} {instruction}".lower()
    wizard_manifest = construction_contracts_commercials_wizard_contracts()["contracts"]
    standalone_operations = _standalone_operations()
    wizard_candidates = tuple(
        item["key"]
        for item in wizard_manifest
        if any(keyword in combined for keyword in item.get("keywords", ()))
    ) or ("pay_application_certification_wizard",)
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in standalone_operations
        if item["operation_kind"] == "command"
        and (item.get("wizard") in wizard_candidates or item["operation"].replace("_", " ") in combined)
    )
    form_candidates = tuple(
        form["key"]
        for form in construction_contracts_commercials_form_contracts()["contracts"]
        if form["operation"] in tuple(
            item["operation"]
            for item in standalone_operations
            if f"{item['method']} {item['path']}" in route_candidates
        )
    ) or ("pay_application_intake_form",)
    return {
        **plan,
        "wizard_candidates": wizard_candidates,
        "form_candidates": form_candidates,
        "route_candidates": route_candidates,
        "standalone_tables": _standalone_tables(),
    }


def datastore_crud_plan(action, table=None, payload=None):
    """Plan governed CRUD against construction-commercial owned tables only."""
    plan = _datastore_crud_plan(action, table=table, payload=payload)
    selected_table = plan.get("table")
    standalone_operations = _standalone_operations()
    normalized_action = str(action).lower()
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in standalone_operations
        if item["table"] == selected_table
        and ((normalized_action == "read" and item["operation_kind"] == "query") or (normalized_action != "read" and item["operation_kind"] == "command"))
    )
    form_candidates = tuple(
        form["key"]
        for form in construction_contracts_commercials_form_contracts()["contracts"]
        if form["table"] == selected_table
    )
    wizard_candidates = tuple(
        item["wizard"]
        for item in standalone_operations
        if item["table"] == selected_table and item.get("wizard")
    )
    return {
        **plan,
        "route_candidates": route_candidates,
        "form_candidates": form_candidates,
        "wizard_candidates": tuple(dict.fromkeys(wizard_candidates)),
        "standalone_tables": _standalone_tables(),
    }


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
        "standalone_workspace": standalone_agent_workspace_contract(),
    }


def smoke_test():
    workspace = standalone_agent_workspace_contract()
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("pay application valuation", "create pay application preview")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"]
        and workspace["ok"],
        "side_effects": (),
    }

"""AI agent and chatbot skill contract for the sports_venue_event_operations PBC."""

from __future__ import annotations

import hashlib

from .models import standalone_model_contract
from .routes import standalone_route_contracts
from .services import service_operation_manifest, standalone_service_operation_contracts
from .ui import (
    sports_venue_event_operations_form_contracts,
    sports_venue_event_operations_wizard_contracts,
)


PBC_KEY = "sports_venue_event_operations"
AGENT_NAME = "SportsVenueEventOperationsAgent"
_DOCUMENT_ACTIONS = ("summarize", "extract_fields", "validate_against_rules", "draft_crud_plan")
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_SKILL_NAMES = (
    f"{PBC_KEY}.event_command",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.governed_delete",
    f"{PBC_KEY}.policy_explanation",
    f"{PBC_KEY}.workbench_navigation",
)


def _owned_tables():
    return tuple(standalone_model_contract().get("table_keys", ()))


def _query_operations():
    return service_operation_manifest().get("query_operations", ())


def _command_operations():
    return service_operation_manifest().get("command_operations", ())


def _standalone_operations():
    return standalone_service_operation_contracts().get("contracts", ())


def standalone_agent_workspace_contract():
    forms = sports_venue_event_operations_form_contracts()
    wizards = sports_venue_event_operations_wizard_contracts()
    route_manifest = standalone_route_contracts()
    model_contract = standalone_model_contract()
    return {
        "format": "appgen.sports-venue-event-operations-standalone-agent-workspace.v1",
        "ok": forms["ok"] and wizards["ok"] and route_manifest["ok"] and model_contract["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "forms": tuple(item["key"] for item in forms["contracts"]),
        "wizards": tuple(item["key"] for item in wizards["contracts"]),
        "routes": route_manifest["routes"],
        "tables": model_contract["business_table_keys"],
        "side_effects": (),
    }


def agent_skill_manifest():
    return {
        "ok": bool(_SKILL_NAMES) and bool(_owned_tables()) and bool(_query_operations()),
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "skills": tuple(
            {
                "name": skill,
                "scope": PBC_KEY,
                "owned_tables": _owned_tables(),
                "allowed_crud_actions": _CRUD_ACTIONS,
                "document_actions": _DOCUMENT_ACTIONS,
                "requires_confirmation_for_mutation": True,
                "uses_appgen_event_contract": True,
                "stream_engine_picker_visible": False,
            }
            for skill in _SKILL_NAMES
        ),
        "query_operations": _query_operations(),
        "command_operations": _command_operations(),
        "side_effects": (),
    }


def chatbot_interface_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_and_instruction_intake",
            "governed_datastore_crud",
            "policy_and_permission_explanation",
            "workbench_navigation",
        ),
        "professional_controls": (
            "citation_required_for_document_facts",
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "audit_event_plan",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document=None, instruction=None):
    document_text = str(document or "")
    instruction_text = str(instruction or "")
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}".encode("utf-8")).hexdigest()
    combined = f"{document_text} {instruction_text}".lower()
    wizards = sports_venue_event_operations_wizard_contracts()["contracts"]
    operations = _standalone_operations()
    wizard_candidates = tuple(
        wizard["key"]
        for wizard in wizards
        if any(keyword in combined for keyword in wizard.get("keywords", ()))
    ) or ("EventCommandSetupWizard",)
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in operations
        if item["operation_kind"] == "command"
        and (
            item["wizard"] in wizard_candidates
            or item["operation"].replace("_", " ") in combined
            or item["table"].split("_")[-1] in combined
        )
    )
    form_candidates = tuple(
        form["key"]
        for form in sports_venue_event_operations_form_contracts()["contracts"]
        if form["operation"] in tuple(
            item["operation"] for item in operations if f"{item['method']} {item['path']}" in route_candidates
        )
    ) or ("EventCalendarForm",)
    preview_action = "update" if "update" in combined or "delay" in combined else "create"
    crud_preview = {
        "action": preview_action,
        "table": next(
            (
                item["table"]
                for item in operations
                if f"{item['method']} {item['path']}" in route_candidates
            ),
            f"{PBC_KEY}_event_calendar",
        ),
        "requires_confirmation": True,
        "event_contract": "AppGen-X",
    }
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": _owned_tables(),
        "candidate_operations": _command_operations() + _query_operations(),
        "wizard_candidates": wizard_candidates,
        "form_candidates": form_candidates,
        "route_candidates": route_candidates,
        "crud_preview": crud_preview,
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None):
    normalized_action = str(action).lower()
    owned_tables = _owned_tables()
    selected_table = table or (owned_tables[0] if owned_tables else None)
    allowed = normalized_action in _CRUD_ACTIONS and selected_table in owned_tables
    operations = _standalone_operations()
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in operations
        if item["table"] == selected_table
        and (
            (normalized_action == "read" and item["operation_kind"] == "query")
            or (normalized_action != "read" and item["operation_kind"] == "command")
        )
    )
    form_candidates = tuple(
        form["key"]
        for form in sports_venue_event_operations_form_contracts()["contracts"]
        if form["table"] == selected_table
    )
    wizard_candidates = tuple(
        item["wizard"]
        for item in operations
        if item["table"] == selected_table and item.get("wizard")
    )
    return {
        "ok": allowed,
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "owned_tables": owned_tables,
        "candidate_operations": _query_operations() if normalized_action == "read" else _command_operations(),
        "route_candidates": route_candidates,
        "form_candidates": form_candidates,
        "wizard_candidates": tuple(dict.fromkeys(wizard_candidates)),
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def composed_agent_contribution():
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    workspace = standalone_agent_workspace_contract()
    return {
        "ok": skills["ok"] and chatbot["ok"] and workspace["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "dsl_tools": (f"{PBC_KEY}_skills", f"{PBC_KEY}_documents", f"{PBC_KEY}_crud"),
        "skills": tuple(item["name"] for item in skills["skills"]),
        "chatbot": chatbot,
        "standalone_workspace": workspace,
        "side_effects": (),
    }


def smoke_test():
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan(
        "Weather deck and accessibility routing",
        "update the weather delay plan and prepare the accessibility workflow",
    )
    read_plan = datastore_crud_plan("read", table=f"{PBC_KEY}_event_calendar")
    create_plan = datastore_crud_plan("create", table=f"{PBC_KEY}_weather_delay", payload={"state": "delay"})
    contribution = composed_agent_contribution()
    workspace = standalone_agent_workspace_contract()
    return {
        "ok": skills["ok"]
        and chatbot["ok"]
        and document["ok"]
        and read_plan["ok"]
        and create_plan["ok"]
        and contribution["ok"]
        and workspace["ok"]
        and bool(document["wizard_candidates"])
        and bool(create_plan["route_candidates"])
        and not create_plan["stream_engine_picker_visible"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "contribution": contribution,
        "workspace": workspace,
        "side_effects": (),
    }

"""AI agent and chatbot contract for the Port Terminal Operations PBC."""

from __future__ import annotations

import hashlib

from .controls import port_terminal_operations_control_catalog
from .forms import port_terminal_operations_form_contracts
from .runtime import PORT_TERMINAL_OPERATIONS_OWNED_TABLES
from .wizards import port_terminal_operations_wizard_contracts

PBC_KEY = "port_terminal_operations"
AGENT_NAME = "PortTerminalOperationsAgent"
_DOCUMENT_ACTIONS = (
    "summarize",
    "extract_fields",
    "validate_against_rules",
    "draft_crud_plan",
)
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_SKILL_NAMES = (
    f"{PBC_KEY}.task_guidance",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.governed_delete",
    f"{PBC_KEY}.rule_and_release_explanation",
    f"{PBC_KEY}.workbench_navigation",
)


def _owned_tables() -> tuple[str, ...]:
    return tuple(PORT_TERMINAL_OPERATIONS_OWNED_TABLES)


def _hash_token(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def _standalone_routes() -> dict:
    from .standalone import port_terminal_operations_standalone_route_contracts

    return port_terminal_operations_standalone_route_contracts()


def standalone_agent_workspace_contract() -> dict:
    forms = port_terminal_operations_form_contracts()
    wizards = port_terminal_operations_wizard_contracts()
    controls = port_terminal_operations_control_catalog()
    routes = _standalone_routes()
    return {
        "format": "appgen.port-terminal-operations-standalone-agent-workspace.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"] and routes["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "forms": tuple(item["key"] for item in forms["contracts"]),
        "wizards": tuple(item["key"] for item in wizards["contracts"]),
        "controls": tuple(item["key"] for item in controls["contracts"]),
        "routes": routes["routes"],
        "tables": _owned_tables(),
        "side_effects": (),
    }


def agent_skill_manifest() -> dict:
    return {
        "ok": bool(_SKILL_NAMES) and bool(_owned_tables()),
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
        "side_effects": (),
    }


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "release_readiness_explanation",
            "workbench_navigation",
        ),
        "professional_controls": (
            "citation_required_for_document_facts",
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "human_confirmation_for_mutations",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str | None = None, instruction: str | None = None) -> dict:
    document_text = str(document or "")
    instruction_text = str(instruction or "")
    combined = f"{document_text} {instruction_text}".lower()
    digest = _hash_token(PBC_KEY, document_text, instruction_text)
    wizards = port_terminal_operations_wizard_contracts()["contracts"]
    routes = _standalone_routes()["contracts"]
    wizard_candidates = tuple(
        item["key"]
        for item in wizards
        if any(keyword in combined for keyword in item.get("keywords", ()))
    ) or ("DocumentInstructionIntakeWizard",)
    matched_routes = tuple(
        route
        for route in routes
        if route["operation_kind"] == "command"
        and (
            route.get("wizard") in wizard_candidates
            or route["operation"].replace("_", " ") in combined
            or route["table"].replace("_", " ") in combined
        )
    )
    form_candidates = tuple(
        form["key"]
        for form in port_terminal_operations_form_contracts()["contracts"]
        if form["operation"] in tuple(route["operation"] for route in matched_routes)
    ) or ("PortTerminalEventInboxForm",)
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "instruction": instruction_text,
        "candidate_tables": _owned_tables(),
        "candidate_operations": tuple(route["operation"] for route in routes),
        "wizard_candidates": wizard_candidates,
        "form_candidates": form_candidates,
        "route_candidates": tuple(f"{route['method']} {route['path']}" for route in matched_routes),
        "requires_human_confirmation": True,
        "crud_preview": {"operation": "create", "event_contract": "AppGen-X"},
        "side_effects": (),
    }


def datastore_crud_plan(action: str = "read", table: str | None = None, payload: dict | None = None) -> dict:
    normalized_action = str(action).lower()
    selected_table = table or _owned_tables()[0]
    if selected_table not in _owned_tables():
        return {
            "ok": False,
            "reason": "foreign_table_rejected",
            "table": selected_table,
            "side_effects": (),
        }
    routes = _standalone_routes()["contracts"]
    route_candidates = tuple(
        f"{route['method']} {route['path']}"
        for route in routes
        if route["table"] == selected_table
        and (
            (normalized_action == "read" and route["operation_kind"] == "query")
            or (normalized_action != "read" and route["operation_kind"] == "command")
        )
    )
    form_candidates = tuple(
        form["key"]
        for form in port_terminal_operations_form_contracts()["contracts"]
        if form["table"] == selected_table
    )
    wizard_candidates = tuple(
        route["wizard"]
        for route in routes
        if route["table"] == selected_table and route.get("wizard")
    )
    return {
        "ok": normalized_action in _CRUD_ACTIONS and bool(route_candidates or normalized_action == "read"),
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "owned_tables": _owned_tables(),
        "route_candidates": route_candidates,
        "form_candidates": form_candidates,
        "wizard_candidates": tuple(dict.fromkeys(wizard_candidates)),
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    return {
        "ok": skills["ok"] and chatbot["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "dsl_tools": (f"{PBC_KEY}_skills", f"{PBC_KEY}_documents", f"{PBC_KEY}_crud"),
        "skills": tuple(item["name"] for item in skills["skills"]),
        "chatbot": chatbot,
        "standalone_workspace": standalone_agent_workspace_contract(),
        "side_effects": (),
    }


def smoke_test() -> dict:
    document = document_instruction_plan("vessel notice", "review berth and customs release")
    crud = datastore_crud_plan("create", _owned_tables()[0], {"record_id": "smoke"})
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document["ok"]
        and crud["ok"]
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }

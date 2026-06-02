"""AI agent and chatbot planning contract for inventory_positioning."""

from __future__ import annotations

import hashlib

from .manifest import PBC_MANIFEST
from .routes import api_route_contracts
from .services import service_operation_manifest


PBC_KEY = "inventory_positioning"
AGENT_NAME = "InventoryPositioningAgent"
_DOCUMENT_ACTIONS = (
    "summarize_inventory_document",
    "extract_receipt_fields",
    "validate_against_rules",
    "draft_adjustment_plan",
    "draft_crud_plan",
)
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_SKILL_NAMES = (
    f"{PBC_KEY}.availability_explanation",
    f"{PBC_KEY}.allocation_preview",
    f"{PBC_KEY}.document_instruction_intake",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.governed_delete",
    f"{PBC_KEY}.policy_explanation",
    f"{PBC_KEY}.workbench_navigation",
)


def _owned_tables() -> tuple[str, ...]:
    return tuple(PBC_MANIFEST["owned_tables"])


def _query_operations() -> tuple[str, ...]:
    return service_operation_manifest()["query_operations"]


def _command_operations() -> tuple[str, ...]:
    return service_operation_manifest()["command_operations"]


def agent_skill_manifest() -> dict:
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


def chatbot_interface_contract() -> dict:
    route_manifest = api_route_contracts()
    return {
        "ok": route_manifest["ok"],
        "pbc": PBC_KEY,
        "agent": AGENT_NAME,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "availability_explanation_with_caveats",
            "allocation_preview_with_human_approval",
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
            "low_confidence_warning_for_availability",
        ),
        "route_surface": route_manifest["routes"],
        "side_effects": (),
    }


def document_instruction_plan(document=None, instructions=None) -> dict:
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    digest = hashlib.sha256(f"{PBC_KEY}:{document_text}:{instruction_text}".encode("utf-8")).hexdigest()
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": digest,
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": _owned_tables(),
        "candidate_operations": _command_operations() + _query_operations(),
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action: str = "read", table: str | None = None, payload: dict | None = None) -> dict:
    normalized_action = str(action).lower()
    owned_tables = _owned_tables()
    selected_table = table or (owned_tables[0] if owned_tables else None)
    allowed = normalized_action in _CRUD_ACTIONS and selected_table in owned_tables
    operation_pool = _query_operations() if normalized_action == "read" else _command_operations()
    return {
        "ok": allowed and bool(operation_pool),
        "pbc": PBC_KEY,
        "action": normalized_action,
        "table": selected_table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "owned_tables": owned_tables,
        "candidate_operations": operation_pool,
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
        "side_effects": (),
    }


def smoke_test() -> dict:
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan("receipt document", "draft a governed receive plan")
    read_plan = datastore_crud_plan("read", table="inventory_positioning_inventory_position")
    create_plan = datastore_crud_plan("create", table="inventory_positioning_adjustment", payload={"reason": "cycle_count"})
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"] and chatbot["ok"] and document["ok"] and read_plan["ok"] and create_plan["ok"] and contribution["ok"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "contribution": contribution,
        "side_effects": (),
    }

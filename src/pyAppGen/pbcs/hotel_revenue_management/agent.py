"""AI agent and chatbot skill contract for hotel_revenue_management."""

from __future__ import annotations

import hashlib

from . import services
from .manifest import PBC_MANIFEST
from .runtime import PBC_KEY


AGENT_NAME = "HotelRevenueManagementAgent"
_DOCUMENT_ACTIONS = (
    "summarize_revenue_context",
    "extract_rate_and_forecast_fields",
    "validate_against_revenue_rules",
    "draft_governed_mutation_preview",
)
_CRUD_ACTIONS = ("create", "read", "update", "delete")
_SKILL_NAMES = (
    f"{PBC_KEY}.task_guidance",
    f"{PBC_KEY}.inventory_and_rate_review",
    f"{PBC_KEY}.compression_night_playbook",
    f"{PBC_KEY}.forecast_override_review",
    f"{PBC_KEY}.governed_create",
    f"{PBC_KEY}.governed_read",
    f"{PBC_KEY}.governed_update",
    f"{PBC_KEY}.policy_explanation",
    f"{PBC_KEY}.release_readiness",
)


def _owned_tables() -> tuple[str, ...]:
    return tuple(f"{PBC_KEY}_{table}" for table in PBC_MANIFEST.get("tables", ())) + (
        f"{PBC_KEY}_appgen_outbox_event",
        f"{PBC_KEY}_appgen_inbox_event",
        f"{PBC_KEY}_appgen_dead_letter_event",
    )


def _query_operations() -> tuple[str, ...]:
    return services.service_operation_manifest().get("query_operations", ())


def _command_operations() -> tuple[str, ...]:
    return services.service_operation_manifest().get("command_operations", ())


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
            "pricing_and_inventory_explanation",
            "workbench_navigation",
            "compression_night_playbook",
        ),
        "professional_controls": (
            "citation_required_for_document_facts",
            "mutation_preview_before_commit",
            "permission_check_before_mutation",
            "owned_table_boundary_check",
            "human_confirmation_for_writes",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document=None, instruction=None) -> dict:
    document_text = str(document or "")
    instruction_text = str(instruction or "")
    text = f"{document_text}\n{instruction_text}".lower()
    candidate_tables = []
    candidate_operations = []
    if "inventory" in text or "room" in text:
        candidate_tables.append(f"{PBC_KEY}_room_type")
        candidate_operations.append("create_room_type")
    if "rate" in text or "bar" in text or "price" in text:
        candidate_tables.append(f"{PBC_KEY}_rate_plan")
        candidate_operations.append("record_rate_plan")
    if "forecast" in text or "pickup" in text or "demand" in text:
        candidate_tables.append(f"{PBC_KEY}_demand_forecast")
        candidate_operations.append("approve_demand_forecast")
    if not candidate_tables:
        candidate_tables = list(_owned_tables()[:3])
    if not candidate_operations:
        candidate_operations = ["query_workbench", "create_yield_decision"]
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": hashlib.sha256(f"{document_text}:{instruction_text}".encode("utf-8")).hexdigest(),
        "instruction": instruction_text,
        "document_actions": _DOCUMENT_ACTIONS,
        "candidate_tables": tuple(dict.fromkeys(candidate_tables)),
        "candidate_operations": tuple(dict.fromkeys(candidate_operations)),
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action="read", table=None, payload=None) -> dict:
    normalized_action = str(action).lower()
    owned_tables = _owned_tables()
    selected_table = table or owned_tables[0]
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
    document = document_instruction_plan("Rate ladder sheet", "Update BAR and forecast")
    read_plan = datastore_crud_plan("read")
    create_plan = datastore_crud_plan("create", table=f"{PBC_KEY}_rate_plan", payload={"code": "BAR"})
    contribution = composed_agent_contribution()
    return {
        "ok": skills["ok"]
        and chatbot["ok"]
        and document["ok"]
        and read_plan["ok"]
        and create_plan["ok"]
        and contribution["ok"]
        and not create_plan["stream_engine_picker_visible"],
        "skills": skills,
        "chatbot": chatbot,
        "document": document,
        "read_plan": read_plan,
        "create_plan": create_plan,
        "contribution": contribution,
        "side_effects": (),
    }

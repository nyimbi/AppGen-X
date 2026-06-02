"""Agent and chatbot contracts for hospitality property operations."""

from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_RULES, workflow_catalog
from .models import BUSINESS_TABLES, OWNED_TABLES

PBC_KEY = "hospitality_property_operations"


def agent_skill_manifest() -> dict:
    skills = (
        {
            "name": f"{PBC_KEY}_arrival_pickup_triage",
            "scope": PBC_KEY,
            "description": "Explain arrival blockers, room-ready gaps, and guarantee issues.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_service_recovery",
            "scope": PBC_KEY,
            "description": "Plan guest recovery, room moves, and urgent request escalation.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_revenue_control",
            "scope": PBC_KEY,
            "description": "Interpret occupancy risk and recommend rate fence actions.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_shift_handover",
            "scope": PBC_KEY,
            "description": "Prepare handover packets for arrivals, blocked rooms, and recoveries.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract() -> dict:
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
            "workflow_recommendation",
            "handover_summary",
        ),
        "side_effects": (),
    }


def _keyword_tables(instruction: str) -> tuple[str, ...]:
    lowered = instruction.lower()
    mapping = {
        "room": "hospitality_property_operations_room_inventory",
        "reservation": "hospitality_property_operations_reservation",
        "stay": "hospitality_property_operations_guest_stay",
        "housekeeping": "hospitality_property_operations_housekeeping_task",
        "request": "hospitality_property_operations_guest_request",
        "occupancy": "hospitality_property_operations_occupancy_snapshot",
        "rate": "hospitality_property_operations_rate_plan",
        "policy": "hospitality_property_operations_hospitality_property_operations_policy_rule",
        "parameter": "hospitality_property_operations_hospitality_property_operations_runtime_parameter",
    }
    tables = [table for keyword, table in mapping.items() if keyword in lowered]
    return tuple(dict.fromkeys(tables or BUSINESS_TABLES[:3]))


def document_instruction_plan(document: str, instruction: str) -> dict:
    from .routes import standalone_route_contracts

    tables = _keyword_tables(instruction)
    routes = standalone_route_contracts()["routes"]
    route_candidates = tuple(route for route in routes if route["table"] in tables)[:5]
    wizard_candidates = tuple(dict.fromkeys(route["wizard"] for route in route_candidates if route["wizard"]))
    workflow_candidates = tuple(
        item["workflow"]
        for item in workflow_catalog()
        if any(step in instruction.lower() for step in item["steps"])
        or any(token in instruction.lower() for token in item["workflow"].split("_"))
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": str(abs(hash(document))),
        "instruction": instruction,
        "candidate_tables": tables,
        "route_candidates": route_candidates,
        "wizard_candidates": wizard_candidates,
        "workflow_candidates": workflow_candidates or tuple(item["workflow"] for item in workflow_catalog()[:2]),
        "requires_human_confirmation": True,
        "crud_preview": {"operation": "create", "event_contract": "AppGen-X"},
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    from .routes import standalone_route_contracts

    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    routes = tuple(route for route in standalone_route_contracts()["routes"] if route["table"] == target)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": action in ("create", "update", "delete"),
        "route_candidates": routes,
        "rule_candidates": DOMAIN_RULES,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def standalone_agent_workspace_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": f"{PBC_KEY}_skills",
        "workspace_tabs": ("workbench", "room_detail", "shift_handover", "rate_control", "release_evidence"),
        "workflow_shortcuts": tuple(item["workflow"] for item in workflow_catalog()),
        "owned_tables": OWNED_TABLES,
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents", f"{PBC_KEY}_handover"),
        "side_effects": (),
    }


def smoke_test() -> dict:
    plan = document_instruction_plan("vip arrival list", "prepare shift handover and review urgent guest request")
    crud = datastore_crud_plan("create", OWNED_TABLES[0], {"room_id": "rm_smoke"})
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and plan["ok"]
        and crud["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and standalone_agent_workspace_contract()["ok"]
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }

"""Governed agent contracts for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from typing import Any

from .models import BUSINESS_TABLES
from .runtime import (
    cybersecurity_operations_center_empty_state,
    cybersecurity_operations_center_generate_handoff_packet,
    cybersecurity_operations_center_parse_document_instruction,
)

PBC_KEY = "cybersecurity_operations_center"
OWNED_TABLES = BUSINESS_TABLES


def agent_skill_manifest() -> dict[str, Any]:
    skills = (
        {
            "name": f"{PBC_KEY}_triage_summary",
            "scope": PBC_KEY,
            "description": "Draft a cited alert or incident triage summary.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_missing_evidence",
            "scope": PBC_KEY,
            "description": "List missing evidence and unresolved approvals for a case.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_threat_intel_recommendation",
            "scope": PBC_KEY,
            "description": "Suggest threat-intel enrichment candidates without mutating records.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_handoff_packet",
            "scope": PBC_KEY,
            "description": "Generate a shift-handoff packet from active cases.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract() -> dict[str, Any]:
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
            "shift_handoff_packet",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict[str, Any]:
    parsed = cybersecurity_operations_center_parse_document_instruction(document, instruction)
    return {
        "ok": parsed["ok"],
        "pbc": PBC_KEY,
        "document_digest": parsed["document_digest"],
        "instruction": instruction,
        "candidate_tables": parsed["candidate_tables"],
        "candidate_actions": parsed["candidate_actions"],
        "requires_human_confirmation": parsed["requires_human_confirmation"],
        "crud_preview": {"operation": parsed["candidate_actions"][0], "event_contract": "AppGen-X"},
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": action in ("create", "update", "delete"),
        "guardrails": {"owned_tables_only": True, "appgen_x_events_required": True},
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def handoff_packet_plan(tenant: str = "default") -> dict[str, Any]:
    state = cybersecurity_operations_center_empty_state()
    packet = cybersecurity_operations_center_generate_handoff_packet(state, tenant=tenant)
    return {"ok": packet["ok"], "pbc": PBC_KEY, "packet": packet["packet"], "side_effects": ()}


def composed_agent_contribution() -> dict[str, Any]:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents", f"{PBC_KEY}_handoff"),
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("alert evidence", "promote incident")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }

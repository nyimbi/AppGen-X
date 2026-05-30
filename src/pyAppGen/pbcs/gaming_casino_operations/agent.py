"""Governed assistant skills for gaming_casino_operations."""

from __future__ import annotations

from typing import Any

from .models import GAMING_COMPLIANCE_TABLE, PAYOUT_TABLE, PLAYER_PROFILE_TABLE, RESPONSIBLE_GAMING_CASE_TABLE, SLOT_MACHINE_TABLE, TABLE_GAME_TABLE, WAGER_SESSION_TABLE
from .runtime import gaming_casino_operations_parse_document_instruction


PBC_KEY = "gaming_casino_operations"
OWNED_TABLES = (
    PLAYER_PROFILE_TABLE,
    TABLE_GAME_TABLE,
    SLOT_MACHINE_TABLE,
    WAGER_SESSION_TABLE,
    PAYOUT_TABLE,
    RESPONSIBLE_GAMING_CASE_TABLE,
    GAMING_COMPLIANCE_TABLE,
)


def agent_skill_manifest() -> dict[str, Any]:
    skills = (
        {
            "name": f"{PBC_KEY}_triage_patron_identity",
            "scope": PBC_KEY,
            "description": "Explain patron enrollment review and restriction reasons.",
            "requires_confirmation_for_mutation": True,
            "route": "/app/gaming-casino-operations/player-profiles",
        },
        {
            "name": f"{PBC_KEY}_guide_shift_close",
            "scope": PBC_KEY,
            "description": "Walk a supervisor through shift close and bankroll reconciliation.",
            "requires_confirmation_for_mutation": True,
            "route": "/app/gaming-casino-operations/workflows/table-shift-close",
        },
        {
            "name": f"{PBC_KEY}_summarize_jackpot_evidence",
            "scope": PBC_KEY,
            "description": "Summarize hand-pay approvals, witness evidence, and cage release readiness.",
            "requires_confirmation_for_mutation": True,
            "route": "/app/gaming-casino-operations/payouts",
        },
        {
            "name": f"{PBC_KEY}_responsible_gaming_guidance",
            "scope": PBC_KEY,
            "description": "Recommend intervention workflows and follow-up scheduling.",
            "requires_confirmation_for_mutation": True,
            "route": "/app/gaming-casino-operations/responsible-gaming-cases",
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def standalone_agent_workspace_contract() -> dict[str, Any]:
    from .routes import standalone_route_contracts
    from .services import standalone_service_operation_contracts

    return {
        "ok": True,
        "pbc": PBC_KEY,
        "skills": agent_skill_manifest()["skills"],
        "routes": standalone_route_contracts()["contracts"],
        "service_methods": standalone_service_operation_contracts()["command_operations"]
        + standalone_service_operation_contracts()["query_operations"],
        "side_effects": (),
    }


def chatbot_interface_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "stream_engine_picker_visible": False,
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "workflow_triage",
            "release_evidence_summary",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict[str, Any]:
    parsed = gaming_casino_operations_parse_document_instruction(document, instruction)
    route_candidates = {
        PLAYER_PROFILE_TABLE: "/app/gaming-casino-operations/player-profiles",
        TABLE_GAME_TABLE: "/app/gaming-casino-operations/table-games",
        SLOT_MACHINE_TABLE: "/app/gaming-casino-operations/slot-machines",
        WAGER_SESSION_TABLE: "/app/gaming-casino-operations/wager-sessions",
        PAYOUT_TABLE: "/app/gaming-casino-operations/payouts",
        RESPONSIBLE_GAMING_CASE_TABLE: "/app/gaming-casino-operations/responsible-gaming-cases",
        GAMING_COMPLIANCE_TABLE: "/app/gaming-casino-operations/compliance-cases",
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": parsed["document_digest"],
        "instruction": instruction,
        "candidate_tables": parsed["candidate_tables"],
        "wizard_candidates": (parsed["workflow"],),
        "route_candidates": tuple(route_candidates[table] for table in parsed["candidate_tables"] if table in route_candidates),
        "requires_human_confirmation": True,
        "crud_preview": {"operation": "create", "event_contract": "AppGen-X"},
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    target = table or PLAYER_PROFILE_TABLE
    route_candidates = {
        PLAYER_PROFILE_TABLE: "/app/gaming-casino-operations/player-profiles",
        TABLE_GAME_TABLE: "/app/gaming-casino-operations/table-games",
        SLOT_MACHINE_TABLE: "/app/gaming-casino-operations/slot-machines",
        WAGER_SESSION_TABLE: "/app/gaming-casino-operations/wager-sessions",
        PAYOUT_TABLE: "/app/gaming-casino-operations/payouts",
        RESPONSIBLE_GAMING_CASE_TABLE: "/app/gaming-casino-operations/responsible-gaming-cases",
        GAMING_COMPLIANCE_TABLE: "/app/gaming-casino-operations/compliance-cases",
    }
    if target not in route_candidates:
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "route_candidates": (route_candidates[target],),
        "requires_confirmation": action in {"create", "update", "delete"},
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def composed_agent_contribution() -> dict[str, Any]:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    document_plan = document_instruction_plan("jackpot evidence", "approve a jackpot handpay")
    crud_plan = datastore_crud_plan("create", PLAYER_PROFILE_TABLE, {"player_number": "P-AGENT"})
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and standalone_agent_workspace_contract()["ok"]
        and document_plan["ok"]
        and crud_plan["ok"],
        "side_effects": (),
    }

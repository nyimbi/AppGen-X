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

# AppGen-X canonical composed-agent interface.
from .manifest import PBC_MANIFEST as _APPGEN_AGENT_MANIFEST


def _appgen_agent_owned_tables() -> tuple[str, ...]:
    tables = tuple(_APPGEN_AGENT_MANIFEST.get('tables', ()))
    return tuple(table if str(table).startswith('gaming_casino_operations_') else f'gaming_casino_operations_{table}' for table in tables) or (f'gaming_casino_operations_record',)


def agent_skill_manifest() -> dict:
    skills = (
        {'name': f'gaming_casino_operations_task_guidance', 'scope': 'gaming_casino_operations', 'description': 'Guide users through domain tasks and release-safe workflows.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'gaming_casino_operations_document_instruction_intake', 'scope': 'gaming_casino_operations', 'description': 'Convert documents and instructions into governed mutation previews.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'gaming_casino_operations_crud_datastore_mutation', 'scope': 'gaming_casino_operations', 'description': 'Prepare owned-datastore CRUD plans with human confirmation for writes.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
    )
    return {'ok': True, 'pbc': 'gaming_casino_operations', 'skills': skills, 'stream_engine_picker_visible': False, 'side_effects': ()}


def chatbot_interface_contract() -> dict:
    return {'ok': True, 'pbc': 'gaming_casino_operations', 'entrypoint': '/assistant/pbc/gaming_casino_operations', 'single_agent_contribution': 'gaming_casino_operations_skills', 'capabilities': ('task_guidance', 'document_instruction_intake', 'governed_datastore_crud', 'mutation_preview'), 'side_effects': ()}


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    return {'ok': True, 'pbc': 'gaming_casino_operations', 'document_digest': str(abs(hash(document)))[:12], 'instruction': instruction, 'context': dict(context or {}), 'requires_human_confirmation': True, 'candidate_tables': tables, 'crud_preview': {'action': 'create', 'table': tables[0], 'event_contract': 'AppGen-X'}, 'side_effects': ()}


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    target = table or tables[0]
    if not str(target).startswith('gaming_casino_operations_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    return {'ok': action in {'create', 'read', 'update', 'delete'}, 'pbc': 'gaming_casino_operations', 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': action in {'create', 'update', 'delete'}, 'event_contract': 'AppGen-X', 'side_effects': ()}


def composed_agent_contribution() -> dict:
    namespace = 'gaming_casino_operations_skills'
    return {'ok': True, 'pbc': 'gaming_casino_operations', 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, 'gaming_casino_operations_crud', 'gaming_casino_operations_documents'), 'side_effects': ()}


def smoke_test() -> dict:
    document = document_instruction_plan('release evidence document', 'create governed market record')
    read_plan = datastore_crud_plan('read')
    create_plan = datastore_crud_plan('create', payload={'status': 'draft'})
    rejected = datastore_crud_plan('update', table='foreign_operational_table')
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document['ok'] and read_plan['ok'] and create_plan['ok'] and rejected['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}

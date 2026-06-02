"""UI forms, wizards, controls, and workbench contracts for gaming_casino_operations."""

from __future__ import annotations

from typing import Any

from .domain_depth import DOMAIN_EDGE_CASES, DOMAIN_OPERATIONS, DOMAIN_PARAMETERS, DOMAIN_RULES, DOMAIN_WORKBENCH_VIEWS, domain_capability_surface_contract
from .permissions import permission_manifest


PBC_KEY = "gaming_casino_operations"


def _forms() -> tuple[dict[str, Any], ...]:
    return (
        {
            "id": "patron_enrollment_form",
            "title": "Patron Enrollment Review",
            "fields": ("player_number", "legal_name", "date_of_birth", "identity_confidence", "age_verified"),
        },
        {
            "id": "slot_fault_form",
            "title": "Slot Fault Recovery",
            "fields": ("slot_machine_id", "fault_state", "meter_snapshot", "recovery_approval"),
        },
        {
            "id": "payout_approval_form",
            "title": "Hand-Pay Approval",
            "fields": ("payout_id", "amount", "approved_by", "witness_id", "approval_notes"),
        },
        {
            "id": "responsible_gaming_case_form",
            "title": "Responsible Gaming Intervention",
            "fields": ("player_profile_id", "risk_level", "intervention_state", "cooling_off_hours", "owner_id"),
        },
    )


def _wizards() -> tuple[dict[str, Any], ...]:
    return (
        {
            "id": "table_shift_close_wizard",
            "workflow": "gaming_casino_operations_table_shift_close_workflow",
            "steps": ("variance_review", "supervisor_signoff", "closure_publish"),
        },
        {
            "id": "jackpot_handpay_wizard",
            "workflow": "gaming_casino_operations_jackpot_handpay_workflow",
            "steps": ("create_payout", "dual_control_review", "release_to_cage"),
        },
        {
            "id": "patron_enrollment_wizard",
            "workflow": "gaming_casino_operations_patron_enrollment_workflow",
            "steps": ("identity_evidence", "duplicate_review", "activation_decision"),
        },
    )


def _controls() -> tuple[dict[str, Any], ...]:
    return (
        {"id": "restriction_override_control", "action": "apply_player_restriction", "confirmation_required": True},
        {"id": "slot_return_to_service_control", "action": "handle_slot_machine", "confirmation_required": True},
        {"id": "payout_release_control", "action": "handle_payout", "confirmation_required": True},
    )


def gaming_casino_operations_ui_contract() -> dict[str, Any]:
    from .routes import standalone_route_contracts

    surface = domain_capability_surface_contract()
    permissions = permission_manifest()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "GamingCasinoOperationsWorkbench",
            "GamingCasinoOperationsDetail",
            "GamingCasinoOperationsAssistantPanel",
        ),
        "forms": _forms(),
        "wizards": _wizards(),
        "controls": _controls(),
        "persona_views": DOMAIN_WORKBENCH_VIEWS,
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": permissions["action_permissions"],
        "routes": standalone_route_contracts()["contracts"],
        "full_capability_surface": surface,
        "side_effects": (),
    }


def gaming_casino_operations_standalone_workbench_blueprint() -> dict[str, Any]:
    contract = gaming_casino_operations_ui_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": "/app/gaming-casino-operations/workbench",
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "queues": (
            "patron_identity_reviews",
            "restricted_players",
            "open_tables",
            "slot_faults",
            "active_sessions",
            "pending_payouts",
            "responsible_gaming_cases",
            "compliance_cases",
            "dead_letters",
        ),
        "navigation_sections": ("overview", "floor", "cage", "responsible_gaming", "compliance", "assistant"),
        "side_effects": (),
    }


def gaming_casino_operations_render_workbench() -> dict[str, Any]:
    blueprint = gaming_casino_operations_standalone_workbench_blueprint()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": blueprint["route"],
        "operation_actions": DOMAIN_OPERATIONS,
        "parameter_editors": DOMAIN_PARAMETERS,
        "rule_editors": DOMAIN_RULES,
        "edge_case_queues": DOMAIN_EDGE_CASES,
        "side_effects": (),
    }


def gaming_casino_operations_render_standalone_workbench(workbench: dict[str, Any]) -> dict[str, Any]:
    queues = workbench.get("queues", {})
    summary = workbench.get("summary", {})
    cards = (
        {"id": "players", "label": "Players", "value": summary.get("player_count", 0)},
        {"id": "tables", "label": "Open Tables", "value": len(queues.get("open_tables", ()))},
        {"id": "slots", "label": "Slot Faults", "value": len(queues.get("slot_faults", ()))},
        {"id": "payouts", "label": "Pending Payouts", "value": len(queues.get("pending_payouts", ()))},
    )
    alerts = tuple(
        alert
        for alert in (
            "identity_reviews_pending" if queues.get("patron_identity_reviews") else None,
            "restricted_players_present" if queues.get("restricted_players") else None,
            "dead_letter_attention" if queues.get("dead_letters") else None,
        )
        if alert
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "cards": cards,
        "alerts": alerts,
        "queues": tuple(sorted(queues)),
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    contract = gaming_casino_operations_ui_contract()
    blueprint = gaming_casino_operations_standalone_workbench_blueprint()
    rendered = gaming_casino_operations_render_standalone_workbench({"summary": {"player_count": 1}, "queues": {"open_tables": (), "slot_faults": (), "pending_payouts": (), "patron_identity_reviews": (), "restricted_players": (), "dead_letters": ()}})
    return {
        "ok": contract["ok"] and blueprint["ok"] and rendered["ok"],
        "side_effects": (),
    }


from .casino_control import improve1_casino_control_contract

_gaming_casino_operations_base_ui_contract = gaming_casino_operations_ui_contract
_gaming_casino_operations_base_render_workbench = gaming_casino_operations_render_workbench

def gaming_casino_operations_ui_contract() -> dict[str, Any]:
    ui = _gaming_casino_operations_base_ui_contract()
    control = improve1_casino_control_contract()
    surface = dict(ui.get('full_capability_surface', {}))
    surface['casino_control_panels'] = tuple(item['evidence']['ui_surface'] for item in control['capabilities'])
    surface['casino_control_service_actions'] = tuple(item['evidence']['service_api'] for item in control['capabilities'])
    surface['casino_control_tables'] = control['owned_tables']
    return {**ui, 'ok': ui.get('ok') is True and control['ok'], 'full_capability_surface': surface, 'casino_control_contract': control, 'side_effects': ()}

def gaming_casino_operations_render_workbench() -> dict[str, Any]:
    workbench = _gaming_casino_operations_base_render_workbench()
    control = improve1_casino_control_contract()
    return {**workbench, 'ok': workbench.get('ok') is True and control['ok'], 'casino_control_panels': tuple(item['evidence']['ui_surface'] for item in control['capabilities']), 'casino_control_service_actions': tuple(item['evidence']['service_api'] for item in control['capabilities']), 'side_effects': ()}

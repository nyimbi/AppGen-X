"""Permissions contract for gaming_casino_operations."""

from __future__ import annotations

from typing import Any


PBC_KEY = "gaming_casino_operations"
PERMISSIONS = (
    "gaming_casino_operations.read",
    "gaming_casino_operations.create",
    "gaming_casino_operations.update",
    "gaming_casino_operations.approve",
    "gaming_casino_operations.admin",
)
ROLE_GRANTS = {
    "operator": (
        "gaming_casino_operations.read",
        "gaming_casino_operations.create",
        "gaming_casino_operations.update",
    ),
    "pit_supervisor": PERMISSIONS[:-1] + ("gaming_casino_operations.admin",),
    "cage_supervisor": PERMISSIONS[:-1] + ("gaming_casino_operations.admin",),
    "compliance_officer": (
        "gaming_casino_operations.read",
        "gaming_casino_operations.update",
        "gaming_casino_operations.approve",
        "gaming_casino_operations.admin",
    ),
    "auditor": (
        "gaming_casino_operations.read",
        "gaming_casino_operations.admin",
    ),
}
ACTION_PERMISSIONS = {
    "configure_runtime": "gaming_casino_operations.admin",
    "register_defaults": "gaming_casino_operations.admin",
    "set_parameter": "gaming_casino_operations.admin",
    "register_rule": "gaming_casino_operations.admin",
    "register_schema_extension": "gaming_casino_operations.admin",
    "receive_event": "gaming_casino_operations.update",
    "create_player_profile": "gaming_casino_operations.create",
    "apply_player_restriction": "gaming_casino_operations.approve",
    "handle_table_game": "gaming_casino_operations.update",
    "handle_slot_machine": "gaming_casino_operations.update",
    "handle_wager_session": "gaming_casino_operations.update",
    "handle_payout": "gaming_casino_operations.approve",
    "open_responsible_gaming_case": "gaming_casino_operations.approve",
    "record_compliance_case": "gaming_casino_operations.approve",
    "request_surveillance_review": "gaming_casino_operations.approve",
    "create_control_assertion": "gaming_casino_operations.admin",
    "register_governed_model": "gaming_casino_operations.admin",
    "build_workbench_view": "gaming_casino_operations.read",
    "query_workbench": "gaming_casino_operations.read",
    "run_advanced_assessment": "gaming_casino_operations.read",
    "parse_document_instruction": "gaming_casino_operations.read",
    "build_schema_contract": "gaming_casino_operations.admin",
    "build_service_contract": "gaming_casino_operations.admin",
    "build_release_evidence": "gaming_casino_operations.admin",
}


def permission_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": ROLE_GRANTS,
        "action_permissions": ACTION_PERMISSIONS,
        "side_effects": (),
    }


def authorize(permission: str | None = None, actor: dict[str, Any] | None = None, action: str | None = None) -> dict[str, Any]:
    actor = dict(actor or {})
    requested = permission or ACTION_PERMISSIONS.get(action or "", "")
    role = actor.get("role")
    granted = requested in PERMISSIONS and (
        not role or requested in ROLE_GRANTS.get(role, ()) or requested == "gaming_casino_operations.read"
    )
    return {
        "ok": granted,
        "permission": requested,
        "actor": actor,
        "action": action,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    return {
        "ok": permission_manifest()["ok"]
        and authorize(action="build_workbench_view", actor={"role": "operator"})["ok"]
        and authorize(action="build_release_evidence", actor={"role": "operator"})["ok"] is False,
        "side_effects": (),
    }

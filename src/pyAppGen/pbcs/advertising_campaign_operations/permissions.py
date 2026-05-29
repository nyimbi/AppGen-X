"""Permission matrix for the advertising campaign standalone slice."""

from __future__ import annotations

PBC_KEY = "advertising_campaign_operations"
PERMISSIONS = (
    "advertising_campaign_operations.read",
    "advertising_campaign_operations.create",
    "advertising_campaign_operations.update",
    "advertising_campaign_operations.approve",
    "advertising_campaign_operations.admin",
)
ROLE_BINDINGS = {
    "campaign_manager": (
        "advertising_campaign_operations.read",
        "advertising_campaign_operations.create",
        "advertising_campaign_operations.update",
    ),
    "buyer": (
        "advertising_campaign_operations.read",
        "advertising_campaign_operations.update",
    ),
    "audience_analyst": (
        "advertising_campaign_operations.read",
        "advertising_campaign_operations.update",
    ),
    "launch_approver": (
        "advertising_campaign_operations.read",
        "advertising_campaign_operations.approve",
    ),
    "auditor": ("advertising_campaign_operations.read",),
    "administrator": PERMISSIONS,
}
ACTION_PERMISSIONS = {
    "configure_runtime": "advertising_campaign_operations.admin",
    "set_parameter": "advertising_campaign_operations.admin",
    "register_rule": "advertising_campaign_operations.admin",
    "register_schema_extension": "advertising_campaign_operations.admin",
    "receive_event": "advertising_campaign_operations.admin",
    "create_campaign_plan": "advertising_campaign_operations.create",
    "review_launch_readiness": "advertising_campaign_operations.read",
    "attempt_launch_campaign": "advertising_campaign_operations.approve",
    "query_workbench": "advertising_campaign_operations.read",
    "document_instruction_plan": "advertising_campaign_operations.update",
    "campaign_brief_preview": "advertising_campaign_operations.read",
    "launch_readiness_preview": "advertising_campaign_operations.read",
    "query_release_snapshot": "advertising_campaign_operations.read",
    "query_service_contract": "advertising_campaign_operations.read",
}


def principal_permissions(actor: dict | None = None) -> tuple[str, ...]:
    actor = dict(actor or {})
    explicit = tuple(actor.get("permissions") or ())
    roles = tuple(actor.get("roles") or ())
    derived = {
        permission
        for role in roles
        for permission in ROLE_BINDINGS.get(role, ())
    }
    return tuple(sorted(set(explicit) | derived))


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": ROLE_BINDINGS,
        "action_permissions": ACTION_PERMISSIONS,
        "side_effects": (),
    }


def permissions_matrix() -> dict:
    manifest = permission_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "roles": tuple(
            {"role": role, "permissions": permissions}
            for role, permissions in ROLE_BINDINGS.items()
        ),
        "action_permissions": ACTION_PERMISSIONS,
        "side_effects": (),
    }


def authorize(permission: str | None = None, actor: dict | None = None, *, action: str | None = None) -> dict:
    requested_permission = permission or ACTION_PERMISSIONS.get(action)
    granted_permissions = principal_permissions(actor)
    authorized = requested_permission in granted_permissions or "advertising_campaign_operations.admin" in granted_permissions
    return {
        "ok": requested_permission in PERMISSIONS,
        "authorized": authorized,
        "permission": requested_permission,
        "action": action,
        "actor": dict(actor or {}),
        "granted_permissions": granted_permissions,
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = permission_manifest()
    admin = authorize(action="configure_runtime", actor={"roles": ("administrator",)})
    auditor = authorize(action="attempt_launch_campaign", actor={"roles": ("auditor",)})
    return {
        "ok": manifest["ok"] and admin["authorized"] is True and auditor["authorized"] is False,
        "manifest": manifest,
        "admin": admin,
        "auditor": auditor,
        "side_effects": (),
    }

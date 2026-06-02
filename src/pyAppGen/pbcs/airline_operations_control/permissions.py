"""Executable permission contract for the airline_operations_control PBC."""

from __future__ import annotations

from .runtime import airline_operations_control_permissions_contract


PBC_KEY = "airline_operations_control"
ACTION_PERMISSIONS = airline_operations_control_permissions_contract()["action_permissions"]
PERMISSIONS = tuple(sorted(set(ACTION_PERMISSIONS.values())))
ROLE_BUNDLES = airline_operations_control_permissions_contract()["role_bundles"]


def permission_manifest() -> dict:
    return {
        "ok": bool(PERMISSIONS) and bool(ACTION_PERMISSIONS),
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": dict(ACTION_PERMISSIONS),
        "role_bundles": ROLE_BUNDLES,
        "side_effects": (),
    }


def authorize(subject: str, granted_permissions: tuple[str, ...] = (), actor: dict | None = None) -> dict:
    granted = tuple(sorted(set(granted_permissions)))
    if subject in ACTION_PERMISSIONS:
        required = ACTION_PERMISSIONS[subject]
        allowed = required in granted
        return {
            "ok": True,
            "allowed": allowed,
            "action": subject,
            "required_permission": required,
            "granted_permissions": granted,
            "actor": dict(actor or {}),
            "side_effects": (),
        }
    if subject in PERMISSIONS or subject == f"{PBC_KEY}.operate":
        allowed = subject in granted or not granted_permissions
        return {
            "ok": True,
            "allowed": allowed,
            "permission": subject,
            "granted_permissions": granted,
            "actor": dict(actor or {}),
            "side_effects": (),
        }
    return {"ok": False, "allowed": False, "subject": subject, "granted_permissions": granted, "actor": dict(actor or {}), "side_effects": ()}


def role_permissions(role: str) -> dict:
    permissions = ROLE_BUNDLES.get(role)
    return {"ok": permissions is not None, "role": role, "permissions": permissions or (), "side_effects": ()}


def smoke_test() -> dict:
    manifest = permission_manifest()
    action = next(iter(ACTION_PERMISSIONS))
    decision = authorize(action, (ACTION_PERMISSIONS[action],))
    bundle = role_permissions("network_controller")
    return {"ok": manifest["ok"] and decision["allowed"] and bundle["ok"], "manifest": manifest, "decision": decision, "bundle": bundle, "side_effects": ()}

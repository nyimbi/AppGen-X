"""Executable permission contract for the enterprise_pim PBC."""

from __future__ import annotations

from .runtime import enterprise_pim_permissions_contract


PBC_KEY = "enterprise_pim"
_PERMISSION_CONTRACT = enterprise_pim_permissions_contract()
PERMISSIONS = _PERMISSION_CONTRACT["permissions"]
ACTION_PERMISSIONS = _PERMISSION_CONTRACT["action_permissions"]


def permission_manifest():
    """Return the permission surface without mutating runtime state."""
    return {
        "ok": bool(PERMISSIONS),
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": dict(ACTION_PERMISSIONS),
        "side_effects": (),
    }


def authorize(action, granted_permissions=()):
    """Evaluate one action against a caller permission set."""
    required = ACTION_PERMISSIONS.get(action)
    allowed = required in set(granted_permissions) if required else False
    return {
        "ok": required is not None,
        "allowed": allowed,
        "action": action,
        "required_permission": required,
        "granted_permissions": tuple(granted_permissions),
        "side_effects": (),
    }


def authorize_permission(required_permission, granted_permissions=()):
    """Evaluate a raw permission requirement against a caller permission set."""
    granted = set(granted_permissions)
    return {
        "ok": bool(required_permission),
        "allowed": required_permission in granted,
        "required_permission": required_permission,
        "granted_permissions": tuple(granted_permissions),
        "side_effects": (),
    }


def smoke_test():
    """Exercise one permission decision side-effect-free."""
    manifest = permission_manifest()
    action, permission = next(iter(ACTION_PERMISSIONS.items())) if ACTION_PERMISSIONS else (None, None)
    decision = authorize(action, (permission,)) if action else {"ok": False, "allowed": False}
    route_decision = authorize_permission(permission, (permission,)) if permission else {"ok": False, "allowed": False}
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"] and route_decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "route_decision": route_decision,
        "side_effects": (),
    }

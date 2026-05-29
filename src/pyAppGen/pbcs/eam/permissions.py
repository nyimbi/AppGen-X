"""Executable permission contract for the EAM PBC."""

from __future__ import annotations

from .runtime import eam_permissions_contract


PBC_KEY = "eam"
_RUNTIME_PERMISSIONS = eam_permissions_contract()
PERMISSIONS = _RUNTIME_PERMISSIONS["permissions"]
ACTION_PERMISSIONS = dict(_RUNTIME_PERMISSIONS["action_permissions"])


def permission_manifest():
    """Return the permission surface without mutating runtime state."""
    return {
        "ok": bool(PERMISSIONS) and bool(ACTION_PERMISSIONS),
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": ACTION_PERMISSIONS,
        "rbac_tables": _RUNTIME_PERMISSIONS.get("rbac_tables", ()),
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


def smoke_test():
    """Exercise one permission decision side-effect-free."""
    manifest = permission_manifest()
    action = "register_equipment"
    decision = authorize(action, ("eam.equipment",))
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }

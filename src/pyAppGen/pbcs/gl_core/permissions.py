"""Executable permission contract for the gl_core PBC."""

from __future__ import annotations

from .runtime import gl_core_permissions_contract


PBC_KEY = "gl_core"
_PERMISSION_CONTRACT = {**gl_core_permissions_contract(), "pbc": PBC_KEY}
PERMISSIONS = _PERMISSION_CONTRACT["permissions"]
ACTION_PERMISSIONS = dict(_PERMISSION_CONTRACT["action_permissions"])


def permission_manifest():
    """Return the permission surface without mutating runtime state."""
    return {
        "ok": bool(PERMISSIONS) and bool(ACTION_PERMISSIONS),
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


def smoke_test():
    """Exercise one permission decision side-effect-free."""
    manifest = permission_manifest()
    action = "receive_event"
    decision = authorize(action, (ACTION_PERMISSIONS[action],))
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }

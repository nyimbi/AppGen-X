"""Executable permission contract for the enterprise_search_vector PBC."""

from __future__ import annotations

from .runtime import enterprise_search_vector_permissions_contract


PBC_KEY = "enterprise_search_vector"
_RUNTIME_PERMISSIONS = enterprise_search_vector_permissions_contract()
PERMISSIONS = _RUNTIME_PERMISSIONS["permissions"]
ACTION_PERMISSIONS = _RUNTIME_PERMISSIONS["action_permissions"]


def permission_manifest() -> dict:
    """Return the permission surface without mutating runtime state."""
    return {
        "ok": bool(PERMISSIONS) and bool(ACTION_PERMISSIONS),
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": dict(ACTION_PERMISSIONS),
        "side_effects": (),
    }


def authorize(action: str, granted_permissions: tuple[str, ...] = ()) -> dict:
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


def smoke_test() -> dict:
    """Exercise one permission decision side-effect-free."""
    manifest = permission_manifest()
    action, permission = next(iter(ACTION_PERMISSIONS.items())) if ACTION_PERMISSIONS else (None, None)
    decision = authorize(action, (permission,)) if action else {"ok": False, "allowed": False}
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }

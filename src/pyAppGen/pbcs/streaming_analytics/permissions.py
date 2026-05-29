"""Executable permission contract for the streaming_analytics PBC."""

from __future__ import annotations

from .runtime import streaming_analytics_permissions_contract


PBC_KEY = "streaming_analytics"


def permission_manifest() -> dict:
    """Return the package-local permission surface without mutating runtime state."""
    manifest = streaming_analytics_permissions_contract()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "permissions": tuple(manifest["permissions"]),
        "roles": dict(manifest["roles"]),
        "policy_controls": tuple(manifest["policy_controls"]),
        "action_permissions": dict(manifest["action_permissions"]),
        "side_effects": (),
    }


def authorize(action: str, granted_permissions: tuple[str, ...] = ()) -> dict:
    """Evaluate one action against a caller permission set."""
    manifest = permission_manifest()
    required = manifest["action_permissions"].get(action)
    granted = tuple(granted_permissions)
    allowed = required in set(granted) if required else False
    return {
        "ok": required is not None,
        "allowed": allowed,
        "action": action,
        "required_permission": required,
        "granted_permissions": granted,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one permission decision side-effect-free."""
    manifest = permission_manifest()
    action, permission = next(iter(manifest["action_permissions"].items()))
    decision = authorize(action, (permission,))
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }

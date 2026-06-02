"""Executable permission contract for the loyalty_rewards PBC."""

from __future__ import annotations

from .runtime import loyalty_rewards_permissions_contract


PBC_KEY = "loyalty_rewards"


def permission_manifest() -> dict:
    """Return the permission surface without mutating runtime state."""
    contract = loyalty_rewards_permissions_contract()
    return {
        "ok": contract.get("ok") is True and bool(contract.get("permissions")),
        "pbc": PBC_KEY,
        "format": contract.get("format"),
        "permissions": tuple(contract.get("permissions", ())),
        "action_permissions": dict(contract.get("action_permissions", {})),
        "side_effects": (),
    }


def authorize(action: str, granted_permissions: tuple[str, ...] = ()) -> dict:
    """Evaluate one action against a caller permission set."""
    manifest = permission_manifest()
    required = manifest["action_permissions"].get(action)
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
    """Exercise permission manifest alignment and one authorization decision."""
    manifest = permission_manifest()
    action = "enroll_member"
    permission = manifest["action_permissions"].get(action)
    decision = authorize(action, (permission,)) if permission else {"ok": False, "allowed": False}
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }

"""Executable permission contract for the ar_credit PBC."""

from __future__ import annotations

from .runtime import ar_credit_permissions_contract


PBC_KEY = "ar_credit"
PERMISSION_CONTRACT = ar_credit_permissions_contract()
PERMISSIONS = PERMISSION_CONTRACT["permissions"]
ACTION_PERMISSIONS = PERMISSION_CONTRACT["action_permissions"]


def permission_manifest() -> dict:
    return {
        **PERMISSION_CONTRACT,
        "pbc": PBC_KEY,
        "side_effects": (),
    }


def authorize(action: str, granted_permissions: tuple[str, ...] = ()) -> dict:
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
    manifest = permission_manifest()
    decision = authorize("apply_cash", ("ar_credit.cash",))
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }

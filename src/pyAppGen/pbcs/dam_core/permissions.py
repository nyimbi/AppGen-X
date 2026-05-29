"""Executable permission contract for the dam_core PBC."""

from __future__ import annotations

from .runtime import dam_core_permissions_contract


PBC_KEY = "dam_core"
ACTION_PERMISSIONS = dam_core_permissions_contract()
PERMISSIONS = tuple(sorted(set(ACTION_PERMISSIONS.values())))
ROLE_BUNDLES = {
    "asset_operator": (
        "dam_core.asset.write",
        "dam_core.rendition.write",
        "dam_core.metadata.write",
        "dam_core.workflow",
    ),
    "rights_manager": (
        "dam_core.rights.manage",
        "dam_core.rights.evaluate",
        "dam_core.audit",
    ),
    "release_auditor": (
        "dam_core.audit",
        "dam_core.event.consume",
        "dam_core.configure",
    ),
}


def permission_manifest() -> dict:
    """Return the permission surface without mutating runtime state."""
    return {
        "ok": bool(PERMISSIONS) and bool(ACTION_PERMISSIONS),
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": dict(ACTION_PERMISSIONS),
        "role_bundles": ROLE_BUNDLES,
        "side_effects": (),
    }


def authorize(action: str, granted_permissions: tuple[str, ...] = ()) -> dict:
    """Evaluate one action against a caller permission set."""
    required = ACTION_PERMISSIONS.get(action)
    granted = set(granted_permissions)
    return {
        "ok": required is not None,
        "allowed": required in granted if required else False,
        "action": action,
        "required_permission": required,
        "granted_permissions": tuple(sorted(granted)),
        "side_effects": (),
    }


def role_permissions(role: str) -> dict:
    """Return the permission bundle for one named role."""
    permissions = ROLE_BUNDLES.get(role)
    return {
        "ok": permissions is not None,
        "role": role,
        "permissions": permissions or (),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one permission decision side-effect-free."""
    manifest = permission_manifest()
    action = next(iter(ACTION_PERMISSIONS), None)
    permission = ACTION_PERMISSIONS[action] if action else None
    decision = authorize(action, (permission,)) if action and permission else {"ok": False, "allowed": False}
    bundle = role_permissions("asset_operator")
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"] and bundle["ok"],
        "manifest": manifest,
        "decision": decision,
        "bundle": bundle,
        "side_effects": (),
    }

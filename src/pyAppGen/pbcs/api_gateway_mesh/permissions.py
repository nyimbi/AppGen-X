"""Executable permission contract for the api_gateway_mesh PBC."""

from __future__ import annotations

from .runtime import api_gateway_mesh_permissions_contract


PBC_KEY = "api_gateway_mesh"


def permission_manifest() -> dict:
    """Return the permission surface aligned to the runtime contract."""
    contract = api_gateway_mesh_permissions_contract()
    return {
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "permissions": tuple(contract["permissions"]),
        "action_permissions": dict(contract["action_permissions"]),
        "side_effects": (),
    }


def authorize(action: str, granted_permissions=()) -> dict:
    """Evaluate one action against a caller permission set."""
    manifest = permission_manifest()
    required = manifest["action_permissions"].get(action)
    granted = set(granted_permissions)
    return {
        "ok": required is not None,
        "allowed": required in granted if required else False,
        "action": action,
        "required_permission": required,
        "granted_permissions": tuple(granted_permissions),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one runtime-aligned permission decision side-effect-free."""
    manifest = permission_manifest()
    action = "publish_route"
    decision = authorize(action, ("api_gateway_mesh.route",))
    return {
        "ok": manifest["ok"] and decision["ok"] and decision["allowed"],
        "manifest": manifest,
        "decision": decision,
        "side_effects": (),
    }

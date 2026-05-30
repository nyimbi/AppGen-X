"""Permission metadata for the energy_grid_operations PBC."""

from __future__ import annotations

from .runtime import PBC_KEY, energy_grid_operations_permissions_contract

_PERMISSION_CONTRACT = energy_grid_operations_permissions_contract()
PERMISSIONS = _PERMISSION_CONTRACT["permission_set"]
ROLE_BINDINGS = _PERMISSION_CONTRACT["roles"]


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "action_permissions": _PERMISSION_CONTRACT["permissions"],
        "roles": ROLE_BINDINGS,
        "side_effects": (),
    }


def authorize(permission: str, actor: dict | None = None) -> dict:
    actor = dict(actor or {})
    roles = tuple(actor.get("roles", ()))
    granted = set()
    for role in roles:
        granted.update(ROLE_BINDINGS.get(role, ()))
    ok = permission in PERMISSIONS or permission == f"{PBC_KEY}.operate"
    if roles:
        ok = ok and (permission in granted or permission == f"{PBC_KEY}.operate" and bool(granted))
    return {
        "ok": ok,
        "permission": permission,
        "actor": actor,
        "granted_permissions": tuple(sorted(granted)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": permission_manifest()["ok"]
        and authorize("energy_grid_operations.read", {"roles": ("operator",)})["ok"],
        "side_effects": (),
    }

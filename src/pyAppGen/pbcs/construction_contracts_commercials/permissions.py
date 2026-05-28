from __future__ import annotations

from .core import PERMISSIONS, PBC_KEY, construction_contracts_commercials_authorize, construction_contracts_commercials_permissions_contract


def permission_manifest():
    contract = construction_contracts_commercials_permissions_contract()
    return {
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(role["role"] for role in contract["roles"]),
        "role_contracts": contract["roles"],
        "side_effects": (),
    }


def authorize(permission, actor=None):
    return construction_contracts_commercials_authorize(permission, actor=actor)


def smoke_test():
    return {
        "ok": permission_manifest()["ok"] and authorize("construction_contracts_commercials.read", {"roles": ("auditor",)})["ok"],
        "side_effects": (),
    }

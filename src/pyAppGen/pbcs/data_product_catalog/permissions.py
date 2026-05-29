"""Permission descriptors for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import PBC_KEY, PERMISSIONS, RBAC_ROLES


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "rbac_roles": RBAC_ROLES,
        "side_effects": (),
    }


def authorize(actor: str, permission: str) -> dict:
    allowed = permission in PERMISSIONS
    return {
        "ok": allowed,
        "allowed": allowed,
        "actor": actor,
        "permission": permission,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": permission_manifest()["ok"] and authorize("system", PERMISSIONS[0])["allowed"],
        "side_effects": (),
    }

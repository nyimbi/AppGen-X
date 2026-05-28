"""RBAC contracts for the case_knowledge_management PBC."""

from __future__ import annotations

from .domain_depth import PBC_KEY
from .domain_depth import PERMISSIONS
from .domain_depth import RBAC_ROLES


ROLE_PERMISSIONS = {
    "reader": (f"{PBC_KEY}.read",),
    "operator": (f"{PBC_KEY}.read", f"{PBC_KEY}.create", f"{PBC_KEY}.update"),
    "knowledge_author": (f"{PBC_KEY}.read", f"{PBC_KEY}.create", f"{PBC_KEY}.update"),
    "approver": (
        f"{PBC_KEY}.read",
        f"{PBC_KEY}.create",
        f"{PBC_KEY}.update",
        f"{PBC_KEY}.approve",
    ),
    "admin": PERMISSIONS,
}


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "rbac_roles": RBAC_ROLES,
        "role_permissions": ROLE_PERMISSIONS,
        "side_effects": (),
    }


def authorize(actor: str | dict, permission: str) -> dict:
    if isinstance(actor, dict):
        roles = tuple(actor.get("roles", ()))
    elif actor == "system":
        roles = ("admin",)
    else:
        roles = (str(actor),)
    granted = set()
    for role in roles:
        granted.update(ROLE_PERMISSIONS.get(role, ()))
    allowed = permission in granted
    return {
        "ok": permission in PERMISSIONS,
        "allowed": allowed,
        "actor": actor,
        "permission": permission,
        "roles": roles,
        "side_effects": (),
    }


def smoke_test() -> dict:
    authorization = authorize("system", PERMISSIONS[0])
    return {
        "ok": permission_manifest()["ok"] and authorization["allowed"],
        "side_effects": (),
    }

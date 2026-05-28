"""RBAC helpers for chemical_batch_compliance."""

from __future__ import annotations

from .slice_app import PBC_KEY
from .slice_app import PERMISSIONS
from .slice_app import ROLE_PERMISSIONS


def permission_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "permissions": PERMISSIONS, "roles": tuple(ROLE_PERMISSIONS), "side_effects": ()}


def authorize(permission: str, actor: dict | None = None) -> dict:
    actor = dict(actor or {})
    role = actor.get("role")
    granted = permission in PERMISSIONS or permission == f"{PBC_KEY}.operate"
    if role and role in ROLE_PERMISSIONS:
        granted = granted and (
            permission in ROLE_PERMISSIONS[role]
            or permission == f"{PBC_KEY}.operate" and role == "admin"
        )
    return {"ok": granted, "permission": permission, "actor": actor, "side_effects": ()}


def smoke_test() -> dict:
    return {
        "ok": permission_manifest()["ok"]
        and authorize(PERMISSIONS[0], {"role": "operator"})["ok"]
        and authorize(f"{PBC_KEY}.approve", {"role": "operator"})["ok"] is False,
        "side_effects": (),
    }

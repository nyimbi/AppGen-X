"""Permission model for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from typing import Any

from .models import PERMISSIONS

PBC_KEY = "cybersecurity_operations_center"
ROLE_PERMISSIONS = {
    "operator": {
        "cybersecurity_operations_center.read",
        "cybersecurity_operations_center.create",
        "cybersecurity_operations_center.update",
    },
    "approver": {
        "cybersecurity_operations_center.read",
        "cybersecurity_operations_center.update",
        "cybersecurity_operations_center.approve",
    },
    "auditor": {"cybersecurity_operations_center.read"},
    "admin": set(PERMISSIONS),
}


def permission_manifest() -> dict[str, Any]:
    return {"ok": True, "pbc": PBC_KEY, "permissions": PERMISSIONS, "roles": tuple(ROLE_PERMISSIONS), "side_effects": ()}


def authorize(permission: str, actor: dict[str, Any] | None = None) -> dict[str, Any]:
    actor = dict(actor or {})
    role = actor.get("role", "operator")
    allowed = permission in ROLE_PERMISSIONS.get(role, set()) or permission == f"{PBC_KEY}.operate"
    return {"ok": allowed, "permission": permission, "actor": actor, "side_effects": ()}


def smoke_test() -> dict[str, Any]:
    return {
        "ok": permission_manifest()["ok"]
        and authorize(PERMISSIONS[0], {"role": "operator"})["ok"]
        and authorize("cybersecurity_operations_center.approve", {"role": "operator"})["ok"] is False,
        "side_effects": (),
    }

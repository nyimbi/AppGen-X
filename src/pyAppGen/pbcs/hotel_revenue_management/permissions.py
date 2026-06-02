"""Permissions and RBAC metadata for hotel_revenue_management."""

from __future__ import annotations

from .runtime import PBC_KEY


PERMISSIONS = (
    "hotel_revenue_management.read",
    "hotel_revenue_management.create",
    "hotel_revenue_management.update",
    "hotel_revenue_management.approve",
    "hotel_revenue_management.admin",
)
ROLE_MATRIX = {
    "reader": ("hotel_revenue_management.read",),
    "operator": (
        "hotel_revenue_management.read",
        "hotel_revenue_management.create",
        "hotel_revenue_management.update",
    ),
    "approver": (
        "hotel_revenue_management.read",
        "hotel_revenue_management.update",
        "hotel_revenue_management.approve",
    ),
    "admin": PERMISSIONS,
}


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(ROLE_MATRIX),
        "role_matrix": ROLE_MATRIX,
        "side_effects": (),
    }


def authorize(permission: str, actor: dict | None = None) -> dict:
    actor = dict(actor or {})
    role = actor.get("role", "reader")
    allowed_permissions = ROLE_MATRIX.get(role, ())
    return {
        "ok": permission in PERMISSIONS or permission == f"{PBC_KEY}.operate",
        "authorized": permission in allowed_permissions or permission == f"{PBC_KEY}.operate",
        "permission": permission,
        "actor": actor,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": permission_manifest()["ok"] and authorize(PERMISSIONS[0], {"role": "reader"})["authorized"],
        "side_effects": (),
    }

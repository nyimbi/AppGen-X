"""Role and permission contracts for the bank_payments_clearing PBC."""

from __future__ import annotations


PBC_KEY = "bank_payments_clearing"
PERMISSIONS = (
    "bank_payments_clearing.read",
    "bank_payments_clearing.create",
    "bank_payments_clearing.update",
    "bank_payments_clearing.approve",
    "bank_payments_clearing.admin",
)
ROLE_PERMISSIONS = {
    "operator": (
        "bank_payments_clearing.read",
        "bank_payments_clearing.create",
        "bank_payments_clearing.update",
    ),
    "approver": (
        "bank_payments_clearing.read",
        "bank_payments_clearing.approve",
    ),
    "release_manager": (
        "bank_payments_clearing.read",
        "bank_payments_clearing.update",
        "bank_payments_clearing.approve",
    ),
    "auditor": ("bank_payments_clearing.read",),
    "admin": PERMISSIONS,
}


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(
            {
                "role": role,
                "permissions": permissions,
            }
            for role, permissions in ROLE_PERMISSIONS.items()
        ),
        "workflow_permissions": {
            "instruction_intake": ("bank_payments_clearing.create",),
            "payment_release": ("bank_payments_clearing.approve",),
            "batch_settlement": ("bank_payments_clearing.update", "bank_payments_clearing.approve"),
            "return_reconciliation": ("bank_payments_clearing.update",),
            "configuration": ("bank_payments_clearing.admin",),
        },
        "side_effects": (),
    }


def authorize(permission: str, actor: dict | None = None) -> dict:
    actor = dict(actor or {})
    granted = set(actor.get("permissions", ()))
    for role in actor.get("roles", ()):
        granted.update(ROLE_PERMISSIONS.get(role, ()))
    if actor.get("superuser"):
        granted.update(PERMISSIONS)
    allowed = permission in granted or "bank_payments_clearing.admin" in granted
    return {
        "ok": allowed,
        "permission": permission,
        "actor": actor,
        "granted_permissions": tuple(sorted(granted)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    operator = authorize("bank_payments_clearing.create", {"roles": ("operator",)})
    denied = authorize("bank_payments_clearing.admin", {"roles": ("operator",)})
    return {
        "ok": permission_manifest()["ok"] and operator["ok"] and denied["ok"] is False,
        "side_effects": (),
    }

"""Permission hooks for trade_finance_operations."""

from __future__ import annotations

PBC_KEY = "trade_finance_operations"
PERMISSIONS = (
    "trade_finance_operations.read",
    "trade_finance_operations.create",
    "trade_finance_operations.update",
    "trade_finance_operations.approve",
    "trade_finance_operations.admin",
)
ROLE_MAP = {
    "operator": ("trade_finance_operations.read", "trade_finance_operations.create", "trade_finance_operations.update"),
    "approver": ("trade_finance_operations.read", "trade_finance_operations.approve"),
    "auditor": ("trade_finance_operations.read",),
    "compliance_officer": ("trade_finance_operations.read", "trade_finance_operations.approve", "trade_finance_operations.admin"),
}


def permission_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(ROLE_MAP),
        "action_permissions": {
            "open_case": "trade_finance_operations.create",
            "update_case": "trade_finance_operations.update",
            "approve_release": "trade_finance_operations.approve",
            "view_workbench": "trade_finance_operations.read",
            "administer_rules": "trade_finance_operations.admin",
        },
        "side_effects": (),
    }


def authorize(permission, actor=None):
    actor = dict(actor or {})
    role = actor.get("role")
    granted = permission in PERMISSIONS or permission == f"{PBC_KEY}.operate"
    if role in ROLE_MAP:
        granted = granted or permission in ROLE_MAP[role]
    return {"ok": granted, "permission": permission, "actor": actor, "side_effects": ()}


def role_permissions(role: str):
    return {"ok": role in ROLE_MAP, "role": role, "permissions": ROLE_MAP.get(role, ()), "side_effects": ()}


def smoke_test():
    return {"ok": permission_manifest()["ok"] and authorize(PERMISSIONS[0])["ok"] and role_permissions("operator")["ok"], "side_effects": ()}

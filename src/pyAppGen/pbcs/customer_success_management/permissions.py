"""Permission descriptors for the customer_success_management PBC."""
from __future__ import annotations

PBC_KEY = "customer_success_management"
PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
    f"{PBC_KEY}.operate",
)


def permission_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "permissions": PERMISSIONS, "rbac_roles": ("reader", "operator", "approver", "admin"), "side_effects": ()}


def authorize(actor: str, permission: str) -> dict:
    allowed = permission in PERMISSIONS
    return {"ok": allowed, "allowed": allowed, "actor": actor, "permission": permission, "side_effects": ()}


def smoke_test() -> dict:
    manifest = permission_manifest()
    return {"ok": manifest["ok"] and authorize("system", PERMISSIONS[-1])["allowed"], "side_effects": ()}

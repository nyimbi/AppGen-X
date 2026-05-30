"""Permissions and role grants for the standalone aviation slice."""
from __future__ import annotations

PBC_KEY = "aviation_maintenance_repair"
PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
)
ROLE_GRANTS = {
    "maintenance_controller": (f"{PBC_KEY}.read", f"{PBC_KEY}.create", f"{PBC_KEY}.update"),
    "certifier": (f"{PBC_KEY}.read", f"{PBC_KEY}.approve"),
    "reliability_engineer": (f"{PBC_KEY}.read", f"{PBC_KEY}.create", f"{PBC_KEY}.update"),
    "auditor": (f"{PBC_KEY}.read",),
    "assistant": (f"{PBC_KEY}.read",),
    "admin": PERMISSIONS,
}
OPERATION_PERMISSIONS = {
    "record_aircraft": f"{PBC_KEY}.create",
    "record_component": f"{PBC_KEY}.create",
    "record_work_card": f"{PBC_KEY}.update",
    "record_deferred_defect": f"{PBC_KEY}.update",
    "record_airworthiness_directive": f"{PBC_KEY}.update",
    "plan_document_instruction": f"{PBC_KEY}.update",
    "assess_release_to_service": f"{PBC_KEY}.approve",
    "query_workbench": f"{PBC_KEY}.read",
}


def permission_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(ROLE_GRANTS.keys()),
        "role_grants": ROLE_GRANTS,
        "operation_permissions": OPERATION_PERMISSIONS,
        "side_effects": (),
    }


def authorize(permission, actor=None):
    actor = dict(actor or {})
    if permission == f"{PBC_KEY}.operate":
        permission = f"{PBC_KEY}.update"
    if permission not in PERMISSIONS:
        return {"ok": False, "permission": permission, "actor": actor, "reason": "unknown_permission", "side_effects": ()}
    roles = tuple(actor.get("roles") or ())
    if not roles:
        return {"ok": True, "permission": permission, "actor": actor, "side_effects": ()}
    granted = any(permission in ROLE_GRANTS.get(role, ()) or role == "admin" for role in roles)
    return {"ok": granted, "permission": permission, "actor": actor, "roles": roles, "side_effects": ()}


def operation_authorization(operation, actor=None):
    permission = OPERATION_PERMISSIONS.get(operation, f"{PBC_KEY}.read")
    decision = authorize(permission, actor=actor)
    return {"ok": decision["ok"], "operation": operation, "required_permission": permission, "actor": dict(actor or {}), "side_effects": ()}


def smoke_test():
    manifest = permission_manifest()
    certifier = authorize(f"{PBC_KEY}.approve", {"roles": ("certifier",)})
    denied = authorize(f"{PBC_KEY}.approve", {"roles": ("assistant",)})
    return {"ok": manifest["ok"] and certifier["ok"] and denied["ok"] is False, "side_effects": ()}

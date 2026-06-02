from __future__ import annotations

PBC_KEY = "capital_projects_delivery"
PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
    f"{PBC_KEY}.operate",
)
ROLE_PERMISSIONS = {
    "operator": (f"{PBC_KEY}.read", f"{PBC_KEY}.create", f"{PBC_KEY}.update"),
    "approver": (f"{PBC_KEY}.read", f"{PBC_KEY}.approve"),
    "auditor": (f"{PBC_KEY}.read",),
    "project_sponsor": (f"{PBC_KEY}.read", f"{PBC_KEY}.create", f"{PBC_KEY}.approve"),
    "project_controls_lead": (f"{PBC_KEY}.read", f"{PBC_KEY}.update", f"{PBC_KEY}.approve"),
    "investment_board": (f"{PBC_KEY}.read", f"{PBC_KEY}.approve"),
    "construction_manager": (f"{PBC_KEY}.read", f"{PBC_KEY}.update", f"{PBC_KEY}.approve"),
    "commissioning_manager": (f"{PBC_KEY}.read", f"{PBC_KEY}.update", f"{PBC_KEY}.approve"),
    "operations_manager": (f"{PBC_KEY}.read", f"{PBC_KEY}.approve"),
    "admin": PERMISSIONS,
}


def permission_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(ROLE_PERMISSIONS),
        "role_permissions": ROLE_PERMISSIONS,
        "side_effects": (),
    }


def authorize(permission, actor=None):
    actor = dict(actor or {})
    role = actor.get("role")
    allowed = permission in PERMISSIONS and (role is None or permission in ROLE_PERMISSIONS.get(role, ()))
    return {
        "ok": allowed or permission == f"{PBC_KEY}.operate",
        "permission": permission,
        "actor": actor,
        "resolved_role": role,
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": permission_manifest()["ok"] and authorize(f"{PBC_KEY}.read", {"role": "operator"})["ok"] and authorize(f"{PBC_KEY}.approve", {"role": "auditor"})["ok"] is False,
        "side_effects": (),
    }

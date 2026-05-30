PBC_KEY = "hospitality_property_operations"
PERMISSIONS = (
    "hospitality_property_operations.read",
    "hospitality_property_operations.create",
    "hospitality_property_operations.update",
    "hospitality_property_operations.approve",
    "hospitality_property_operations.admin",
)
ROLE_MAP = {
    "front_office": {PERMISSIONS[0], PERMISSIONS[1], PERMISSIONS[2]},
    "housekeeping_supervisor": {PERMISSIONS[0], PERMISSIONS[2]},
    "revenue_manager": {PERMISSIONS[0], PERMISSIONS[3]},
    "operator": set(PERMISSIONS[:-1]),
    "approver": set(PERMISSIONS),
    "auditor": {PERMISSIONS[0]},
}


def permission_manifest():
    return {"ok": True, "pbc": PBC_KEY, "permissions": PERMISSIONS, "roles": tuple(ROLE_MAP), "side_effects": ()}


def authorize(permission, actor=None):
    actor = dict(actor or {})
    role = actor.get("role", "operator")
    allowed = ROLE_MAP.get(role, set())
    return {"ok": permission in allowed or permission == f"{PBC_KEY}.operate", "permission": permission, "actor": actor, "side_effects": ()}


def smoke_test():
    return {"ok": permission_manifest()["ok"] and authorize(PERMISSIONS[0], {"role": "front_office"})["ok"], "side_effects": ()}

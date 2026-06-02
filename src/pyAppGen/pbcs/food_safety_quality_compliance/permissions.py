from .slice_app import PERMISSIONS
from .slice_app import ROLE_PERMISSIONS
from .slice_app import PBC_KEY


def permission_manifest():
    return {"ok": True, "pbc": PBC_KEY, "permissions": PERMISSIONS, "roles": tuple(ROLE_PERMISSIONS), "role_permissions": ROLE_PERMISSIONS, "side_effects": ()}


def authorize(permission, actor=None):
    actor = dict(actor or {})
    role = actor.get("role")
    allowed = set(PERMISSIONS)
    if role in ROLE_PERMISSIONS:
        allowed.update(ROLE_PERMISSIONS[role])
    allowed.add(f"{PBC_KEY}.operate")
    return {"ok": permission in allowed, "permission": permission, "actor": actor, "side_effects": ()}


def smoke_test():
    return {"ok": permission_manifest()["ok"] and authorize(PERMISSIONS[0], {"role": "operator"})["ok"], "side_effects": ()}

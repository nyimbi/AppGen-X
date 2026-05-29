from .standalone import PERMISSIONS, PBC_KEY, build_permission_manifest


def permission_manifest():
    return build_permission_manifest()


def authorize(permission, actor=None):
    actor = dict(actor or {})
    return {"ok": permission in PERMISSIONS, "permission": permission, "actor": actor, "side_effects": ()}


def smoke_test():
    return {"ok": permission_manifest()["ok"] and authorize(PERMISSIONS[0])["ok"], "side_effects": ()}

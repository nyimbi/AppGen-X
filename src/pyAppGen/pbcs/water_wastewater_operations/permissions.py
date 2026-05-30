from .runtime import water_wastewater_operations_permissions_contract

PBC_KEY = "water_wastewater_operations"


def permission_manifest():
    return water_wastewater_operations_permissions_contract()


def authorize(permission, actor=None):
    manifest = permission_manifest()
    allowed = permission in manifest["permissions"] or permission in manifest["action_permissions"].values()
    return {"ok": allowed, "permission": permission, "actor": dict(actor or {}), "side_effects": ()}


def smoke_test():
    return {"ok": permission_manifest()["ok"] and authorize(f"{PBC_KEY}.operate")["ok"], "side_effects": ()}

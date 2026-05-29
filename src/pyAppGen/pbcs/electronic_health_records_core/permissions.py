"""Permissions for electronic health records core."""
from __future__ import annotations

PBC_KEY = "electronic_health_records_core"
PERMISSIONS = (
    "electronic_health_records_core.read",
    "electronic_health_records_core.create",
    "electronic_health_records_core.update",
    "electronic_health_records_core.approve",
    "electronic_health_records_core.admin",
)
ROLE_PERMISSIONS = {
    "clinician": {PERMISSIONS[0], PERMISSIONS[1], PERMISSIONS[2], PERMISSIONS[3], f"{PBC_KEY}.operate"},
    "nurse": {PERMISSIONS[0], PERMISSIONS[1], PERMISSIONS[2], f"{PBC_KEY}.operate"},
    "pharmacist": {PERMISSIONS[0], PERMISSIONS[1], PERMISSIONS[2], f"{PBC_KEY}.operate"},
    "him_analyst": {PERMISSIONS[0], PERMISSIONS[2], PERMISSIONS[3]},
    "admin": set(PERMISSIONS) | {f"{PBC_KEY}.operate"},
}


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(ROLE_PERMISSIONS),
        "side_effects": (),
    }


def authorize(permission: str, actor: dict | None = None) -> dict:
    actor = dict(actor or {})
    role = actor.get("role")
    if role is None:
        ok = permission in PERMISSIONS or permission == f"{PBC_KEY}.operate"
    else:
        ok = permission in ROLE_PERMISSIONS.get(role, set())
    return {"ok": ok, "permission": permission, "actor": actor, "side_effects": ()}


def smoke_test() -> dict:
    return {
        "ok": permission_manifest()["ok"] and authorize(PERMISSIONS[0])["ok"] and authorize(PERMISSIONS[3], {"role": "clinician"})["ok"],
        "side_effects": (),
    }

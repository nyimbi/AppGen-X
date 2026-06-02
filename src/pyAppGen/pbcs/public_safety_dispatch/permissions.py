from __future__ import annotations

from .standalone import PBC_KEY, PERMISSIONS, build_permissions_contract


def permission_manifest() -> dict:
    return build_permissions_contract()


def authorize(permission: str, actor: dict | None = None) -> dict:
    return {"ok": permission in PERMISSIONS, "permission": permission, "actor": dict(actor or {}), "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": permission_manifest()["ok"] and authorize(PERMISSIONS[0])["ok"], "side_effects": ()}

"""RBAC wrappers for the healthcare claims adjudication package."""

from __future__ import annotations

from .config import PERMISSIONS
from .config import authorize as _authorize
from .config import permission_manifest as _permission_manifest

PBC_KEY = "claims_adjudication_healthcare"


def permission_manifest():
    return _permission_manifest()


def authorize(permission, actor=None):
    return _authorize(permission, actor)


def smoke_test():
    return {
        "ok": permission_manifest()["ok"] and authorize(PERMISSIONS[0], {"role": "platform_admin"})["ok"],
        "side_effects": (),
    }

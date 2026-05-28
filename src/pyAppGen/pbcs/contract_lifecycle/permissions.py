"""Permission descriptors for the contract_lifecycle PBC."""

from .application import PERMISSIONS as _PERMISSIONS
from .application import authorize as _authorize
from .application import permission_manifest as _permission_manifest

PBC_KEY = "contract_lifecycle"
PERMISSIONS = _PERMISSIONS


def permission_manifest():
    return _permission_manifest()


def authorize(actor, permission):
    return _authorize(actor, permission)


def smoke_test():
    return {
        "ok": permission_manifest()["ok"] and authorize({"roles": ("admin",)}, PERMISSIONS[0])["allowed"],
        "manifest": permission_manifest(),
    }

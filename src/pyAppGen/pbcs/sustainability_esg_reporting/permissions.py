"""Permission descriptors for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .blueprint import PBC_KEY, PERMISSIONS


def permission_manifest() -> dict:
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader', 'operator', 'approver', 'admin'), 'side_effects': ()}


def authorize(actor: str, permission: str) -> dict:
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test() -> dict:
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

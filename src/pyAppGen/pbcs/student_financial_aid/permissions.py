from __future__ import annotations

from .slice_app import PBC_KEY, PERMISSIONS


def permission_manifest() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'permissions': PERMISSIONS,
        'roles': ('reader', 'operator', 'approver', 'admin'),
        'side_effects': (),
    }


def authorize(permission: str, granted_permissions=None) -> dict:
    granted = set(granted_permissions or PERMISSIONS)
    return {
        'ok': permission in granted,
        'permission': permission,
        'granted_permissions': tuple(sorted(granted)),
        'side_effects': (),
    }


def permissions_contract() -> dict:
    return permission_manifest()


def smoke_test() -> dict:
    manifest = permission_manifest()
    return {'ok': manifest['ok'] and authorize(f'{PBC_KEY}.read')['ok'], 'side_effects': ()}

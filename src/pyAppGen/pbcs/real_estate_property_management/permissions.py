"""Permission and RBAC descriptors for real estate property management."""
from .standalone import PBC_KEY, PERMISSIONS
from .standalone import permission_manifest as _permission_manifest
from .standalone import authorize as _authorize


def permission_manifest():
    manifest = _permission_manifest()
    manifest['rbac'] = {'roles': manifest.get('roles', ()), 'permissions': PERMISSIONS}
    return manifest


def authorize(permission, actor=None):
    return _authorize(permission, actor)


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

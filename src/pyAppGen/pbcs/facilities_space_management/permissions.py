"""Permission descriptors for the facilities_space_management PBC."""
PBC_KEY = 'facilities_space_management'
PERMISSIONS = ('facilities_space_management.read', 'facilities_space_management.create', 'facilities_space_management.update', 'facilities_space_management.approve', 'facilities_space_management.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

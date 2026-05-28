"""Permission descriptors for the travel_management PBC."""
PBC_KEY = 'travel_management'
PERMISSIONS = ('travel_management.read', 'travel_management.create', 'travel_management.update', 'travel_management.approve', 'travel_management.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

"""Permission descriptors for the revenue_recognition PBC."""
PBC_KEY = 'revenue_recognition'
PERMISSIONS = ('revenue_recognition.read', 'revenue_recognition.create', 'revenue_recognition.update', 'revenue_recognition.approve', 'revenue_recognition.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

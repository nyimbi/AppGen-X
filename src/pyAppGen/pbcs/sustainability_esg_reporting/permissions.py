"""Permission descriptors for the sustainability_esg_reporting PBC."""
PBC_KEY = 'sustainability_esg_reporting'
PERMISSIONS = ('sustainability_esg_reporting.read', 'sustainability_esg_reporting.create', 'sustainability_esg_reporting.update', 'sustainability_esg_reporting.approve', 'sustainability_esg_reporting.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

"""Permission descriptors for the legal_matter_management PBC."""
PBC_KEY = 'legal_matter_management'
PERMISSIONS = ('legal_matter_management.read', 'legal_matter_management.create', 'legal_matter_management.update', 'legal_matter_management.approve', 'legal_matter_management.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

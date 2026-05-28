"""Permission descriptors for the master_data_governance PBC."""
PBC_KEY = 'master_data_governance'
PERMISSIONS = ('master_data_governance.read', 'master_data_governance.create', 'master_data_governance.update', 'master_data_governance.approve', 'master_data_governance.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

"""Permission descriptors for the contract_lifecycle PBC."""
PBC_KEY = 'contract_lifecycle'
PERMISSIONS = ('contract_lifecycle.read', 'contract_lifecycle.create', 'contract_lifecycle.update', 'contract_lifecycle.approve', 'contract_lifecycle.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

"""Permission descriptors for the grant_fund_accounting PBC."""
PBC_KEY = 'grant_fund_accounting'
PERMISSIONS = ('grant_fund_accounting.read', 'grant_fund_accounting.create', 'grant_fund_accounting.update', 'grant_fund_accounting.approve', 'grant_fund_accounting.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

"""Permission descriptors for the project_portfolio_management PBC."""
PBC_KEY = 'project_portfolio_management'
PERMISSIONS = ('project_portfolio_management.read', 'project_portfolio_management.create', 'project_portfolio_management.update', 'project_portfolio_management.approve', 'project_portfolio_management.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

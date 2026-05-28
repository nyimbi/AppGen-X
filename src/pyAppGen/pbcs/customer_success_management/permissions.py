"""Permission descriptors for the customer_success_management PBC."""
PBC_KEY = 'customer_success_management'
PERMISSIONS = ('customer_success_management.read', 'customer_success_management.create', 'customer_success_management.update', 'customer_success_management.approve', 'customer_success_management.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

"""Permission descriptors for the data_product_catalog PBC."""
PBC_KEY = 'data_product_catalog'
PERMISSIONS = ('data_product_catalog.read', 'data_product_catalog.create', 'data_product_catalog.update', 'data_product_catalog.approve', 'data_product_catalog.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

"""Permission descriptors for the vendor_supplier_360 PBC."""
PBC_KEY = 'vendor_supplier_360'
PERMISSIONS = ('vendor_supplier_360.read', 'vendor_supplier_360.create', 'vendor_supplier_360.update', 'vendor_supplier_360.approve', 'vendor_supplier_360.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

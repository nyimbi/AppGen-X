PBC_KEY = 'hospitality_property_operations'
PERMISSIONS = ('hospitality_property_operations.read',
 'hospitality_property_operations.create',
 'hospitality_property_operations.update',
 'hospitality_property_operations.approve',
 'hospitality_property_operations.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

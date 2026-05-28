PBC_KEY = 'land_real_estate_development'
PERMISSIONS = ('land_real_estate_development.read',
 'land_real_estate_development.create',
 'land_real_estate_development.update',
 'land_real_estate_development.approve',
 'land_real_estate_development.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

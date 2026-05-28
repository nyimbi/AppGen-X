PBC_KEY = 'food_safety_quality_compliance'
PERMISSIONS = ('food_safety_quality_compliance.read',
 'food_safety_quality_compliance.create',
 'food_safety_quality_compliance.update',
 'food_safety_quality_compliance.approve',
 'food_safety_quality_compliance.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

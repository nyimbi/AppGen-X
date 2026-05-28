PBC_KEY = 'pharmacy_benefits_management'
PERMISSIONS = ('pharmacy_benefits_management.read',
 'pharmacy_benefits_management.create',
 'pharmacy_benefits_management.update',
 'pharmacy_benefits_management.approve',
 'pharmacy_benefits_management.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

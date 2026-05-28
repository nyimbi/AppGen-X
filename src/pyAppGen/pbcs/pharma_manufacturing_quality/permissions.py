PBC_KEY = 'pharma_manufacturing_quality'
PERMISSIONS = ('pharma_manufacturing_quality.read',
 'pharma_manufacturing_quality.create',
 'pharma_manufacturing_quality.update',
 'pharma_manufacturing_quality.approve',
 'pharma_manufacturing_quality.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

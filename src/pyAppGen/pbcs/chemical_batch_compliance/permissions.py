PBC_KEY = 'chemical_batch_compliance'
PERMISSIONS = ('chemical_batch_compliance.read',
 'chemical_batch_compliance.create',
 'chemical_batch_compliance.update',
 'chemical_batch_compliance.approve',
 'chemical_batch_compliance.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

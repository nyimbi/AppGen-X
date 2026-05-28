PBC_KEY = 'claims_adjudication_healthcare'
PERMISSIONS = ('claims_adjudication_healthcare.read',
 'claims_adjudication_healthcare.create',
 'claims_adjudication_healthcare.update',
 'claims_adjudication_healthcare.approve',
 'claims_adjudication_healthcare.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

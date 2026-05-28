PBC_KEY = 'clinical_care_coordination'
PERMISSIONS = ('clinical_care_coordination.read',
 'clinical_care_coordination.create',
 'clinical_care_coordination.update',
 'clinical_care_coordination.approve',
 'clinical_care_coordination.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

PBC_KEY = 'permitting_licensing_inspections'
PERMISSIONS = ('permitting_licensing_inspections.read',
 'permitting_licensing_inspections.create',
 'permitting_licensing_inspections.update',
 'permitting_licensing_inspections.approve',
 'permitting_licensing_inspections.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

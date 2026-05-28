PBC_KEY = 'humanitarian_relief_operations'
PERMISSIONS = ('humanitarian_relief_operations.read',
 'humanitarian_relief_operations.create',
 'humanitarian_relief_operations.update',
 'humanitarian_relief_operations.approve',
 'humanitarian_relief_operations.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

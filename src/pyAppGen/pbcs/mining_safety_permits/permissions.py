PBC_KEY = 'mining_safety_permits'
PERMISSIONS = ('mining_safety_permits.read',
 'mining_safety_permits.create',
 'mining_safety_permits.update',
 'mining_safety_permits.approve',
 'mining_safety_permits.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

PBC_KEY = 'gaming_casino_operations'
PERMISSIONS = ('gaming_casino_operations.read',
 'gaming_casino_operations.create',
 'gaming_casino_operations.update',
 'gaming_casino_operations.approve',
 'gaming_casino_operations.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

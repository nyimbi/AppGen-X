PBC_KEY = 'livestock_herd_management'
PERMISSIONS = ('livestock_herd_management.read',
 'livestock_herd_management.create',
 'livestock_herd_management.update',
 'livestock_herd_management.approve',
 'livestock_herd_management.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

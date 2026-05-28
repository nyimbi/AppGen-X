PBC_KEY = 'public_safety_dispatch'
PERMISSIONS = ('public_safety_dispatch.read',
 'public_safety_dispatch.create',
 'public_safety_dispatch.update',
 'public_safety_dispatch.approve',
 'public_safety_dispatch.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

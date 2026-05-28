PBC_KEY = 'medical_device_lifecycle'
PERMISSIONS = ('medical_device_lifecycle.read',
 'medical_device_lifecycle.create',
 'medical_device_lifecycle.update',
 'medical_device_lifecycle.approve',
 'medical_device_lifecycle.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

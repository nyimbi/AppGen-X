PBC_KEY = 'airline_operations_control'
PERMISSIONS = ('airline_operations_control.read',
 'airline_operations_control.create',
 'airline_operations_control.update',
 'airline_operations_control.approve',
 'airline_operations_control.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

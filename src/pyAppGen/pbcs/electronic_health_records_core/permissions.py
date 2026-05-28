PBC_KEY = 'electronic_health_records_core'
PERMISSIONS = ('electronic_health_records_core.read',
 'electronic_health_records_core.create',
 'electronic_health_records_core.update',
 'electronic_health_records_core.approve',
 'electronic_health_records_core.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

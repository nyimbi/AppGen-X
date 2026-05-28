PBC_KEY = 'aviation_maintenance_repair'
PERMISSIONS = ('aviation_maintenance_repair.read',
 'aviation_maintenance_repair.create',
 'aviation_maintenance_repair.update',
 'aviation_maintenance_repair.approve',
 'aviation_maintenance_repair.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

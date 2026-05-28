PBC_KEY = 'water_wastewater_operations'
PERMISSIONS = ('water_wastewater_operations.read',
 'water_wastewater_operations.create',
 'water_wastewater_operations.update',
 'water_wastewater_operations.approve',
 'water_wastewater_operations.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

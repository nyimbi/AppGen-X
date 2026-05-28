PBC_KEY = 'defense_readiness_logistics'
PERMISSIONS = ('defense_readiness_logistics.read',
 'defense_readiness_logistics.create',
 'defense_readiness_logistics.update',
 'defense_readiness_logistics.approve',
 'defense_readiness_logistics.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

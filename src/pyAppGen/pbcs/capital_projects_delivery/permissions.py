PBC_KEY = 'capital_projects_delivery'
PERMISSIONS = ('capital_projects_delivery.read',
 'capital_projects_delivery.create',
 'capital_projects_delivery.update',
 'capital_projects_delivery.approve',
 'capital_projects_delivery.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

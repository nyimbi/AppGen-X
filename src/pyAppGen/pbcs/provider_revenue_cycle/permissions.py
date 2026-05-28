PBC_KEY = 'provider_revenue_cycle'
PERMISSIONS = ('provider_revenue_cycle.read',
 'provider_revenue_cycle.create',
 'provider_revenue_cycle.update',
 'provider_revenue_cycle.approve',
 'provider_revenue_cycle.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

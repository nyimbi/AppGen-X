PBC_KEY = 'utility_outage_restoration'
PERMISSIONS = ('utility_outage_restoration.read',
 'utility_outage_restoration.create',
 'utility_outage_restoration.update',
 'utility_outage_restoration.approve',
 'utility_outage_restoration.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

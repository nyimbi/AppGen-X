PBC_KEY = 'donor_grant_fundraising'
PERMISSIONS = ('donor_grant_fundraising.read',
 'donor_grant_fundraising.create',
 'donor_grant_fundraising.update',
 'donor_grant_fundraising.approve',
 'donor_grant_fundraising.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

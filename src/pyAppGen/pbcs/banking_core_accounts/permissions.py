PBC_KEY = 'banking_core_accounts'
PERMISSIONS = ('banking_core_accounts.read',
 'banking_core_accounts.create',
 'banking_core_accounts.update',
 'banking_core_accounts.approve',
 'banking_core_accounts.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

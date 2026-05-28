PBC_KEY = 'construction_contracts_commercials'
PERMISSIONS = ('construction_contracts_commercials.read',
 'construction_contracts_commercials.create',
 'construction_contracts_commercials.update',
 'construction_contracts_commercials.approve',
 'construction_contracts_commercials.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

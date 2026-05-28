PBC_KEY = 'tax_administration_public_sector'
PERMISSIONS = ('tax_administration_public_sector.read',
 'tax_administration_public_sector.create',
 'tax_administration_public_sector.update',
 'tax_administration_public_sector.approve',
 'tax_administration_public_sector.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

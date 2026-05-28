PBC_KEY = 'public_sector_case_management'
PERMISSIONS = ('public_sector_case_management.read',
 'public_sector_case_management.create',
 'public_sector_case_management.update',
 'public_sector_case_management.approve',
 'public_sector_case_management.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

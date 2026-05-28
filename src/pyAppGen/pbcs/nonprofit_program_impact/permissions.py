PBC_KEY = 'nonprofit_program_impact'
PERMISSIONS = ('nonprofit_program_impact.read',
 'nonprofit_program_impact.create',
 'nonprofit_program_impact.update',
 'nonprofit_program_impact.approve',
 'nonprofit_program_impact.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

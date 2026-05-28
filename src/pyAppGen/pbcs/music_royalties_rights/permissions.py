PBC_KEY = 'music_royalties_rights'
PERMISSIONS = ('music_royalties_rights.read',
 'music_royalties_rights.create',
 'music_royalties_rights.update',
 'music_royalties_rights.approve',
 'music_royalties_rights.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

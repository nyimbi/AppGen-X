PBC_KEY = 'building_information_modeling_ops'
PERMISSIONS = ('building_information_modeling_ops.read',
 'building_information_modeling_ops.create',
 'building_information_modeling_ops.update',
 'building_information_modeling_ops.approve',
 'building_information_modeling_ops.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

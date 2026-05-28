PBC_KEY = 'telecom_network_operations'
PERMISSIONS = ('telecom_network_operations.read',
 'telecom_network_operations.create',
 'telecom_network_operations.update',
 'telecom_network_operations.approve',
 'telecom_network_operations.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

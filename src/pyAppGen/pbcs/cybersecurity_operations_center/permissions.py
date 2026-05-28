PBC_KEY = 'cybersecurity_operations_center'
PERMISSIONS = ('cybersecurity_operations_center.read',
 'cybersecurity_operations_center.create',
 'cybersecurity_operations_center.update',
 'cybersecurity_operations_center.approve',
 'cybersecurity_operations_center.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

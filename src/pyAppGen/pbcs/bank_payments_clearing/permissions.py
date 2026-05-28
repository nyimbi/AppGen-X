PBC_KEY = 'bank_payments_clearing'
PERMISSIONS = ('bank_payments_clearing.read',
 'bank_payments_clearing.create',
 'bank_payments_clearing.update',
 'bank_payments_clearing.approve',
 'bank_payments_clearing.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

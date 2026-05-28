PBC_KEY = 'utilities_metering_billing'
PERMISSIONS = ('utilities_metering_billing.read',
 'utilities_metering_billing.create',
 'utilities_metering_billing.update',
 'utilities_metering_billing.approve',
 'utilities_metering_billing.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

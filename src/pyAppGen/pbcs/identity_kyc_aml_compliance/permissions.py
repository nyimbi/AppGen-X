PBC_KEY = 'identity_kyc_aml_compliance'
PERMISSIONS = ('identity_kyc_aml_compliance.read',
 'identity_kyc_aml_compliance.create',
 'identity_kyc_aml_compliance.update',
 'identity_kyc_aml_compliance.approve',
 'identity_kyc_aml_compliance.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

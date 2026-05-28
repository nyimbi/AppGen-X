"""Permission descriptors for the insurance_claims_policy PBC."""
PBC_KEY = 'insurance_claims_policy'
PERMISSIONS = ('insurance_claims_policy.read', 'insurance_claims_policy.create', 'insurance_claims_policy.update', 'insurance_claims_policy.approve', 'insurance_claims_policy.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

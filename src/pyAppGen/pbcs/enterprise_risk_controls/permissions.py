"""Permission descriptors for the enterprise_risk_controls PBC."""
PBC_KEY = 'enterprise_risk_controls'
PERMISSIONS = ('enterprise_risk_controls.read', 'enterprise_risk_controls.create', 'enterprise_risk_controls.update', 'enterprise_risk_controls.approve', 'enterprise_risk_controls.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

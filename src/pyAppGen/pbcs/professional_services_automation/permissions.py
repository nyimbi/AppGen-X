"""Permission descriptors for the professional_services_automation PBC."""
PBC_KEY = 'professional_services_automation'
PERMISSIONS = ('professional_services_automation.read', 'professional_services_automation.create', 'professional_services_automation.update', 'professional_services_automation.approve', 'professional_services_automation.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

"""Permission descriptors for the case_knowledge_management PBC."""
PBC_KEY = 'case_knowledge_management'
PERMISSIONS = ('case_knowledge_management.read', 'case_knowledge_management.create', 'case_knowledge_management.update', 'case_knowledge_management.approve', 'case_knowledge_management.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

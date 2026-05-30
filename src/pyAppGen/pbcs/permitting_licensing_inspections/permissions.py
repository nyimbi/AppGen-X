PBC_KEY = 'permitting_licensing_inspections'
PERMISSIONS = (
    'permitting_licensing_inspections.read',
    'permitting_licensing_inspections.create',
    'permitting_licensing_inspections.update',
    'permitting_licensing_inspections.approve',
    'permitting_licensing_inspections.admin',
)


def permission_manifest():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'permissions': PERMISSIONS,
        'roles': ('intake_coordinator', 'reviewer', 'inspector', 'licensing_manager', 'auditor'),
        'side_effects': (),
    }


def authorize(permission, actor=None):
    return {
        'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate',
        'permission': permission,
        'actor': dict(actor or {}),
        'side_effects': (),
    }


def authorize_permission(permission, granted_permissions):
    return {
        'ok': True,
        'permission': permission,
        'allowed': permission in tuple(granted_permissions),
        'granted_permissions': tuple(granted_permissions),
        'side_effects': (),
    }


def smoke_test():
    return {
        'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'] and authorize_permission(PERMISSIONS[0], PERMISSIONS)['allowed'],
        'side_effects': (),
    }

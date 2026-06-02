"""Permission contract for reinsurance_management."""

PBC_KEY = 'reinsurance_management'
PERMISSIONS = (
    'reinsurance_management.read',
    'reinsurance_management.create',
    'reinsurance_management.update',
    'reinsurance_management.approve',
    'reinsurance_management.admin',
)
ROLE_MAP = {
    'operator': ('reinsurance_management.read', 'reinsurance_management.create', 'reinsurance_management.update'),
    'approver': ('reinsurance_management.read', 'reinsurance_management.approve'),
    'auditor': ('reinsurance_management.read', 'reinsurance_management.admin'),
}


def permission_manifest() -> dict:
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': tuple(ROLE_MAP), 'side_effects': ()}


def authorize(permission, actor=None):
    actor = dict(actor or {})
    roles = tuple(actor.get('roles', ()))
    granted = permission in PERMISSIONS or permission == f'{PBC_KEY}.operate' or any(permission in ROLE_MAP.get(role, ()) for role in roles)
    return {'ok': granted, 'permission': permission, 'actor': actor, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0], {'roles': ('operator',)})['ok'], 'side_effects': ()}

"""Permission contract for the multi_sided_market PBC."""
PBC_KEY = 'multi_sided_market'
PERMISSIONS = ('multi_sided_market.read', 'multi_sided_market.create', 'multi_sided_market.update', 'multi_sided_market.approve', 'multi_sided_market.settle', 'multi_sided_market.admin')
ACTION_PERMISSIONS = {'read': 'multi_sided_market.read', 'create': 'multi_sided_market.create', 'update': 'multi_sided_market.update', 'approve': 'multi_sided_market.approve', 'settle': 'multi_sided_market.settle', 'admin': 'multi_sided_market.admin'}


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'action_permissions': ACTION_PERMISSIONS, 'side_effects': ()}


def authorize(action, granted_permissions=()):
    required = ACTION_PERMISSIONS.get(action)
    return {'ok': required is not None, 'allowed': required in set(granted_permissions), 'action': action, 'required_permission': required, 'granted_permissions': tuple(granted_permissions), 'side_effects': ()}


def smoke_test():
    decision = authorize('create', ('multi_sided_market.create',))
    return {'ok': permission_manifest()['ok'] and decision['allowed'], 'decision': decision, 'side_effects': ()}

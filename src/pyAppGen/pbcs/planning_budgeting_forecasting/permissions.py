"""Permission descriptors for the planning_budgeting_forecasting PBC."""
PBC_KEY = 'planning_budgeting_forecasting'
PERMISSIONS = ('planning_budgeting_forecasting.read', 'planning_budgeting_forecasting.create', 'planning_budgeting_forecasting.update', 'planning_budgeting_forecasting.approve', 'planning_budgeting_forecasting.admin')


def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def authorize(actor, permission):
    return {'ok': permission in PERMISSIONS, 'allowed': permission in PERMISSIONS, 'actor': actor, 'permission': permission, 'side_effects': ()}


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'], 'side_effects': ()}

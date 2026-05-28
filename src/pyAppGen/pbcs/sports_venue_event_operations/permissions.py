PBC_KEY = 'sports_venue_event_operations'
PERMISSIONS = ('sports_venue_event_operations.read',
 'sports_venue_event_operations.create',
 'sports_venue_event_operations.update',
 'sports_venue_event_operations.approve',
 'sports_venue_event_operations.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

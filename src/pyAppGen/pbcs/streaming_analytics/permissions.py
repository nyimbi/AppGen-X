"""Executable permission contract for the streaming_analytics PBC."""

PBC_KEY = 'streaming_analytics'
PERMISSIONS = ('streaming_analytics.read', 'streaming_analytics.create', 'streaming_analytics.update', 'streaming_analytics.approve', 'streaming_analytics.admin')
ACTION_PERMISSIONS = {
    permission.rsplit('.', 1)[-1]: permission
    for permission in PERMISSIONS
}


def permission_manifest():
    """Return the permission surface without mutating runtime state."""
    return {
        'ok': bool(PERMISSIONS),
        'pbc': PBC_KEY,
        'permissions': PERMISSIONS,
        'action_permissions': dict(ACTION_PERMISSIONS),
        'side_effects': (),
    }


def authorize(action, granted_permissions=()):
    """Evaluate one action against a caller permission set."""
    required = ACTION_PERMISSIONS.get(action)
    allowed = required in set(granted_permissions) if required else False
    return {
        'ok': required is not None,
        'allowed': allowed,
        'action': action,
        'required_permission': required,
        'granted_permissions': tuple(granted_permissions),
        'side_effects': (),
    }


def smoke_test():
    """Exercise one permission decision side-effect-free."""
    manifest = permission_manifest()
    action, permission = next(iter(ACTION_PERMISSIONS.items())) if ACTION_PERMISSIONS else (None, None)
    decision = authorize(action, (permission,)) if action else {'ok': False, 'allowed': False}
    return {
        'ok': manifest['ok'] and decision['ok'] and decision['allowed'],
        'manifest': manifest,
        'decision': decision,
        'side_effects': (),
    }

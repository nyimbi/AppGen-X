from .standalone import PBC_KEY, PERMISSIONS, permission_manifest, authorize


def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

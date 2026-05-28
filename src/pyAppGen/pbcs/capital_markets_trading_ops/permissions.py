PBC_KEY = 'capital_markets_trading_ops'
PERMISSIONS = ('capital_markets_trading_ops.read',
 'capital_markets_trading_ops.create',
 'capital_markets_trading_ops.update',
 'capital_markets_trading_ops.approve',
 'capital_markets_trading_ops.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

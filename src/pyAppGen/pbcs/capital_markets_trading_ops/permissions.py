PBC_KEY = 'capital_markets_trading_ops'
PERMISSIONS = ('capital_markets_trading_ops.read',
 'capital_markets_trading_ops.create',
 'capital_markets_trading_ops.update',
 'capital_markets_trading_ops.approve',
 'capital_markets_trading_ops.admin')
ACTION_PERMISSIONS = {
    'open_trade_order_form': 'capital_markets_trading_ops.create',
    'run_trade_order_wizard': 'capital_markets_trading_ops.update',
    'review_trade_order_controls': 'capital_markets_trading_ops.read',
    'release_trade_order': 'capital_markets_trading_ops.approve',
}

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'action_permissions': ACTION_PERMISSIONS, 'side_effects': ()}

def authorize(permission, actor=None):
    allowed = permission in PERMISSIONS or permission == f'{PBC_KEY}.operate' or permission in ACTION_PERMISSIONS
    resolved = ACTION_PERMISSIONS.get(permission, permission)
    return {'ok': allowed, 'permission': permission, 'resolved_permission': resolved, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

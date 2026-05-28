PBC_KEY = 'energy_trading_risk'
PERMISSIONS = ('energy_trading_risk.read',
 'energy_trading_risk.create',
 'energy_trading_risk.update',
 'energy_trading_risk.approve',
 'energy_trading_risk.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

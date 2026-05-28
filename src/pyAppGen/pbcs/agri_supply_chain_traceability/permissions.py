PBC_KEY = 'agri_supply_chain_traceability'
PERMISSIONS = ('agri_supply_chain_traceability.read',
 'agri_supply_chain_traceability.create',
 'agri_supply_chain_traceability.update',
 'agri_supply_chain_traceability.approve',
 'agri_supply_chain_traceability.admin')

def permission_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': PERMISSIONS, 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    return {'ok': permission_manifest()['ok'] and authorize(PERMISSIONS[0])['ok'], 'side_effects': ()}

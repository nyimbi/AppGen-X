PBC_KEY = 'rail_operations_management'


def seed_manifest():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'records': (
            {'table': f'{PBC_KEY}_train_plan', 'code': 'SEED-TRAIN', 'tenant': 'tenant_seed'},
            {'table': f'{PBC_KEY}_route_path', 'code': 'SEED-PATH', 'tenant': 'tenant_seed'},
            {'table': f'{PBC_KEY}_consist', 'code': 'SEED-CONSIST', 'tenant': 'tenant_seed'},
        ),
        'side_effects': (),
    }

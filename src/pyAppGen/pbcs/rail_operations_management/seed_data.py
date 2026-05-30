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


def validate_seed_data(records=None):
    records = tuple(records or seed_manifest()['records'])
    invalid = tuple(record for record in records if not str(record.get('table', '')).startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid and bool(records), 'invalid_records': invalid, 'records': records, 'side_effects': ()}


def seed_plan(tenant='tenant_seed'):
    records = tuple({**record, 'tenant': tenant} for record in seed_manifest()['records'])
    validation = validate_seed_data(records)
    return {'ok': validation['ok'], 'pbc': PBC_KEY, 'records': records, 'mutates_datastore': False, 'side_effects': ()}


def smoke_test():
    return {'ok': seed_manifest()['ok'] and validate_seed_data()['ok'] and seed_plan()['ok'], 'side_effects': ()}

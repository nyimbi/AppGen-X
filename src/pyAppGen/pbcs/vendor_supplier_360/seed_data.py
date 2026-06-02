"""Seed data for the vendor_supplier_360 PBC."""
PBC_KEY = 'vendor_supplier_360'
SEED_ROWS = ({'table': f'{PBC_KEY}_supplier_profile', 'code': 'DEFAULT', 'status': 'active'},)


def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'rows': SEED_ROWS, 'side_effects': ()}


def validate_seed_data():
    return {'ok': all(row['table'].startswith(f'{PBC_KEY}_') for row in SEED_ROWS), 'rows': SEED_ROWS, 'side_effects': ()}


def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'] and standalone_seed_bundle()['ok'], 'standalone_seed_bundle': standalone_seed_bundle(), 'side_effects': ()}


def standalone_seed_bundle():
    rows = (
        {'table': 'vendor_supplier_360_supplier_profile', 'rows': ({'code': 'STRATEGIC-SUPPLIER', 'status': 'active', 'risk_tier': 'low'},)},
        {'table': 'vendor_supplier_360_supplier_certification', 'rows': ({'code': 'ISO-9001', 'status': 'active', 'certification_type': 'quality'},)},
        {'table': 'vendor_supplier_360_supplier_bank_validation', 'rows': ({'code': 'PRIMARY-BANK', 'status': 'validated'},)},
        {'table': 'vendor_supplier_360_supplier_scorecard', 'rows': ({'code': 'DEFAULT-SCORECARD', 'status': 'active'},)},
    )
    invalid_tables = tuple(item['table'] for item in rows if not item['table'].startswith(f'{PBC_KEY}_'))
    return {'ok': bool(rows) and not invalid_tables, 'pbc': PBC_KEY, 'rows': rows, 'invalid_tables': invalid_tables, 'side_effects': ()}

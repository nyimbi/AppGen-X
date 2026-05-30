"""Seed data for the field_service_management PBC."""
PBC_KEY = 'field_service_management'
SEED_ROWS = ({'table': f'{PBC_KEY}_field_work_order', 'code': 'DEFAULT', 'status': 'active'},)


def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'rows': SEED_ROWS, 'side_effects': ()}


def validate_seed_data():
    return {'ok': all(row['table'].startswith(f'{PBC_KEY}_') for row in SEED_ROWS), 'rows': SEED_ROWS, 'side_effects': ()}


def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'] and standalone_seed_bundle()['ok'], 'standalone_seed_bundle': standalone_seed_bundle(), 'side_effects': ()}


def standalone_seed_bundle():
    rows = (
        {'table': 'field_service_management_technician_profile', 'rows': ({'code': 'TECH-HVAC-001', 'status': 'active', 'skills': 'hvac,electrical'},)},
        {'table': 'field_service_management_tool_inventory', 'rows': ({'code': 'CALIBRATED-METER', 'status': 'available', 'tool_type': 'meter'},)},
        {'table': 'field_service_management_service_route_plan', 'rows': ({'code': 'DEFAULT-ROUTE', 'status': 'planned'},)},
        {'table': 'field_service_management_location_privacy_consent', 'rows': ({'code': 'TECH-CONSENT', 'status': 'active'},)},
    )
    invalid_tables = tuple(item['table'] for item in rows if not item['table'].startswith(f'{PBC_KEY}_'))
    return {'ok': bool(rows) and not invalid_tables, 'pbc': PBC_KEY, 'rows': rows, 'invalid_tables': invalid_tables, 'side_effects': ()}

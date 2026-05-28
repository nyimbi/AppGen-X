"""Seed data for the facilities_space_management PBC."""
PBC_KEY = 'facilities_space_management'
SEED_ROWS = ({'table': f'{PBC_KEY}_facility_site', 'code': 'DEFAULT', 'status': 'active'},)


def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'rows': SEED_ROWS, 'side_effects': ()}


def validate_seed_data():
    return {'ok': all(row['table'].startswith(f'{PBC_KEY}_') for row in SEED_ROWS), 'rows': SEED_ROWS, 'side_effects': ()}


def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}

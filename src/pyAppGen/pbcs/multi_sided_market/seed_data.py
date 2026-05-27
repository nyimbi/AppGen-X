"""Seed-data contract for the multi_sided_market PBC."""
PBC_KEY = 'multi_sided_market'
SEED_DATA = ({'table': 'multi_sided_market_participant_profile', 'rows': ({'code': 'MARKET-PARTICIPANT-001', 'status': 'verified'},)}, {'table': 'multi_sided_market_marketplace_listing', 'rows': ({'code': 'MARKET-LISTING-001', 'status': 'published'},)})


def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'tables': tuple(item['table'] for item in SEED_DATA), 'rows': SEED_DATA, 'side_effects': ()}


def validate_seed_data():
    invalid_tables = tuple(item['table'] for item in SEED_DATA if not item['table'].startswith(PBC_KEY + '_'))
    invalid_rows = tuple(row for item in SEED_DATA for row in item['rows'] if not row.get('code') or not row.get('status'))
    return {'ok': not invalid_tables and not invalid_rows, 'invalid_tables': invalid_tables, 'invalid_rows': invalid_rows, 'plan': seed_plan(), 'side_effects': ()}


def smoke_test():
    return validate_seed_data()

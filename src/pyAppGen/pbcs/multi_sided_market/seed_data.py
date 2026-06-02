"""Seed-data contract for the multi_sided_market PBC."""
PBC_KEY = 'multi_sided_market'
SEED_DATA = ({'table': 'multi_sided_market_participant_profile', 'rows': ({'code': 'MARKET-PARTICIPANT-001', 'status': 'verified'},)}, {'table': 'multi_sided_market_marketplace_listing', 'rows': ({'code': 'MARKET-LISTING-001', 'status': 'published'},)})


def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'tables': tuple(item['table'] for item in SEED_DATA), 'rows': SEED_DATA, 'side_effects': ()}


def validate_seed_data():
    invalid_tables = tuple(item['table'] for item in SEED_DATA if not item['table'].startswith(PBC_KEY + '_'))
    invalid_rows = tuple(row for item in SEED_DATA for row in item['rows'] if not row.get('code') or not row.get('status'))
    return {'ok': not invalid_tables and not invalid_rows, 'invalid_tables': invalid_tables, 'invalid_rows': invalid_rows, 'plan': seed_plan(), 'side_effects': ()}


def standalone_seed_bundle():
    rows = (
        {'table': 'multi_sided_market_participant_profile', 'rows': ({'code': 'VERIFIED-SELLER', 'status': 'verified', 'role': 'seller'}, {'code': 'VERIFIED-BUYER', 'status': 'verified', 'role': 'buyer'})},
        {'table': 'multi_sided_market_marketplace_listing', 'rows': ({'code': 'EQUIPMENT-RENTAL', 'status': 'published', 'listing_type': 'rental'},)},
        {'table': 'multi_sided_market_market_rule', 'rows': ({'code': 'ESCROW-FIRST', 'status': 'active', 'scope': 'settlement'},)},
        {'table': 'multi_sided_market_market_parameter', 'rows': ({'code': 'ESCROW-HOLD-DAYS', 'status': 'active', 'value': '7'},)},
    )
    invalid_tables = tuple(item['table'] for item in rows if not item['table'].startswith(PBC_KEY + '_'))
    return {'ok': bool(rows) and not invalid_tables, 'pbc': PBC_KEY, 'rows': rows, 'invalid_tables': invalid_tables, 'side_effects': ()}


def smoke_test():
    validation = validate_seed_data()
    standalone = standalone_seed_bundle()
    return {**validation, "ok": validation["ok"] and standalone["ok"], "standalone_seed_bundle": standalone}

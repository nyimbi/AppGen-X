"""Executable seed-data contract for the lead_opportunity PBC."""

PBC_KEY = 'lead_opportunity'
SEED_DATA = ({'table': 'lead_opportunity_lead', 'rows': ({'code': 'LEAD_OPPORTUNITY-001', 'status': 'active'},)}, {'table': 'lead_opportunity_opportunity', 'rows': ({'code': 'LEAD_OPPORTUNITY-002', 'status': 'active'},)})


def seed_plan():
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item['table'] for item in SEED_DATA))
    return {
        'ok': bool(SEED_DATA),
        'pbc': PBC_KEY,
        'tables': tables,
        'rows': SEED_DATA,
        'side_effects': (),
    }


def validate_seed_data():
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(
        item['table'] for item in SEED_DATA if not item.get('table', '').startswith(f'{PBC_KEY}_')
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get('rows', ())
        if not row.get('code') or not row.get('status')
    )
    plan = seed_plan()
    return {
        'ok': plan['ok'] and not invalid_tables and not invalid_rows and standalone_seed_bundle()['ok'],
        'pbc': PBC_KEY,
        'plan': plan,
        'invalid_tables': invalid_tables,
        'invalid_rows': invalid_rows,
        'side_effects': (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()


def standalone_seed_bundle():
    """Return domain-rich seed rows for a one-PBC sales pipeline app."""
    rows = (
        {
            'table': 'lead_opportunity_account_hierarchy',
            'rows': (
                {'account_id': 'acct_global_001', 'name': 'Global Manufacturing Group', 'region': 'west', 'owner': 'ae_west', 'status': 'active'},
            ),
        },
        {
            'table': 'lead_opportunity_lead',
            'rows': (
                {'lead_id': 'lead_enterprise_001', 'account_id': 'acct_global_001', 'company': 'Global Manufacturing Group', 'source': 'partner', 'status': 'new'},
            ),
        },
        {
            'table': 'lead_opportunity_opportunity',
            'rows': (
                {'opportunity_id': 'opp_platform_001', 'lead_id': 'lead_enterprise_001', 'amount': 150000, 'stage': 'proposal', 'status': 'open'},
            ),
        },
        {
            'table': 'lead_opportunity_lead_opportunity_rule',
            'rows': (
                {'rule_id': 'rule_enterprise_qualification', 'scope': 'qualification', 'status': 'active'},
            ),
        },
    )
    return {'ok': True, 'pbc': PBC_KEY, 'rows': rows, 'side_effects': ()}

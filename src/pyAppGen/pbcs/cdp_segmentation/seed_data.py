"""Executable seed-data contract for the cdp_segmentation PBC."""

PBC_KEY = 'cdp_segmentation'
SEED_DATA = (
    {
        'table': 'cdp_segmentation_activation_destination',
        'rows': (
            {'code': 'dest_loyalty', 'status': 'active', 'destination': 'loyalty', 'channel': 'retention'},
            {'code': 'dest_notifications', 'status': 'active', 'destination': 'notifications', 'channel': 'engagement'},
        ),
    },
    {
        'table': 'cdp_segmentation_segment_definition',
        'rows': (
            {'code': 'seg_high_value_repeat', 'status': 'active', 'name': 'High Value Repeat Buyers'},
            {'code': 'seg_at_risk_recent', 'status': 'draft', 'name': 'At-Risk Recent Buyers'},
        ),
    },
    {
        'table': 'cdp_segmentation_cdp_segmentation_parameter',
        'rows': (
            {'code': 'membership_score_threshold', 'status': 'active', 'value': 0.68},
            {'code': 'consent_risk_threshold', 'status': 'active', 'value': 0.60},
        ),
    },
)


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
        'ok': plan['ok'] and not invalid_tables and not invalid_rows,
        'pbc': PBC_KEY,
        'plan': plan,
        'invalid_tables': invalid_tables,
        'invalid_rows': invalid_rows,
        'side_effects': (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()

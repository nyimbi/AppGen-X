"""Executable seed-data contract for the cdp_segmentation PBC."""

from __future__ import annotations


PBC_KEY = 'cdp_segmentation'
DEFAULT_STANDALONE_CONFIGURATION = {
    'database_backend': 'postgresql',
    'event_topic': 'appgen.cdp_segmentation.events',
    'retry_limit': 3,
    'default_region': 'US',
    'supported_regions': ('US', 'EU'),
    'supported_event_types': ('profile', 'payment', 'shipment', 'engagement'),
    'identity_keys': ('customer_id', 'email'),
    'default_timezone': 'UTC',
    'activation_mode': 'policy',
    'workbench_limit': 100,
}
DEFAULT_STANDALONE_PARAMETERS = {
    'membership_score_threshold': 0.68,
    'profile_merge_confidence_threshold': 0.85,
    'event_freshness_days': 180,
    'payment_value_weight': 0.35,
    'order_recency_weight': 0.25,
    'engagement_weight': 0.40,
    'consent_risk_threshold': 0.60,
    'activation_batch_limit': 5000,
    'max_segments_per_profile': 20,
    'workbench_limit': 100,
}
SEED_DATA = (
    {
        'table': 'cdp_segmentation_activation_destination',
        'rows': (
            {'code': 'dest_loyalty', 'status': 'active', 'destination': 'loyalty', 'channel': 'retention'},
            {'code': 'dest_notifications', 'status': 'active', 'destination': 'notifications', 'channel': 'engagement'},
            {'code': 'dest_pricing', 'status': 'active', 'destination': 'pricing', 'channel': 'upsell'},
        ),
    },
    {
        'table': 'cdp_segmentation_segment_definition',
        'rows': (
            {'code': 'seg_high_value_repeat', 'status': 'active', 'name': 'High Value Repeat Buyers'},
            {'code': 'seg_at_risk_recent', 'status': 'draft', 'name': 'At-Risk Recent Buyers'},
            {'code': 'seg_opted_in_growth', 'status': 'active', 'name': 'Opted-In Growth Audience'},
        ),
    },
    {
        'table': 'cdp_segmentation_cdp_segmentation_parameter',
        'rows': (
            {'code': 'membership_score_threshold', 'status': 'active', 'value': 0.68},
            {'code': 'consent_risk_threshold', 'status': 'active', 'value': 0.60},
            {'code': 'activation_batch_limit', 'status': 'active', 'value': 5000},
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
        'row_count': sum(len(item['rows']) for item in SEED_DATA),
        'side_effects': (),
    }


def standalone_seed_bundle(*, tenant: str = 'tenant_demo') -> dict:
    """Return a one-PBC bootstrap bundle for the standalone app shell."""
    plan = seed_plan()
    rule = {
        'rule_id': f'{tenant}.segmentation.policy',
        'tenant': tenant,
        'scope': 'cdp_segmentation',
        'status': 'active',
        'allowed_event_types': DEFAULT_STANDALONE_CONFIGURATION['supported_event_types'],
        'allowed_regions': DEFAULT_STANDALONE_CONFIGURATION['supported_regions'],
        'segment_policy': {'minimum_score': DEFAULT_STANDALONE_PARAMETERS['membership_score_threshold'], 'required_properties': ('customer_id',)},
        'consent_policy': {'require_opt_in': True, 'restricted_regions': ()},
        'activation_policy': {'destinations': ('notifications', 'loyalty', 'pricing')},
    }
    return {
        'ok': plan['ok'],
        'pbc': PBC_KEY,
        'tenant': tenant,
        'configuration': dict(DEFAULT_STANDALONE_CONFIGURATION),
        'parameters': dict(DEFAULT_STANDALONE_PARAMETERS),
        'rules': (rule,),
        'seed_rows': plan['rows'],
        'tables': plan['tables'],
        'row_count': plan['row_count'],
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
    bundle = standalone_seed_bundle()
    return {
        'ok': plan['ok'] and bundle['ok'] and not invalid_tables and not invalid_rows and plan['row_count'] >= 6,
        'pbc': PBC_KEY,
        'plan': plan,
        'bundle': bundle,
        'invalid_tables': invalid_tables,
        'invalid_rows': invalid_rows,
        'side_effects': (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()

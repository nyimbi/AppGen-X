"""Executable seed-data contract for the service_ticketing PBC."""

PBC_KEY = 'service_ticketing'
SEED_DATA = ({'table': 'service_ticketing_support_ticket', 'rows': ({'code': 'SERVICE_TICKETING-001', 'status': 'active'},)}, {'table': 'service_ticketing_sla_policy', 'rows': ({'code': 'SERVICE_TICKETING-002', 'status': 'active'},)})


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
    """Return domain-rich seed rows for a one-PBC service desk app."""
    rows = (
        {'table': 'service_ticketing_service_queue', 'rows': ({'queue_id': 'queue_enterprise_support', 'name': 'Enterprise Support', 'assignment_mode': 'skill_balanced', 'status': 'active'},)},
        {'table': 'service_ticketing_sla_policy', 'rows': ({'sla_policy_id': 'sla_p1', 'priority': 'P1', 'first_response_minutes': 15, 'resolution_target_hours': 4, 'status': 'active'},)},
        {'table': 'service_ticketing_support_ticket', 'rows': ({'ticket_id': 'ticket_seed_001', 'customer_id': 'cust_001', 'priority': 'P2', 'queue': 'queue_enterprise_support', 'status': 'open'},)},
        {'table': 'service_ticketing_service_rule', 'rows': ({'rule_id': 'rule_assignment_skill_balance', 'scope': 'assignment', 'status': 'active'},)},
    )
    return {'ok': True, 'pbc': PBC_KEY, 'rows': rows, 'side_effects': ()}

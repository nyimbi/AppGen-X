"""Executable seed-data contract for the order_routing_optimization PBC."""

PBC_KEY = 'order_routing_optimization'
SEED_DATA = ({'table': 'order_routing_optimization_routing_rule', 'rows': ({'code': 'ORDER_ROUTING_OPTIMIZATION-001', 'status': 'active'},)}, {'table': 'order_routing_optimization_route_candidate', 'rows': ({'code': 'ORDER_ROUTING_OPTIMIZATION-002', 'status': 'active'},)})


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
    """Return domain-rich seed rows for a one-PBC routing app."""
    rows = (
        {
            'table': 'order_routing_optimization_routing_node',
            'rows': (
                {'node_id': 'node_west_dc', 'region': 'west', 'node_type': 'distribution_center', 'status': 'active'},
                {'node_id': 'node_central_store', 'region': 'central', 'node_type': 'store', 'status': 'active'},
            ),
        },
        {
            'table': 'order_routing_optimization_capacity_snapshot',
            'rows': (
                {'snapshot_id': 'cap_west_001', 'node_id': 'node_west_dc', 'available_units': 60, 'reserved_units': 10, 'status': 'current'},
                {'snapshot_id': 'cap_central_001', 'node_id': 'node_central_store', 'available_units': 22, 'reserved_units': 4, 'status': 'current'},
            ),
        },
        {
            'table': 'order_routing_optimization_routing_rule',
            'rows': (
                {'rule_id': 'rule_split_sla', 'rule_type': 'split', 'regions': ('west', 'central'), 'status': 'active'},
            ),
        },
    )
    return {'ok': True, 'pbc': PBC_KEY, 'rows': rows, 'side_effects': ()}

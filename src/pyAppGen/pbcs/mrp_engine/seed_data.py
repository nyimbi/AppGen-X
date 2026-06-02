"""Executable seed-data contract for the mrp_engine PBC."""

PBC_KEY = 'mrp_engine'
SEED_DATA = ({'table': 'mrp_engine_bill_of_material', 'rows': ({'code': 'MRP_ENGINE-001', 'status': 'active'},)}, {'table': 'mrp_engine_bom_revision', 'rows': ({'code': 'MRP_ENGINE-002', 'status': 'active'},)})


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



def standalone_seed_bundle(*, tenant='tenant_demo'):
    """Return a realistic standalone MRP seed bundle."""
    return {
        'pbc': PBC_KEY,
        'tenant': tenant,
        'configuration': {'database_backend': 'postgresql', 'event_topic': 'appgen.mrp.events', 'retry_limit': 3, 'allowed_sites': ('factory_east', 'factory_west'), 'allowed_order_types': ('production', 'purchase'), 'allowed_procurement_routes': ('buy', 'subcontract'), 'allowed_production_routes': ('make', 'assemble'), 'default_planning_bucket': 'daily', 'workbench_limit': 100},
        'parameters': {'planning_horizon_days': 30, 'bucket_size_days': 1, 'safety_stock_multiplier': 1.1, 'lot_size_minimum': 10, 'lead_time_days': 3, 'capacity_threshold': 0.85, 'shortage_severity_threshold': 20, 'scrap_factor': 0.03, 'planner_approval_threshold': 0.8, 'workbench_limit': 100},
        'rules': ({'rule_id': 'mrp.demo.factory_rule', 'tenant': tenant, 'rule_type': 'planning', 'eligible_item_types': ('finished_good', 'component'), 'allowed_sites': ('factory_east',), 'allowed_bom_statuses': ('released',), 'demand_sources': ('order', 'forecast'), 'release_routes': {'component_a': 'buy', 'fg_100': 'make'}, 'substitutions': {'component_a': ('component_a_alt',)}, 'status': 'active'},),
        'bom': {'bom_id': 'bom_demo_100', 'tenant': tenant, 'parent_item': 'fg_100', 'component_item': 'component_a', 'component_qty': 2, 'scrap_percent': 0.05, 'revision': 'A', 'status': 'released', 'site': 'factory_east'},
        'demand_projection': {'demand_id': 'demand_demo_100', 'tenant': tenant, 'item': 'fg_100', 'site': 'factory_east', 'quantity': 30, 'source': 'order', 'need_date': '2026-06-01'},
        'inventory_projection': {'inventory_id': 'inv_demo_100', 'tenant': tenant, 'item': 'component_a', 'site': 'factory_east', 'available_qty': 40, 'quality_status': 'released'},
        'mrp_run': {'run_id': 'run_demo_100', 'tenant': tenant, 'site': 'factory_east', 'horizon_days': 30, 'scenario': 'base', 'planner': 'planner_1'},
        'document': 'Demand for 30 fg_100 at factory_east; component_a has 40 released units; run net requirements and release planned order.',
        'instructions': 'Create BOM, ingest demand and inventory, run MRP, release purchase suggestion, and generate supply proof.',
    }

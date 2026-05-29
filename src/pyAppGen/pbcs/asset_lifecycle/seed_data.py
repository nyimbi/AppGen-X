"""Executable seed-data contract for the asset_lifecycle PBC."""

PBC_KEY = 'asset_lifecycle'
SEED_DATA = ({'table': 'asset_lifecycle_fixed_asset', 'rows': ({'code': 'ASSET_LIFECYCLE-001', 'status': 'active'},)}, {'table': 'asset_lifecycle_asset_component', 'rows': ({'code': 'ASSET_LIFECYCLE-002', 'status': 'active'},)})


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
    return {
        'pbc': PBC_KEY, 'tenant': tenant,
        'configuration': {'database_backend':'postgresql','event_topic':'appgen.asset.events','retry_limit':3,'default_currency':'USD','default_timezone':'UTC','default_book':'corporate','workbench_limit':100},
        'parameters': {'capitalization_threshold':5000,'impairment_indicator_threshold':0.65,'physical_verification_interval_days':180,'depreciation_batch_size':100,'retirement_approval_limit':25000,'workbench_limit':100},
        'rules': ({'rule_id':'asset.demo.capitalization','tenant':tenant,'scope':'capitalization','status':'active','predicate':'cost >= capitalization_threshold'}, {'rule_id':'asset.demo.depreciation','tenant':tenant,'scope':'depreciation','status':'active','predicate':'active_schedule_required'}),
        'events': ({'event_id':'receipt_evt_demo','event_type':'PurchaseReceiptCapitalized','payload':{'tenant':tenant,'receipt_id':'receipt_demo_100','asset_id':'asset_demo_100','amount':120000}}, {'event_id':'maint_evt_demo','event_type':'MaintenanceCompleted','payload':{'tenant':tenant,'asset_id':'asset_demo_100','work_order_id':'wo_demo_100','useful_life_delta_months':6}}),
        'asset': {'asset_id':'asset_demo_100','tenant':tenant,'legal_entity':'us01','description':'CNC milling machine','category':'production_equipment','cost':120000.0,'residual_value':20000.0,'useful_life_months':60,'book':'corporate','location':'plant_a','custodian':'operations_manager','cost_center':'mfg-100','components':('spindle','controller'),'identity':{'did':'did:appgen:asset-demo-100','issuer':'asset_registry','status':'active'}},
        'service_date':'2026-01-01',
        'depreciation_method':'straight_line',
        'depreciation_run': {'run_id':'dep_demo_2026_01','period':'2026-01'},
        'transfer': {'location':'plant_b','cost_center':'mfg-200','approved_by':'asset_controller'},
        'maintenance_adjustment': {'useful_life_delta_months':6,'evidence':'maintenance work order wo_demo_100 replaced spindle and extended useful life'},
        'document':'Capitalization packet for asset_demo_100 CNC milling machine cost 120000 life 60 component spindle component controller.',
        'instructions':'Register the asset, place it in service, build depreciation, post depreciation, transfer location, record maintenance life extension, and generate audit proof.',
    }

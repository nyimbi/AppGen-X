"""Executable seed-data contract for the production_control PBC."""

PBC_KEY = 'production_control'
SEED_DATA = ({'table': 'production_control_work_center', 'rows': ({'code': 'PRODUCTION_CONTROL-001', 'status': 'active'},)}, {'table': 'production_control_production_order', 'rows': ({'code': 'PRODUCTION_CONTROL-002', 'status': 'active'},)})


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
        'configuration': {'database_backend':'postgresql','event_topic':'appgen.production.events','retry_limit':3,'allowed_sites':('factory_east','factory_west'),'allowed_work_center_types':('assembly','test'),'allowed_downtime_reasons':('maintenance','material','quality'),'allowed_production_routes':('make','assemble'),'default_timezone':'UTC','workbench_limit':100},
        'parameters': {'capacity_threshold':0.85,'oee_target':0.75,'scrap_threshold':0.05,'takt_time_minutes':10,'schedule_horizon_days':14,'downtime_severity_minutes':30},
        'rules': ({'rule_id':'prod.demo.factory','tenant':tenant,'rule_type':'production','eligible_work_center_types':('assembly','test'),'allowed_sites':('factory_east',),'allowed_routes':('make','assemble'),'quality_gates':('final_test',),'asset_commissioning_items':('machine_kit',),'dispatch_priorities':('expedite','standard'),'status':'active'},),
        'events': ({'event_id':'mrp_evt_demo','event_type':'PlannedOrderReleased','payload':{'planned_order_id':'po_demo_100','tenant':tenant,'site':'factory_east','item':'machine_kit','quantity':10,'route':'make','priority':'standard'}}, {'event_id':'maint_evt_demo','event_type':'MaintenanceCompleted','payload':{'maintenance_order_id':'mo_demo_100','tenant':tenant,'work_center_id':'wc_demo_100','asset_id':'asset_demo_100','released_capacity_hours':8}}),
        'work_center': {'work_center_id':'wc_demo_100','tenant':tenant,'site':'factory_east','name':'Assembly Cell 1','work_center_type':'assembly','capacity_hours':8,'efficiency':0.9,'status':'available','identity':{'did':'did:appgen:wc-demo-100','issuer':'trusted_registry','status':'active'}},
        'production_order': {'order_id':'order_demo_100','tenant':tenant,'site':'factory_east','item':'machine_kit','quantity':10,'route':'make','priority':'standard','planned_order_id':'po_demo_100'},
        'routing_step': {'step_id':'step_demo_100','tenant':tenant,'order_id':'order_demo_100','sequence':10,'work_center_id':'wc_demo_100','standard_minutes':100,'setup_minutes':20,'quality_gate':'final_test'},
        'material_consumption': {'consumption_id':'mat_demo_100','tenant':tenant,'order_id':'order_demo_100','material_id':'steel_kit','quantity':10,'uom':'EA','source':'inventory_readiness_projection'},
        'labor_booking': {'booking_id':'lab_demo_100','tenant':tenant,'order_id':'order_demo_100','step_id':'step_demo_100','operator_id':'operator_1','hours':2.0},
        'machine_booking': {'booking_id':'mach_demo_100','tenant':tenant,'order_id':'order_demo_100','step_id':'step_demo_100','work_center_id':'wc_demo_100','hours':2.3},
        'downtime': {'downtime_id':'dt_demo_100','tenant':tenant,'work_center_id':'wc_demo_100','order_id':'order_demo_100','reason':'maintenance','minutes':20},
        'quality_gate': {'gate_id':'qg_demo_100','tenant':tenant,'order_id':'order_demo_100','step_id':'step_demo_100','quality_gate':'final_test','result':'passed','inspector':'qa_1'},
        'scrap_rework': {'scrap_rework_id':'sr_demo_100','tenant':tenant,'order_id':'order_demo_100','step_id':'step_demo_100','scrap_qty':1,'rework_qty':0,'reason':'setup_loss'},
        'document':'Shop floor packet for order_demo_100 at wc_demo_100 with material issue, labor, machine time, downtime, quality gate and completion.',
        'instructions':'Start operation, record consumption/time/downtime/quality/scrap, confirm and complete production order with completion proof.',
    }

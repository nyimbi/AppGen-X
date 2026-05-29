"""Executable seed-data contract for the quality_assurance PBC."""

PBC_KEY = 'quality_assurance'
SEED_DATA = ({'table': 'quality_assurance_inspection_plan', 'rows': ({'code': 'QUALITY_ASSURANCE-001', 'status': 'active'},)}, {'table': 'quality_assurance_inspection_result', 'rows': ({'code': 'QUALITY_ASSURANCE-002', 'status': 'active'},)})


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
    """Return a realistic standalone QA workspace seed bundle."""
    return {
        'pbc': PBC_KEY,
        'tenant': tenant,
        'configuration': {
            'database_backend': 'postgresql',
            'event_topic': 'appgen.quality.events',
            'retry_limit': 3,
            'allowed_sites': ('factory_east', 'dc_east'),
            'allowed_inspection_sources': ('production', 'receipt'),
            'allowed_hold_reasons': ('defect', 'spc_breach', 'supplier_review'),
            'allowed_dispositions': ('rework', 'scrap', 'release', 'return_to_supplier'),
            'default_timezone': 'UTC',
            'workbench_limit': 100,
        },
        'parameters': {
            'default_sample_size': 5,
            'defect_threshold': 1,
            'cpk_minimum': 1.33,
            'hold_severity_threshold': 0.7,
            'capa_due_days': 14,
            'retention_days': 2555,
            'release_approval_threshold': 0.8,
        },
        'rules': (
            {
                'rule_id': 'qa.demo.inspection_release',
                'tenant': tenant,
                'rule_type': 'quality',
                'eligible_sources': ('production', 'receipt'),
                'allowed_sites': ('factory_east',),
                'sampling_methods': ('fixed', 'risk_based'),
                'required_measurements': ('length', 'torque'),
                'critical_defect_classes': ('safety', 'regulatory'),
                'release_dispositions': ('release', 'rework'),
                'status': 'active',
            },
        ),
        'inspection_plan': {'plan_id': 'plan_demo_100', 'tenant': tenant, 'item': 'machine_kit', 'site': 'factory_east', 'source': 'production', 'sampling_method': 'fixed', 'sample_size': 5, 'revision': 'A', 'status': 'released'},
        'inspection_result': {'result_id': 'result_demo_100', 'tenant': tenant, 'plan_id': 'plan_demo_100', 'lot_id': 'lot_demo_100', 'order_id': 'order_demo_100', 'measurements': {'length': (10.0, 10.1, 9.9, 10.2, 10.0), 'torque': (4.9, 5.0, 5.1, 5.0, 5.2)}, 'defects': ('scratch',), 'inspector': 'qa_1'},
        'quality_hold': {'hold_id': 'hold_demo_100', 'tenant': tenant, 'item': 'machine_kit', 'lot_id': 'lot_demo_100', 'site': 'factory_east', 'reason': 'defect', 'severity': 0.8},
        'nonconformance': {'nonconformance_id': 'nc_demo_100', 'tenant': tenant, 'result_id': 'result_demo_100', 'defect_class': 'safety', 'severity': 0.8, 'root_cause': 'assembly_variation'},
        'document': 'Inspection certificate, lot lot_demo_100, one scratch defect, route to rework with hold release approval.',
        'instructions': 'Create inspection result, hold the lot, raise nonconformance, disposition to rework, and prepare release evidence.',
    }

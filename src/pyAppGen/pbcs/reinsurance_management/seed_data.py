"""Seed plan for the reinsurance_management PBC."""

from .runtime import REINSURANCE_MANAGEMENT_BUSINESS_TABLES

PBC_KEY = 'reinsurance_management'


def seed_plan():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'records': (
            {'table': REINSURANCE_MANAGEMENT_BUSINESS_TABLES[0], 'code': 'TRT-DEMO'},
            {'table': 'reinsurance_management_counterparty_projection', 'code': 'CP-DEMO'},
            {'table': 'reinsurance_management_exposure_layer', 'code': 'LAYER-DEMO'},
            {'table': 'reinsurance_management_bordereau', 'code': 'BOR-DEMO'},
        ),
        'side_effects': (),
    }


def validate_seed_data():
    plan = seed_plan()
    invalid_tables = tuple(item for item in plan['records'] if not item['table'].startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid_tables, 'pbc': PBC_KEY, 'invalid_tables': invalid_tables, 'side_effects': ()}


def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}

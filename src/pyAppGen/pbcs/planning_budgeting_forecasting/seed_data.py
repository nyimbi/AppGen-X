"""Seed data for the planning_budgeting_forecasting PBC."""
PBC_KEY = 'planning_budgeting_forecasting'
SEED_ROWS = ({'table': f'{PBC_KEY}_planning_model', 'code': 'DEFAULT', 'status': 'active'},)


def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'rows': SEED_ROWS, 'side_effects': ()}


def validate_seed_data():
    return {'ok': all(row['table'].startswith(f'{PBC_KEY}_') for row in SEED_ROWS), 'rows': SEED_ROWS, 'side_effects': ()}


def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'] and standalone_seed_bundle()['ok'], 'standalone_seed_bundle': standalone_seed_bundle(), 'side_effects': ()}


def standalone_seed_bundle():
    rows = (
        {'table': 'planning_budgeting_forecasting_planning_model', 'rows': ({'code': 'CORPORATE-FINANCIAL-PLAN', 'status': 'active'},)},
        {'table': 'planning_budgeting_forecasting_budget_version', 'rows': ({'code': 'FY-BUDGET-V1', 'status': 'draft'},)},
        {'table': 'planning_budgeting_forecasting_forecast_cycle', 'rows': ({'code': 'ROLLING-FORECAST', 'status': 'open'},)},
        {'table': 'planning_budgeting_forecasting_allocation_rule', 'rows': ({'code': 'HEADCOUNT-ALLOC', 'status': 'active'},)},
    )
    invalid_tables = tuple(item['table'] for item in rows if not item['table'].startswith(f'{PBC_KEY}_'))
    return {'ok': bool(rows) and not invalid_tables, 'pbc': PBC_KEY, 'rows': rows, 'invalid_tables': invalid_tables, 'side_effects': ()}

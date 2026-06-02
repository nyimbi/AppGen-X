"""Seed data for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .blueprint import PBC_KEY, owned_table

SEED_ROWS = (
    {'table': owned_table('esg_metric'), 'code': 'METRIC-NET-ZERO', 'status': 'active'},
    {'table': owned_table('reporting_framework_mapping'), 'code': 'FRAME-ISSB-CSRD', 'status': 'active'},
    {'table': owned_table('runtime_parameter'), 'code': 'quality_score_floor', 'status': 'active'},
)


def seed_plan() -> dict:
    return {'ok': True, 'pbc': PBC_KEY, 'rows': SEED_ROWS, 'side_effects': ()}


def validate_seed_data() -> dict:
    return {'ok': all(row['table'].startswith(f'{PBC_KEY}_') for row in SEED_ROWS), 'rows': SEED_ROWS, 'side_effects': ()}


def smoke_test() -> dict:
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}

from __future__ import annotations

from .slice_app import PBC_KEY, build_seed_plan


def seed_plan() -> dict:
    return build_seed_plan()


def validate_seed_data() -> dict:
    plan = seed_plan()
    return {
        'ok': plan['ok'] and bool(plan['rows']),
        'pbc': PBC_KEY,
        'row_count': len(plan['rows']),
        'side_effects': (),
    }


def seed_manifest() -> dict:
    return seed_plan()


def smoke_test() -> dict:
    validation = validate_seed_data()
    return {'ok': validation['ok'], 'pbc': PBC_KEY, 'side_effects': ()}

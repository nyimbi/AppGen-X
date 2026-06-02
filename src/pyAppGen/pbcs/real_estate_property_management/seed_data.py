"""Seed data plans for real estate property management."""
from .standalone import PBC_KEY
from .standalone import seed_plan as _seed_plan
from .standalone import validate_seed_data as _validate_seed_data


def seed_plan():
    return _seed_plan()


def validate_seed_data():
    return _validate_seed_data()


def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}

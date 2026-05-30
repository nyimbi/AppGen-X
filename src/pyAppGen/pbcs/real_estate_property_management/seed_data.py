from .standalone import PBC_KEY, seed_plan, validate_seed_data


def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}

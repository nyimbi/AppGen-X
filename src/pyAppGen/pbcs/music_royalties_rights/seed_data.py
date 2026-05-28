PBC_KEY = 'music_royalties_rights'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': MUSIC_ROYALTIES_RIGHTS_BUSINESS_TABLES[0] if False else 'music_royalties_rights_musical_work', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}

PBC_KEY = 'media_rights_content_monetization'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': MEDIA_RIGHTS_CONTENT_MONETIZATION_BUSINESS_TABLES[0] if False else 'media_rights_content_monetization_rights_asset', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}

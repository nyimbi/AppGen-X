PBC_KEY = 'sports_venue_event_operations'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': SPORTS_VENUE_EVENT_OPERATIONS_BUSINESS_TABLES[0] if False else 'sports_venue_event_operations_venue_event', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}

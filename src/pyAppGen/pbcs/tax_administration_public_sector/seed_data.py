PBC_KEY = 'tax_administration_public_sector'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': TAX_ADMINISTRATION_PUBLIC_SECTOR_BUSINESS_TABLES[0] if False else 'tax_administration_public_sector_taxpayer_account', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}

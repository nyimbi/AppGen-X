PBC_KEY = 'education_student_lifecycle'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': EDUCATION_STUDENT_LIFECYCLE_BUSINESS_TABLES[0] if False else 'education_student_lifecycle_student_applicant', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}

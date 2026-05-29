PBC_KEY = "education_student_lifecycle"
SEED_RECORDS = (
    {"table": "education_student_lifecycle_student_applicant", "code": "SEED-APPLICANT-ADMIT", "scenario": "accepted_applicant_ready_for_matriculation"},
    {"table": "education_student_lifecycle_transfer_credit_evaluation", "code": "SEED-TRANSFER-CREDIT", "scenario": "approved_transfer_credit_applied_to_audit"},
    {"table": "education_student_lifecycle_student_risk_signal", "code": "SEED-RISK-HIGH", "scenario": "high_risk_student_requires_human_review"},
    {"table": "education_student_lifecycle_academic_petition", "code": "SEED-PETITION", "scenario": "petition_pending_committee_review"},
    {"table": "education_student_lifecycle_course_attempt", "code": "SEED-COURSE-REPEAT", "scenario": "repeat_attempt_with_override"},
    {"table": "education_student_lifecycle_degree_audit", "code": "SEED-GRAD-AUDIT", "scenario": "degree_audit_complete_ready_for_clearance"},
    {"table": "education_student_lifecycle_credential", "code": "SEED-CREDENTIAL", "scenario": "credential_conferral_complete"},
    {"table": "education_student_lifecycle_accommodation_projection", "code": "SEED-PRIVACY", "scenario": "privacy_restricted_accommodation_projection"},
)


def seed_plan():
    return {"ok": True, "pbc": PBC_KEY, "records": SEED_RECORDS, "side_effects": ()}


def validate_seed_data():
    invalid_tables = tuple(record for record in SEED_RECORDS if not record["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid_tables, "pbc": PBC_KEY, "invalid_tables": invalid_tables, "side_effects": ()}


def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}

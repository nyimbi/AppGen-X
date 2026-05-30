BEGIN;

CREATE TABLE IF NOT EXISTS student_financial_aid_aid_year (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_aid_year_tenant ON student_financial_aid_aid_year (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_aid_year_subject ON student_financial_aid_aid_year (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_student_aid_profile (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_student_aid_profile_tenant ON student_financial_aid_student_aid_profile (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_student_aid_profile_subject ON student_financial_aid_student_aid_profile (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_aid_application (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_aid_application_tenant ON student_financial_aid_aid_application (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_aid_application_subject ON student_financial_aid_aid_application (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_dependency_review (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_dependency_review_tenant ON student_financial_aid_dependency_review (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_dependency_review_subject ON student_financial_aid_dependency_review (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_verification_item (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_verification_item_tenant ON student_financial_aid_verification_item (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_verification_item_subject ON student_financial_aid_verification_item (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_document_artifact (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_document_artifact_tenant ON student_financial_aid_document_artifact (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_document_artifact_subject ON student_financial_aid_document_artifact (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_sap_evaluation (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_sap_evaluation_tenant ON student_financial_aid_sap_evaluation (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_sap_evaluation_subject ON student_financial_aid_sap_evaluation (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_cost_of_attendance_budget (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_cost_of_attendance_budget_tenant ON student_financial_aid_cost_of_attendance_budget (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_cost_of_attendance_budget_subject ON student_financial_aid_cost_of_attendance_budget (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_need_analysis (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_need_analysis_tenant ON student_financial_aid_need_analysis (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_need_analysis_subject ON student_financial_aid_need_analysis (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_award_package (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_award_package_tenant ON student_financial_aid_award_package (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_award_package_subject ON student_financial_aid_award_package (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_award_line (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_award_line_tenant ON student_financial_aid_award_line (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_award_line_subject ON student_financial_aid_award_line (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_scholarship_resource (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_scholarship_resource_tenant ON student_financial_aid_scholarship_resource (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_scholarship_resource_subject ON student_financial_aid_scholarship_resource (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_grant_eligibility (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_grant_eligibility_tenant ON student_financial_aid_grant_eligibility (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_grant_eligibility_subject ON student_financial_aid_grant_eligibility (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_loan_offer (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_loan_offer_tenant ON student_financial_aid_loan_offer (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_loan_offer_subject ON student_financial_aid_loan_offer (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_work_study_plan (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_work_study_plan_tenant ON student_financial_aid_work_study_plan (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_work_study_plan_subject ON student_financial_aid_work_study_plan (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_disbursement_schedule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_disbursement_schedule_tenant ON student_financial_aid_disbursement_schedule (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_disbursement_schedule_subject ON student_financial_aid_disbursement_schedule (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_refund_return_case (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_refund_return_case_tenant ON student_financial_aid_refund_return_case (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_refund_return_case_subject ON student_financial_aid_refund_return_case (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_overaward_case (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_overaward_case_tenant ON student_financial_aid_overaward_case (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_overaward_case_subject ON student_financial_aid_overaward_case (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_professional_judgment_case (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_professional_judgment_case_tenant ON student_financial_aid_professional_judgment_case (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_professional_judgment_case_subject ON student_financial_aid_professional_judgment_case (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_aid_appeal (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_aid_appeal_tenant ON student_financial_aid_aid_appeal (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_aid_appeal_subject ON student_financial_aid_aid_appeal (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_aid_compliance_obligation (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_aid_compliance_obligation_tenant ON student_financial_aid_aid_compliance_obligation (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_aid_compliance_obligation_subject ON student_financial_aid_aid_compliance_obligation (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_communication_log (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_communication_log_tenant ON student_financial_aid_communication_log (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_communication_log_subject ON student_financial_aid_communication_log (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_policy_rule_tenant ON student_financial_aid_policy_rule (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_policy_rule_subject ON student_financial_aid_policy_rule (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_runtime_parameter_tenant ON student_financial_aid_runtime_parameter (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_runtime_parameter_subject ON student_financial_aid_runtime_parameter (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_schema_extension_tenant ON student_financial_aid_schema_extension (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_schema_extension_subject ON student_financial_aid_schema_extension (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_control_assertion_tenant ON student_financial_aid_control_assertion (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_control_assertion_subject ON student_financial_aid_control_assertion (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_governed_model_tenant ON student_financial_aid_governed_model (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_governed_model_subject ON student_financial_aid_governed_model (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_appgen_outbox_event_tenant ON student_financial_aid_appgen_outbox_event (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_appgen_outbox_event_subject ON student_financial_aid_appgen_outbox_event (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_appgen_inbox_event_tenant ON student_financial_aid_appgen_inbox_event (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_appgen_inbox_event_subject ON student_financial_aid_appgen_inbox_event (primary_subject_id, aid_year_code);

CREATE TABLE IF NOT EXISTS student_financial_aid_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    aid_year_code TEXT,
    primary_subject_id TEXT,
    secondary_subject_id TEXT,
    record_stage TEXT,
    amount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_appgen_dead_letter_event_tenant ON student_financial_aid_appgen_dead_letter_event (tenant, created_at);
CREATE INDEX IF NOT EXISTS idx_student_financial_aid_appgen_dead_letter_event_subject ON student_financial_aid_appgen_dead_letter_event (primary_subject_id, aid_year_code);

COMMIT;

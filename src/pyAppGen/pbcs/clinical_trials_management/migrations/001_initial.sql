CREATE TABLE clinical_trials_management_trial_protocol (
    tenant TEXT NOT NULL,
    protocol_id TEXT PRIMARY KEY,
    protocol_code TEXT NOT NULL,
    title TEXT,
    phase TEXT,
    version INTEGER NOT NULL,
    status TEXT NOT NULL,
    amendment_reason TEXT,
    effective_date TEXT,
    countries JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_study_site (
    tenant TEXT NOT NULL,
    site_id TEXT PRIMARY KEY,
    protocol_id TEXT NOT NULL,
    site_number TEXT NOT NULL,
    country TEXT NOT NULL,
    principal_investigator TEXT,
    status TEXT NOT NULL,
    activation_checklist JSON,
    activation_gaps JSON,
    activation_date TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_subject (
    tenant TEXT NOT NULL,
    subject_id TEXT PRIMARY KEY,
    protocol_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    screening_number TEXT NOT NULL,
    status TEXT NOT NULL,
    eligibility_status TEXT NOT NULL,
    consent_status TEXT NOT NULL,
    cohort TEXT,
    arm TEXT,
    withdrawal_reason TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_consent_record (
    tenant TEXT NOT NULL,
    consent_id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL,
    protocol_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    consent_version INTEGER NOT NULL,
    language TEXT NOT NULL,
    signer_role TEXT,
    consent_scope JSON,
    status TEXT NOT NULL,
    signed_on TEXT,
    expires_on TEXT,
    source_document_ref TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_visit_schedule (
    tenant TEXT NOT NULL,
    visit_id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL,
    protocol_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    visit_code TEXT NOT NULL,
    visit_type TEXT NOT NULL,
    target_day INTEGER,
    actual_day INTEGER,
    window_classification TEXT,
    status TEXT NOT NULL,
    missing_procedures JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_adverse_event (
    tenant TEXT NOT NULL,
    adverse_event_id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL,
    protocol_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    event_term TEXT,
    seriousness TEXT NOT NULL,
    grade TEXT,
    expectedness TEXT,
    relatedness TEXT,
    status TEXT NOT NULL,
    reporting_due_hours INTEGER,
    reporting_status TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_monitoring_finding (
    tenant TEXT NOT NULL,
    finding_id TEXT PRIMARY KEY,
    protocol_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    subject_id TEXT,
    finding_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    owner TEXT,
    status TEXT NOT NULL,
    remediation_due_days INTEGER,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_clinical_trials_management_policy_rule (
    tenant TEXT NOT NULL,
    rule_id TEXT PRIMARY KEY,
    rule_type TEXT NOT NULL,
    scope TEXT,
    status TEXT NOT NULL,
    compiled_hash TEXT,
    policy_version TEXT,
    description TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_clinical_trials_management_runtime_parameter (
    tenant TEXT NOT NULL,
    parameter_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    value INTEGER NOT NULL,
    min_value INTEGER,
    max_value INTEGER,
    unit TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_clinical_trials_management_schema_extension (
    tenant TEXT NOT NULL,
    extension_id TEXT PRIMARY KEY,
    table_name TEXT NOT NULL,
    field_name TEXT NOT NULL,
    field_type TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_clinical_trials_management_control_assertion (
    tenant TEXT NOT NULL,
    control_id TEXT PRIMARY KEY,
    focus_area TEXT NOT NULL,
    threshold TEXT,
    status TEXT NOT NULL,
    failing_population JSON,
    owner TEXT,
    remediation_due_on TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_clinical_trials_management_governed_model (
    tenant TEXT NOT NULL,
    model_id TEXT PRIMARY KEY,
    use_case TEXT NOT NULL,
    model_version TEXT NOT NULL,
    approval_status TEXT NOT NULL,
    drift_status TEXT NOT NULL,
    review_due_on TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE clinical_trials_management_appgen_outbox_event (
    tenant TEXT NOT NULL,
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    aggregate_table TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    payload JSON,
    created_at TEXT
);

CREATE TABLE clinical_trials_management_appgen_inbox_event (
    tenant TEXT NOT NULL,
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    payload JSON,
    status TEXT,
    retry_count INTEGER,
    processed_at TEXT
);

CREATE TABLE clinical_trials_management_appgen_dead_letter_event (
    tenant TEXT NOT NULL,
    dead_letter_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    reason TEXT,
    payload JSON,
    retry_count INTEGER,
    last_attempt_at TEXT
);

CREATE TABLE identity_kyc_aml_compliance_kyc_profile (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    subject_name TEXT NOT NULL,
    customer_type TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    product_exposure TEXT NOT NULL,
    channel TEXT NOT NULL,
    status TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    edd_required BOOLEAN NOT NULL,
    next_rescreen_due_at TEXT,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_identity_document (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    profile_id TEXT NOT NULL,
    document_class TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    identifier TEXT NOT NULL,
    verification_status TEXT NOT NULL,
    authenticity_status TEXT NOT NULL,
    expiry_state TEXT NOT NULL,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_beneficial_owner (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    profile_id TEXT NOT NULL,
    owner_name TEXT NOT NULL,
    role_type TEXT NOT NULL,
    ownership_pct NUMERIC,
    screening_required BOOLEAN NOT NULL,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_screening_hit (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    profile_id TEXT NOT NULL,
    category TEXT NOT NULL,
    watchlist_source TEXT NOT NULL,
    severity TEXT NOT NULL,
    confidence NUMERIC NOT NULL,
    disposition TEXT NOT NULL,
    blocking BOOLEAN NOT NULL,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_monitoring_alert (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    profile_id TEXT,
    source_type TEXT NOT NULL,
    typology TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    assigned_to TEXT,
    due_at TEXT,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_suspicious_activity_case (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    profile_id TEXT NOT NULL,
    alert_id TEXT,
    case_status TEXT NOT NULL,
    escalation_reason TEXT NOT NULL,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_compliance_review (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    profile_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    review_status TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    approved_score NUMERIC,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    severity TEXT NOT NULL,
    compiled_hash TEXT NOT NULL,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    value TEXT NOT NULL,
    scope TEXT NOT NULL,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    table_name TEXT NOT NULL,
    field_map JSON NOT NULL,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    assertion_type TEXT NOT NULL,
    assertion_status TEXT NOT NULL,
    evidence_hash TEXT NOT NULL,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    approval_status TEXT NOT NULL,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload JSON NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    payload JSON NOT NULL,
    received_at TEXT NOT NULL
);

CREATE TABLE identity_kyc_aml_compliance_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    payload JSON NOT NULL,
    reason TEXT NOT NULL,
    received_at TEXT NOT NULL
);

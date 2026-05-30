CREATE TABLE IF NOT EXISTS insurance_underwriting_underwriting_submission (
    submission_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    product_line TEXT NOT NULL,
    applicant_name TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    source TEXT,
    broker_code TEXT,
    requested_limit REAL NOT NULL,
    declared_revenue REAL,
    completeness_score REAL NOT NULL,
    lifecycle_state TEXT NOT NULL,
    referral_flag INTEGER NOT NULL,
    effective_date TEXT,
    exposure_locations_json TEXT NOT NULL,
    prior_losses_json TEXT NOT NULL,
    documents_json TEXT NOT NULL,
    metadata_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_risk_profile (
    risk_profile_id TEXT PRIMARY KEY,
    submission_id TEXT NOT NULL,
    tenant TEXT NOT NULL,
    industry_code TEXT NOT NULL,
    hazard_score REAL NOT NULL,
    catastrophe_score REAL NOT NULL,
    prior_loss_count INTEGER NOT NULL,
    appetite_result TEXT NOT NULL,
    risk_notes TEXT,
    hazard_factors_json TEXT NOT NULL,
    financial_signals_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_rating_factor (
    factor_id TEXT PRIMARY KEY,
    submission_id TEXT NOT NULL,
    tenant TEXT NOT NULL,
    factor_type TEXT NOT NULL,
    selected_value REAL NOT NULL,
    weight REAL NOT NULL,
    source TEXT NOT NULL,
    override_reason TEXT,
    supported INTEGER NOT NULL,
    transformation_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_quote (
    quote_id TEXT PRIMARY KEY,
    submission_id TEXT NOT NULL,
    tenant TEXT NOT NULL,
    version INTEGER NOT NULL,
    scenario_name TEXT NOT NULL,
    premium REAL NOT NULL,
    rate REAL NOT NULL,
    status TEXT NOT NULL,
    valid_until TEXT NOT NULL,
    subjectivity_count INTEGER NOT NULL,
    subjectivities_json TEXT NOT NULL,
    exclusions_json TEXT NOT NULL,
    pricing_trace_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_underwriting_decision (
    decision_id TEXT PRIMARY KEY,
    submission_id TEXT NOT NULL,
    quote_id TEXT NOT NULL,
    tenant TEXT NOT NULL,
    decision_type TEXT NOT NULL,
    status TEXT NOT NULL,
    authority_level TEXT NOT NULL,
    approved_by TEXT,
    rationale TEXT,
    referral_open INTEGER NOT NULL,
    decision_packet_json TEXT NOT NULL,
    approved_at TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_bind_package (
    bind_package_id TEXT PRIMARY KEY,
    submission_id TEXT NOT NULL,
    quote_id TEXT NOT NULL,
    tenant TEXT NOT NULL,
    status TEXT NOT NULL,
    checklist_json TEXT NOT NULL,
    subjectivities_json TEXT NOT NULL,
    missing_items_json TEXT NOT NULL,
    handoff_event_id TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_exclusion (
    exclusion_id TEXT PRIMARY KEY,
    submission_id TEXT NOT NULL,
    quote_id TEXT,
    tenant TEXT NOT NULL,
    clause_code TEXT NOT NULL,
    reason TEXT NOT NULL,
    customer_explanation TEXT NOT NULL,
    approval_required INTEGER NOT NULL,
    approved_by TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_insurance_underwriting_policy_rule (
    rule_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    rule_type TEXT NOT NULL,
    version INTEGER NOT NULL,
    status TEXT NOT NULL,
    definition_json TEXT NOT NULL,
    compiled_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_insurance_underwriting_runtime_parameter (
    parameter_name TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    value_json TEXT NOT NULL,
    bounded_min REAL,
    bounded_max REAL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_insurance_underwriting_schema_extension (
    extension_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    table_name TEXT NOT NULL,
    field_name TEXT NOT NULL,
    field_type TEXT NOT NULL,
    status TEXT NOT NULL,
    approved_by TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_insurance_underwriting_control_assertion (
    assertion_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    control_name TEXT NOT NULL,
    subject TEXT NOT NULL,
    status TEXT NOT NULL,
    evidence_json TEXT NOT NULL,
    checked_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_insurance_underwriting_governed_model (
    model_key TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    version TEXT NOT NULL,
    domain TEXT NOT NULL,
    status TEXT NOT NULL,
    freshness_date TEXT NOT NULL,
    requirements_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_appgen_outbox_event (
    event_id TEXT PRIMARY KEY,
    aggregate_id TEXT NOT NULL,
    aggregate_type TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    tenant TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_appgen_inbox_event (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    source_pbc TEXT,
    tenant TEXT,
    payload_json TEXT NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS insurance_underwriting_appgen_dead_letter_event (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    tenant TEXT,
    payload_json TEXT NOT NULL,
    reason TEXT NOT NULL,
    retry_count INTEGER NOT NULL,
    created_at TEXT NOT NULL
);

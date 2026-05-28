CREATE TABLE claims_adjudication_healthcare_health_claim (
    claim_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    claim_number TEXT NOT NULL,
    claim_type TEXT NOT NULL,
    source_format TEXT NOT NULL,
    member_id TEXT NOT NULL,
    provider_id TEXT NOT NULL,
    plan_id TEXT NOT NULL,
    received_date TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    total_charge NUMERIC NOT NULL DEFAULT 0,
    duplicate_of TEXT,
    pend_reason TEXT,
    original_claim_id TEXT,
    correction_type TEXT,
    evidence JSON NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_claim_line (
    line_id TEXT PRIMARY KEY,
    claim_id TEXT NOT NULL,
    tenant TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    service_date TEXT NOT NULL,
    procedure_code TEXT NOT NULL,
    diagnosis_code TEXT NOT NULL,
    place_of_service TEXT NOT NULL,
    units INTEGER NOT NULL,
    charge_amount NUMERIC NOT NULL,
    authorization_id TEXT,
    modifiers JSON NOT NULL DEFAULT '[]',
    status TEXT NOT NULL,
    allowed_amount NUMERIC NOT NULL DEFAULT 0,
    member_responsibility NUMERIC NOT NULL DEFAULT 0,
    payer_responsibility NUMERIC NOT NULL DEFAULT 0,
    adjudication_reason TEXT,
    reason_codes JSON NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_coding_review (
    review_id TEXT PRIMARY KEY,
    claim_id TEXT NOT NULL,
    tenant TEXT NOT NULL,
    line_id TEXT,
    issue_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    notes TEXT NOT NULL,
    override_reason TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_benefit_rule (
    rule_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    plan_id TEXT NOT NULL,
    service_code TEXT NOT NULL,
    description TEXT NOT NULL,
    covered BOOLEAN NOT NULL,
    auth_required BOOLEAN NOT NULL,
    allowed_percentage NUMERIC NOT NULL,
    copay_amount NUMERIC NOT NULL,
    deductible_apply BOOLEAN NOT NULL,
    max_units INTEGER NOT NULL,
    effective_from TEXT NOT NULL,
    effective_to TEXT NOT NULL,
    status TEXT NOT NULL,
    approval_reference TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_denial (
    denial_id TEXT PRIMARY KEY,
    claim_id TEXT NOT NULL,
    tenant TEXT NOT NULL,
    denial_code TEXT NOT NULL,
    rationale TEXT NOT NULL,
    policy_rule_id TEXT NOT NULL,
    line_ids JSON NOT NULL DEFAULT '[]',
    notice_deadline TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_appeal (
    appeal_id TEXT PRIMARY KEY,
    denial_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    tenant TEXT NOT NULL,
    level TEXT NOT NULL,
    requester TEXT NOT NULL,
    evidence_summary TEXT NOT NULL,
    status TEXT NOT NULL,
    determination TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_payment_integrity_case (
    case_id TEXT PRIMARY KEY,
    claim_id TEXT NOT NULL,
    tenant TEXT NOT NULL,
    trigger TEXT NOT NULL,
    exposure_amount NUMERIC NOT NULL,
    reviewer TEXT NOT NULL,
    notes TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_policy_rule (
    policy_rule_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    description TEXT NOT NULL,
    condition_key TEXT NOT NULL,
    threshold NUMERIC NOT NULL,
    action TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_runtime_parameter (
    parameter_name TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    value NUMERIC NOT NULL,
    minimum NUMERIC NOT NULL,
    maximum NUMERIC NOT NULL,
    unit TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_schema_extension (
    extension_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    target_table TEXT NOT NULL,
    column_name TEXT NOT NULL,
    data_type TEXT NOT NULL,
    justification TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_control_assertion (
    assertion_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    control_name TEXT NOT NULL,
    objective TEXT NOT NULL,
    frequency TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_governed_model (
    model_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    model_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    version TEXT NOT NULL,
    approval_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_document_instruction (
    instruction_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    document_name TEXT NOT NULL,
    instruction_text TEXT NOT NULL,
    target_table TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT NOT NULL,
    structured_fields JSON NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_appgen_outbox_event (
    event_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload JSON NOT NULL DEFAULT '{}',
    idempotency_key TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_appgen_inbox_event (
    event_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload JSON NOT NULL DEFAULT '{}',
    idempotency_key TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE claims_adjudication_healthcare_appgen_dead_letter_event (
    event_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload JSON NOT NULL DEFAULT '{}',
    idempotency_key TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

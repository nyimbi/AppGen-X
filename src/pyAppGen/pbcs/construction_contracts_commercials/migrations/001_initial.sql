CREATE TABLE construction_contracts_commercials_construction_contract (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    contract_code TEXT NOT NULL,
    title TEXT NOT NULL,
    contract_type TEXT NOT NULL,
    pricing_basis TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    counterparty TEXT NOT NULL,
    lifecycle_stage TEXT NOT NULL,
    contract_value NUMERIC(18,2) NOT NULL,
    approved_change_value NUMERIC(18,2) NOT NULL,
    current_contract_value NUMERIC(18,2) NOT NULL,
    retainage_percent NUMERIC(8,2) NOT NULL,
    final_account_status TEXT NOT NULL,
    closeout_blockers JSON NOT NULL,
    schedule_of_values JSON NOT NULL,
    guarantees JSON NOT NULL,
    obligations JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_pay_application (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    contract_id TEXT NOT NULL,
    application_number TEXT NOT NULL,
    intake_status TEXT NOT NULL,
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    gross_claimed NUMERIC(18,2) NOT NULL,
    certified_amount NUMERIC(18,2) NOT NULL,
    retainage_withheld NUMERIC(18,2) NOT NULL,
    waiver_status TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    attachments JSON NOT NULL,
    lines JSON NOT NULL,
    validation_issues JSON NOT NULL,
    certificate_trace JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_retainage (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    contract_id TEXT NOT NULL,
    pay_application_id TEXT NOT NULL,
    status TEXT NOT NULL,
    retainage_percent NUMERIC(8,2) NOT NULL,
    withheld_amount NUMERIC(18,2) NOT NULL,
    release_trigger TEXT NOT NULL,
    release_blockers JSON NOT NULL,
    released_amount NUMERIC(18,2) NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_variation_order (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    contract_id TEXT NOT NULL,
    variation_number TEXT NOT NULL,
    status TEXT NOT NULL,
    instruction_date TEXT,
    event_date TEXT,
    notice_date TEXT,
    contractual_deadline TEXT,
    time_bar_status TEXT NOT NULL,
    quoted_amount NUMERIC(18,2) NOT NULL,
    approved_amount NUMERIC(18,2) NOT NULL,
    time_impact_days INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_commercial_claim (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    contract_id TEXT NOT NULL,
    claim_number TEXT NOT NULL,
    claim_type TEXT NOT NULL,
    status TEXT NOT NULL,
    event_date TEXT,
    notice_date TEXT,
    contractual_deadline TEXT,
    time_bar_status TEXT NOT NULL,
    claimed_amount NUMERIC(18,2) NOT NULL,
    assessed_amount NUMERIC(18,2) NOT NULL,
    settled_amount NUMERIC(18,2) NOT NULL,
    entitlement_risk NUMERIC(8,2) NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_lien_waiver (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    contract_id TEXT NOT NULL,
    pay_application_id TEXT,
    waiver_number TEXT NOT NULL,
    waiver_type TEXT NOT NULL,
    status TEXT NOT NULL,
    covered_amount NUMERIC(18,2) NOT NULL,
    covered_period TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    signed_date TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_subcontract_package (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    contract_id TEXT NOT NULL,
    package_code TEXT NOT NULL,
    subcontractor_name TEXT NOT NULL,
    status TEXT NOT NULL,
    contract_value NUMERIC(18,2) NOT NULL,
    insurance_status TEXT NOT NULL,
    bond_status TEXT NOT NULL,
    compliance_hold BOOLEAN NOT NULL,
    closeout_checklist JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_construction_contracts_commercials_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    rule_code TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    policy_area TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    compiled_hash TEXT NOT NULL,
    effective_from TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_construction_contracts_commercials_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    value_json JSON NOT NULL,
    unit TEXT NOT NULL,
    bounded BOOLEAN NOT NULL,
    status TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_construction_contracts_commercials_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    target_table TEXT NOT NULL,
    extension_name TEXT NOT NULL,
    status TEXT NOT NULL,
    fields_json JSON NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_construction_contracts_commercials_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    control_code TEXT NOT NULL,
    control_name TEXT NOT NULL,
    status TEXT NOT NULL,
    failing_population JSON NOT NULL,
    remediation_owner TEXT,
    last_run_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_construction_contracts_commercials_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    model_name TEXT NOT NULL,
    status TEXT NOT NULL,
    task_type TEXT NOT NULL,
    requires_human_confirmation BOOLEAN NOT NULL,
    latest_instruction_digest TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload_json JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    source_event_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload_json JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    received_at TEXT NOT NULL
);

CREATE TABLE construction_contracts_commercials_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload_json JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    failure_reason TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE reinsurance_management_reinsurance_treaty (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    treaty_type TEXT,
    effective_from TEXT,
    effective_to TEXT,
    aggregate_limit REAL,
    remaining_limit REAL,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_facultative_placement (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    risk_reference TEXT,
    required_share_pct REAL,
    bound_share_pct REAL,
    quote_count INTEGER,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_cession (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    treaty_id TEXT,
    layer_id TEXT,
    gross_premium REAL,
    gross_loss REAL,
    ceded_premium REAL,
    ceded_loss REAL,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_bordereau (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    bordereau_type TEXT,
    period TEXT,
    accepted_rows INTEGER,
    rejected_rows INTEGER,
    submission_status TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_recoverable (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    counterparty_id TEXT,
    amount REAL,
    currency TEXT,
    aging_bucket TEXT,
    impairment_flag INTEGER,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_claim_recovery (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    claim_reference TEXT,
    recoverable_id TEXT,
    notice_date TEXT,
    documentation_complete INTEGER,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_exposure_layer (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    peril TEXT,
    attachment_point REAL,
    exhaustion_point REAL,
    utilized_limit REAL,
    remaining_limit REAL,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_counterparty_projection (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    role TEXT,
    rating TEXT,
    domicile TEXT,
    signed_share_pct REAL,
    watchlist INTEGER,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_collateral_position (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    counterparty_id TEXT,
    required_amount REAL,
    posted_amount REAL,
    deficiency_amount REAL,
    expiry_date TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_settlement_statement (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    counterparty_id TEXT,
    statement_period TEXT,
    line_count INTEGER,
    balance_due REAL,
    currency TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_cash_call (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    statement_id TEXT,
    recoverable_id TEXT,
    amount_due REAL,
    due_date TEXT,
    urgency TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_commutation_case (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    treaty_id TEXT,
    recoverable_count INTEGER,
    negotiated_amount REAL,
    approval_state TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_retrocession_program (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    source_treaty_id TEXT,
    retro_share_pct REAL,
    retro_limit REAL,
    protection_basis TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_catastrophe_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    peril TEXT,
    occurrence_start TEXT,
    occurrence_end TEXT,
    gross_loss_estimate REAL,
    ceded_loss_estimate REAL,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_audit_reconciliation (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    source_total REAL,
    ledger_total REAL,
    statement_total REAL,
    variance REAL,
    resolution_status TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_assistant_preview (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    instruction TEXT,
    suggested_action TEXT,
    candidate_tables JSON,
    requires_confirmation INTEGER,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_reinsurance_management_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_reinsurance_management_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_reinsurance_management_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_reinsurance_management_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_reinsurance_management_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE reinsurance_management_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

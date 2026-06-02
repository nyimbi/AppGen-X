CREATE TABLE IF NOT EXISTS gaming_casino_operations_player_profile (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    player_number TEXT NOT NULL,
    legal_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    loyalty_tier TEXT NOT NULL,
    enrollment_status TEXT NOT NULL,
    identity_confidence NUMERIC NOT NULL,
    age_verified BOOLEAN NOT NULL,
    restriction_state TEXT NOT NULL,
    property_id TEXT NOT NULL,
    host_id TEXT,
    duplicate_review_state TEXT NOT NULL,
    payload JSON
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_table_game (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    table_number TEXT NOT NULL,
    pit TEXT NOT NULL,
    game_variant TEXT NOT NULL,
    table_status TEXT NOT NULL,
    shift_id TEXT NOT NULL,
    opening_bankroll NUMERIC NOT NULL,
    current_bankroll NUMERIC NOT NULL,
    dealer_id TEXT NOT NULL,
    supervisor_id TEXT NOT NULL,
    dispute_state TEXT NOT NULL,
    payload JSON
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_slot_machine (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    asset_code TEXT NOT NULL,
    bank_location TEXT NOT NULL,
    denomination NUMERIC NOT NULL,
    paytable_version TEXT NOT NULL,
    progressive_link TEXT,
    operational_state TEXT NOT NULL,
    fault_state TEXT NOT NULL,
    jurisdiction_approval_state TEXT NOT NULL,
    last_meter_reading NUMERIC NOT NULL,
    payload JSON
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_wager_session (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    player_profile_id TEXT NOT NULL,
    asset_kind TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    session_status TEXT NOT NULL,
    rating_status TEXT NOT NULL,
    average_bet NUMERIC,
    theoretical_win NUMERIC,
    dispute_flag BOOLEAN NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    payload JSON
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_payout (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payout_number TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_id TEXT NOT NULL,
    payout_kind TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    currency TEXT NOT NULL,
    approval_state TEXT NOT NULL,
    patron_verification_level TEXT NOT NULL,
    suspicious_activity_flag BOOLEAN NOT NULL,
    payload JSON
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_responsible_gaming_case (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    case_number TEXT NOT NULL,
    player_profile_id TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    intervention_state TEXT NOT NULL,
    cooling_off_until TEXT,
    owner_id TEXT NOT NULL,
    payload JSON
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_gaming_compliance (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    case_number TEXT NOT NULL,
    compliance_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    case_status TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    payload JSON
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    rule_id TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    scope TEXT NOT NULL,
    rule_status TEXT NOT NULL,
    version INTEGER NOT NULL,
    effective_from TEXT NOT NULL,
    effective_to TEXT,
    payload JSON
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_value JSON NOT NULL,
    scope TEXT NOT NULL,
    parameter_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    table_name TEXT NOT NULL,
    extension_name TEXT NOT NULL,
    extension_status TEXT NOT NULL,
    fields_json JSON NOT NULL
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    assertion_id TEXT NOT NULL,
    control_name TEXT NOT NULL,
    frequency TEXT NOT NULL,
    assertion_status TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    payload JSON
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    approval_state TEXT NOT NULL,
    drift_state TEXT NOT NULL,
    last_reviewed_at TEXT NOT NULL,
    payload JSON
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    event_type TEXT NOT NULL,
    aggregate_table TEXT,
    aggregate_id TEXT,
    topic TEXT NOT NULL,
    event_status TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    event_type TEXT NOT NULL,
    aggregate_table TEXT,
    aggregate_id TEXT,
    topic TEXT NOT NULL,
    event_status TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE IF NOT EXISTS gaming_casino_operations_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    event_type TEXT NOT NULL,
    aggregate_table TEXT,
    aggregate_id TEXT,
    topic TEXT NOT NULL,
    event_status TEXT NOT NULL,
    payload JSON NOT NULL
);

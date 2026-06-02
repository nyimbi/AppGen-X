CREATE TABLE energy_grid_operations_grid_asset (
    asset_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    asset_name TEXT NOT NULL,
    voltage_kv REAL NOT NULL,
    parent_asset_id TEXT,
    substation_id TEXT NOT NULL,
    feeder_id TEXT NOT NULL,
    normal_state TEXT NOT NULL,
    phases TEXT,
    protection_zone TEXT,
    gis_reference TEXT,
    scada_points TEXT,
    quality_score REAL,
    status TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_load_forecast (
    forecast_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    feeder_id TEXT NOT NULL,
    horizon_hours INTEGER NOT NULL,
    forecast_mw REAL NOT NULL,
    peak_mw REAL NOT NULL,
    confidence REAL NOT NULL,
    weather_scenario TEXT,
    risk_band TEXT,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_switching_order (
    switching_order_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    feeder_id TEXT NOT NULL,
    substation_id TEXT,
    clearance_id TEXT NOT NULL,
    hold_points JSON,
    step_count INTEGER NOT NULL,
    simulation_status TEXT NOT NULL,
    simulation_findings JSON,
    status TEXT NOT NULL,
    requested_by TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_dispatch_instruction (
    dispatch_instruction_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    objective_type TEXT NOT NULL,
    feeder_id TEXT NOT NULL,
    target_asset_id TEXT NOT NULL,
    expected_load_shift_mw REAL,
    telemetry_freshness_seconds INTEGER,
    conflicts JSON,
    rollback_conditions JSON,
    status TEXT NOT NULL,
    approved_by TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_outage_event (
    outage_event_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    feeder_id TEXT NOT NULL,
    substation_id TEXT,
    cause TEXT NOT NULL,
    affected_customers INTEGER NOT NULL,
    restoration_priority TEXT NOT NULL,
    eta_minutes INTEGER,
    crew_status TEXT,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_reliability_constraint (
    constraint_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    constraint_type TEXT NOT NULL,
    scope_id TEXT NOT NULL,
    scope_level TEXT,
    severity TEXT NOT NULL,
    limit_value REAL NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_grid_topology (
    topology_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    feeder_id TEXT NOT NULL,
    source_asset_id TEXT NOT NULL,
    segment_count INTEGER NOT NULL,
    normally_open_ties JSON,
    backfeed_paths JSON,
    phase_map JSON,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_energy_grid_operations_policy_rule (
    rule_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    scope TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    compiled_hash TEXT NOT NULL,
    required_approver_role TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_energy_grid_operations_runtime_parameter (
    parameter_name TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    value REAL NOT NULL,
    datatype TEXT NOT NULL,
    minimum REAL NOT NULL,
    maximum REAL NOT NULL,
    status TEXT NOT NULL,
    approved_by TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_energy_grid_operations_schema_extension (
    extension_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    target_table TEXT NOT NULL,
    new_fields JSON NOT NULL,
    compatibility_result TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_energy_grid_operations_control_assertion (
    assertion_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    control_name TEXT NOT NULL,
    scope_id TEXT NOT NULL,
    assertion_status TEXT NOT NULL,
    evidence_summary TEXT,
    review_required BOOLEAN,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_energy_grid_operations_governed_model (
    model_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    model_kind TEXT NOT NULL,
    approval_scope TEXT NOT NULL,
    training_boundary TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_appgen_outbox_event (
    event_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_appgen_inbox_event (
    event_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    source_pbc TEXT,
    idempotency_key TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE energy_grid_operations_appgen_dead_letter_event (
    event_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    reason TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    payload JSON NOT NULL
);

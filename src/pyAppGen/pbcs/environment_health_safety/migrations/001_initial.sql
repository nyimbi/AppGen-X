CREATE TABLE environment_health_safety_ehs_incident (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    site TEXT NOT NULL,
    area TEXT NOT NULL,
    task TEXT NOT NULL,
    severity TEXT NOT NULL,
    recordability TEXT NOT NULL,
    notification_due_at TIMESTAMPTZ,
    notification_status TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    status TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    payload JSON NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE environment_health_safety_hazard (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    site TEXT NOT NULL,
    area TEXT NOT NULL,
    process TEXT NOT NULL,
    task_step TEXT NOT NULL,
    energy_source TEXT NOT NULL,
    hazard_type TEXT NOT NULL,
    residual_risk INTEGER NOT NULL,
    cluster_count INTEGER NOT NULL,
    status TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    payload JSON NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE environment_health_safety_inspection (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    template TEXT NOT NULL,
    asset TEXT,
    area TEXT NOT NULL,
    due_at TIMESTAMPTZ,
    recurrence TEXT NOT NULL,
    status TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    payload JSON NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE environment_health_safety_permit (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    permit_type TEXT NOT NULL,
    area TEXT NOT NULL,
    start_at TIMESTAMPTZ NOT NULL,
    end_at TIMESTAMPTZ NOT NULL,
    energy_source TEXT NOT NULL,
    status TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    payload JSON NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE environment_health_safety_corrective_action (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    incident_id TEXT,
    owner TEXT NOT NULL,
    due_date TIMESTAMPTZ NOT NULL,
    hierarchy_of_controls TEXT NOT NULL,
    verification_step TEXT NOT NULL,
    status TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    payload JSON NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE environment_health_safety_safety_training (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    worker TEXT NOT NULL,
    course TEXT NOT NULL,
    status TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE environment_health_safety_audit_finding (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    finding TEXT NOT NULL,
    evidence_bundle_id TEXT
);

CREATE TABLE environment_health_safety_policy_rule (
    rule_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    description TEXT NOT NULL,
    compiled_hash TEXT NOT NULL
);

CREATE TABLE environment_health_safety_runtime_parameter (
    name TEXT PRIMARY KEY,
    value NUMERIC NOT NULL,
    minimum NUMERIC NOT NULL,
    maximum NUMERIC NOT NULL
);

CREATE TABLE environment_health_safety_schema_extension (
    id TEXT PRIMARY KEY,
    table_name TEXT NOT NULL,
    fields JSON NOT NULL
);

CREATE TABLE environment_health_safety_control_assertion (
    assertion_id TEXT PRIMARY KEY,
    rule TEXT NOT NULL,
    status TEXT NOT NULL,
    record_id TEXT NOT NULL,
    details JSON NOT NULL
);

CREATE TABLE environment_health_safety_governed_model (
    id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    approval_status TEXT NOT NULL
);

CREATE TABLE environment_health_safety_appgen_outbox_event (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    payload JSON NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE environment_health_safety_appgen_inbox_event (
    idempotency_key TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    payload JSON NOT NULL,
    received_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE environment_health_safety_appgen_dead_letter_event (
    id TEXT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event JSON NOT NULL,
    retry_policy JSON NOT NULL
);

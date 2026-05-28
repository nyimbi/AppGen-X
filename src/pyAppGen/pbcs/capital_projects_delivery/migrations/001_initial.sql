CREATE TABLE capital_projects_delivery_capital_project (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    lifecycle_stage TEXT NOT NULL,
    rebaseline_required BOOLEAN NOT NULL DEFAULT FALSE,
    rebaseline_count INTEGER NOT NULL DEFAULT 0,
    criteria_status JSON,
    gate_dates JSON,
    gate_history JSON,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_epc_package (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_permit_milestone (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_progress_measurement (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_commissioning_system (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_project_risk (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_turnover_package (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_capital_projects_delivery_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_capital_projects_delivery_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_capital_projects_delivery_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_capital_projects_delivery_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_capital_projects_delivery_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE capital_projects_delivery_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant TEXT,
    code TEXT,
    status TEXT,
    version INTEGER,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

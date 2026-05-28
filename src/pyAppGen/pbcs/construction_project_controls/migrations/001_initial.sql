CREATE TABLE construction_project_controls_construction_project (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    project_manager TEXT,
    contractor TEXT,
    original_budget NUMERIC,
    approved_budget NUMERIC,
    active_baseline_revision_id TEXT,
    baseline_revisions JSON,
    reporting_periods JSON,
    release_scorecard JSON,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_work_package (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    project_id TEXT NOT NULL,
    wbs_code TEXT NOT NULL,
    parent_wbs_code TEXT,
    control_account TEXT,
    discipline TEXT,
    area TEXT,
    contractor TEXT,
    progress_method TEXT,
    planned_quantity NUMERIC,
    installed_quantity NUMERIC,
    measurement_unit TEXT,
    planned_percent_complete NUMERIC,
    percent_complete NUMERIC,
    original_budget NUMERIC,
    approved_budget NUMERIC,
    actual_cost NUMERIC,
    forecast_remaining_cost NUMERIC,
    payment_readiness TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_rfi (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    project_id TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    subject TEXT,
    affected_wbs_code TEXT,
    required_by_date TEXT,
    schedule_impact_classification TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_submittal (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    project_id TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    linked_wbs_code TEXT,
    planned_submit_date TEXT,
    required_approval_date TEXT,
    approval_cycle_count INTEGER,
    blocked_work JSON,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_site_progress (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    project_id TEXT NOT NULL,
    work_package_id TEXT NOT NULL,
    submission_key TEXT NOT NULL,
    measurement_date TEXT NOT NULL,
    progress_method TEXT NOT NULL,
    installed_quantity NUMERIC,
    measurement_unit TEXT,
    percent_complete NUMERIC,
    accepted_status TEXT,
    evidence_bundle JSON,
    actual_cost_incurred NUMERIC,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_change_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    project_id TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    trend_reference TEXT,
    cause_category TEXT,
    affected_wbs_codes JSON,
    cost_impact NUMERIC,
    schedule_impact_days NUMERIC,
    approval_state TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_schedule_risk (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    project_id TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    work_package_id TEXT,
    current_float_days NUMERIC,
    prior_float_days NUMERIC,
    path_status TEXT,
    owner TEXT,
    issue_state TEXT,
    escalation_required BOOLEAN,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_construction_project_controls_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_construction_project_controls_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_construction_project_controls_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_construction_project_controls_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_construction_project_controls_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT,
    status TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT,
    code TEXT,
    status TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT,
    code TEXT,
    status TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE construction_project_controls_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant TEXT,
    code TEXT,
    status TEXT,
    payload JSON,
    created_at TEXT,
    updated_at TEXT
);

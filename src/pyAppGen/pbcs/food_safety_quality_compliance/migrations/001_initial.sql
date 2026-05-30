CREATE TABLE food_safety_quality_compliance_haccp_plan (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    plan_code TEXT NOT NULL,
    version TEXT NOT NULL,
    facility_code TEXT NOT NULL,
    product_scope JSON NOT NULL,
    lifecycle_state TEXT NOT NULL,
    process_steps JSON NOT NULL,
    hazard_analysis JSON NOT NULL,
    approvals JSON NOT NULL,
    effective_from TEXT,
    supersedes_plan_id TEXT,
    supersession_reason TEXT,
    evidence_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_critical_control_point (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    plan_id TEXT NOT NULL,
    process_step_code TEXT NOT NULL,
    hazard_id TEXT NOT NULL,
    limit_min REAL NOT NULL,
    limit_max REAL NOT NULL,
    unit TEXT NOT NULL,
    monitoring_method TEXT NOT NULL,
    monitoring_frequency_minutes INTEGER NOT NULL,
    responsible_role TEXT NOT NULL,
    verification_requirement TEXT NOT NULL,
    corrective_action TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_inspection (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    plan_id TEXT NOT NULL,
    plan_code TEXT NOT NULL,
    plan_version TEXT NOT NULL,
    facility_code TEXT NOT NULL,
    area TEXT NOT NULL,
    checklist JSON NOT NULL,
    findings JSON NOT NULL,
    score INTEGER NOT NULL,
    repeat_findings JSON NOT NULL,
    status TEXT NOT NULL,
    created_hold_ids JSON NOT NULL,
    created_nonconformance_ids JSON NOT NULL,
    inspector TEXT NOT NULL,
    started_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_nonconformance (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    category TEXT NOT NULL,
    severity TEXT NOT NULL,
    product_impact TEXT NOT NULL,
    process_step_code TEXT NOT NULL,
    containment_action TEXT NOT NULL,
    corrective_action TEXT NOT NULL,
    preventive_action TEXT NOT NULL,
    root_cause_method TEXT NOT NULL,
    confirmed_root_cause TEXT NOT NULL,
    effectiveness_evidence TEXT NOT NULL,
    recurrence_flag INTEGER NOT NULL,
    status TEXT NOT NULL,
    source_inspection_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_recall_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    classification TEXT NOT NULL,
    reason TEXT NOT NULL,
    consumer_risk TEXT NOT NULL,
    distribution_scope TEXT NOT NULL,
    affected_lots JSON NOT NULL,
    customers JSON NOT NULL,
    regulator_notification JSON NOT NULL,
    communication_plan JSON NOT NULL,
    is_mock_drill INTEGER NOT NULL,
    trace_elapsed_minutes INTEGER NOT NULL,
    projection_boundary_ok INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_supplier_audit (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    supplier_projection JSON NOT NULL,
    commodity TEXT NOT NULL,
    audit_type TEXT NOT NULL,
    risk_rating TEXT NOT NULL,
    findings JSON NOT NULL,
    corrective_actions JSON NOT NULL,
    approval_status TEXT NOT NULL,
    expiry_date TEXT NOT NULL,
    days_until_expiry INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_quality_hold (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    hold_reason TEXT NOT NULL,
    affected_lots JSON NOT NULL,
    quantity REAL NOT NULL,
    location TEXT NOT NULL,
    release_criteria JSON NOT NULL,
    disposition TEXT NOT NULL,
    approved_by JSON NOT NULL,
    released_at TEXT,
    source_inspection_id TEXT NOT NULL,
    haccp_plan_id TEXT NOT NULL,
    haccp_plan_version TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_food_safety_quality_compliance_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    rule_id TEXT NOT NULL,
    scope TEXT NOT NULL,
    status TEXT NOT NULL,
    rule_text TEXT NOT NULL,
    compiled_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_food_safety_quality_compliance_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_value REAL NOT NULL,
    unit TEXT NOT NULL,
    bounded INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_food_safety_quality_compliance_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    table_name TEXT NOT NULL,
    field_map JSON NOT NULL,
    rationale TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_food_safety_quality_compliance_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    control_id TEXT NOT NULL,
    control_name TEXT NOT NULL,
    frequency TEXT NOT NULL,
    status TEXT NOT NULL,
    assertion_payload JSON NOT NULL,
    evidence_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_food_safety_quality_compliance_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    artifact_key TEXT NOT NULL,
    status TEXT NOT NULL,
    document_digest TEXT NOT NULL,
    instruction_payload JSON NOT NULL,
    mutation_preview JSON NOT NULL,
    citations JSON NOT NULL,
    human_confirmation_state TEXT NOT NULL,
    approved_by TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE food_safety_quality_compliance_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    retry_policy JSON NOT NULL,
    created_at TEXT NOT NULL
);

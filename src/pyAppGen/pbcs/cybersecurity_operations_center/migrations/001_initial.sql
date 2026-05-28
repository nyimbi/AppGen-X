CREATE TABLE cybersecurity_operations_center_security_alert (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    confidence REAL NOT NULL,
    asset_ref TEXT NOT NULL,
    principal_ref TEXT NOT NULL,
    indicator_value TEXT NOT NULL,
    blast_radius TEXT NOT NULL,
    lane TEXT NOT NULL,
    previous_status TEXT,
    incident_id TEXT,
    duplicate_of TEXT,
    cluster_id TEXT,
    suppression JSON,
    false_positive JSON,
    detection_context JSON NOT NULL,
    enrichment JSON,
    evidence_ids JSON,
    lineage JSON,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_security_incident (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    title TEXT NOT NULL,
    severity TEXT NOT NULL,
    explainable_score REAL NOT NULL,
    commander TEXT,
    communications_owner TEXT,
    evidence_owner TEXT,
    containment_owner TEXT,
    promotion_summary JSON,
    alert_ids JSON,
    evidence_ids JSON,
    containment_action_ids JSON,
    timeline JSON,
    closure_checklist JSON,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_asset_exposure (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    asset_ref TEXT NOT NULL,
    criticality TEXT NOT NULL,
    internet_exposed BOOLEAN NOT NULL,
    open_alert_ids JSON,
    open_incident_ids JSON,
    containment_action_ids JSON,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_threat_intel (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    indicator_value TEXT NOT NULL,
    observed_fact JSON,
    assessed_relationship JSON,
    campaign_context JSON,
    analyst_inference JSON,
    confidence REAL NOT NULL,
    expires_at TEXT,
    source_provenance TEXT,
    recommendation_preview JSON,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_playbook_run (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    template_name TEXT NOT NULL,
    stage TEXT NOT NULL,
    checkpoint_statuses JSON,
    breakpoint_required BOOLEAN NOT NULL,
    requires_human_confirmation BOOLEAN NOT NULL,
    related_incident_id TEXT,
    related_alert_id TEXT,
    notes JSON,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_containment_action (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    incident_id TEXT,
    alert_id TEXT,
    action_type TEXT NOT NULL,
    approval_path TEXT NOT NULL,
    approved_by TEXT,
    risk_level TEXT NOT NULL,
    rollback_instructions TEXT,
    outcome_summary TEXT,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_response_evidence (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    case_id TEXT NOT NULL,
    source_system TEXT NOT NULL,
    checksum TEXT NOT NULL,
    acquired_at TEXT NOT NULL,
    storage_reference TEXT NOT NULL,
    redaction_status TEXT NOT NULL,
    admissibility_notes TEXT,
    handling_history JSON,
    request_status TEXT NOT NULL,
    sealed_bundle_id TEXT,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_cybersecurity_operations_center_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    policy JSON NOT NULL,
    simulation_preview JSON,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_cybersecurity_operations_center_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    value TEXT NOT NULL,
    minimum REAL,
    maximum REAL,
    rationale TEXT,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_cybersecurity_operations_center_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    target_table TEXT NOT NULL,
    fields JSON NOT NULL,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_cybersecurity_operations_center_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    control_name TEXT NOT NULL,
    control_status TEXT NOT NULL,
    evidence JSON,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_cybersecurity_operations_center_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    model_name TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    guardrails JSON NOT NULL,
    created_at TEXT,
    updated_at TEXT,
    version INTEGER
);

CREATE TABLE cybersecurity_operations_center_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    payload JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    created_at TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE cybersecurity_operations_center_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    created_at TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE cybersecurity_operations_center_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    created_at TEXT NOT NULL,
    status TEXT NOT NULL,
    failure_reason TEXT NOT NULL,
    retry_policy JSON NOT NULL
);

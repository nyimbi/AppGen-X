CREATE TABLE chemical_batch_compliance_chemical_formula (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    formula_code TEXT NOT NULL,
    revision TEXT NOT NULL,
    lifecycle_state TEXT NOT NULL,
    product_name TEXT NOT NULL,
    target_concentration JSON NOT NULL,
    composition_window JSON NOT NULL,
    approved_substitutes JSON,
    required_sds_ids JSON,
    required_hazard_material_ids JSON,
    required_permits JSON,
    equipment_classes JSON,
    approvals JSON,
    effectivity_start TEXT NOT NULL,
    effectivity_end TEXT,
    process_steps JSON,
    evidence_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_batch_record (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    batch_number TEXT NOT NULL,
    formula_id TEXT NOT NULL,
    formula_revision TEXT NOT NULL,
    lifecycle_state TEXT NOT NULL,
    equipment_profile JSON NOT NULL,
    step_timeline JSON NOT NULL,
    dispense_reconciliation JSON NOT NULL,
    parameter_log JSON NOT NULL,
    sampling_plan JSON,
    deviation_summary JSON,
    release_decision TEXT NOT NULL,
    risk_score NUMERIC NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_sds_document (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    material_code TEXT NOT NULL,
    revision TEXT NOT NULL,
    status TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    expiration_date TEXT NOT NULL,
    jurisdictions JSON,
    hazard_summary JSON,
    exposure_controls JSON,
    document_digest TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_hazardous_material (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    material_code TEXT NOT NULL,
    status TEXT NOT NULL,
    un_number TEXT,
    ghs_classification JSON NOT NULL,
    storage_class TEXT,
    approved_sources JSON,
    ppe_requirements JSON,
    label_profile JSON,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_regulatory_submission (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    dossier_number TEXT NOT NULL,
    status TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    submission_type TEXT NOT NULL,
    product_code TEXT NOT NULL,
    source_record_ids JSON,
    commitment_actions JSON,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_quality_test (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    batch_id TEXT NOT NULL,
    sample_point TEXT NOT NULL,
    test_name TEXT NOT NULL,
    specification JSON NOT NULL,
    result_value TEXT,
    result_status TEXT NOT NULL,
    requires_hold BOOLEAN NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_compliance_hold (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    hold_reason TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    disposition TEXT NOT NULL,
    released_by TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_chemical_batch_compliance_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    rule_id TEXT NOT NULL,
    status TEXT NOT NULL,
    scope TEXT NOT NULL,
    rule_kind TEXT NOT NULL,
    threshold_json JSON,
    compiled_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_chemical_batch_compliance_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_value TEXT NOT NULL,
    unit TEXT NOT NULL,
    bounded BOOLEAN NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_chemical_batch_compliance_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    table_name TEXT NOT NULL,
    status TEXT NOT NULL,
    field_map JSON NOT NULL,
    rationale TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_chemical_batch_compliance_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    control_id TEXT NOT NULL,
    control_name TEXT NOT NULL,
    status TEXT NOT NULL,
    frequency TEXT NOT NULL,
    assertion_payload JSON,
    evidence_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_chemical_batch_compliance_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    artifact_key TEXT NOT NULL,
    status TEXT NOT NULL,
    document_digest TEXT NOT NULL,
    instruction_payload JSON NOT NULL,
    mutation_preview JSON NOT NULL,
    human_confirmation_state TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE chemical_batch_compliance_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload JSON NOT NULL,
    idempotency_key TEXT NOT NULL,
    retry_policy JSON NOT NULL,
    created_at TEXT NOT NULL
);

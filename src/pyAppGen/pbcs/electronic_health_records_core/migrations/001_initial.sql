CREATE TABLE electronic_health_records_core_patient_chart (
    chart_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    patient_ref TEXT NOT NULL,
    chart_number TEXT,
    legal_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL,
    national_id TEXT,
    state TEXT NOT NULL,
    identity_confidence REAL,
    duplicate_candidate_chart_ids JSON,
    merge_review_required BOOLEAN,
    merge_decision JSON,
    source_system TEXT,
    source_lineage JSON,
    active_problem_list JSON,
    sensitive_flags JSON,
    consent_scope JSON,
    version INTEGER NOT NULL
);

CREATE TABLE electronic_health_records_core_clinical_encounter (
    encounter_id TEXT PRIMARY KEY,
    chart_id TEXT NOT NULL,
    encounter_class TEXT NOT NULL,
    care_setting TEXT NOT NULL,
    modality TEXT NOT NULL,
    attending_role TEXT NOT NULL,
    service_line TEXT,
    started_at TEXT NOT NULL,
    discharged_at TEXT,
    external_source TEXT,
    documentation_checklist JSON,
    documentation_complete BOOLEAN,
    missing_documentation JSON,
    status TEXT NOT NULL,
    version INTEGER NOT NULL
);

CREATE TABLE electronic_health_records_core_clinical_order (
    order_id TEXT PRIMARY KEY,
    chart_id TEXT NOT NULL,
    order_type TEXT NOT NULL,
    priority TEXT NOT NULL,
    ordering_clinician TEXT NOT NULL,
    indication TEXT NOT NULL,
    status TEXT NOT NULL,
    requires_result_evidence BOOLEAN,
    medication_substance TEXT,
    scheduling_dependency TEXT,
    result_expectation TEXT,
    result_evidence JSON,
    cancellation_reason TEXT,
    discontinuation_authority TEXT,
    allergy_warnings JSON,
    version INTEGER NOT NULL
);

CREATE TABLE electronic_health_records_core_observation (
    observation_id TEXT PRIMARY KEY,
    chart_id TEXT NOT NULL,
    observation_code TEXT NOT NULL,
    value TEXT NOT NULL,
    unit TEXT NOT NULL,
    method TEXT,
    specimen_type TEXT,
    collected_at TEXT NOT NULL,
    resulted_at TEXT,
    reference_range JSON,
    abnormal_flag BOOLEAN,
    critical_flag BOOLEAN,
    performer TEXT,
    corrected_result_of TEXT,
    acknowledgement_state TEXT,
    acknowledgement_owner TEXT,
    acknowledgement_deadline TEXT,
    read_back_evidence TEXT,
    version INTEGER NOT NULL
);

CREATE TABLE electronic_health_records_core_allergy (
    allergy_id TEXT PRIMARY KEY,
    chart_id TEXT NOT NULL,
    substance_class TEXT,
    specific_substance TEXT NOT NULL,
    reaction TEXT NOT NULL,
    severity TEXT NOT NULL,
    onset TEXT,
    verification_status TEXT,
    source TEXT,
    inactive_reason TEXT,
    clinical_override_guidance TEXT,
    duplicate_candidate_ids JSON,
    status TEXT NOT NULL,
    version INTEGER NOT NULL
);

CREATE TABLE electronic_health_records_core_medication_list (
    medication_list_id TEXT PRIMARY KEY,
    chart_id TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    source_list JSON,
    patient_reported_list JSON,
    reconciliation_actions JSON,
    discrepancies JSON,
    unresolved_discrepancy_count INTEGER,
    status TEXT NOT NULL,
    version INTEGER NOT NULL
);

CREATE TABLE electronic_health_records_core_care_note (
    note_id TEXT PRIMARY KEY,
    chart_id TEXT NOT NULL,
    note_type TEXT NOT NULL,
    author_ref TEXT NOT NULL,
    contributors JSON,
    supervising_signer TEXT,
    co_signature_required BOOLEAN,
    attestation_status TEXT NOT NULL,
    note_text TEXT NOT NULL,
    amends_note_id TEXT,
    correction_reason TEXT,
    late_entry_marker BOOLEAN,
    source_evidence JSON,
    signed_by TEXT,
    signed_role TEXT,
    signed_at TEXT,
    version INTEGER NOT NULL
);

CREATE TABLE electronic_health_records_core_electronic_health_records_core_policy_rule (
    rule_id TEXT PRIMARY KEY,
    scope TEXT,
    severity TEXT,
    compiled_hash TEXT,
    payload JSON
);

CREATE TABLE electronic_health_records_core_electronic_health_records_core_runtime_parameter (
    name TEXT PRIMARY KEY,
    value TEXT,
    bounds JSON,
    scope TEXT
);

CREATE TABLE electronic_health_records_core_electronic_health_records_core_schema_extension (
    table_name TEXT PRIMARY KEY,
    fields JSON,
    approved_by TEXT
);

CREATE TABLE electronic_health_records_core_electronic_health_records_core_control_assertion (
    assertion_id TEXT PRIMARY KEY,
    assertion_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    subject_table TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    details JSON,
    queue TEXT,
    status TEXT NOT NULL
);

CREATE TABLE electronic_health_records_core_electronic_health_records_core_governed_model (
    model_id TEXT PRIMARY KEY,
    purpose TEXT,
    approval_status TEXT,
    evidence_hash TEXT
);

CREATE TABLE electronic_health_records_core_appgen_outbox_event (
    idempotency_key TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE electronic_health_records_core_appgen_inbox_event (
    idempotency_key TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    payload JSON NOT NULL
);

CREATE TABLE electronic_health_records_core_appgen_dead_letter_event (
    idempotency_key TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    payload JSON NOT NULL,
    retry_policy JSON
);

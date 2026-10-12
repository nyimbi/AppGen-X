CREATE SCHEMA IF NOT EXISTS electronic_health_records_core;

CREATE TABLE electronic_health_records_core_patient_chart (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  patient_chart_id VARCHAR(255) NOT NULL,
  patient_reference VARCHAR(255) NOT NULL,
  chart_name VARCHAR(255) NOT NULL,
  identity_confidence DECIMAL(18, 4) NOT NULL,
  duplicate_candidate_flag BOOLEAN NOT NULL,
  provisional_state VARCHAR(255) NOT NULL,
  merge_recommendation VARCHAR(255) NOT NULL,
  merge_rejection_reason TEXT,
  source_system_lineage VARCHAR(255) NOT NULL,
  problem_summary TEXT,
  risk_flags VARCHAR(255) NOT NULL,
  chart_completeness_score DECIMAL(18, 4) NOT NULL,
  retention_category VARCHAR(255) NOT NULL,
  legal_hold_flag BOOLEAN NOT NULL,
  amendment_chain VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
,
  UNIQUE (patient_chart_id));

CREATE TABLE electronic_health_records_core_clinical_encounter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  clinical_encounter_id VARCHAR(255) NOT NULL,
  patient_chart_id VARCHAR(255) NOT NULL,
  encounter_class VARCHAR(255) NOT NULL,
  care_setting VARCHAR(255) NOT NULL,
  visit_modality VARCHAR(255) NOT NULL,
  attending_role VARCHAR(255) NOT NULL,
  service_line VARCHAR(255) NOT NULL,
  arrival_at TIMESTAMP,
  discharge_at TIMESTAMP,
  external_source VARCHAR(255) NOT NULL,
  documentation_checklist TEXT,
  encounter_note TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (patient_chart_id) REFERENCES electronic_health_records_core_patient_chart(patient_chart_id)
,
  UNIQUE (clinical_encounter_id));

CREATE TABLE electronic_health_records_core_clinical_order (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  clinical_order_id VARCHAR(255) NOT NULL,
  clinical_encounter_id VARCHAR(255) NOT NULL,
  order_type VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  ordering_clinician VARCHAR(255) NOT NULL,
  indication TEXT,
  specimen_detail VARCHAR(255) NOT NULL,
  scheduling_dependency VARCHAR(255) NOT NULL,
  result_expectation VARCHAR(255) NOT NULL,
  order_set_template VARCHAR(255) NOT NULL,
  order_set_version VARCHAR(255) NOT NULL,
  cancellation_reason TEXT,
  discontinuation_authority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (clinical_encounter_id) REFERENCES electronic_health_records_core_clinical_encounter(clinical_encounter_id)
);

CREATE TABLE electronic_health_records_core_observation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  observation_id VARCHAR(255) NOT NULL,
  patient_chart_id VARCHAR(255) NOT NULL,
  clinical_encounter_id VARCHAR(255),
  observation_code VARCHAR(255) NOT NULL,
  observation_value DECIMAL(18, 4) NOT NULL,
  unit VARCHAR(255) NOT NULL,
  method VARCHAR(255) NOT NULL,
  specimen_type VARCHAR(255) NOT NULL,
  collection_at TIMESTAMP,
  result_at TIMESTAMP,
  reference_range VARCHAR(255) NOT NULL,
  abnormal_flag BOOLEAN NOT NULL,
  critical_flag BOOLEAN NOT NULL,
  performer VARCHAR(255) NOT NULL,
  corrected_result_lineage VARCHAR(255) NOT NULL,
  acknowledgement_owner VARCHAR(255) NOT NULL,
  acknowledgement_deadline TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (patient_chart_id) REFERENCES electronic_health_records_core_patient_chart(patient_chart_id),
  FOREIGN KEY (clinical_encounter_id) REFERENCES electronic_health_records_core_clinical_encounter(clinical_encounter_id)
);

CREATE TABLE electronic_health_records_core_allergy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  allergy_id VARCHAR(255) NOT NULL,
  patient_chart_id VARCHAR(255) NOT NULL,
  substance_class VARCHAR(255) NOT NULL,
  specific_substance VARCHAR(255) NOT NULL,
  reaction TEXT,
  severity VARCHAR(255) NOT NULL,
  onset_at TIMESTAMP,
  verification_status VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  inactive_reason TEXT,
  override_guidance TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (patient_chart_id) REFERENCES electronic_health_records_core_patient_chart(patient_chart_id)
);

CREATE TABLE electronic_health_records_core_medication_list (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  medication_list_id VARCHAR(255) NOT NULL,
  patient_chart_id VARCHAR(255) NOT NULL,
  medication_name VARCHAR(255) NOT NULL,
  source_list VARCHAR(255) NOT NULL,
  patient_reported BOOLEAN NOT NULL,
  reconciliation_action VARCHAR(255) NOT NULL,
  discrepancy_reason TEXT,
  reviewer VARCHAR(255) NOT NULL,
  unresolved_discrepancy BOOLEAN NOT NULL,
  dose_amount DECIMAL(18, 4) NOT NULL,
  dose_unit VARCHAR(255) NOT NULL,
  route VARCHAR(255) NOT NULL,
  started_at TIMESTAMP,
  stopped_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (patient_chart_id) REFERENCES electronic_health_records_core_patient_chart(patient_chart_id)
);

CREATE TABLE electronic_health_records_core_care_note (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  care_note_id VARCHAR(255) NOT NULL,
  patient_chart_id VARCHAR(255) NOT NULL,
  clinical_encounter_id VARCHAR(255),
  note_author VARCHAR(255) NOT NULL,
  contributor VARCHAR(255) NOT NULL,
  supervising_signer VARCHAR(255) NOT NULL,
  attestation_status VARCHAR(255) NOT NULL,
  co_signature_required BOOLEAN NOT NULL,
  addendum_chain VARCHAR(255) NOT NULL,
  correction_reason TEXT,
  late_entry_flag BOOLEAN NOT NULL,
  note_text TEXT,
  source_evidence TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (patient_chart_id) REFERENCES electronic_health_records_core_patient_chart(patient_chart_id),
  FOREIGN KEY (clinical_encounter_id) REFERENCES electronic_health_records_core_clinical_encounter(clinical_encounter_id)
);

CREATE TABLE electronic_health_records_core_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT,
  ambiguity_flag BOOLEAN NOT NULL,
  approver_role VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE electronic_health_records_core_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value DECIMAL(18, 4) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  effective_from TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE electronic_health_records_core_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) NOT NULL,
  target_table VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  validation_rule TEXT,
  ui_placement VARCHAR(255) NOT NULL,
  migration_evidence TEXT,
  registered_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE electronic_health_records_core_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  assertion_result VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  remediation_task TEXT,
  evaluated_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE electronic_health_records_core_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  intended_use VARCHAR(255) NOT NULL,
  evaluation_cohort VARCHAR(255) NOT NULL,
  confidence_threshold DECIMAL(18, 4) NOT NULL,
  governance_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE electronic_health_records_core_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE electronic_health_records_core_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE electronic_health_records_core_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

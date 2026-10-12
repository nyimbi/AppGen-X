CREATE SCHEMA IF NOT EXISTS clinical_care_coordination;

CREATE TABLE clinical_care_coordination_patient_care_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  patient_care_plan_id VARCHAR(255) NOT NULL,
  patient_id VARCHAR(255) NOT NULL,
  plan_title VARCHAR(255) NOT NULL,
  care_setting VARCHAR(255) NOT NULL,
  problem_reference VARCHAR(255) NOT NULL,
  goal_hierarchy VARCHAR(255) NOT NULL,
  planned_intervention TEXT NOT NULL,
  responsible_discipline VARCHAR(255) NOT NULL,
  patient_preference TEXT NOT NULL,
  preferred_language VARCHAR(255) NOT NULL,
  target_date TIMESTAMP,
  review_cadence VARCHAR(255) NOT NULL,
  barrier_summary TEXT NOT NULL,
  variance_reason VARCHAR(255) NOT NULL,
  closure_reason VARCHAR(255),
  plan_state VARCHAR(255) NOT NULL,
  risk_tier VARCHAR(255) NOT NULL,
  last_reviewed_at TIMESTAMP,
  legal_hold BOOLEAN NOT NULL,
  retention_category VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE clinical_care_coordination_care_team (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  care_team_id VARCHAR(255) NOT NULL,
  patient_id VARCHAR(255) NOT NULL,
  participant_name VARCHAR(255) NOT NULL,
  participant_role VARCHAR(255) NOT NULL,
  clinical_authority VARCHAR(255) NOT NULL,
  communication_channel VARCHAR(255) NOT NULL,
  consent_scope VARCHAR(255) NOT NULL,
  coverage_start TIMESTAMP,
  coverage_end TIMESTAMP,
  backup_contact VARCHAR(255) NOT NULL,
  escalation_route VARCHAR(255) NOT NULL,
  protected_detail_access BOOLEAN NOT NULL,
  active_member BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE clinical_care_coordination_referral (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  referral_id VARCHAR(255) NOT NULL,
  patient_id VARCHAR(255) NOT NULL,
  patient_care_plan_id VARCHAR(255) NOT NULL,
  specialty VARCHAR(255) NOT NULL,
  urgency VARCHAR(255) NOT NULL,
  referral_reason TEXT NOT NULL,
  receiving_organization VARCHAR(255) NOT NULL,
  expected_turnaround_hours INTEGER NOT NULL,
  authorization_evidence VARCHAR(255) NOT NULL,
  appointment_at TIMESTAMP,
  result_document_pointer VARCHAR(255),
  closure_accountability VARCHAR(255) NOT NULL,
  referral_state VARCHAR(255) NOT NULL,
  priority_reason VARCHAR(255) NOT NULL,
  sent_at TIMESTAMP,
  result_received_at TIMESTAMP,
  reconciled_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (patient_care_plan_id) REFERENCES clinical_care_coordination_patient_care_plan(patient_care_plan_id)
);

CREATE TABLE clinical_care_coordination_encounter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  encounter_id VARCHAR(255) NOT NULL,
  patient_id VARCHAR(255) NOT NULL,
  patient_care_plan_id VARCHAR(255),
  encounter_type VARCHAR(255) NOT NULL,
  encounter_at TIMESTAMP NOT NULL,
  source_note_span VARCHAR(255) NOT NULL,
  clinical_priority VARCHAR(255) NOT NULL,
  follow_up_required BOOLEAN NOT NULL,
  task_count INTEGER NOT NULL,
  responsible_role VARCHAR(255) NOT NULL,
  outreach_required BOOLEAN NOT NULL,
  discharge_disposition VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (patient_care_plan_id) REFERENCES clinical_care_coordination_patient_care_plan(patient_care_plan_id)
);

CREATE TABLE clinical_care_coordination_care_gap (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  care_gap_id VARCHAR(255) NOT NULL,
  patient_id VARCHAR(255) NOT NULL,
  patient_care_plan_id VARCHAR(255),
  gap_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  gap_source VARCHAR(255) NOT NULL,
  guideline_basis VARCHAR(255) NOT NULL,
  guideline_version VARCHAR(255) NOT NULL,
  denominator_eligible BOOLEAN NOT NULL,
  exclusion_reason VARCHAR(255),
  exclusion_expires_at TIMESTAMP,
  closure_evidence VARCHAR(255),
  gap_state VARCHAR(255) NOT NULL,
  detected_at TIMESTAMP NOT NULL,
  closed_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (patient_care_plan_id) REFERENCES clinical_care_coordination_patient_care_plan(patient_care_plan_id)
);

CREATE TABLE clinical_care_coordination_transition_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  transition_plan_id VARCHAR(255) NOT NULL,
  patient_id VARCHAR(255) NOT NULL,
  patient_care_plan_id VARCHAR(255) NOT NULL,
  discharge_source VARCHAR(255) NOT NULL,
  receiving_setting VARCHAR(255) NOT NULL,
  medication_reconciliation_status VARCHAR(255) NOT NULL,
  pending_test_results TEXT NOT NULL,
  follow_up_appointment_at TIMESTAMP,
  durable_equipment VARCHAR(255) NOT NULL,
  home_services VARCHAR(255) NOT NULL,
  patient_instructions TEXT NOT NULL,
  caregiver_confirmation BOOLEAN NOT NULL,
  transportation_plan VARCHAR(255) NOT NULL,
  readmission_risk VARCHAR(255) NOT NULL,
  packet_completeness_score DECIMAL(18, 4) NOT NULL,
  readiness_checklist TEXT NOT NULL,
  watchlist_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (patient_care_plan_id) REFERENCES clinical_care_coordination_patient_care_plan(patient_care_plan_id)
);

CREATE TABLE clinical_care_coordination_outcome_measure (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  outcome_measure_id VARCHAR(255) NOT NULL,
  patient_id VARCHAR(255) NOT NULL,
  patient_care_plan_id VARCHAR(255) NOT NULL,
  measure_name VARCHAR(255) NOT NULL,
  measure_owner VARCHAR(255) NOT NULL,
  measure_unit VARCHAR(255) NOT NULL,
  baseline_value DECIMAL(18, 4) NOT NULL,
  target_value DECIMAL(18, 4) NOT NULL,
  current_value DECIMAL(18, 4) NOT NULL,
  collection_cadence VARCHAR(255) NOT NULL,
  measure_source VARCHAR(255) NOT NULL,
  numerator INTEGER NOT NULL,
  denominator INTEGER NOT NULL,
  patient_reported BOOLEAN NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  trend_classification VARCHAR(255) NOT NULL,
  measured_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (patient_care_plan_id) REFERENCES clinical_care_coordination_patient_care_plan(patient_care_plan_id)
);

CREATE TABLE clinical_care_coordination_clinical_care_coordination_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
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

CREATE TABLE clinical_care_coordination_clinical_care_coordination_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  effective_from TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE clinical_care_coordination_clinical_care_coordination_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) NOT NULL,
  target_table VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  registered_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE clinical_care_coordination_clinical_care_coordination_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  assertion_result VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  remediation_task VARCHAR(255) NOT NULL,
  evaluated_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE clinical_care_coordination_clinical_care_coordination_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  governance_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE clinical_care_coordination_appgen_outbox_event (
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

CREATE TABLE clinical_care_coordination_appgen_inbox_event (
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

CREATE TABLE clinical_care_coordination_appgen_dead_letter_event (
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

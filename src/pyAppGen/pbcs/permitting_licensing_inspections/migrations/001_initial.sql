CREATE SCHEMA IF NOT EXISTS permitting_licensing_inspections;

CREATE TABLE permitting_licensing_inspections_application (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  application_id VARCHAR(255) NOT NULL,
  application_type VARCHAR(255) NOT NULL,
  applicant_name VARCHAR(255) NOT NULL,
  applicant_party_role VARCHAR(255) NOT NULL,
  parcel_identifier VARCHAR(255) NOT NULL,
  site_address VARCHAR(255) NOT NULL,
  zoning_district VARCHAR(255) NOT NULL,
  consultation_reference VARCHAR(255),
  completeness_state VARCHAR(255) NOT NULL,
  intake_channel VARCHAR(255) NOT NULL,
  preferred_language VARCHAR(255),
  hearing_required BOOLEAN NOT NULL,
  public_notice_required BOOLEAN NOT NULL,
  submitted_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE permitting_licensing_inspections_permit (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  permit_id VARCHAR(255) NOT NULL,
  application_id VARCHAR(255) NOT NULL,
  permit_number VARCHAR(255) NOT NULL,
  permit_type VARCHAR(255) NOT NULL,
  issuance_readiness_state VARCHAR(255) NOT NULL,
  temporary_permit BOOLEAN NOT NULL,
  term_limit_days INTEGER NOT NULL,
  condition_count INTEGER NOT NULL,
  supersedes_permit_id VARCHAR(255),
  issued_at TIMESTAMP,
  expires_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (application_id) REFERENCES permitting_licensing_inspections_application(application_id)
);

CREATE TABLE permitting_licensing_inspections_license (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  license_id VARCHAR(255) NOT NULL,
  application_id VARCHAR(255) NOT NULL,
  license_number VARCHAR(255) NOT NULL,
  license_class VARCHAR(255) NOT NULL,
  qualified_activities TEXT NOT NULL,
  allowed_locations TEXT NOT NULL,
  occupancy_limit INTEGER NOT NULL,
  operating_conditions TEXT NOT NULL,
  provisional_license BOOLEAN NOT NULL,
  renewal_state VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (application_id) REFERENCES permitting_licensing_inspections_application(application_id)
);

CREATE TABLE permitting_licensing_inspections_review_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  review_task_id VARCHAR(255) NOT NULL,
  application_id VARCHAR(255) NOT NULL,
  discipline VARCHAR(255) NOT NULL,
  review_mode VARCHAR(255) NOT NULL,
  reviewer_identity VARCHAR(255) NOT NULL,
  lead_reviewer_identity VARCHAR(255),
  dependency_task_id VARCHAR(255),
  plan_set_version VARCHAR(255),
  correction_round INTEGER NOT NULL,
  referral_scope TEXT,
  sla_state VARCHAR(255) NOT NULL,
  due_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (application_id) REFERENCES permitting_licensing_inspections_application(application_id)
);

CREATE TABLE permitting_licensing_inspections_fee_assessment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  fee_assessment_id VARCHAR(255) NOT NULL,
  application_id VARCHAR(255) NOT NULL,
  fee_schedule_reference VARCHAR(255) NOT NULL,
  assessment_basis TEXT NOT NULL,
  assessed_amount DECIMAL(18, 4) NOT NULL,
  waiver_amount DECIMAL(18, 4) NOT NULL,
  credit_amount DECIMAL(18, 4) NOT NULL,
  refund_eligible BOOLEAN NOT NULL,
  payment_status VARCHAR(255) NOT NULL,
  payment_confirmed_at TIMESTAMP,
  effective_from TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (application_id) REFERENCES permitting_licensing_inspections_application(application_id)
);

CREATE TABLE permitting_licensing_inspections_inspection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  inspection_id VARCHAR(255) NOT NULL,
  permit_id VARCHAR(255) NOT NULL,
  inspection_type VARCHAR(255) NOT NULL,
  inspection_route VARCHAR(255),
  inspector_identity VARCHAR(255) NOT NULL,
  outcome VARCHAR(255) NOT NULL,
  reinspection_required BOOLEAN NOT NULL,
  reinspection_of_inspection_id VARCHAR(255),
  evidence_capture_state VARCHAR(255) NOT NULL,
  geolocation VARCHAR(255),
  offline_captured BOOLEAN NOT NULL,
  scheduled_window_start TIMESTAMP,
  scheduled_window_end TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (permit_id) REFERENCES permitting_licensing_inspections_permit(permit_id)
);

CREATE TABLE permitting_licensing_inspections_violation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  violation_id VARCHAR(255) NOT NULL,
  inspection_id VARCHAR(255) NOT NULL,
  violation_taxonomy VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  imminence VARCHAR(255) NOT NULL,
  recurrence_count INTEGER NOT NULL,
  remedy_type VARCHAR(255) NOT NULL,
  enforcement_step VARCHAR(255) NOT NULL,
  escalation_authority VARCHAR(255) NOT NULL,
  stop_work_issued BOOLEAN NOT NULL,
  notice_served_at TIMESTAMP,
  cure_deadline_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (inspection_id) REFERENCES permitting_licensing_inspections_inspection(inspection_id)
);

CREATE TABLE permitting_licensing_inspections_permitting_licensing_inspections_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_rule_id VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  jurisdiction_scope VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE permitting_licensing_inspections_permitting_licensing_inspections_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  runtime_parameter_id VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE permitting_licensing_inspections_permitting_licensing_inspections_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schema_extension_id VARCHAR(255) NOT NULL,
  target_table VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  registered_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE permitting_licensing_inspections_permitting_licensing_inspections_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  control_assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  assertion_result VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  remediation_task VARCHAR(255),
  evaluated_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE permitting_licensing_inspections_permitting_licensing_inspections_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  governed_model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  governance_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255),
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE permitting_licensing_inspections_appgen_outbox_event (
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

CREATE TABLE permitting_licensing_inspections_appgen_inbox_event (
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

CREATE TABLE permitting_licensing_inspections_appgen_dead_letter_event (
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

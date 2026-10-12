CREATE SCHEMA IF NOT EXISTS land_real_estate_development;

CREATE TABLE land_real_estate_development_land_parcel (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  land_parcel_id VARCHAR(255) NOT NULL,
  parcel_number VARCHAR(255) NOT NULL,
  assessor_parcel_number VARCHAR(255),
  parcel_alias VARCHAR(255),
  recorder_reference VARCHAR(255),
  legal_description TEXT NOT NULL,
  survey_revision VARCHAR(255),
  gross_acreage DECIMAL(18, 4) NOT NULL,
  constrained_acreage DECIMAL(18, 4),
  dedication_acreage DECIMAL(18, 4),
  net_buildable_acreage DECIMAL(18, 4),
  source_of_truth_rank INTEGER NOT NULL,
  title_status VARCHAR(255) NOT NULL,
  environmental_stage VARCHAR(255) NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
,
  UNIQUE (land_parcel_id));

CREATE TABLE land_real_estate_development_zoning_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  zoning_case_id VARCHAR(255) NOT NULL,
  land_parcel_id VARCHAR(255) NOT NULL,
  zoning_district VARCHAR(255) NOT NULL,
  overlay_district VARCHAR(255),
  permitted_use_category VARCHAR(255) NOT NULL,
  density_limit DECIMAL(18, 4),
  height_envelope DECIMAL(18, 4),
  setback_standard VARCHAR(255),
  parking_ratio DECIMAL(18, 4),
  open_space_requirement DECIMAL(18, 4),
  ordinance_citation VARCHAR(255),
  hearing_cadence VARCHAR(255),
  notice_lead_days INTEGER,
  opposition_risk_score DECIMAL(18, 4),
  case_disposition VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (land_parcel_id) REFERENCES land_real_estate_development_land_parcel(land_parcel_id)
,
  UNIQUE (zoning_case_id));

CREATE TABLE land_real_estate_development_entitlement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  entitlement_id VARCHAR(255) NOT NULL,
  zoning_case_id VARCHAR(255) NOT NULL,
  entitlement_type VARCHAR(255) NOT NULL,
  approval_path VARCHAR(255) NOT NULL,
  prerequisite_entitlement_id VARCHAR(255),
  agency_name VARCHAR(255) NOT NULL,
  map_type VARCHAR(255),
  recording_status VARCHAR(255),
  appeal_deadline TIMESTAMP,
  effective_from TIMESTAMP,
  expiry_date TIMESTAMP,
  condition_summary TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (zoning_case_id) REFERENCES land_real_estate_development_zoning_case(zoning_case_id)
,
  UNIQUE (entitlement_id));

CREATE TABLE land_real_estate_development_feasibility_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  feasibility_model_id VARCHAR(255) NOT NULL,
  land_parcel_id VARCHAR(255) NOT NULL,
  scenario_name VARCHAR(255) NOT NULL,
  program_mix VARCHAR(255) NOT NULL,
  density_assumption DECIMAL(18, 4),
  residual_land_value DECIMAL(18, 4),
  seller_asking_price DECIMAL(18, 4),
  hard_cost_total DECIMAL(18, 4),
  soft_cost_total DECIMAL(18, 4),
  infrastructure_cost DECIMAL(18, 4),
  developer_margin_pct DECIMAL(18, 4),
  absorption_rate DECIMAL(18, 4),
  hurdle_rate DECIMAL(18, 4),
  is_baseline BOOLEAN NOT NULL,
  assumption_confidence VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (land_parcel_id) REFERENCES land_real_estate_development_land_parcel(land_parcel_id)
);

CREATE TABLE land_real_estate_development_permit_application (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  permit_application_id VARCHAR(255) NOT NULL,
  entitlement_id VARCHAR(255) NOT NULL,
  permit_type VARCHAR(255) NOT NULL,
  issuing_agency VARCHAR(255) NOT NULL,
  drawing_set_version VARCHAR(255),
  completeness_score DECIMAL(18, 4),
  open_comment_count INTEGER NOT NULL,
  highest_comment_severity VARCHAR(255),
  submittal_stage VARCHAR(255) NOT NULL,
  agency_comment_due TIMESTAMP,
  issued_at TIMESTAMP,
  expires_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (entitlement_id) REFERENCES land_real_estate_development_entitlement(entitlement_id)
,
  UNIQUE (permit_application_id));

CREATE TABLE land_real_estate_development_development_milestone (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  development_milestone_id VARCHAR(255) NOT NULL,
  permit_application_id VARCHAR(255),
  milestone_name VARCHAR(255) NOT NULL,
  milestone_type VARCHAR(255) NOT NULL,
  predecessor_milestone_id VARCHAR(255),
  long_lead_flag BOOLEAN NOT NULL,
  critical_path_flag BOOLEAN NOT NULL,
  float_days INTEGER,
  planned_date TIMESTAMP,
  forecast_date TIMESTAMP,
  completed_at TIMESTAMP,
  handoff_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (permit_application_id) REFERENCES land_real_estate_development_permit_application(permit_application_id)
);

CREATE TABLE land_real_estate_development_land_option (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  land_option_id VARCHAR(255) NOT NULL,
  land_parcel_id VARCHAR(255) NOT NULL,
  option_tier VARCHAR(255) NOT NULL,
  option_premium DECIMAL(18, 4),
  deposit_amount DECIMAL(18, 4),
  exercise_deadline TIMESTAMP,
  extension_rights VARCHAR(255),
  extension_payment DECIMAL(18, 4),
  cure_window_days INTEGER,
  notice_address VARCHAR(255),
  is_refundable BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (land_parcel_id) REFERENCES land_real_estate_development_land_parcel(land_parcel_id)
);

CREATE TABLE land_real_estate_development_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  rule_scope VARCHAR(255) NOT NULL,
  ambiguity_flag BOOLEAN NOT NULL,
  approver_role VARCHAR(255),
  effective_from TIMESTAMP,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE land_real_estate_development_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  parameter_scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  jurisdiction VARCHAR(255),
  effective_from TIMESTAMP,
  effective_to TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE land_real_estate_development_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) NOT NULL,
  target_table VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  compatibility_rule VARCHAR(255),
  migration_note TEXT,
  registered_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE land_real_estate_development_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  population_count INTEGER,
  failing_record_count INTEGER,
  assertion_result VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  rule_reference VARCHAR(255),
  remediation_task TEXT,
  closure_evidence TEXT,
  evaluated_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE land_real_estate_development_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  model_purpose VARCHAR(255),
  feature_inputs TEXT,
  governance_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255),
  approved_at TIMESTAMP,
  retirement_policy TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE land_real_estate_development_appgen_outbox_event (
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

CREATE TABLE land_real_estate_development_appgen_inbox_event (
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

CREATE TABLE land_real_estate_development_appgen_dead_letter_event (
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

CREATE SCHEMA IF NOT EXISTS construction_project_controls;

CREATE TABLE construction_project_controls_construction_project (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  construction_project_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  project_manager VARCHAR(255),
  contractor VARCHAR(255),
  original_budget DECIMAL(18, 4),
  approved_budget DECIMAL(18, 4),
  active_baseline_revision_id VARCHAR(255),
  baseline_revisions TEXT,
  reporting_periods TEXT,
  release_scorecard TEXT,
  payload TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE construction_project_controls_work_package (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  work_package_id VARCHAR(255) NOT NULL,
  project_id VARCHAR(255) NOT NULL,
  wbs_code VARCHAR(255) NOT NULL,
  parent_wbs_code VARCHAR(255),
  control_account VARCHAR(255),
  discipline VARCHAR(255),
  area VARCHAR(255),
  contractor VARCHAR(255),
  progress_method VARCHAR(255),
  planned_quantity DECIMAL(18, 4),
  installed_quantity DECIMAL(18, 4),
  measurement_unit VARCHAR(255),
  planned_percent_complete DECIMAL(18, 4),
  percent_complete DECIMAL(18, 4),
  original_budget DECIMAL(18, 4),
  approved_budget DECIMAL(18, 4),
  actual_cost DECIMAL(18, 4),
  forecast_remaining_cost DECIMAL(18, 4),
  payment_readiness VARCHAR(255),
  payload TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (project_id) REFERENCES construction_project_controls_construction_project(construction_project_id)
);

CREATE TABLE construction_project_controls_rfi (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rfi_id VARCHAR(255) NOT NULL,
  project_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  subject VARCHAR(255),
  affected_wbs_code VARCHAR(255),
  required_by_date TIMESTAMP,
  schedule_impact_classification VARCHAR(255),
  payload TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (project_id) REFERENCES construction_project_controls_construction_project(construction_project_id)
);

CREATE TABLE construction_project_controls_submittal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  submittal_id VARCHAR(255) NOT NULL,
  project_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  linked_wbs_code VARCHAR(255),
  planned_submit_date TIMESTAMP,
  required_approval_date TIMESTAMP,
  approval_cycle_count INTEGER,
  blocked_work TEXT,
  payload TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (project_id) REFERENCES construction_project_controls_construction_project(construction_project_id)
);

CREATE TABLE construction_project_controls_site_progress (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  site_progress_id VARCHAR(255) NOT NULL,
  project_id VARCHAR(255) NOT NULL,
  work_package_id VARCHAR(255) NOT NULL,
  submission_key VARCHAR(255) NOT NULL,
  measurement_date TIMESTAMP NOT NULL,
  progress_method VARCHAR(255) NOT NULL,
  installed_quantity DECIMAL(18, 4),
  measurement_unit VARCHAR(255),
  percent_complete DECIMAL(18, 4),
  accepted_status VARCHAR(255),
  evidence_bundle TEXT,
  actual_cost_incurred DECIMAL(18, 4),
  payload TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (project_id) REFERENCES construction_project_controls_construction_project(construction_project_id),
  FOREIGN KEY (work_package_id) REFERENCES construction_project_controls_work_package(work_package_id)
);

CREATE TABLE construction_project_controls_change_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  change_event_id VARCHAR(255) NOT NULL,
  project_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  trend_reference VARCHAR(255),
  cause_category VARCHAR(255),
  affected_wbs_codes TEXT,
  cost_impact DECIMAL(18, 4),
  schedule_impact_days DECIMAL(18, 4),
  approval_state VARCHAR(255),
  payload TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (project_id) REFERENCES construction_project_controls_construction_project(construction_project_id)
);

CREATE TABLE construction_project_controls_schedule_risk (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schedule_risk_id VARCHAR(255) NOT NULL,
  project_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  work_package_id VARCHAR(255),
  current_float_days DECIMAL(18, 4),
  prior_float_days DECIMAL(18, 4),
  path_status VARCHAR(255),
  owner VARCHAR(255),
  issue_state VARCHAR(255),
  escalation_required BOOLEAN,
  payload TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (project_id) REFERENCES construction_project_controls_construction_project(construction_project_id),
  FOREIGN KEY (work_package_id) REFERENCES construction_project_controls_work_package(work_package_id)
);

CREATE TABLE construction_project_controls_construction_project_controls_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_rule_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  ambiguity_flag BOOLEAN NOT NULL,
  example_text TEXT,
  approver_role VARCHAR(255),
  effective_from TIMESTAMP,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255),
  conflict_reference VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE construction_project_controls_construction_project_controls_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255),
  scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  impact_simulation_reference VARCHAR(255),
  effective_from TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE construction_project_controls_construction_project_controls_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) NOT NULL,
  target_table VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  registered_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE construction_project_controls_construction_project_controls_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  population_count INTEGER,
  threshold_value DECIMAL(18, 4),
  failing_record_count INTEGER,
  owner_role VARCHAR(255),
  remediation_task VARCHAR(255),
  assertion_result VARCHAR(255),
  severity VARCHAR(255),
  is_recurrence BOOLEAN NOT NULL,
  closure_evidence TEXT,
  evaluated_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE construction_project_controls_construction_project_controls_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  intended_use TEXT NOT NULL,
  governance_state VARCHAR(255) NOT NULL,
  feature_set TEXT,
  evaluation_evidence_reference VARCHAR(255),
  confidence_threshold DECIMAL(18, 4),
  drift_check_reference VARCHAR(255),
  human_feedback_reference VARCHAR(255),
  approved_by VARCHAR(255),
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE construction_project_controls_appgen_outbox_event (
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

CREATE TABLE construction_project_controls_appgen_inbox_event (
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

CREATE TABLE construction_project_controls_appgen_dead_letter_event (
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

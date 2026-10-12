CREATE SCHEMA IF NOT EXISTS food_safety_quality_compliance;

CREATE TABLE food_safety_quality_compliance_haccp_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  haccp_plan_id VARCHAR(255) NOT NULL,
  plan_name VARCHAR(255) NOT NULL,
  plan_version VARCHAR(255) NOT NULL,
  facility_id VARCHAR(255) NOT NULL,
  product_scope VARCHAR(255) NOT NULL,
  process_flow_reference VARCHAR(255),
  hazard_analysis_summary TEXT NOT NULL,
  approved_controls TEXT,
  prerequisite_programs TEXT,
  reviewer_role VARCHAR(255),
  supersession_reason TEXT,
  effective_from TIMESTAMP,
  effective_to TIMESTAMP,
  is_active BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE food_safety_quality_compliance_critical_control_point (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  critical_control_point_id VARCHAR(255) NOT NULL,
  haccp_plan_id VARCHAR(255) NOT NULL,
  process_step VARCHAR(255) NOT NULL,
  hazard_type VARCHAR(255) NOT NULL,
  hazard_likelihood VARCHAR(255),
  hazard_severity VARCHAR(255),
  limit_type VARCHAR(255) NOT NULL,
  limit_minimum DECIMAL(18, 4),
  limit_maximum DECIMAL(18, 4),
  limit_unit VARCHAR(255),
  monitoring_method VARCHAR(255) NOT NULL,
  monitoring_frequency VARCHAR(255) NOT NULL,
  responsible_role VARCHAR(255) NOT NULL,
  verification_requirement VARCHAR(255),
  preventive_control TEXT,
  is_verified BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (haccp_plan_id) REFERENCES food_safety_quality_compliance_haccp_plan(haccp_plan_id)
);

CREATE TABLE food_safety_quality_compliance_inspection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  inspection_id VARCHAR(255) NOT NULL,
  facility_id VARCHAR(255) NOT NULL,
  area_id VARCHAR(255) NOT NULL,
  inspection_type VARCHAR(255) NOT NULL,
  checklist_reference VARCHAR(255) NOT NULL,
  inspector_role VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  quality_score DECIMAL(18, 4),
  finding_count INTEGER NOT NULL,
  finding_text TEXT,
  action_required BOOLEAN NOT NULL,
  is_repeat_finding BOOLEAN NOT NULL,
  inspected_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE food_safety_quality_compliance_nonconformance (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  nonconformance_id VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  process_step VARCHAR(255),
  product_impact TEXT,
  containment_action TEXT,
  root_cause_method VARCHAR(255),
  root_cause_text TEXT,
  corrective_action TEXT,
  preventive_action TEXT,
  owner_role VARCHAR(255) NOT NULL,
  effectiveness_check TEXT,
  is_recurrence BOOLEAN NOT NULL,
  due_date TIMESTAMP,
  closed_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE food_safety_quality_compliance_recall_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  recall_event_id VARCHAR(255) NOT NULL,
  classification VARCHAR(255) NOT NULL,
  recall_reason TEXT NOT NULL,
  affected_lot_count INTEGER NOT NULL,
  distribution_scope VARCHAR(255) NOT NULL,
  consumer_risk VARCHAR(255) NOT NULL,
  regulator_notification_state VARCHAR(255) NOT NULL,
  communication_plan TEXT,
  is_mock_drill BOOLEAN NOT NULL,
  elapsed_minutes INTEGER,
  initiated_at TIMESTAMP NOT NULL,
  completed_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE food_safety_quality_compliance_supplier_audit (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  supplier_audit_id VARCHAR(255) NOT NULL,
  supplier_reference VARCHAR(255) NOT NULL,
  commodity VARCHAR(255) NOT NULL,
  audit_type VARCHAR(255) NOT NULL,
  risk_rating VARCHAR(255) NOT NULL,
  audit_score DECIMAL(18, 4),
  finding_count INTEGER NOT NULL,
  corrective_action TEXT,
  approval_state VARCHAR(255) NOT NULL,
  is_repeat_finding BOOLEAN NOT NULL,
  audited_at TIMESTAMP NOT NULL,
  expires_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE food_safety_quality_compliance_quality_hold (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  quality_hold_id VARCHAR(255) NOT NULL,
  hold_reason TEXT NOT NULL,
  affected_lot_reference VARCHAR(255) NOT NULL,
  held_quantity DECIMAL(18, 4) NOT NULL,
  quantity_unit VARCHAR(255) NOT NULL,
  location_reference VARCHAR(255),
  release_criteria TEXT,
  disposition VARCHAR(255),
  approver_role VARCHAR(255),
  released_quantity DECIMAL(18, 4),
  held_at TIMESTAMP NOT NULL,
  released_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE food_safety_quality_compliance_food_safety_quality_compliance_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  ambiguity_flag BOOLEAN NOT NULL,
  example_text TEXT,
  approver_role VARCHAR(255),
  effective_from TIMESTAMP,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE food_safety_quality_compliance_food_safety_quality_compliance_runtime_parameter (
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

CREATE TABLE food_safety_quality_compliance_food_safety_quality_compliance_schema_extension (
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

CREATE TABLE food_safety_quality_compliance_food_safety_quality_compliance_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  population_count INTEGER NOT NULL,
  threshold_value DECIMAL(18, 4),
  failing_record_count INTEGER NOT NULL,
  owner_role VARCHAR(255),
  remediation_task TEXT,
  assertion_result VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  is_recurrence BOOLEAN NOT NULL,
  closure_evidence TEXT,
  evaluated_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE food_safety_quality_compliance_food_safety_quality_compliance_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
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

CREATE TABLE food_safety_quality_compliance_appgen_outbox_event (
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

CREATE TABLE food_safety_quality_compliance_appgen_inbox_event (
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

CREATE TABLE food_safety_quality_compliance_appgen_dead_letter_event (
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

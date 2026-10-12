CREATE SCHEMA IF NOT EXISTS utility_outage_restoration;

CREATE TABLE utility_outage_restoration_outage_incident (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  outage_incident_id VARCHAR(255) NOT NULL,
  incident_reference VARCHAR(255) NOT NULL,
  detection_source VARCHAR(255) NOT NULL,
  detection_confidence DECIMAL(18, 4) NOT NULL,
  detected_at TIMESTAMP NOT NULL,
  incident_state VARCHAR(255) NOT NULL,
  transition_reason VARCHAR(255),
  severity_score DECIMAL(18, 4) NOT NULL,
  severity_factors TEXT,
  cause_code VARCHAR(255),
  cause_state VARCHAR(255),
  major_event_flag BOOLEAN NOT NULL,
  parent_incident_reference VARCHAR(255),
  nested_incident_flag BOOLEAN NOT NULL,
  affected_customer_count INTEGER NOT NULL,
  critical_customer_count INTEGER NOT NULL,
  storm_mode_level VARCHAR(255),
  restoration_owner VARCHAR(255),
  verified_at TIMESTAMP,
  closed_at TIMESTAMP,
  reopened_at TIMESTAMP,
  incident_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
,
  UNIQUE (outage_incident_id));

CREATE TABLE utility_outage_restoration_device_interruption (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  device_interruption_id VARCHAR(255) NOT NULL,
  outage_incident_id VARCHAR(255) NOT NULL,
  device_reference VARCHAR(255) NOT NULL,
  device_class VARCHAR(255) NOT NULL,
  interruption_type VARCHAR(255) NOT NULL,
  upstream_device_reference VARCHAR(255),
  predicted_fault_segment VARCHAR(255),
  lockout_status VARCHAR(255),
  momentary_flag BOOLEAN NOT NULL,
  interruption_duration_minutes INTEGER,
  affected_phase VARCHAR(255),
  restoration_dependency VARCHAR(255),
  topology_freshness TIMESTAMP,
  interrupted_at TIMESTAMP NOT NULL,
  restored_at TIMESTAMP,
  interruption_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (outage_incident_id) REFERENCES utility_outage_restoration_outage_incident(outage_incident_id)
,
  UNIQUE (device_interruption_id));

CREATE TABLE utility_outage_restoration_switching_step (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  switching_step_id VARCHAR(255) NOT NULL,
  outage_incident_id VARCHAR(255) NOT NULL,
  step_sequence INTEGER NOT NULL,
  device_reference VARCHAR(255) NOT NULL,
  switching_action VARCHAR(255) NOT NULL,
  hold_point VARCHAR(255),
  switching_authority VARCHAR(255),
  clearance_reference VARCHAR(255),
  expected_customer_impact INTEGER NOT NULL,
  authorization_state VARCHAR(255) NOT NULL,
  executed_at TIMESTAMP,
  completion_evidence_reference VARCHAR(255),
  blocking_hazard_reference VARCHAR(255),
  switching_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (outage_incident_id) REFERENCES utility_outage_restoration_outage_incident(outage_incident_id)
);

CREATE TABLE utility_outage_restoration_crew_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  crew_assignment_id VARCHAR(255) NOT NULL,
  outage_incident_id VARCHAR(255) NOT NULL,
  crew_reference VARCHAR(255) NOT NULL,
  crew_type VARCHAR(255) NOT NULL,
  required_skills VARCHAR(255),
  required_equipment VARCHAR(255),
  shift_status VARCHAR(255),
  staging_area VARCHAR(255),
  travel_estimate_minutes INTEGER,
  estimated_arrival TIMESTAMP,
  arrival_confirmed_at TIMESTAMP,
  task_type VARCHAR(255) NOT NULL,
  safety_briefing_reference VARCHAR(255),
  mutual_aid_flag BOOLEAN NOT NULL,
  assignment_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (outage_incident_id) REFERENCES utility_outage_restoration_outage_incident(outage_incident_id)
);

CREATE TABLE utility_outage_restoration_restoration_estimate (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  restoration_estimate_id VARCHAR(255) NOT NULL,
  outage_incident_id VARCHAR(255) NOT NULL,
  estimate_type VARCHAR(255) NOT NULL,
  estimated_restoration_at TIMESTAMP NOT NULL,
  estimate_confidence DECIMAL(18, 4) NOT NULL,
  estimate_source VARCHAR(255) NOT NULL,
  estimate_assumptions TEXT,
  revision_reason VARCHAR(255),
  revision_number INTEGER NOT NULL,
  communicated_at TIMESTAMP,
  estimate_expires_at TIMESTAMP,
  approval_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255),
  public_display_flag BOOLEAN NOT NULL,
  estimate_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (outage_incident_id) REFERENCES utility_outage_restoration_outage_incident(outage_incident_id)
);

CREATE TABLE utility_outage_restoration_customer_impact (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  customer_impact_id VARCHAR(255) NOT NULL,
  outage_incident_id VARCHAR(255) NOT NULL,
  device_interruption_id VARCHAR(255),
  service_point_reference VARCHAR(255) NOT NULL,
  customer_class VARCHAR(255) NOT NULL,
  critical_customer_flag BOOLEAN NOT NULL,
  critical_customer_type VARCHAR(255),
  life_support_flag BOOLEAN NOT NULL,
  facility_type VARCHAR(255),
  affected_phase VARCHAR(255),
  impact_start_at TIMESTAMP NOT NULL,
  impact_end_at TIMESTAMP,
  impact_segment VARCHAR(255),
  notification_channel VARCHAR(255),
  impact_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (outage_incident_id) REFERENCES utility_outage_restoration_outage_incident(outage_incident_id),
  FOREIGN KEY (device_interruption_id) REFERENCES utility_outage_restoration_device_interruption(device_interruption_id)
);

CREATE TABLE utility_outage_restoration_reliability_metric (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reliability_metric_id VARCHAR(255) NOT NULL,
  outage_incident_id VARCHAR(255),
  metric_type VARCHAR(255) NOT NULL,
  metric_period_start TIMESTAMP NOT NULL,
  metric_period_end TIMESTAMP NOT NULL,
  customers_interrupted INTEGER NOT NULL,
  outage_duration_minutes INTEGER NOT NULL,
  momentary_interruption_count INTEGER NOT NULL,
  major_event_exclusion_flag BOOLEAN NOT NULL,
  metric_value DECIMAL(18, 4) NOT NULL,
  certified_at TIMESTAMP,
  certification_evidence_reference VARCHAR(255),
  metric_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (outage_incident_id) REFERENCES utility_outage_restoration_outage_incident(outage_incident_id)
);

CREATE TABLE utility_outage_restoration_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  ambiguity_flag BOOLEAN NOT NULL,
  example_text TEXT,
  approver_role VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE utility_outage_restoration_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
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

CREATE TABLE utility_outage_restoration_schema_extension (
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

CREATE TABLE utility_outage_restoration_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
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

CREATE TABLE utility_outage_restoration_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  model_type VARCHAR(255) NOT NULL,
  coverage_scope VARCHAR(255) NOT NULL,
  backtest_exception_count INTEGER NOT NULL,
  governance_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255),
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE utility_outage_restoration_appgen_outbox_event (
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

CREATE TABLE utility_outage_restoration_appgen_inbox_event (
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

CREATE TABLE utility_outage_restoration_appgen_dead_letter_event (
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

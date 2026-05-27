CREATE SCHEMA IF NOT EXISTS predictive_demand;

CREATE TABLE predictive_demand_forecast_model (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_forecast_run (
  id INTEGER PRIMARY KEY NOT NULL,
  forecast_model_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (forecast_model_id) REFERENCES predictive_demand_forecast_model(id)
);

CREATE TABLE predictive_demand_demand_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  forecast_model_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (forecast_model_id) REFERENCES predictive_demand_forecast_model(id)
);

CREATE TABLE predictive_demand_forecast_result (
  id INTEGER PRIMARY KEY NOT NULL,
  forecast_model_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (forecast_model_id) REFERENCES predictive_demand_forecast_model(id)
);

CREATE TABLE predictive_demand_planning_horizon (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  horizon_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  granularity VARCHAR(255) NOT NULL,
  starts_on DATE NOT NULL,
  ends_on DATE NOT NULL,
  freeze_window_days INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_forecast_driver (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  driver_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  driver_type VARCHAR(255) NOT NULL,
  driver_value NUMERIC NOT NULL,
  weight NUMERIC NOT NULL,
  source VARCHAR(255) NOT NULL,
  effective_on DATE NOT NULL,
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_consensus_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  adjustment_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  planner_id VARCHAR(255) NOT NULL,
  adjustment_quantity NUMERIC NOT NULL,
  reason_code VARCHAR(255) NOT NULL,
  approval_status VARCHAR(255) NOT NULL,
  policy_result TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_scenario_version (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  scenario_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  scenario_name VARCHAR(255) NOT NULL,
  assumption_set TEXT NOT NULL,
  forecast_quantity NUMERIC NOT NULL,
  confidence NUMERIC NOT NULL,
  selected BOOLEAN NOT NULL,
  created_by VARCHAR(255) NOT NULL,
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_shortage_risk (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  risk_id VARCHAR(255) NOT NULL,
  result_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  shortage_quantity NUMERIC NOT NULL,
  risk_band VARCHAR(255) NOT NULL,
  material_constraint TEXT NOT NULL,
  alert_due_on DATE NOT NULL,
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_replenishment_recommendation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  recommendation_id VARCHAR(255) NOT NULL,
  result_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  recommended_quantity NUMERIC NOT NULL,
  recommended_date DATE NOT NULL,
  service_level_target NUMERIC NOT NULL,
  action_status VARCHAR(255) NOT NULL,
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_forecast_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  exception_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  detected_value NUMERIC NOT NULL,
  threshold NUMERIC NOT NULL,
  resolution_status VARCHAR(255) NOT NULL,
  assigned_to VARCHAR(255),
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_model_drift_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  drift_id VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  metric_name VARCHAR(255) NOT NULL,
  metric_value NUMERIC NOT NULL,
  threshold NUMERIC NOT NULL,
  drift_band VARCHAR(255) NOT NULL,
  retrain_recommended BOOLEAN NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_planning_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  allowed_signal_types TEXT NOT NULL,
  allowed_regions TEXT NOT NULL,
  forecast_policy TEXT NOT NULL,
  shortage_policy TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_planning_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  value TEXT NOT NULL,
  bounds TEXT NOT NULL,
  changed_by VARCHAR(255),
  effective_from TIMESTAMP NOT NULL,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_governed_model_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  evidence_id VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  algorithm VARCHAR(255) NOT NULL,
  training_window TEXT NOT NULL,
  validation_metrics TEXT NOT NULL,
  approval_status VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255),
  approved_at TIMESTAMP,
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_forecast_audit_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) NOT NULL,
  entity_type VARCHAR(255) NOT NULL,
  entity_id VARCHAR(255) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  previous_hash VARCHAR(255),
  signature TEXT NOT NULL,
  control_assertions TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  audit_proof TEXT NOT NULL
);

CREATE TABLE predictive_demand_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE predictive_demand_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE predictive_demand_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE SCHEMA IF NOT EXISTS agriculture_farm_operations;

CREATE TABLE agriculture_farm_operations_field (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  field_id VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  parent_field_id VARCHAR(255),
  management_zone VARCHAR(255),
  geometry_state VARCHAR(255) NOT NULL,
  acreage DECIMAL(18, 4) NOT NULL,
  soil_type VARCHAR(255),
  drainage_class VARCHAR(255),
  stewardship_practice VARCHAR(255),
  readiness_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
,
  UNIQUE (field_id));

CREATE TABLE agriculture_farm_operations_crop_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  crop_plan_id VARCHAR(255) NOT NULL,
  field_id VARCHAR(255) NOT NULL,
  management_zone VARCHAR(255),
  season VARCHAR(255) NOT NULL,
  market_year INTEGER NOT NULL,
  crop VARCHAR(255) NOT NULL,
  fallback_crop VARCHAR(255),
  previous_crop VARCHAR(255),
  replant_of VARCHAR(255),
  variety VARCHAR(255),
  acreage DECIMAL(18, 4) NOT NULL,
  planting_date TIMESTAMP,
  planned_start TIMESTAMP,
  planned_end TIMESTAMP,
  window_status VARCHAR(255) NOT NULL,
  readiness_state VARCHAR(255) NOT NULL,
  yield_risk_percent DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_id) REFERENCES agriculture_farm_operations_field(field_id)
);

CREATE TABLE agriculture_farm_operations_input_application (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  input_application_id VARCHAR(255) NOT NULL,
  field_id VARCHAR(255) NOT NULL,
  crop_plan_id VARCHAR(255),
  product_name VARCHAR(255) NOT NULL,
  product_category VARCHAR(255) NOT NULL,
  application_method VARCHAR(255) NOT NULL,
  application_rate DECIMAL(18, 4) NOT NULL,
  rate_unit VARCHAR(255) NOT NULL,
  carrier_water_volume DECIMAL(18, 4),
  applied_at TIMESTAMP,
  restricted_entry_interval_hours INTEGER,
  pre_harvest_interval_days INTEGER,
  operator_id VARCHAR(255),
  calibration_id VARCHAR(255),
  treatment_justification TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_id) REFERENCES agriculture_farm_operations_field(field_id)
);

CREATE TABLE agriculture_farm_operations_irrigation_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  irrigation_event_id VARCHAR(255) NOT NULL,
  field_id VARCHAR(255) NOT NULL,
  crop_stage VARCHAR(255) NOT NULL,
  water_source VARCHAR(255) NOT NULL,
  applied_volume_mm DECIMAL(18, 4) NOT NULL,
  rainfall_mm DECIMAL(18, 4),
  net_water_balance_mm DECIMAL(18, 4),
  pump_hours DECIMAL(18, 4),
  stress_sensitivity VARCHAR(255),
  scheduled_at TIMESTAMP,
  completed_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_id) REFERENCES agriculture_farm_operations_field(field_id)
);

CREATE TABLE agriculture_farm_operations_equipment_use (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  equipment_use_id VARCHAR(255) NOT NULL,
  field_id VARCHAR(255) NOT NULL,
  equipment_id VARCHAR(255) NOT NULL,
  operation_type VARCHAR(255) NOT NULL,
  operator_id VARCHAR(255),
  calibrated_at TIMESTAMP,
  calibration_expires_at TIMESTAMP,
  target_rate DECIMAL(18, 4),
  measured_rate DECIMAL(18, 4),
  swath_width DECIMAL(18, 4),
  pass_count INTEGER NOT NULL,
  fuel_used_liters DECIMAL(18, 4),
  started_at TIMESTAMP,
  ended_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_id) REFERENCES agriculture_farm_operations_field(field_id)
);

CREATE TABLE agriculture_farm_operations_harvest_lot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  harvest_lot_id VARCHAR(255) NOT NULL,
  field_id VARCHAR(255) NOT NULL,
  crop_plan_id VARCHAR(255),
  variety VARCHAR(255),
  harvest_date TIMESTAMP NOT NULL,
  machine_pass VARCHAR(255),
  gross_weight_kg DECIMAL(18, 4) NOT NULL,
  net_weight_kg DECIMAL(18, 4),
  moisture_percent DECIMAL(18, 4),
  quality_grade VARCHAR(255),
  segregation_rule VARCHAR(255),
  storage_destination VARCHAR(255),
  drying_target_percent DECIMAL(18, 4),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_id) REFERENCES agriculture_farm_operations_field(field_id)
);

CREATE TABLE agriculture_farm_operations_yield_observation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  yield_observation_id VARCHAR(255) NOT NULL,
  field_id VARCHAR(255) NOT NULL,
  harvest_lot_id VARCHAR(255),
  observation_source VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  yield_amount DECIMAL(18, 4) NOT NULL,
  yield_unit VARCHAR(255) NOT NULL,
  moisture_normalized BOOLEAN NOT NULL,
  expected_amount DECIMAL(18, 4),
  variance_percent DECIMAL(18, 4),
  variance_reason VARCHAR(255),
  is_source_of_truth BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_id) REFERENCES agriculture_farm_operations_field(field_id)
);

CREATE TABLE agriculture_farm_operations_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
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

CREATE TABLE agriculture_farm_operations_runtime_parameter (
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

CREATE TABLE agriculture_farm_operations_schema_extension (
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

CREATE TABLE agriculture_farm_operations_control_assertion (
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

CREATE TABLE agriculture_farm_operations_governed_model (
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

CREATE TABLE agriculture_farm_operations_appgen_outbox_event (
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

CREATE TABLE agriculture_farm_operations_appgen_inbox_event (
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

CREATE TABLE agriculture_farm_operations_appgen_dead_letter_event (
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

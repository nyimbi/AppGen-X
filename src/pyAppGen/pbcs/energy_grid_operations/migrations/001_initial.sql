CREATE SCHEMA IF NOT EXISTS energy_grid_operations;

CREATE TABLE energy_grid_operations_grid_asset (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  grid_asset_id VARCHAR(255) NOT NULL,
  asset_name VARCHAR(255) NOT NULL,
  device_class VARCHAR(255) NOT NULL,
  parent_asset_id VARCHAR(255),
  substation_id VARCHAR(255),
  feeder_id VARCHAR(255),
  voltage_class VARCHAR(255) NOT NULL,
  phasing VARCHAR(255),
  normal_state VARCHAR(255) NOT NULL,
  protection_zone VARCHAR(255),
  interrupting_rating DECIMAL(18, 4),
  operating_mode VARCHAR(255),
  gis_reference VARCHAR(255),
  scada_tag VARCHAR(255),
  commissioning_evidence TEXT,
  is_der_intertie BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (parent_asset_id) REFERENCES energy_grid_operations_grid_asset(grid_asset_id)
,
  UNIQUE (grid_asset_id));

CREATE TABLE energy_grid_operations_load_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  load_forecast_id VARCHAR(255) NOT NULL,
  grid_asset_id VARCHAR(255) NOT NULL,
  substation_id VARCHAR(255),
  feeder_id VARCHAR(255),
  segment_id VARCHAR(255),
  source_system VARCHAR(255) NOT NULL,
  forecast_horizon_hours INTEGER NOT NULL,
  interval_minutes INTEGER NOT NULL,
  native_load_mw DECIMAL(18, 4) NOT NULL,
  der_contribution_mw DECIMAL(18, 4) NOT NULL,
  net_load_mw DECIMAL(18, 4) NOT NULL,
  weather_sensitivity DECIMAL(18, 4),
  confidence_band DECIMAL(18, 4) NOT NULL,
  contingency_variant VARCHAR(255),
  weather_station VARCHAR(255),
  der_availability_assumption VARCHAR(255),
  is_operator_override BOOLEAN NOT NULL,
  override_reason TEXT,
  forecast_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (grid_asset_id) REFERENCES energy_grid_operations_grid_asset(grid_asset_id)
);

CREATE TABLE energy_grid_operations_switching_order (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  switching_order_id VARCHAR(255) NOT NULL,
  grid_asset_id VARCHAR(255) NOT NULL,
  substation_id VARCHAR(255),
  feeder_id VARCHAR(255),
  order_type VARCHAR(255) NOT NULL,
  sequence_number INTEGER NOT NULL,
  step_count INTEGER NOT NULL,
  hold_point_count INTEGER NOT NULL,
  precondition_text TEXT,
  hold_point_text TEXT,
  telemetry_confirmation VARCHAR(255),
  clearance_reference VARCHAR(255),
  reversal_instruction TEXT,
  simulation_state VARCHAR(255) NOT NULL,
  impacted_feeder_count INTEGER NOT NULL,
  backfeed_risk VARCHAR(255),
  required_approver_role VARCHAR(255),
  planned_start TIMESTAMP,
  planned_end TIMESTAMP,
  executed_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (grid_asset_id) REFERENCES energy_grid_operations_grid_asset(grid_asset_id)
);

CREATE TABLE energy_grid_operations_dispatch_instruction (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  dispatch_instruction_id VARCHAR(255) NOT NULL,
  grid_asset_id VARCHAR(255) NOT NULL,
  substation_id VARCHAR(255),
  feeder_id VARCHAR(255),
  objective_type VARCHAR(255) NOT NULL,
  control_target VARCHAR(255) NOT NULL,
  target_interval_minutes INTEGER NOT NULL,
  expected_load_movement_mw DECIMAL(18, 4),
  voltage_support_intent VARCHAR(255),
  der_participation VARCHAR(255),
  reason_code VARCHAR(255) NOT NULL,
  rollback_condition TEXT,
  constraint_conflict VARCHAR(255),
  telemetry_freshness_state VARCHAR(255),
  issued_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (grid_asset_id) REFERENCES energy_grid_operations_grid_asset(grid_asset_id)
);

CREATE TABLE energy_grid_operations_outage_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  outage_event_id VARCHAR(255) NOT NULL,
  grid_asset_id VARCHAR(255) NOT NULL,
  initiating_device_id VARCHAR(255),
  feeder_id VARCHAR(255),
  section_ids TEXT,
  cause_code VARCHAR(255),
  lifecycle_state VARCHAR(255) NOT NULL,
  customers_at_risk INTEGER,
  load_at_risk_mw DECIMAL(18, 4),
  crew_eta TIMESTAMP,
  restoration_hypothesis TEXT,
  correlation_id VARCHAR(255),
  reported_at TIMESTAMP NOT NULL,
  isolated_at TIMESTAMP,
  restored_at TIMESTAMP,
  restoration_clock_minutes INTEGER,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (grid_asset_id) REFERENCES energy_grid_operations_grid_asset(grid_asset_id)
);

CREATE TABLE energy_grid_operations_reliability_constraint (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reliability_constraint_id VARCHAR(255) NOT NULL,
  grid_asset_id VARCHAR(255) NOT NULL,
  constraint_type VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  threshold_value DECIMAL(18, 4),
  threshold_unit VARCHAR(255),
  governed_asset_id VARCHAR(255),
  owner_role VARCHAR(255),
  expires_at TIMESTAMP,
  is_active BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (grid_asset_id) REFERENCES energy_grid_operations_grid_asset(grid_asset_id)
);

CREATE TABLE energy_grid_operations_grid_topology (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  grid_topology_id VARCHAR(255) NOT NULL,
  grid_asset_id VARCHAR(255) NOT NULL,
  topology_version INTEGER NOT NULL,
  segment_id VARCHAR(255),
  from_node_id VARCHAR(255),
  to_node_id VARCHAR(255),
  connection_state VARCHAR(255) NOT NULL,
  is_normally_open BOOLEAN NOT NULL,
  is_backfeed_path BOOLEAN NOT NULL,
  is_der_island BOOLEAN NOT NULL,
  phase_code VARCHAR(255),
  directional_connectivity VARCHAR(255),
  restoration_rank INTEGER,
  projected_switching_count INTEGER,
  verified_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (grid_asset_id) REFERENCES energy_grid_operations_grid_asset(grid_asset_id)
);

CREATE TABLE energy_grid_operations_energy_grid_operations_policy_rule (
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

CREATE TABLE energy_grid_operations_energy_grid_operations_runtime_parameter (
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

CREATE TABLE energy_grid_operations_energy_grid_operations_schema_extension (
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

CREATE TABLE energy_grid_operations_energy_grid_operations_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  assertion_result VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  remediation_task TEXT,
  evaluated_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE energy_grid_operations_energy_grid_operations_governed_model (
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

CREATE TABLE energy_grid_operations_appgen_outbox_event (
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

CREATE TABLE energy_grid_operations_appgen_inbox_event (
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

CREATE TABLE energy_grid_operations_appgen_dead_letter_event (
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

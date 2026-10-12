CREATE SCHEMA IF NOT EXISTS renewables_asset_operations;

CREATE TABLE renewables_asset_operations_renewable_asset (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  renewable_asset_id VARCHAR(255) NOT NULL,
  asset_name VARCHAR(255) NOT NULL,
  technology_type VARCHAR(255) NOT NULL,
  asset_class VARCHAR(255) NOT NULL,
  parent_asset_id VARCHAR(255),
  oem VARCHAR(255),
  model VARCHAR(255),
  serial_number VARCHAR(255),
  site_reference VARCHAR(255) NOT NULL,
  grid_node VARCHAR(255),
  latitude DECIMAL(18, 4),
  longitude DECIMAL(18, 4),
  nameplate_capacity_mw DECIMAL(18, 4) NOT NULL,
  commissioning_date TIMESTAMP,
  owner_reference VARCHAR(255),
  criticality VARCHAR(255),
  warranty_start_date TIMESTAMP,
  warranty_end_date TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE renewables_asset_operations_generation_reading (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  generation_reading_id VARCHAR(255) NOT NULL,
  renewable_asset_id VARCHAR(255) NOT NULL,
  reading_interval_start TIMESTAMP NOT NULL,
  reading_interval_end TIMESTAMP NOT NULL,
  source_system VARCHAR(255) NOT NULL,
  meter_reference VARCHAR(255),
  interval_minutes INTEGER NOT NULL,
  active_energy_mwh DECIMAL(18, 4) NOT NULL,
  reactive_energy_mvarh DECIMAL(18, 4),
  irradiance_wm2 DECIMAL(18, 4),
  wind_speed_ms DECIMAL(18, 4),
  ambient_temperature_c DECIMAL(18, 4),
  availability_flag BOOLEAN NOT NULL,
  quality_flag VARCHAR(255) NOT NULL,
  corrected_flag BOOLEAN NOT NULL,
  correction_reason VARCHAR(255),
  late_arrival_flag BOOLEAN NOT NULL,
  received_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (renewable_asset_id) REFERENCES renewables_asset_operations_renewable_asset(renewable_asset_id)
);

CREATE TABLE renewables_asset_operations_curtailment_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  curtailment_event_id VARCHAR(255) NOT NULL,
  renewable_asset_id VARCHAR(255) NOT NULL,
  initiator VARCHAR(255) NOT NULL,
  instruction_source VARCHAR(255) NOT NULL,
  cause_code VARCHAR(255) NOT NULL,
  start_at TIMESTAMP NOT NULL,
  end_at TIMESTAMP,
  duration_minutes INTEGER,
  requested_mw DECIMAL(18, 4) NOT NULL,
  delivered_mw DECIMAL(18, 4),
  recoverable BOOLEAN NOT NULL,
  compensation_status VARCHAR(255),
  instruction_evidence_reference VARCHAR(255),
  estimated_lost_energy_mwh DECIMAL(18, 4),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (renewable_asset_id) REFERENCES renewables_asset_operations_renewable_asset(renewable_asset_id)
);

CREATE TABLE renewables_asset_operations_availability_record (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  availability_record_id VARCHAR(255) NOT NULL,
  renewable_asset_id VARCHAR(255) NOT NULL,
  period_start TIMESTAMP NOT NULL,
  period_end TIMESTAMP NOT NULL,
  availability_view VARCHAR(255) NOT NULL,
  denominator_hours DECIMAL(18, 4) NOT NULL,
  outage_hours DECIMAL(18, 4) NOT NULL,
  derate_hours DECIMAL(18, 4),
  curtailment_hours DECIMAL(18, 4),
  force_majeure_hours DECIMAL(18, 4),
  planned_work_hours DECIMAL(18, 4),
  technical_availability_pct DECIMAL(18, 4) NOT NULL,
  contractual_availability_pct DECIMAL(18, 4),
  grid_adjusted_availability_pct DECIMAL(18, 4),
  energy_based_availability_pct DECIMAL(18, 4),
  exclusion_reason_code VARCHAR(255),
  exclusion_approved_by VARCHAR(255),
  period_locked BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (renewable_asset_id) REFERENCES renewables_asset_operations_renewable_asset(renewable_asset_id)
);

CREATE TABLE renewables_asset_operations_ppa_obligation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  ppa_obligation_id VARCHAR(255) NOT NULL,
  contract_reference VARCHAR(255) NOT NULL,
  counterparty VARCHAR(255) NOT NULL,
  renewable_asset_id VARCHAR(255),
  obligation_type VARCHAR(255) NOT NULL,
  guarantee_threshold DECIMAL(18, 4),
  milestone_date TIMESTAMP,
  reporting_deadline TIMESTAMP,
  notice_period_days INTEGER,
  ld_trigger_condition VARCHAR(255),
  settlement_evidence_due TIMESTAMP,
  contract_year VARCHAR(255),
  obligation_state VARCHAR(255) NOT NULL,
  required_attachment VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (renewable_asset_id) REFERENCES renewables_asset_operations_renewable_asset(renewable_asset_id)
);

CREATE TABLE renewables_asset_operations_maintenance_work (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  maintenance_work_id VARCHAR(255) NOT NULL,
  renewable_asset_id VARCHAR(255) NOT NULL,
  work_type VARCHAR(255) NOT NULL,
  work_description TEXT,
  criticality_score DECIMAL(18, 4),
  mw_at_risk DECIMAL(18, 4),
  priority VARCHAR(255) NOT NULL,
  assigned_crew VARCHAR(255),
  contractor_reference VARCHAR(255),
  permit_to_work_reference VARCHAR(255),
  safety_hold BOOLEAN NOT NULL,
  planned_start TIMESTAMP,
  planned_end TIMESTAMP,
  actual_start TIMESTAMP,
  actual_end TIMESTAMP,
  spares_reference VARCHAR(255),
  warranty_claim_flag BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (renewable_asset_id) REFERENCES renewables_asset_operations_renewable_asset(renewable_asset_id)
);

CREATE TABLE renewables_asset_operations_performance_ratio (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  performance_ratio_id VARCHAR(255) NOT NULL,
  renewable_asset_id VARCHAR(255) NOT NULL,
  period_start TIMESTAMP NOT NULL,
  period_end TIMESTAMP NOT NULL,
  time_bucket VARCHAR(255) NOT NULL,
  expected_energy_mwh DECIMAL(18, 4) NOT NULL,
  actual_energy_mwh DECIMAL(18, 4) NOT NULL,
  performance_ratio_pct DECIMAL(18, 4) NOT NULL,
  weather_deviation_pct DECIMAL(18, 4),
  outage_loss_pct DECIMAL(18, 4),
  curtailment_loss_pct DECIMAL(18, 4),
  clipping_loss_pct DECIMAL(18, 4),
  soiling_loss_pct DECIMAL(18, 4),
  residual_loss_pct DECIMAL(18, 4),
  normalization_method VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (renewable_asset_id) REFERENCES renewables_asset_operations_renewable_asset(renewable_asset_id)
);

CREATE TABLE renewables_asset_operations_renewables_asset_operations_policy_rule (
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

CREATE TABLE renewables_asset_operations_renewables_asset_operations_runtime_parameter (
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

CREATE TABLE renewables_asset_operations_renewables_asset_operations_schema_extension (
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

CREATE TABLE renewables_asset_operations_renewables_asset_operations_control_assertion (
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

CREATE TABLE renewables_asset_operations_renewables_asset_operations_governed_model (
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

CREATE TABLE renewables_asset_operations_appgen_outbox_event (
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

CREATE TABLE renewables_asset_operations_appgen_inbox_event (
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

CREATE TABLE renewables_asset_operations_appgen_dead_letter_event (
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

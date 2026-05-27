CREATE SCHEMA IF NOT EXISTS eam;

CREATE TABLE eam_equipment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  equipment_id VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  asset_tag VARCHAR(255) NOT NULL,
  criticality VARCHAR(32) NOT NULL,
  location VARCHAR(255) NOT NULL,
  parent_equipment_id VARCHAR(255),
  warranty_until VARCHAR(32),
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE eam_maintenance_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255) NOT NULL,
  equipment_id VARCHAR(255) NOT NULL,
  strategy VARCHAR(64) NOT NULL,
  interval_days INTEGER,
  meter_threshold DOUBLE PRECISION,
  condition_threshold DOUBLE PRECISION,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE eam_work_order (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  work_order_id VARCHAR(255) NOT NULL,
  equipment_id VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255),
  work_type VARCHAR(64) NOT NULL,
  priority VARCHAR(64) NOT NULL,
  risk_score DOUBLE PRECISION NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE eam_spare_part_usage (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  usage_id VARCHAR(255) NOT NULL,
  work_order_id VARCHAR(255) NOT NULL,
  part_number VARCHAR(255) NOT NULL,
  quantity DOUBLE PRECISION NOT NULL,
  unit_cost DOUBLE PRECISION NOT NULL,
  cost DOUBLE PRECISION NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE eam_condition_reading (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reading_id VARCHAR(255) NOT NULL,
  equipment_id VARCHAR(255) NOT NULL,
  sensor VARCHAR(255) NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  unit VARCHAR(64) NOT NULL,
  risk_score DOUBLE PRECISION NOT NULL,
  alarm BOOLEAN NOT NULL,
  captured_at TIMESTAMP
);

CREATE TABLE eam_meter_reading (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  meter_id VARCHAR(255) NOT NULL,
  equipment_id VARCHAR(255) NOT NULL,
  meter_name VARCHAR(255) NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  unit VARCHAR(64) NOT NULL,
  triggered_plans TEXT NOT NULL,
  captured_at TIMESTAMP
);

CREATE TABLE eam_failure_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  failure_event_id VARCHAR(255) NOT NULL,
  equipment_id VARCHAR(255) NOT NULL,
  failure_code VARCHAR(255) NOT NULL,
  downtime_hours DOUBLE PRECISION NOT NULL,
  severity VARCHAR(64) NOT NULL,
  recorded_at TIMESTAMP NOT NULL
);

CREATE TABLE eam_maintenance_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schedule_id VARCHAR(255) NOT NULL,
  work_order_id VARCHAR(255) NOT NULL,
  technician VARCHAR(255) NOT NULL,
  scheduled_start TIMESTAMP NOT NULL,
  scheduled_end TIMESTAMP,
  carbon_score DOUBLE PRECISION,
  status VARCHAR(64) NOT NULL
);

CREATE TABLE eam_service_vendor_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  vendor_event_id VARCHAR(255) NOT NULL,
  work_order_id VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  sla_state VARCHAR(64) NOT NULL,
  warranty_recovery DOUBLE PRECISION NOT NULL,
  status VARCHAR(64) NOT NULL
);

CREATE TABLE eam_safety_permit (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  permit_id VARCHAR(255) NOT NULL,
  equipment_id VARCHAR(255) NOT NULL,
  permit_type VARCHAR(64) NOT NULL,
  risk_score DOUBLE PRECISION NOT NULL,
  approved_by VARCHAR(255),
  status VARCHAR(64) NOT NULL
);

CREATE TABLE eam_maintenance_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  rule_type VARCHAR(64) NOT NULL,
  status VARCHAR(64) NOT NULL,
  eligible_work_types TEXT NOT NULL,
  allowed_sites TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL
);

CREATE TABLE eam_maintenance_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  value TEXT NOT NULL,
  bounds TEXT NOT NULL,
  compiled_hash VARCHAR(255)
);

CREATE TABLE eam_maintenance_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(64) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit INTEGER NOT NULL,
  default_timezone VARCHAR(64) NOT NULL
);

CREATE TABLE eam_maintenance_outbox (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE eam_maintenance_inbox (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE eam_maintenance_dead_letter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

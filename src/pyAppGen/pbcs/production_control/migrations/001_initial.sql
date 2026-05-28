CREATE SCHEMA IF NOT EXISTS production_control;

CREATE TABLE production_control_work_center (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  work_center_id VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  work_center_type VARCHAR(255) NOT NULL,
  capacity_hours VARCHAR(255) NOT NULL,
  efficiency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_production_order (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  route VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  planned_order_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  completed_qty VARCHAR(255) NOT NULL,
  scrap_qty VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_routing_step (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  step_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  sequence VARCHAR(255) NOT NULL,
  work_center_id VARCHAR(255) NOT NULL,
  standard_minutes VARCHAR(255) NOT NULL,
  setup_minutes VARCHAR(255) NOT NULL,
  quality_gate VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_production_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schedule_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  capacity_load VARCHAR(255) NOT NULL,
  step_count INTEGER NOT NULL,
  scheduled_by VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_dispatch_list (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  dispatch_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  work_center_ids VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_operation_confirmation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  confirmation_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  step_id VARCHAR(255) NOT NULL,
  good_qty VARCHAR(255) NOT NULL,
  scrap_qty VARCHAR(255) NOT NULL,
  labor_hours VARCHAR(255) NOT NULL,
  machine_hours VARCHAR(255) NOT NULL,
  confirmed_by VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_downtime_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  downtime_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  work_center_id VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  minutes VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_material_consumption (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  consumption_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  material_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  uom VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_wip_inventory (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  wip_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  material_id VARCHAR(255) NOT NULL,
  quantity_in_process VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_labor_time_booking (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  booking_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  step_id VARCHAR(255) NOT NULL,
  operator_id VARCHAR(255) NOT NULL,
  hours VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_machine_time_booking (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  booking_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  step_id VARCHAR(255) NOT NULL,
  work_center_id VARCHAR(255) NOT NULL,
  hours VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_quality_gate_result (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  gate_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  step_id VARCHAR(255) NOT NULL,
  quality_gate VARCHAR(255) NOT NULL,
  result VARCHAR(255) NOT NULL,
  inspector VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_production_completion_record (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  completion_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  completed_qty VARCHAR(255) NOT NULL,
  scrap_qty VARCHAR(255) NOT NULL,
  completed_by VARCHAR(255) NOT NULL,
  handoffs VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_scrap_rework_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  scrap_rework_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  step_id VARCHAR(255) NOT NULL,
  scrap_qty VARCHAR(255) NOT NULL,
  rework_qty VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_oee_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  work_center_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  oee VARCHAR(255) NOT NULL,
  downtime_minutes VARCHAR(255) NOT NULL,
  completed_qty VARCHAR(255) NOT NULL,
  scrap_qty VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_throughput_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  forecast_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  forecast_throughput VARCHAR(255) NOT NULL,
  horizon_days VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_production_exception_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  case_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  case_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  recommended_action VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_production_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  screening_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  restricted_sites VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_capacity_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  allocation_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  work_center_id VARCHAR(255) NOT NULL,
  allocated_hours VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_completion_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  proof_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_production_audit_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  audit_entry_id VARCHAR(255) NOT NULL,
  action VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_governed_model_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  features VARCHAR(255) NOT NULL,
  auc VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_production_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  rule_type VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  enabled VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_production_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  changed_by VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE production_control_production_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  event_contract VARCHAR(255) NOT NULL,
  default_timezone VARCHAR(255) NOT NULL,
  workbench_limit VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

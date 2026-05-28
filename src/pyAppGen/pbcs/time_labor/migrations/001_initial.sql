CREATE SCHEMA IF NOT EXISTS time_labor;

CREATE TABLE time_labor_shift (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  shift_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  date VARCHAR(255) NOT NULL,
  planned_start VARCHAR(255) NOT NULL,
  planned_end VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  cost_center DECIMAL(18, 4) NOT NULL,
  job VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_shift_pattern (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  pattern_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  cycle_days VARCHAR(255) NOT NULL,
  planned_start VARCHAR(255) NOT NULL,
  planned_end VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_shift_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assignment_id VARCHAR(255) NOT NULL,
  shift_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  assignment_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_shift_swap_request (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  swap_id VARCHAR(255) NOT NULL,
  from_employee_id VARCHAR(255) NOT NULL,
  to_employee_id VARCHAR(255) NOT NULL,
  shift_id VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_schedule_bid (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  bid_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  shift_id VARCHAR(255) NOT NULL,
  preference_score DECIMAL(18, 4) NOT NULL,
  bid_status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_labor_demand_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  forecast_id VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  date VARCHAR(255) NOT NULL,
  required_hours VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_clock_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shift_id VARCHAR(255) NOT NULL,
  kind VARCHAR(255) NOT NULL,
  time VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  distance_meters VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_clock_device (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  device_id VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  trust_score DECIMAL(18, 4) NOT NULL,
  last_seen_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_clock_source_route (
  tenant VARCHAR(255) NOT NULL,
  route_id VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  route VARCHAR(255) NOT NULL,
  latency VARCHAR(255) NOT NULL,
  failover_used VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_clock_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) NOT NULL,
  shift_id VARCHAR(255) NOT NULL,
  exception_type VARCHAR(255) NOT NULL,
  resolution VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  entry_id VARCHAR(255) NOT NULL,
  shift_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  hours VARCHAR(255) NOT NULL,
  overtime_hours VARCHAR(255) NOT NULL,
  premium_hours VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_entry_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  line_id VARCHAR(255) NOT NULL,
  entry_id VARCHAR(255) NOT NULL,
  earning_code VARCHAR(255) NOT NULL,
  hours VARCHAR(255) NOT NULL,
  rate_multiplier DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_break_deduction (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  deduction_id VARCHAR(255) NOT NULL,
  entry_id VARCHAR(255) NOT NULL,
  break_minutes VARCHAR(255) NOT NULL,
  policy_rule_id VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_overtime_bucket (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  bucket_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  period TIMESTAMP NOT NULL,
  threshold DECIMAL(18, 4) NOT NULL,
  overtime_hours VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_premium_calculation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  premium_id VARCHAR(255) NOT NULL,
  entry_id VARCHAR(255) NOT NULL,
  premium_code VARCHAR(255) NOT NULL,
  hours VARCHAR(255) NOT NULL,
  multiplier VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_holiday_calendar (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_absence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  absence_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  absence_type VARCHAR(255) NOT NULL,
  hours VARCHAR(255) NOT NULL,
  date VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_absence_balance (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  balance_id DECIMAL(18, 4) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  absence_type VARCHAR(255) NOT NULL,
  available_hours VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_absence_entitlement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  entitlement_id VARCHAR(255) NOT NULL,
  absence_type VARCHAR(255) NOT NULL,
  annual_hours VARCHAR(255) NOT NULL,
  eligibility_rule_id VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_absence_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  approval_id VARCHAR(255) NOT NULL,
  absence_id VARCHAR(255) NOT NULL,
  approver VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  decided_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_labor_summary (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  summary_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  period TIMESTAMP NOT NULL,
  approved_hours VARCHAR(255) NOT NULL,
  overtime_hours VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_labor_summary_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  line_id VARCHAR(255) NOT NULL,
  summary_id VARCHAR(255) NOT NULL,
  entry_id VARCHAR(255) NOT NULL,
  earning_code VARCHAR(255) NOT NULL,
  hours VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_labor_cost_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  allocation_id VARCHAR(255) NOT NULL,
  summary_id VARCHAR(255) NOT NULL,
  cost_center DECIMAL(18, 4) NOT NULL,
  project_id VARCHAR(255) NOT NULL,
  hours VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_labor_distribution (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_approval_workflow (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  sla_hours VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_approval_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  task_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  subject_id VARCHAR(255) NOT NULL,
  assignee VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_employee_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  role VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  identity_hash VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_role_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  role VARCHAR(255) NOT NULL,
  received_event_id VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_payroll_labor_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_warehouse_site_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_manufacturing_shift_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_project_cost_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_audit_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_hours_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_carbon_schedule_window (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_schedule_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_shift_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_risk_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_parsed_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  enabled VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_time_parameter (
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

CREATE TABLE time_labor_time_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  event_contract VARCHAR(255) NOT NULL,
  stream_engine_picker_visible VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  published_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

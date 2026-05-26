CREATE SCHEMA IF NOT EXISTS time_labor;

CREATE TABLE time_labor_shift (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE time_labor_shift_pattern (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_shift_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_shift_swap_request (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_schedule_bid (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_labor_demand_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_clock_event (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_clock_device (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_clock_source_route (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_clock_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_entry_line (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_break_deduction (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_overtime_bucket (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_premium_calculation (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_holiday_calendar (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_absence (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_absence_balance (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_absence_entitlement (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_absence_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_labor_summary (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_labor_summary_line (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_labor_cost_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_labor_distribution (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_approval_workflow (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_approval_task (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_employee_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_role_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_payroll_labor_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_warehouse_site_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_manufacturing_shift_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_project_cost_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_audit_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_hours_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_carbon_schedule_window (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_schedule_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_shift_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_labor_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_labor_risk_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_parsed_event (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_labor_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_labor_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_time_labor_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  shift_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shift_id) REFERENCES time_labor_shift(id)
);

CREATE TABLE time_labor_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE time_labor_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE time_labor_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

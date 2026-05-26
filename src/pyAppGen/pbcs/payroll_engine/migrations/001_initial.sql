CREATE SCHEMA IF NOT EXISTS payroll_engine;

CREATE TABLE payroll_engine_payroll_calendar (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_period (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_pay_group (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_legal_entity (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_run (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_run_worker (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_run_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_run_lock (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_worker_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_worker_pay_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_worker_bank_instruction (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_labor_hours (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_labor_hours_line (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_earning_code (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_earning_calculation (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_overtime_calculation (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_gross_pay_component (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payslip (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payslip_line (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_tax_withholding_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_deduction (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_deduction_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_deduction_arrear (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_garnishment_order (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_benefit_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_benefit_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_employer_contribution (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_net_pay_distribution (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payment_instruction (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payment_batch_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_journal_request_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_tax_wage_base_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_filing (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_filing_line (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_correction (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_retro_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_off_cycle_payment (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_audit_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_carbon_batch_window (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_batch_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_cash_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_cash_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_parsed_instruction (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_engine_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_engine_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_payroll_engine_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  payroll_calendar_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (payroll_calendar_id) REFERENCES payroll_engine_payroll_calendar(id)
);

CREATE TABLE payroll_engine_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE payroll_engine_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE payroll_engine_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

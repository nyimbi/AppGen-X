CREATE SCHEMA IF NOT EXISTS payroll_engine;

CREATE TABLE payroll_engine_payroll_calendar (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  calendar_id VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  frequency VARCHAR(255) NOT NULL,
  timezone VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_period (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  period_id VARCHAR(255) NOT NULL,
  calendar_id VARCHAR(255) NOT NULL,
  period_start VARCHAR(255) NOT NULL,
  period_end VARCHAR(255) NOT NULL,
  pay_date TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_pay_group (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  pay_group_id VARCHAR(255) NOT NULL,
  legal_entity VARCHAR(255) NOT NULL,
  frequency VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_legal_entity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  legal_entity VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  tax_registration VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_run (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  period TIMESTAMP NOT NULL,
  country VARCHAR(255) NOT NULL,
  legal_entity VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  run_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_run_worker (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  run_worker_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  pay_group_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_run_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  approval_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  approver VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  decided_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_run_lock (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  lock_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  locked_by VARCHAR(255) NOT NULL,
  locked_at TIMESTAMP NOT NULL,
  reason VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_worker_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  worker_type VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  legal_entity VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  identity_hash VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_worker_pay_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  pay_group_id VARCHAR(255) NOT NULL,
  hourly_rate DECIMAL(18, 4) NOT NULL,
  salary_per_period VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_worker_bank_instruction (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  instruction_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  distribution_type VARCHAR(255) NOT NULL,
  tokenized_account_ref VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_labor_hours (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  labor_event_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  period TIMESTAMP NOT NULL,
  approved_hours VARCHAR(255) NOT NULL,
  overtime_hours VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_labor_hours_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  line_id VARCHAR(255) NOT NULL,
  labor_event_id VARCHAR(255) NOT NULL,
  earning_code VARCHAR(255) NOT NULL,
  hours VARCHAR(255) NOT NULL,
  source_event_id VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_earning_code (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  earning_code VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  taxable VARCHAR(255) NOT NULL,
  rate_multiplier DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_earning_calculation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  calculation_id VARCHAR(255) NOT NULL,
  payslip_id VARCHAR(255) NOT NULL,
  earning_code VARCHAR(255) NOT NULL,
  hours VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_overtime_calculation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  calculation_id VARCHAR(255) NOT NULL,
  payslip_id VARCHAR(255) NOT NULL,
  overtime_hours VARCHAR(255) NOT NULL,
  multiplier VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_gross_pay_component (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  component_id VARCHAR(255) NOT NULL,
  payslip_id VARCHAR(255) NOT NULL,
  component_type VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payslip (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  payslip_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  gross_pay VARCHAR(255) NOT NULL,
  tax_withheld VARCHAR(255) NOT NULL,
  net_pay VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payslip_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  line_id VARCHAR(255) NOT NULL,
  payslip_id VARCHAR(255) NOT NULL,
  line_type VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_tax_withholding_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  taxable_wages VARCHAR(255) NOT NULL,
  tax_withheld VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_deduction (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  deduction_id VARCHAR(255) NOT NULL,
  payslip_id VARCHAR(255) NOT NULL,
  deduction_type VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_deduction_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  deduction_rule_id VARCHAR(255) NOT NULL,
  deduction_type VARCHAR(255) NOT NULL,
  limit_percent VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_deduction_arrear (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  arrear_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  deduction_type VARCHAR(255) NOT NULL,
  amount_due DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_garnishment_order (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  remaining_amount DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_benefit_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  benefit_id VARCHAR(255) NOT NULL,
  payslip_id VARCHAR(255) NOT NULL,
  benefit_type VARCHAR(255) NOT NULL,
  employer_amount DECIMAL(18, 4) NOT NULL,
  employee_amount DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_benefit_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255) NOT NULL,
  benefit_type VARCHAR(255) NOT NULL,
  eligibility_rule_id VARCHAR(255) NOT NULL,
  employer_share VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_employer_contribution (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  contribution_id VARCHAR(255) NOT NULL,
  payslip_id VARCHAR(255) NOT NULL,
  benefit_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_net_pay_distribution (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  distribution_id VARCHAR(255) NOT NULL,
  payslip_id VARCHAR(255) NOT NULL,
  payment_instruction_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payment_instruction (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  payment_instruction_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  rail VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  tokenized_destination VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payment_batch_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  batch_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  rail VARCHAR(255) NOT NULL,
  net_total VARCHAR(255) NOT NULL,
  handoff_status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_journal_request_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  journal_request_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  gross_total VARCHAR(255) NOT NULL,
  net_total VARCHAR(255) NOT NULL,
  handoff_status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_tax_wage_base_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  wage_base VARCHAR(255) NOT NULL,
  withheld_total VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_filing (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  filing_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  gross_total VARCHAR(255) NOT NULL,
  net_total VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_filing_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  line_id VARCHAR(255) NOT NULL,
  filing_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  taxable_wages VARCHAR(255) NOT NULL,
  tax_withheld VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_correction (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  correction_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  payslip_id VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_retro_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  adjustment_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  source_period VARCHAR(255) NOT NULL,
  target_run_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_off_cycle_payment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  off_cycle_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  gross_pay VARCHAR(255) NOT NULL,
  net_pay VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE payroll_engine_payroll_exception (
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

CREATE TABLE payroll_engine_payroll_policy_screening (
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

CREATE TABLE payroll_engine_payroll_audit_trace (
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

CREATE TABLE payroll_engine_payroll_proof (
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

CREATE TABLE payroll_engine_payroll_federation_projection (
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

CREATE TABLE payroll_engine_payroll_carbon_batch_window (
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

CREATE TABLE payroll_engine_payroll_batch_optimization (
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

CREATE TABLE payroll_engine_payroll_cash_allocation (
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

CREATE TABLE payroll_engine_payroll_anomaly_signal (
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

CREATE TABLE payroll_engine_payroll_risk_model (
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

CREATE TABLE payroll_engine_payroll_cash_forecast (
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

CREATE TABLE payroll_engine_payroll_parsed_instruction (
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

CREATE TABLE payroll_engine_payroll_seed_data (
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

CREATE TABLE payroll_engine_payroll_schema_extension (
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

CREATE TABLE payroll_engine_payroll_control_assertion (
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

CREATE TABLE payroll_engine_payroll_governed_model (
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

CREATE TABLE payroll_engine_payroll_rule (
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

CREATE TABLE payroll_engine_payroll_parameter (
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

CREATE TABLE payroll_engine_payroll_configuration (
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

CREATE TABLE payroll_engine_appgen_outbox_event (
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

CREATE TABLE payroll_engine_appgen_inbox_event (
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

CREATE TABLE payroll_engine_dead_letter_event (
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

CREATE SCHEMA IF NOT EXISTS ar_credit;

CREATE TABLE ar_credit_ar_customer (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  default_probability VARCHAR(255) NOT NULL,
  credit_limit DECIMAL(18, 4) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_customer_site (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  site_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  address VARCHAR(255) NOT NULL,
  bill_to VARCHAR(255) NOT NULL,
  ship_to VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_ar_customer(customer_id)
);

CREATE TABLE ar_credit_ar_customer_graph (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  graph_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  parent VARCHAR(255) NOT NULL,
  owners VARCHAR(255) NOT NULL,
  network_hash VARCHAR(255) NOT NULL,
  risk_context VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_customer_credit_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  credit_profile_id DECIMAL(18, 4) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  credit_limit DECIMAL(18, 4) NOT NULL,
  risk_grade VARCHAR(255) NOT NULL,
  approval_state VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_ar_customer(customer_id)
);

CREATE TABLE ar_credit_ar_customer_payment_terms (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  terms_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  net_days VARCHAR(255) NOT NULL,
  discount_days VARCHAR(255) NOT NULL,
  discount_rate DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_ar_customer(customer_id)
);

CREATE TABLE ar_credit_ar_customer_risk_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  signal_type VARCHAR(255) NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  source VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_invoice (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  currency VARCHAR(255) NOT NULL,
  invoice_date TIMESTAMP NOT NULL,
  due_date TIMESTAMP NOT NULL,
  total VARCHAR(255) NOT NULL,
  open_amount DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_ar_customer(customer_id)
);

CREATE TABLE ar_credit_ar_invoice_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  invoice_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  sku VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  unit_price VARCHAR(255) NOT NULL,
  account VARCHAR(255) NOT NULL,
  tax_code VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (invoice_id) REFERENCES ar_credit_ar_invoice(invoice_id)
);

CREATE TABLE ar_credit_ar_invoice_tax (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  tax_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  rate DECIMAL(18, 4) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (invoice_id) REFERENCES ar_credit_ar_invoice(invoice_id)
);

CREATE TABLE ar_credit_ar_invoice_performance_obligation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  obligation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  obligation VARCHAR(255) NOT NULL,
  allocation VARCHAR(255) NOT NULL,
  satisfied VARCHAR(255) NOT NULL,
  recognized_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (invoice_id) REFERENCES ar_credit_ar_invoice(invoice_id)
);

CREATE TABLE ar_credit_ar_delivery_confirmation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  delivery_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  confirmed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_cash_receipt (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  receipt_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  bank_reference VARCHAR(255) NOT NULL,
  received_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_remittance_advice (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  remittance_id VARCHAR(255) PRIMARY KEY NOT NULL,
  receipt_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  parse_confidence DECIMAL(18, 4) NOT NULL,
  source_hash VARCHAR(255) NOT NULL,
  bank_reference VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_cash_application (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  application_id VARCHAR(255) PRIMARY KEY NOT NULL,
  receipt_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  applied_amount DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (invoice_id) REFERENCES ar_credit_ar_invoice(invoice_id)
);

CREATE TABLE ar_credit_ar_unapplied_cash (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  receipt_id VARCHAR(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  resolution_trace VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_memo (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  credit_memo_id DECIMAL(18, 4) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (invoice_id) REFERENCES ar_credit_ar_invoice(invoice_id)
);

CREATE TABLE ar_credit_ar_write_off (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  write_off_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_refund (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  refund_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_dispute_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  dispute_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  reason VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  audit_trace VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_collection_action (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  action_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  due_date TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_dunning_notice (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  notice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  level VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  days_past_due VARCHAR(255) NOT NULL,
  sent_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_statement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  statement_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  as_of VARCHAR(255) NOT NULL,
  open_balance DECIMAL(18, 4) NOT NULL,
  statement_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_ar_customer(customer_id)
);

CREATE TABLE ar_credit_ar_revenue_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schedule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  recognized_amount DECIMAL(18, 4) NOT NULL,
  deferred_amount DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (invoice_id) REFERENCES ar_credit_ar_invoice(invoice_id)
);

CREATE TABLE ar_credit_ar_revenue_schedule_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schedule_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  schedule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  obligation VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  recognized VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_cash_pool (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  cash_pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  currency VARCHAR(255) NOT NULL,
  received_cash VARCHAR(255) NOT NULL,
  unapplied_cash VARCHAR(255) NOT NULL,
  as_of VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  recommended_limit VARCHAR(255) NOT NULL,
  risk_adjusted_score DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_e_invoice_submission (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  submission_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  standard VARCHAR(255) NOT NULL,
  submission_hash VARCHAR(255) NOT NULL,
  accepted VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_cross_border_receivable (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  federation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  target_country VARCHAR(255) NOT NULL,
  settlement_amount DECIMAL(18, 4) NOT NULL,
  message_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_invoice_finance_program (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  finance_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  program VARCHAR(255) NOT NULL,
  advance_amount DECIMAL(18, 4) NOT NULL,
  counterparty VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  predicate TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  bounds VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) PRIMARY KEY NOT NULL,
  table_name VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  control_id VARCHAR(255) PRIMARY KEY NOT NULL,
  assertion VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  tested_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_ar_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  feature_lineage VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  governance_status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

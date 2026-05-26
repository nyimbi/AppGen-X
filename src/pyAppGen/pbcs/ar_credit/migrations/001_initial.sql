CREATE SCHEMA IF NOT EXISTS ar_credit;

CREATE TABLE ar_credit_customer (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ar_credit_customer_site (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_customer_graph (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_customer_credit_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_customer_payment_terms (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_customer_risk_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_invoice (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_invoice_line (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_invoice_tax (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_invoice_performance_obligation (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_delivery_confirmation (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_cash_receipt (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_remittance_advice (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_cash_application (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_unapplied_cash (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_credit_memo (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_write_off (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_refund (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_dispute_case (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_collection_action (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_dunning_notice (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_statement (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_revenue_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_revenue_schedule_line (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_cash_pool (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_credit_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_e_invoice_submission (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_cross_border_receivable (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_invoice_finance_program (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  customer_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES ar_credit_customer(id)
);

CREATE TABLE ar_credit_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE ar_credit_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE ar_credit_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

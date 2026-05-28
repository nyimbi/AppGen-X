CREATE SCHEMA IF NOT EXISTS subscription_billing;

CREATE TABLE subscription_billing_plan_catalog (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255) PRIMARY KEY NOT NULL,
  family VARCHAR(255) NOT NULL,
  name VARCHAR(255) PRIMARY KEY NOT NULL,
  currency VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  billing_period VARCHAR(255) NOT NULL,
  base_price VARCHAR(255) NOT NULL,
  usage_rate DECIMAL(18, 4) NOT NULL,
  included_units VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (plan_id) REFERENCES subscription_billing_subscription(plan_id)
);

CREATE TABLE subscription_billing_subscription (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  subscription_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  plan_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  mrr VARCHAR(255) NOT NULL,
  renewal_confidence DECIMAL(18, 4) NOT NULL,
  churn_risk VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (subscription_id) REFERENCES subscription_billing_subscription_phase(subscription_id),
  FOREIGN KEY (subscription_id) REFERENCES subscription_billing_subscription_addon(subscription_id),
  FOREIGN KEY (subscription_id) REFERENCES subscription_billing_subscription_change_order(subscription_id),
  FOREIGN KEY (subscription_id) REFERENCES subscription_billing_billing_schedule(subscription_id),
  FOREIGN KEY (subscription_id) REFERENCES subscription_billing_usage_meter(subscription_id),
  FOREIGN KEY (subscription_id) REFERENCES subscription_billing_invoice(subscription_id),
  FOREIGN KEY (subscription_id) REFERENCES subscription_billing_entitlement_grant(subscription_id),
  FOREIGN KEY (subscription_id) REFERENCES subscription_billing_dunning_notice(subscription_id),
  FOREIGN KEY (subscription_id) REFERENCES subscription_billing_billing_exception(subscription_id)
);

CREATE TABLE subscription_billing_subscription_phase (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  phase_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) PRIMARY KEY NOT NULL,
  plan_id VARCHAR(255) NOT NULL,
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_trial_period (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  trial_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  plan_id VARCHAR(255) NOT NULL,
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP NOT NULL,
  conversion_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_subscription_addon (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  addon_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  unit_price VARCHAR(255) NOT NULL,
  mrr_delta VARCHAR(255) NOT NULL,
  effective_date TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_subscription_change_order (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  change_order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) PRIMARY KEY NOT NULL,
  from_plan_id VARCHAR(255) NOT NULL,
  to_plan_id VARCHAR(255) NOT NULL,
  effective_date TIMESTAMP NOT NULL,
  reason VARCHAR(255) NOT NULL,
  proration_amount DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_usage_meter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  usage_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) PRIMARY KEY NOT NULL,
  meter_name VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  billable_units VARCHAR(255) NOT NULL,
  rated_amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_billing_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  subscription_id VARCHAR(255) PRIMARY KEY NOT NULL,
  next_invoice_date TIMESTAMP NOT NULL,
  period TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_invoice (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  period TIMESTAMP NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  usage_amount DECIMAL(18, 4) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (invoice_id) REFERENCES subscription_billing_invoice_line(invoice_id),
  FOREIGN KEY (invoice_id) REFERENCES subscription_billing_credit_memo(invoice_id),
  FOREIGN KEY (invoice_id) REFERENCES subscription_billing_payment_application(invoice_id),
  FOREIGN KEY (invoice_id) REFERENCES subscription_billing_revenue_schedule(invoice_id)
);

CREATE TABLE subscription_billing_invoice_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  invoice_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) NOT NULL,
  line_type VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  unit_price VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_credit_memo (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  credit_memo_id DECIMAL(18, 4) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_payment_application (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  payment_application_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) NOT NULL,
  payment_event_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_dunning_notice (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  dunning_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  retry_policy VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_entitlement_grant (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  entitlement_grant_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  entitlement_key VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  projection VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_revenue_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  revenue_schedule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) NOT NULL,
  period TIMESTAMP NOT NULL,
  recognition_type VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  ledger_handoff VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_billing_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subscription_id VARCHAR(255) PRIMARY KEY NOT NULL,
  exception_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  recommended_action VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_billing_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rule_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  allowed_plan_families VARCHAR(255) NOT NULL,
  allowed_currencies VARCHAR(255) NOT NULL,
  allowed_regions VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_billing_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  name VARCHAR(255) PRIMARY KEY NOT NULL,
  value VARCHAR(255) NOT NULL,
  bounds VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_billing_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_currency VARCHAR(255) NOT NULL,
  supported_currencies VARCHAR(255) NOT NULL,
  supported_regions VARCHAR(255) NOT NULL,
  billing_calendars VARCHAR(255) NOT NULL,
  default_timezone VARCHAR(255) NOT NULL,
  invoice_approval_mode VARCHAR(255) NOT NULL,
  workbench_limit VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_billing_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  table VARCHAR(255) PRIMARY KEY NOT NULL,
  fields VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  retry_policy VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_billing_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

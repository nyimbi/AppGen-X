CREATE SCHEMA IF NOT EXISTS price_promotion_engine;

CREATE TABLE price_promotion_engine_price_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_currency VARCHAR(255) NOT NULL,
  default_timezone VARCHAR(255) NOT NULL,
  approval_mode VARCHAR(255) NOT NULL,
  simulation_horizon_days VARCHAR(255) NOT NULL,
  telemetry_window_minutes VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE price_promotion_engine_price_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  bounds VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (parameter_name) REFERENCES price_promotion_engine_price_configuration(configuration_id)
);

CREATE TABLE price_promotion_engine_price_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  allowed_currencies VARCHAR(255) NOT NULL,
  allowed_regions VARCHAR(255) NOT NULL,
  allowed_segments VARCHAR(255) NOT NULL,
  promotion_policy VARCHAR(255) NOT NULL,
  margin_policy VARCHAR(255) NOT NULL,
  stacking_policy VARCHAR(255) NOT NULL,
  exclusion_policy VARCHAR(255) NOT NULL,
  approval_policy VARCHAR(255) NOT NULL,
  budget_policy VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (rule_id) REFERENCES price_promotion_engine_price_configuration(configuration_id)
);

CREATE TABLE price_promotion_engine_price_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) NOT NULL,
  table_name VARCHAR(255) NOT NULL,
  fields VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (table_name) REFERENCES price_promotion_engine_price_policy_rule(rule_id)
);

CREATE TABLE price_promotion_engine_price_list (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  price_list_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  calendar VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE price_promotion_engine_price_book (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  price_book_id VARCHAR(255) NOT NULL,
  price_list_id VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (price_list_id) REFERENCES price_promotion_engine_price_list(price_list_id)
);

CREATE TABLE price_promotion_engine_price_book_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  price_book_entry_id VARCHAR(255) NOT NULL,
  price_book_id VARCHAR(255) NOT NULL,
  price_rule_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  base_price VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (price_book_id) REFERENCES price_promotion_engine_price_book(price_book_id),
  FOREIGN KEY (price_rule_id) REFERENCES price_promotion_engine_price_rule(price_rule_id)
);

CREATE TABLE price_promotion_engine_price_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  price_rule_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  price_list_id VARCHAR(255) NOT NULL,
  price_book_id VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  base_price VARCHAR(255) NOT NULL,
  cost DECIMAL(18, 4) NOT NULL,
  margin_percent VARCHAR(255) NOT NULL,
  segments VARCHAR(255) NOT NULL,
  volume_breaks VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE price_promotion_engine_price_agreement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  agreement_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  contracted_price VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sku) REFERENCES price_promotion_engine_price_rule(sku)
);

CREATE TABLE price_promotion_engine_customer_price (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  customer_price_id VARCHAR(255) NOT NULL,
  price_rule_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  price VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (price_rule_id) REFERENCES price_promotion_engine_price_rule(price_rule_id)
);

CREATE TABLE price_promotion_engine_channel_price (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  channel_price_id VARCHAR(255) NOT NULL,
  price_rule_id VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  price VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (price_rule_id) REFERENCES price_promotion_engine_price_rule(price_rule_id)
);

CREATE TABLE price_promotion_engine_currency_price (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  currency_price_id VARCHAR(255) NOT NULL,
  price_rule_id VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  base_price VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (price_rule_id) REFERENCES price_promotion_engine_price_rule(price_rule_id)
);

CREATE TABLE price_promotion_engine_trade_promotion_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255) NOT NULL,
  promotion_id VARCHAR(255) NOT NULL,
  calendar VARCHAR(255) NOT NULL,
  target_uplift_percent VARCHAR(255) NOT NULL,
  spend_amount DECIMAL(18, 4) NOT NULL,
  owner_role VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (promotion_id) REFERENCES price_promotion_engine_promotion(promotion_id)
);

CREATE TABLE price_promotion_engine_promotion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  promotion_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  discount_percent VARCHAR(255) NOT NULL,
  channels VARCHAR(255) NOT NULL,
  currencies VARCHAR(255) NOT NULL,
  regions VARCHAR(255) NOT NULL,
  segments VARCHAR(255) NOT NULL,
  customer_ids VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE price_promotion_engine_promotion_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  promotion_rule_id VARCHAR(255) NOT NULL,
  promotion_id VARCHAR(255) NOT NULL,
  policy VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (promotion_id) REFERENCES price_promotion_engine_promotion(promotion_id)
);

CREATE TABLE price_promotion_engine_coupon (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  coupon_id VARCHAR(255) NOT NULL,
  promotion_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  reuse_limit VARCHAR(255) NOT NULL,
  redemption_count INTEGER NOT NULL,
  redeemed_decision_ids VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (promotion_id) REFERENCES price_promotion_engine_promotion(promotion_id)
);

CREATE TABLE price_promotion_engine_promotion_eligibility (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  eligibility_id VARCHAR(255) NOT NULL,
  promotion_id VARCHAR(255) NOT NULL,
  segments VARCHAR(255) NOT NULL,
  regions VARCHAR(255) NOT NULL,
  currencies VARCHAR(255) NOT NULL,
  channels VARCHAR(255) NOT NULL,
  customer_ids VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (promotion_id) REFERENCES price_promotion_engine_promotion(promotion_id)
);

CREATE TABLE price_promotion_engine_promotion_stacking_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  stacking_policy_id VARCHAR(255) NOT NULL,
  promotion_id VARCHAR(255) NOT NULL,
  stackable VARCHAR(255) NOT NULL,
  stack_limit VARCHAR(255) NOT NULL,
  mutual_group VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (promotion_id) REFERENCES price_promotion_engine_promotion(promotion_id)
);

CREATE TABLE price_promotion_engine_promotion_exclusion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  promotion_exclusion_id VARCHAR(255) NOT NULL,
  promotion_id VARCHAR(255) NOT NULL,
  excluded_promotion_ids VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (promotion_id) REFERENCES price_promotion_engine_promotion(promotion_id)
);

CREATE TABLE price_promotion_engine_campaign_budget (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  campaign_budget_id VARCHAR(255) NOT NULL,
  promotion_id VARCHAR(255) NOT NULL,
  budget_amount DECIMAL(18, 4) NOT NULL,
  consumed_amount DECIMAL(18, 4) NOT NULL,
  budget_currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (promotion_id) REFERENCES price_promotion_engine_promotion(promotion_id)
);

CREATE TABLE price_promotion_engine_promotion_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  promotion_approval_id VARCHAR(255) NOT NULL,
  promotion_id VARCHAR(255) NOT NULL,
  approval_required VARCHAR(255) NOT NULL,
  approval_status VARCHAR(255) NOT NULL,
  approver_role VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (promotion_id) REFERENCES price_promotion_engine_promotion(promotion_id)
);

CREATE TABLE price_promotion_engine_promotion_accrual (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  accrual_id VARCHAR(255) NOT NULL,
  promotion_id VARCHAR(255) NOT NULL,
  decision_id VARCHAR(255) NOT NULL,
  accrual_amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (promotion_id) REFERENCES price_promotion_engine_promotion(promotion_id),
  FOREIGN KEY (decision_id) REFERENCES price_promotion_engine_price_decision(decision_id)
);

CREATE TABLE price_promotion_engine_promotion_settlement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  settlement_id VARCHAR(255) NOT NULL,
  accrual_id VARCHAR(255) NOT NULL,
  promotion_id VARCHAR(255) NOT NULL,
  settled_amount DECIMAL(18, 4) NOT NULL,
  settled_by VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (accrual_id) REFERENCES price_promotion_engine_promotion_accrual(accrual_id)
);

CREATE TABLE price_promotion_engine_loyalty_tier (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  tier_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  rank VARCHAR(255) NOT NULL,
  discount_percent VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE price_promotion_engine_price_exception_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) NOT NULL,
  subject_type VARCHAR(255) NOT NULL,
  subject_id VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  resolution VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (subject_id) REFERENCES price_promotion_engine_price_decision(decision_id)
);

CREATE TABLE price_promotion_engine_price_simulation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  simulation_id VARCHAR(255) NOT NULL,
  decision_id VARCHAR(255) NOT NULL,
  scenario_count INTEGER NOT NULL,
  counterfactuals VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (decision_id) REFERENCES price_promotion_engine_price_decision(decision_id)
);

CREATE TABLE price_promotion_engine_price_margin_guardrail (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  guardrail_id VARCHAR(255) NOT NULL,
  subject_type VARCHAR(255) NOT NULL,
  subject_id VARCHAR(255) NOT NULL,
  margin_floor_percent VARCHAR(255) NOT NULL,
  discount_ceiling_percent VARCHAR(255) NOT NULL,
  breach VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (subject_id) REFERENCES price_promotion_engine_price_decision(decision_id)
);

CREATE TABLE price_promotion_engine_price_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  decision_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  price_book_id VARCHAR(255) NOT NULL,
  price_list_id VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  base_price VARCHAR(255) NOT NULL,
  optimized_unit_price VARCHAR(255) NOT NULL,
  extended_price VARCHAR(255) NOT NULL,
  total_discount_percent VARCHAR(255) NOT NULL,
  margin_percent VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  eligible_promotions VARCHAR(255) NOT NULL,
  applied_promotions VARCHAR(255) NOT NULL,
  counterfactuals VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE price_promotion_engine_price_audit_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  trace_id VARCHAR(255) NOT NULL,
  trace_type VARCHAR(255) NOT NULL,
  subject_id VARCHAR(255) NOT NULL,
  related_tables VARCHAR(255) NOT NULL,
  trace_hash VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (subject_id) REFERENCES price_promotion_engine_price_decision(decision_id)
);

CREATE TABLE price_promotion_engine_price_performance_telemetry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  telemetry_id VARCHAR(255) NOT NULL,
  metric_key VARCHAR(255) NOT NULL,
  subject_id VARCHAR(255) NOT NULL,
  sample_ms VARCHAR(255) NOT NULL,
  rule_hits VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (subject_id) REFERENCES price_promotion_engine_price_decision(decision_id)
);

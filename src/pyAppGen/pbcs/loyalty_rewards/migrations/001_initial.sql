CREATE SCHEMA IF NOT EXISTS loyalty_rewards;

CREATE TABLE loyalty_rewards_reward_account (
  id INTEGER PRIMARY KEY NOT NULL,
  account_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  tier VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  balance DECIMAL(18, 4) NOT NULL,
  lifetime_points VARCHAR(255) NOT NULL,
  liability_amount DECIMAL(18, 4) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_points_ledger (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_id VARCHAR(255) PRIMARY KEY NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  entry_type VARCHAR(255) NOT NULL,
  points VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  source_ref VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_earning_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  earning_rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  activity_type VARCHAR(255) NOT NULL,
  points_per_currency_unit VARCHAR(255) NOT NULL,
  tier_multipliers VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_redemption (
  id INTEGER PRIMARY KEY NOT NULL,
  redemption_id VARCHAR(255) PRIMARY KEY NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  points VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  monetary_value VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_reward_tier (
  id INTEGER PRIMARY KEY NOT NULL,
  account_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  tier VARCHAR(255) NOT NULL,
  lifetime_points VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  qualified_at TIMESTAMP NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_tier_benefit (
  id INTEGER PRIMARY KEY NOT NULL,
  account_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  tier VARCHAR(255) NOT NULL,
  benefits VARCHAR(255) NOT NULL,
  benefit_count INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_referral_reward (
  id INTEGER PRIMARY KEY NOT NULL,
  referral_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  referred_customer_id VARCHAR(255) NOT NULL,
  points VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_partner_accrual (
  id INTEGER PRIMARY KEY NOT NULL,
  partner_accrual_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  partner_id VARCHAR(255) NOT NULL,
  activity_ref VARCHAR(255) NOT NULL,
  points VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_offer_eligibility (
  id INTEGER PRIMARY KEY NOT NULL,
  eligibility_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  offer_id VARCHAR(255) NOT NULL,
  required_tier VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  account_tier VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_expiration_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  schedule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  points VARCHAR(255) NOT NULL,
  expires_in_days VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_liability_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  snapshot_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  liability_amount DECIMAL(18, 4) NOT NULL,
  reserve_amount DECIMAL(18, 4) NOT NULL,
  account_count INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_fraud_review (
  id INTEGER PRIMARY KEY NOT NULL,
  review_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  signals VARCHAR(255) NOT NULL,
  fraud_score DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_churn_risk_score (
  id INTEGER PRIMARY KEY NOT NULL,
  score_id DECIMAL(18, 4) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  churn_risk VARCHAR(255) NOT NULL,
  risk_band VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_breakage_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  forecast_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  horizon_days VARCHAR(255) NOT NULL,
  outstanding_points VARCHAR(255) NOT NULL,
  expected_breakage_points VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_offer_simulation (
  id INTEGER PRIMARY KEY NOT NULL,
  simulation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  offer_id VARCHAR(255) NOT NULL,
  bonus_multiplier VARCHAR(255) NOT NULL,
  current_balance DECIMAL(18, 4) NOT NULL,
  projected_balance DECIMAL(18, 4) NOT NULL,
  incremental_points VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_loyalty_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  exception_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  resolution VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_balance_reconciliation (
  id INTEGER PRIMARY KEY NOT NULL,
  reconciliation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  recorded_balance DECIMAL(18, 4) NOT NULL,
  computed_balance DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_reward_balance_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  proof_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  balance DECIMAL(18, 4) NOT NULL,
  ledger_hash VARCHAR(255) NOT NULL,
  account_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_loyalty_audit_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  audit_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  action VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  payload TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_rewards_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  screening_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  activity_type VARCHAR(255) NOT NULL,
  points VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  max_daily_earn_points VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_liability_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  assertion_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  liability_amount DECIMAL(18, 4) NOT NULL,
  reserve_amount DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  checked_at TIMESTAMP NOT NULL,
  control_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_loyalty_federation_view (
  id INTEGER PRIMARY KEY NOT NULL,
  view_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  balance DECIMAL(18, 4) NOT NULL,
  tier VARCHAR(255) NOT NULL,
  projection_sources VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE loyalty_rewards_loyalty_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_type VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  training_boundary VARCHAR(255) NOT NULL,
  governance_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

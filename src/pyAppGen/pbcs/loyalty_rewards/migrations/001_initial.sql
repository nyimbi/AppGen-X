CREATE SCHEMA IF NOT EXISTS loyalty_rewards;

CREATE TABLE loyalty_rewards_reward_account (
  id INTEGER PRIMARY KEY NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  currency VARCHAR(16) NOT NULL,
  region VARCHAR(64) NOT NULL,
  tier VARCHAR(64) NOT NULL,
  status VARCHAR(255) NOT NULL,
  balance DECIMAL(18, 6) NOT NULL,
  lifetime_points DECIMAL(18, 6) NOT NULL,
  liability_amount DECIMAL(18, 6) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (account_id)
);

CREATE TABLE loyalty_rewards_points_ledger (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_id VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  entry_type VARCHAR(64) NOT NULL,
  points DECIMAL(18, 6) NOT NULL,
  source VARCHAR(255) NOT NULL,
  source_ref VARCHAR(255),
  audit_proof VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (ledger_id),
  FOREIGN KEY (account_id) REFERENCES loyalty_rewards_reward_account(account_id)
);

CREATE TABLE loyalty_rewards_earning_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  earning_rule_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  activity_type VARCHAR(255) NOT NULL,
  points_per_currency_unit DECIMAL(18, 6) NOT NULL,
  tier_multipliers TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (earning_rule_id)
);

CREATE TABLE loyalty_rewards_redemption (
  id INTEGER PRIMARY KEY NOT NULL,
  redemption_id VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  points DECIMAL(18, 6) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  monetary_value DECIMAL(18, 6) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (redemption_id),
  FOREIGN KEY (account_id) REFERENCES loyalty_rewards_reward_account(account_id)
);

CREATE TABLE loyalty_rewards_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  contract VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE loyalty_rewards_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  handler VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE loyalty_rewards_dead_letter_event (
  id INTEGER PRIMARY KEY,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  handler VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

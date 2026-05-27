CREATE SCHEMA IF NOT EXISTS treasury_cash;

CREATE TABLE treasury_cash_bank_account (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE treasury_cash_bank_account_signatory (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_bank_counterparty (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_bank_topology (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_balance (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_intraday_balance (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_statement (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_statement_line (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_reconciliation_match (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_reconciliation_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_cash_position (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_cash_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_cash_forecast_line (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_liquidity_pool (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_liquidity_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_sweep_instruction (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_concentration_run (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_intercompany_netting (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_in_house_bank_account (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_payment_funding (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_payment_rail_route (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_fx_exposure (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_hedge_recommendation (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_capital_action (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_debt_facility (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_debt_draw (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_investment (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_bank_fee (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_covenant_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_cross_border_liquidity (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_working_capital_finance (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_counterparty_risk_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  bank_account_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bank_account_id) REFERENCES treasury_cash_bank_account(id)
);

CREATE TABLE treasury_cash_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE treasury_cash_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE treasury_cash_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

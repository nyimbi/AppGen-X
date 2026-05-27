CREATE SCHEMA IF NOT EXISTS checkout_processing;

CREATE TABLE checkout_processing_cart (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE checkout_processing_cart_line (
  id INTEGER PRIMARY KEY NOT NULL,
  cart_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (cart_id) REFERENCES checkout_processing_cart(id)
);

CREATE TABLE checkout_processing_checkout_session (
  id INTEGER PRIMARY KEY NOT NULL,
  cart_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (cart_id) REFERENCES checkout_processing_cart(id)
);

CREATE TABLE checkout_processing_promotion_redemption (
  id INTEGER PRIMARY KEY NOT NULL,
  cart_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (cart_id) REFERENCES checkout_processing_cart(id)
);

CREATE TABLE checkout_processing_checkout_pricing_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  pricing_handoff_id VARCHAR(255) NOT NULL,
  session_id VARCHAR(255) NOT NULL,
  cart_id VARCHAR(255) NOT NULL,
  currency VARCHAR(32) NOT NULL,
  subtotal DECIMAL(18, 4) NOT NULL,
  discount_total DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL
);

CREATE TABLE checkout_processing_checkout_tax_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  tax_handoff_id VARCHAR(255) NOT NULL,
  session_id VARCHAR(255) NOT NULL,
  cart_id VARCHAR(255) NOT NULL,
  calculation_id VARCHAR(255) NOT NULL,
  tax_total DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL
);

CREATE TABLE checkout_processing_checkout_inventory_reservation_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  inventory_handoff_id VARCHAR(255) NOT NULL,
  session_id VARCHAR(255) NOT NULL,
  reservation_id VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 8) NOT NULL,
  status VARCHAR(255) NOT NULL
);

CREATE TABLE checkout_processing_checkout_payment_intent_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  payment_handoff_id VARCHAR(255) NOT NULL,
  session_id VARCHAR(255) NOT NULL,
  payment_intent_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  method VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL
);

CREATE TABLE checkout_processing_checkout_risk_screen (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  session_id VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 8) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  signals TEXT NOT NULL
);

CREATE TABLE checkout_processing_checkout_address_validation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  cart_id VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  shipping_option VARCHAR(255) NOT NULL,
  shipping_total DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL
);

CREATE TABLE checkout_processing_checkout_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  compiled_expression TEXT NOT NULL
);

CREATE TABLE checkout_processing_checkout_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  value TEXT NOT NULL,
  tenant_scope VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL
);

CREATE TABLE checkout_processing_checkout_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit INTEGER NOT NULL,
  default_currency VARCHAR(32) NOT NULL,
  default_country VARCHAR(255) NOT NULL
);

CREATE TABLE checkout_processing_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE checkout_processing_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE checkout_processing_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

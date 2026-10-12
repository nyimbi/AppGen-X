CREATE SCHEMA IF NOT EXISTS checkout_processing;

CREATE TABLE checkout_processing_cart (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  cart_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255),
  channel VARCHAR(255) NOT NULL,
  currency VARCHAR(32) NOT NULL,
  market VARCHAR(255),
  subtotal DECIMAL(18, 4) NOT NULL,
  discount_total DECIMAL(18, 4) NOT NULL,
  tax_total DECIMAL(18, 4) NOT NULL,
  shipping_total DECIMAL(18, 4) NOT NULL,
  total DECIMAL(18, 4) NOT NULL,
  code VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE checkout_processing_cart_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  line_id VARCHAR(255) NOT NULL,
  cart_id VARCHAR(255) NOT NULL,
  product_id VARCHAR(255) NOT NULL,
  product_variant VARCHAR(255),
  product_title VARCHAR(255),
  unit VARCHAR(255),
  quantity INTEGER NOT NULL,
  unit_price DECIMAL(18, 4) NOT NULL,
  extended_price DECIMAL(18, 4) NOT NULL,
  tax_class VARCHAR(255),
  inventory_eligible BOOLEAN NOT NULL,
  source_event_version VARCHAR(255),
  code VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (cart_id) REFERENCES checkout_processing_cart(cart_id)
);

CREATE TABLE checkout_processing_checkout_session (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  session_id VARCHAR(255) NOT NULL,
  cart_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255),
  pricing_handoff_id VARCHAR(255),
  tax_handoff_id VARCHAR(255),
  inventory_handoff_id VARCHAR(255),
  payment_handoff_id VARCHAR(255),
  risk_decision VARCHAR(255),
  total DECIMAL(18, 4) NOT NULL,
  code VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (cart_id) REFERENCES checkout_processing_cart(cart_id)
);

CREATE TABLE checkout_processing_promotion_redemption (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  redemption_id VARCHAR(255) NOT NULL,
  cart_id VARCHAR(255) NOT NULL,
  coupon_code VARCHAR(255) NOT NULL,
  campaign VARCHAR(255),
  discount_rate DECIMAL(18, 8) NOT NULL,
  discount_total DECIMAL(18, 4) NOT NULL,
  usage_cap INTEGER,
  stackable BOOLEAN NOT NULL,
  code VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (cart_id) REFERENCES checkout_processing_cart(cart_id)
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
  fees_total DECIMAL(18, 4) NOT NULL,
  rounding_adjustment DECIMAL(18, 4) NOT NULL,
  price_version VARCHAR(255),
  quote_expires_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (session_id) REFERENCES checkout_processing_checkout_session(session_id)
);

CREATE TABLE checkout_processing_checkout_tax_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  tax_handoff_id VARCHAR(255) NOT NULL,
  session_id VARCHAR(255) NOT NULL,
  cart_id VARCHAR(255) NOT NULL,
  calculation_id VARCHAR(255) NOT NULL,
  taxable_basis DECIMAL(18, 4) NOT NULL,
  jurisdiction VARCHAR(255),
  tax_total DECIMAL(18, 4) NOT NULL,
  tax_inclusive BOOLEAN NOT NULL,
  quote_expires_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (session_id) REFERENCES checkout_processing_checkout_session(session_id)
);

CREATE TABLE checkout_processing_checkout_inventory_reservation_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  inventory_handoff_id VARCHAR(255) NOT NULL,
  session_id VARCHAR(255) NOT NULL,
  reservation_id VARCHAR(255) NOT NULL,
  reservation_state VARCHAR(255) NOT NULL,
  quantity INTEGER NOT NULL,
  fulfillment_node VARCHAR(255),
  ttl_minutes INTEGER,
  confidence DECIMAL(18, 8) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (session_id) REFERENCES checkout_processing_checkout_session(session_id)
);

CREATE TABLE checkout_processing_checkout_payment_intent_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  payment_handoff_id VARCHAR(255) NOT NULL,
  session_id VARCHAR(255) NOT NULL,
  payment_intent_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(32) NOT NULL,
  method VARCHAR(255) NOT NULL,
  authorization_id VARCHAR(255),
  capture_id VARCHAR(255),
  retry_count INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (session_id) REFERENCES checkout_processing_checkout_session(session_id)
);

CREATE TABLE checkout_processing_checkout_risk_screen (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  session_id VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 8) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  score_factors TEXT,
  model_version VARCHAR(255),
  rule_hits TEXT,
  reviewer VARCHAR(255),
  expires_at TIMESTAMP,
  signals TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (session_id) REFERENCES checkout_processing_checkout_session(session_id)
);

CREATE TABLE checkout_processing_checkout_address_validation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  cart_id VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  region VARCHAR(255),
  city VARCHAR(255),
  postal_code VARCHAR(255),
  normalized_address TEXT,
  confidence DECIMAL(18, 8) NOT NULL,
  deliverable BOOLEAN NOT NULL,
  restricted_destination BOOLEAN NOT NULL,
  customer_override BOOLEAN NOT NULL,
  provider VARCHAR(255),
  shipping_option VARCHAR(255) NOT NULL,
  shipping_total DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (cart_id) REFERENCES checkout_processing_cart(cart_id)
);

CREATE TABLE checkout_processing_checkout_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  promotion_policy TEXT NOT NULL,
  shipping_policy TEXT NOT NULL,
  risk_policy TEXT NOT NULL,
  payment_policy TEXT NOT NULL,
  enabled BOOLEAN NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  compiled_expression TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE checkout_processing_checkout_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  value TEXT NOT NULL,
  tenant_scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  effective_from TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE checkout_processing_checkout_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit INTEGER NOT NULL,
  default_currency VARCHAR(32) NOT NULL,
  default_country VARCHAR(255) NOT NULL,
  workbench_limit INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE checkout_processing_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE checkout_processing_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE checkout_processing_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP,
  updated_at TIMESTAMP NOT NULL
);

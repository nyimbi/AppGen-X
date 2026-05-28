CREATE SCHEMA IF NOT EXISTS cross_border_trade;

CREATE TABLE cross_border_trade_hs_classification (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  classification_id VARCHAR(255) NOT NULL,
  product_id VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  hs_code VARCHAR(255) NOT NULL,
  country_of_origin VARCHAR(255) NOT NULL,
  destination_country VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  review_required VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  audit_evidence_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (classification_id) REFERENCES cross_border_trade_landed_cost_quote(classification_id),
  FOREIGN KEY (classification_id) REFERENCES cross_border_trade_export_control_check(classification_id)
);

CREATE TABLE cross_border_trade_landed_cost_quote (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  quote_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  classification_id VARCHAR(255) NOT NULL,
  incoterm VARCHAR(255) NOT NULL,
  origin_country VARCHAR(255) NOT NULL,
  destination_country VARCHAR(255) NOT NULL,
  goods_value VARCHAR(255) NOT NULL,
  shipping_cost DECIMAL(18, 4) NOT NULL,
  duty VARCHAR(255) NOT NULL,
  tax VARCHAR(255) NOT NULL,
  insurance VARCHAR(255) NOT NULL,
  broker_fee VARCHAR(255) NOT NULL,
  landed_total VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (quote_id) REFERENCES cross_border_trade_customs_declaration(quote_id)
);

CREATE TABLE cross_border_trade_export_control_check (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  check_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  classification_id VARCHAR(255) NOT NULL,
  destination_country VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  license_required VARCHAR(255) NOT NULL,
  denied_party_hits VARCHAR(255) NOT NULL,
  country_restriction_status VARCHAR(255) NOT NULL,
  compliance_hold VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (check_id) REFERENCES cross_border_trade_denied_party_screening(check_id),
  FOREIGN KEY (check_id) REFERENCES cross_border_trade_customs_declaration(check_id)
);

CREATE TABLE cross_border_trade_customs_declaration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  declaration_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  quote_id VARCHAR(255) NOT NULL,
  check_id VARCHAR(255) NOT NULL,
  document_packet_id VARCHAR(255) NOT NULL,
  broker_handoff_id VARCHAR(255) NOT NULL,
  carrier_handoff_id VARCHAR(255) NOT NULL,
  country_restriction_status VARCHAR(255) NOT NULL,
  compliance_hold VARCHAR(255) NOT NULL,
  customs_documents_complete VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_evidence_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (declaration_id) REFERENCES cross_border_trade_trade_document_packet(declaration_id),
  FOREIGN KEY (declaration_id) REFERENCES cross_border_trade_broker_handoff(declaration_id),
  FOREIGN KEY (declaration_id) REFERENCES cross_border_trade_carrier_handoff(declaration_id),
  FOREIGN KEY (declaration_id) REFERENCES cross_border_trade_trade_compliance_hold(entity_id)
);

CREATE TABLE cross_border_trade_denied_party_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  screening_id VARCHAR(255) NOT NULL,
  check_id VARCHAR(255) NOT NULL,
  matches VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_trade_document_packet (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  packet_id VARCHAR(255) NOT NULL,
  declaration_id VARCHAR(255) NOT NULL,
  documents VARCHAR(255) NOT NULL,
  missing_documents VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_broker_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  handoff_id VARCHAR(255) NOT NULL,
  declaration_id VARCHAR(255) NOT NULL,
  broker_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  submission_payload TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_carrier_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  handoff_id VARCHAR(255) NOT NULL,
  declaration_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  carrier_ref VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_trade_compliance_hold (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  hold_id VARCHAR(255) NOT NULL,
  entity_id VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  released_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_country_restriction_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  restriction_id VARCHAR(255) NOT NULL,
  destination_country VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  restriction_basis VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_trade_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  classification_policy VARCHAR(255) NOT NULL,
  landed_cost_policy DECIMAL(18, 4) NOT NULL,
  export_control_policy VARCHAR(255) NOT NULL,
  declaration_policy VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_trade_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  bounds VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_trade_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  required_event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_currency VARCHAR(255) NOT NULL,
  supported_countries VARCHAR(255) NOT NULL,
  supported_incoterms VARCHAR(255) NOT NULL,
  workbench_limit VARCHAR(255) NOT NULL,
  configuration_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_trade_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  entity VARCHAR(255) NOT NULL,
  fields VARCHAR(255) NOT NULL,
  compatible VARCHAR(255) NOT NULL,
  migration VARCHAR(255) NOT NULL,
  projection_rebuild_required VARCHAR(255) NOT NULL,
  extension_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_trade_audit_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  artifact_type VARCHAR(255) NOT NULL,
  artifact_id VARCHAR(255) NOT NULL,
  hash VARCHAR(255) NOT NULL,
  captured_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  aggregate_id VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  event_contract VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  payload TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  handled VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cross_border_trade_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

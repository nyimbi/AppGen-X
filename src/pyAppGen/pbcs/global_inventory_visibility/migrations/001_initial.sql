CREATE SCHEMA IF NOT EXISTS global_inventory_visibility;

CREATE TABLE global_inventory_visibility_inventory_pool (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_type VARCHAR(255) NOT NULL,
  allocation_policy VARCHAR(255) NOT NULL,
  safety_stock_units VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_supply_node (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_type VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  health_score DECIMAL(18, 4) NOT NULL,
  carbon_intensity VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_availability_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  on_hand VARCHAR(255) NOT NULL,
  reserved VARCHAR(255) NOT NULL,
  allocated VARCHAR(255) NOT NULL,
  in_transit VARCHAR(255) NOT NULL,
  staleness_minutes VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (pool_id) REFERENCES global_inventory_visibility_inventory_pool(pool_id),
  FOREIGN KEY (node_id) REFERENCES global_inventory_visibility_supply_node(node_id)
);

CREATE TABLE global_inventory_visibility_inventory_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  available_to_promise VARCHAR(255) NOT NULL,
  capable_to_promise VARCHAR(255) NOT NULL,
  freshness_score DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (pool_id) REFERENCES global_inventory_visibility_inventory_pool(pool_id)
);

CREATE TABLE global_inventory_visibility_available_to_promise_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  available_to_promise VARCHAR(255) NOT NULL,
  confidence_score DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (projection_id) REFERENCES global_inventory_visibility_inventory_projection(projection_id)
);

CREATE TABLE global_inventory_visibility_capable_to_promise_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  capable_to_promise VARCHAR(255) NOT NULL,
  confidence_score DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (projection_id) REFERENCES global_inventory_visibility_inventory_projection(projection_id)
);

CREATE TABLE global_inventory_visibility_channel_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  channel VARCHAR(255) NOT NULL,
  reserved_quantity VARCHAR(255) NOT NULL,
  available_to_promise VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (projection_id) REFERENCES global_inventory_visibility_inventory_projection(projection_id)
);

CREATE TABLE global_inventory_visibility_supply_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  signal_type VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (pool_id) REFERENCES global_inventory_visibility_inventory_pool(pool_id)
);

CREATE TABLE global_inventory_visibility_demand_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  channel VARCHAR(255) NOT NULL,
  signal_type VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (pool_id) REFERENCES global_inventory_visibility_inventory_pool(pool_id)
);

CREATE TABLE global_inventory_visibility_inventory_reservation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reservation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  ttl_minutes VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (pool_id) REFERENCES global_inventory_visibility_inventory_pool(pool_id)
);

CREATE TABLE global_inventory_visibility_inventory_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  allocation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (pool_id) REFERENCES global_inventory_visibility_inventory_pool(pool_id)
);

CREATE TABLE global_inventory_visibility_inventory_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  adjustment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  adjustment_type VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_inventory_reconciliation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reconciliation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  cycle_id VARCHAR(255) NOT NULL,
  variance_units VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (pool_id) REFERENCES global_inventory_visibility_inventory_pool(pool_id)
);

CREATE TABLE global_inventory_visibility_inventory_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  exception_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  opened_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (pool_id) REFERENCES global_inventory_visibility_inventory_pool(pool_id)
);

CREATE TABLE global_inventory_visibility_freshness_sla_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  evidence_id TEXT PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  freshness_score DECIMAL(18, 4) NOT NULL,
  sla_minutes VARCHAR(255) NOT NULL,
  breached VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (snapshot_id) REFERENCES global_inventory_visibility_availability_snapshot(snapshot_id)
);

CREATE TABLE global_inventory_visibility_inventory_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  federation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pool_id VARCHAR(255) PRIMARY KEY NOT NULL,
  system_name VARCHAR(255) NOT NULL,
  lag_minutes VARCHAR(255) NOT NULL,
  available_to_promise VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (pool_id) REFERENCES global_inventory_visibility_inventory_pool(pool_id)
);

CREATE TABLE global_inventory_visibility_inventory_audit_trace (
  tenant VARCHAR(255) NOT NULL,
  trace_id VARCHAR(255) PRIMARY KEY NOT NULL,
  subject_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_inventory_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) PRIMARY KEY NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  control_status VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  checked_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_inventory_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) PRIMARY KEY NOT NULL,
  entity_name VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  registered_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_inventory_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  scope VARCHAR(255) NOT NULL,
  rule_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_inventory_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) PRIMARY KEY NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  lower_bound VARCHAR(255) NOT NULL,
  upper_bound VARCHAR(255) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_inventory_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) PRIMARY KEY NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_currency VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_inventory_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) PRIMARY KEY NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  explainability_status VARCHAR(255) NOT NULL,
  registered_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE global_inventory_visibility_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

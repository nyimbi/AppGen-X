CREATE SCHEMA IF NOT EXISTS inventory_positioning;

CREATE TABLE inventory_positioning_item (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  sku VARCHAR(255) NOT NULL,
  uom VARCHAR(255) NOT NULL,
  lot_tracked VARCHAR(255) NOT NULL,
  serial_tracked VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_item_attribute (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  attribute_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(item_id)
);

CREATE TABLE inventory_positioning_item_substitution (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  substitution_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  substitute_item_id VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_lot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  lot_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  expires VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  trace_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(item_id)
);

CREATE TABLE inventory_positioning_serial (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  serial_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  lot_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (lot_id) REFERENCES inventory_positioning_lot(lot_id)
);

CREATE TABLE inventory_positioning_node (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_type VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  calendar VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_node_calendar (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  calendar_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  timezone VARCHAR(255) NOT NULL,
  working_days VARCHAR(255) NOT NULL,
  cutoff_time VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (node_id) REFERENCES inventory_positioning_node(node_id)
);

CREATE TABLE inventory_positioning_node_capacity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  capacity_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  daily_capacity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_node_identity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  identity_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  did VARCHAR(255) NOT NULL,
  issuer VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_inventory_position (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  position_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  on_hand VARCHAR(255) NOT NULL,
  reserved VARCHAR(255) NOT NULL,
  quarantine VARCHAR(255) NOT NULL,
  in_transit VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(item_id),
  FOREIGN KEY (node_id) REFERENCES inventory_positioning_node(node_id)
);

CREATE TABLE inventory_positioning_position_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) PRIMARY KEY NOT NULL,
  position_id VARCHAR(255) PRIMARY KEY NOT NULL,
  as_of VARCHAR(255) NOT NULL,
  on_hand VARCHAR(255) NOT NULL,
  available VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_receipt (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  receipt_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_receipt_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  receipt_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  receipt_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  lot_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (receipt_id) REFERENCES inventory_positioning_receipt(receipt_id)
);

CREATE TABLE inventory_positioning_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  adjustment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_cycle_count (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  cycle_count_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  physical_count INTEGER NOT NULL,
  variance VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_reservation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reservation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  allocation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity_allocated VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_allocation_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  allocation_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  allocation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  lot_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (allocation_id) REFERENCES inventory_positioning_allocation(allocation_id)
);

CREATE TABLE inventory_positioning_allocation_expiry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  expiry_id VARCHAR(255) PRIMARY KEY NOT NULL,
  allocation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  released VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_quality_hold (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  hold_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_quality_release (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  release_id VARCHAR(255) PRIMARY KEY NOT NULL,
  hold_id VARCHAR(255) PRIMARY KEY NOT NULL,
  released_by VARCHAR(255) NOT NULL,
  released_at TIMESTAMP NOT NULL,
  evidence_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (hold_id) REFERENCES inventory_positioning_quality_hold(hold_id)
);

CREATE TABLE inventory_positioning_in_transit_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  transit_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  eta_days VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_traceability_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  trace_event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  lot_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  trace_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_backorder (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  backorder_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_replenishment_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  recommended_quantity VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_replenishment_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  due_date TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_reconciliation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reconciliation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  ledger VARCHAR(255) NOT NULL,
  physical_count INTEGER NOT NULL,
  variance VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  screening_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision VARCHAR(255) NOT NULL,
  policy VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_stock_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  public_claims TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_cross_node_federation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  federation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  external_system VARCHAR(255) NOT NULL,
  projection_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_carbon_fulfillment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  carbon_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  carbon_intensity VARCHAR(255) NOT NULL,
  selected VARCHAR(255) NOT NULL,
  scheduled_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_channel_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  channel_allocation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  channel VARCHAR(255) NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  clearing_bid VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  entropy VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  decision VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_stock_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  risk_model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) PRIMARY KEY NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  explanations TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  seed_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  uom VARCHAR(255) NOT NULL,
  allocation_policy VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) PRIMARY KEY NOT NULL,
  table_name VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  control_id VARCHAR(255) PRIMARY KEY NOT NULL,
  assertion VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  tested_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  feature_lineage VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  governance_status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  predicate TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  bounds VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) PRIMARY KEY NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_uom VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

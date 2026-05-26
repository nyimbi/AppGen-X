CREATE SCHEMA IF NOT EXISTS inventory_positioning;

CREATE TABLE inventory_positioning_item (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_positioning_item_attribute (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_item_substitution (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_lot (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_serial (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_node (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_node_calendar (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_node_capacity (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_node_identity (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_inventory_position (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_position_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_receipt (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_receipt_line (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_cycle_count (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_reservation (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_allocation_line (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_allocation_expiry (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_quality_hold (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_quality_release (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_in_transit_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_traceability_event (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_backorder (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_replenishment_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_replenishment_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_reconciliation (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_stock_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_cross_node_federation (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_carbon_fulfillment (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_channel_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_stock_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  item_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (item_id) REFERENCES inventory_positioning_item(id)
);

CREATE TABLE inventory_positioning_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE inventory_positioning_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE inventory_positioning_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

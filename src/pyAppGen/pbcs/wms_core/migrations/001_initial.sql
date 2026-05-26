CREATE SCHEMA IF NOT EXISTS wms_core;

CREATE TABLE wms_core_warehouse (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_zone (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_bin_location (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_inbound_receipt (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_inbound_receipt_line (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_dock_door (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_dock_appointment (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_putaway_task (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_pick_wave (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_pick_task (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_pack_task (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_shipment_confirmation (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_cycle_count (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_labor_task (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_edge_device_command (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_wms_core_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_wms_core_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_wms_core_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  warehouse_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(id)
);

CREATE TABLE wms_core_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE wms_core_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE wms_core_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

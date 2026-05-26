CREATE SCHEMA IF NOT EXISTS mrp_engine;

CREATE TABLE mrp_engine_bill_of_material (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_bom_revision (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_bom_component (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_item_planning_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_material_demand (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_inventory_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_capacity_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_mrp_run (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_mrp_run_item (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_planned_order (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_planned_purchase_suggestion (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_planned_production_order (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_material_shortage (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_shortage_pegging (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_planning_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_mrp_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_mrp_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_mrp_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  bill_of_material_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bill_of_material_id) REFERENCES mrp_engine_bill_of_material(id)
);

CREATE TABLE mrp_engine_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE mrp_engine_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE mrp_engine_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE SCHEMA IF NOT EXISTS procurement_sourcing;

CREATE TABLE procurement_sourcing_procurement_sourcing_purchase_requisition (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_procurement_sourcing_purchase_requisition_line (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_requisition_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_category_strategy (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_supplier_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_supplier_qualification (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_rfq (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_rfq_line (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_supplier_invitation (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_supplier_bid (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_supplier_scorecard (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_supplier_award (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_vendor_contract (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_purchase_order (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_purchase_order_line (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_procurement_sourcing_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  procurement_sourcing_purchase_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (procurement_sourcing_purchase_requisition_id) REFERENCES procurement_sourcing_procurement_sourcing_purchase_requisition(id)
);

CREATE TABLE procurement_sourcing_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE procurement_sourcing_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE procurement_sourcing_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

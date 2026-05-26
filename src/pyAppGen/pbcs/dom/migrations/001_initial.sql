CREATE SCHEMA IF NOT EXISTS dom;

CREATE TABLE dom_sales_order (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE dom_order_line (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_order_status (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_order_promise (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_customer_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_tax_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_fraud_screen (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_order_verification (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_order_price_component (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_inventory_allocation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_payment_authorization_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_fulfillment_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_fulfillment_plan_line (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_fulfillment_node_candidate (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_split_shipment (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_backorder (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_substitution (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_shipment_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_dom_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_dom_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_dom_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  sales_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (sales_order_id) REFERENCES dom_sales_order(id)
);

CREATE TABLE dom_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE dom_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE dom_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE SCHEMA IF NOT EXISTS transportation_management;

CREATE TABLE transportation_management_shipment (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_shipment_line (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_shipment_package (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_carrier (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_carrier_service_level (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_carrier_lane (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_freight_route (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_route_stop (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_route_leg (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_carrier_tender (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_dispatch_confirmation (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_tracking_event (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_eta_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_inbound_arrival (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_delivery_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_freight_cost_accrual (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_transportation_management_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_transportation_management_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_transportation_management_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  shipment_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(id)
);

CREATE TABLE transportation_management_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE transportation_management_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE transportation_management_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

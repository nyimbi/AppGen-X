CREATE SCHEMA IF NOT EXISTS transportation_management;

CREATE TABLE transportation_management_shipment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_ref VARCHAR(255) NOT NULL,
  origin VARCHAR(255) NOT NULL,
  destination VARCHAR(255) NOT NULL,
  mode VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_shipment_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  shipment_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  weight VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(shipment_id)
);

CREATE TABLE transportation_management_shipment_party (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  party_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  role VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  address_ref VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_shipment_reference (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reference_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  reference_type VARCHAR(255) NOT NULL,
  reference_value VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_shipment_package (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  package_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  weight VARCHAR(255) NOT NULL,
  dimensions TEXT NOT NULL,
  handling_code VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(shipment_id)
);

CREATE TABLE transportation_management_carrier (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  carrier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  mode VARCHAR(255) NOT NULL,
  cost_per_mile DECIMAL(18, 4) NOT NULL,
  on_time_rate DECIMAL(18, 4) NOT NULL,
  risk VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_carrier_service_level (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  service_level_id VARCHAR(255) PRIMARY KEY NOT NULL,
  carrier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  service_level VARCHAR(255) NOT NULL,
  transit_days VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (carrier_id) REFERENCES transportation_management_carrier(carrier_id)
);

CREATE TABLE transportation_management_carrier_lane (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  lane_id VARCHAR(255) PRIMARY KEY NOT NULL,
  carrier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  origin VARCHAR(255) NOT NULL,
  destination VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (carrier_id) REFERENCES transportation_management_carrier(carrier_id)
);

CREATE TABLE transportation_management_carrier_contract (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  carrier_contract_id VARCHAR(255) PRIMARY KEY NOT NULL,
  carrier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rate_card DECIMAL(18, 4) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_carrier_identity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  identity_id VARCHAR(255) PRIMARY KEY NOT NULL,
  carrier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  did VARCHAR(255) NOT NULL,
  issuer VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (carrier_id) REFERENCES transportation_management_carrier(carrier_id)
);

CREATE TABLE transportation_management_freight_route (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  route_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  carrier_id VARCHAR(255) NOT NULL,
  distance_miles VARCHAR(255) NOT NULL,
  estimated_cost DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(shipment_id)
);

CREATE TABLE transportation_management_route_stop (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  stop_id VARCHAR(255) PRIMARY KEY NOT NULL,
  route_id VARCHAR(255) PRIMARY KEY NOT NULL,
  sequence VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  appointment_window VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (route_id) REFERENCES transportation_management_freight_route(route_id)
);

CREATE TABLE transportation_management_route_leg (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  leg_id VARCHAR(255) PRIMARY KEY NOT NULL,
  route_id VARCHAR(255) PRIMARY KEY NOT NULL,
  origin VARCHAR(255) NOT NULL,
  destination VARCHAR(255) NOT NULL,
  distance_miles VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (route_id) REFERENCES transportation_management_freight_route(route_id)
);

CREATE TABLE transportation_management_route_constraint (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  constraint_id VARCHAR(255) PRIMARY KEY NOT NULL,
  route_id VARCHAR(255) PRIMARY KEY NOT NULL,
  constraint_type VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_carrier_tender (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  tender_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  carrier_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  sent_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(shipment_id)
);

CREATE TABLE transportation_management_carrier_tender_response (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  response_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tender_id VARCHAR(255) PRIMARY KEY NOT NULL,
  carrier_id VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  responded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tender_id) REFERENCES transportation_management_carrier_tender(tender_id)
);

CREATE TABLE transportation_management_dispatch_confirmation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  dispatch_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tender_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  dispatched_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(shipment_id)
);

CREATE TABLE transportation_management_tracking_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  location VARCHAR(255) NOT NULL,
  distance_remaining VARCHAR(255) NOT NULL,
  delay_minutes VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(shipment_id)
);

CREATE TABLE transportation_management_eta_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  eta_snapshot_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  eta_hours VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_inbound_arrival (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  arrival_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  facility VARCHAR(255) NOT NULL,
  arrived_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_delivery_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  public_claims TEXT NOT NULL,
  delivered_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES transportation_management_shipment(shipment_id)
);

CREATE TABLE transportation_management_delivery_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_freight_cost_accrual (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_freight_invoice_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_cross_border_document (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_temperature_hazard_control (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_carrier_scorecard (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_carrier_risk_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_carbon_distance_metric (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_packed_order_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_purchase_order_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_return_authorization_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_inventory_transfer_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_access_policy_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_telematics_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_telematics_replay (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_delivery_proof_hash (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_audit_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_carbon_route_selection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_route_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_tender_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_tracking_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_transit_exposure_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_eta_cost_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_parsed_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_transportation_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE transportation_management_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

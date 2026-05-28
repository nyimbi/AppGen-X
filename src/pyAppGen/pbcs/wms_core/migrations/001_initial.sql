CREATE SCHEMA IF NOT EXISTS wms_core;

CREATE TABLE wms_core_warehouse (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  timezone VARCHAR(255) NOT NULL,
  calendar_id VARCHAR(255) PRIMARY KEY NOT NULL,
  identity_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_zone (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  zone_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  zone_type VARCHAR(255) NOT NULL,
  temperature VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(warehouse_id)
);

CREATE TABLE wms_core_warehouse_calendar (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  calendar_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  working_days VARCHAR(255) NOT NULL,
  cutoff_time VARCHAR(255) NOT NULL,
  timezone VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(warehouse_id)
);

CREATE TABLE wms_core_warehouse_identity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  identity_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  did VARCHAR(255) NOT NULL,
  issuer VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(warehouse_id)
);

CREATE TABLE wms_core_bin_location (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  bin_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  zone VARCHAR(255) NOT NULL,
  capacity VARCHAR(255) NOT NULL,
  current_load VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES wms_core_warehouse(warehouse_id)
);

CREATE TABLE wms_core_bin_attribute (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  attribute_id VARCHAR(255) PRIMARY KEY NOT NULL,
  bin_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bin_id) REFERENCES wms_core_bin_location(bin_id)
);

CREATE TABLE wms_core_bin_capacity_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) PRIMARY KEY NOT NULL,
  bin_id VARCHAR(255) PRIMARY KEY NOT NULL,
  capacity VARCHAR(255) NOT NULL,
  current_load VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_inbound_receipt (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  receipt_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  dock_door VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  received_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_inbound_receipt_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  receipt_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  receipt_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  lot_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (receipt_id) REFERENCES wms_core_inbound_receipt(receipt_id)
);

CREATE TABLE wms_core_dock_door (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  dock_door_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  door_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  zone_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_dock_appointment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  appointment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  dock_door_id VARCHAR(255) PRIMARY KEY NOT NULL,
  carrier VARCHAR(255) NOT NULL,
  window_start VARCHAR(255) NOT NULL,
  window_end VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_putaway_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  task_id VARCHAR(255) PRIMARY KEY NOT NULL,
  receipt_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  bin_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_putaway_confirmation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  confirmation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  task_id VARCHAR(255) PRIMARY KEY NOT NULL,
  confirmed_by VARCHAR(255) NOT NULL,
  confirmed_at TIMESTAMP NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (task_id) REFERENCES wms_core_putaway_task(task_id)
);

CREATE TABLE wms_core_replenishment_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  replenishment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  bin_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  recommended_quantity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_replenishment_trigger (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  trigger_id VARCHAR(255) PRIMARY KEY NOT NULL,
  bin_id VARCHAR(255) PRIMARY KEY NOT NULL,
  minimum VARCHAR(255) NOT NULL,
  forward_pick_demand VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_pick_wave (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  wave_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  method VARCHAR(255) NOT NULL,
  released_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_pick_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  pick_id VARCHAR(255) PRIMARY KEY NOT NULL,
  wave_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  picked_quantity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (wave_id) REFERENCES wms_core_pick_wave(wave_id)
);

CREATE TABLE wms_core_pick_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pick_id VARCHAR(255) PRIMARY KEY NOT NULL,
  exception_type VARCHAR(255) NOT NULL,
  resolution VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (pick_id) REFERENCES wms_core_pick_task(pick_id)
);

CREATE TABLE wms_core_pack_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  pack_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  station VARCHAR(255) NOT NULL,
  label_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_carton (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  carton_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pack_id VARCHAR(255) PRIMARY KEY NOT NULL,
  material VARCHAR(255) NOT NULL,
  weight VARCHAR(255) NOT NULL,
  dimensions TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (pack_id) REFERENCES wms_core_pack_task(pack_id)
);

CREATE TABLE wms_core_label_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  label_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pack_id VARCHAR(255) PRIMARY KEY NOT NULL,
  format VARCHAR(255) NOT NULL,
  hash VARCHAR(255) NOT NULL,
  printed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_pack_station (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  station_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  capability VARCHAR(255) NOT NULL,
  current_load VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_staging_lane (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  lane_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  dock_door_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  shipment_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_shipment_confirmation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  carrier VARCHAR(255) NOT NULL,
  dock_door VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_shipment_label (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  shipment_label_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  label_id VARCHAR(255) NOT NULL,
  carrier VARCHAR(255) NOT NULL,
  hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES wms_core_shipment_confirmation(shipment_id)
);

CREATE TABLE wms_core_cross_dock_flow (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  flow_id VARCHAR(255) PRIMARY KEY NOT NULL,
  receipt_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) NOT NULL,
  dock_door_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_cycle_count (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  cycle_count_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  started_at TIMESTAMP NOT NULL,
  completed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_cycle_count_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  cycle_count_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  cycle_count_id VARCHAR(255) PRIMARY KEY NOT NULL,
  bin_id VARCHAR(255) NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  variance VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (cycle_count_id) REFERENCES wms_core_cycle_count(cycle_count_id)
);

CREATE TABLE wms_core_warehouse_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  exception_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_labor_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  labor_task_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  task_type VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_labor_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assignment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  labor_task_id VARCHAR(255) PRIMARY KEY NOT NULL,
  worker_id VARCHAR(255) NOT NULL,
  tasks VARCHAR(255) NOT NULL,
  clearing_bid VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (labor_task_id) REFERENCES wms_core_labor_task(labor_task_id)
);

CREATE TABLE wms_core_labor_productivity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  productivity_id VARCHAR(255) PRIMARY KEY NOT NULL,
  worker_id VARCHAR(255) PRIMARY KEY NOT NULL,
  units VARCHAR(255) NOT NULL,
  labor_hours VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_edge_device_command (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  command_id VARCHAR(255) PRIMARY KEY NOT NULL,
  device_id VARCHAR(255) PRIMARY KEY NOT NULL,
  kind VARCHAR(255) NOT NULL,
  route VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_edge_device_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  edge_event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  device_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_edge_device_replay (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  replay_id VARCHAR(255) PRIMARY KEY NOT NULL,
  command_id VARCHAR(255) PRIMARY KEY NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  screening_id VARCHAR(255) PRIMARY KEY NOT NULL,
  bin_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision VARCHAR(255) NOT NULL,
  policy VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_traceability_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  trace_event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  trace_hash VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_shipment_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) PRIMARY KEY NOT NULL,
  shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  public_claims TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  external_system VARCHAR(255) NOT NULL,
  projection_hash VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_carbon_wave (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  carbon_wave_id VARCHAR(255) PRIMARY KEY NOT NULL,
  wave_id VARCHAR(255) PRIMARY KEY NOT NULL,
  carbon_intensity VARCHAR(255) NOT NULL,
  selected_window VARCHAR(255) NOT NULL,
  scheduled_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_pick_path_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  optimization_id VARCHAR(255) PRIMARY KEY NOT NULL,
  wave_id VARCHAR(255) PRIMARY KEY NOT NULL,
  path VARCHAR(255) NOT NULL,
  objective_score DECIMAL(18, 4) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_labor_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  allocation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  worker_id VARCHAR(255) NOT NULL,
  tasks VARCHAR(255) NOT NULL,
  clearing_bid VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  entropy VARCHAR(255) NOT NULL,
  outliers VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  risk_model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  explanations TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_warehouse_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  seed_id VARCHAR(255) PRIMARY KEY NOT NULL,
  warehouse_type VARCHAR(255) NOT NULL,
  zone_type VARCHAR(255) NOT NULL,
  label_format VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_wms_schema_extension (
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

CREATE TABLE wms_core_wms_control_assertion (
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

CREATE TABLE wms_core_wms_governed_model (
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

CREATE TABLE wms_core_wms_rule (
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

CREATE TABLE wms_core_wms_parameter (
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

CREATE TABLE wms_core_wms_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) PRIMARY KEY NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  label_format VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE wms_core_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE SCHEMA IF NOT EXISTS order_routing_optimization;

CREATE TABLE order_routing_optimization_routing_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) NOT NULL,
  selected_node_ids VARCHAR(255) NOT NULL,
  split VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_plan_leg (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  leg_id VARCHAR(255) PRIMARY KEY NOT NULL,
  plan_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  allocated_units VARCHAR(255) NOT NULL,
  sequence VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (plan_id) REFERENCES order_routing_optimization_routing_plan(plan_id)
);

CREATE TABLE order_routing_optimization_routing_node (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_type VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  timezone VARCHAR(255) NOT NULL,
  available_to_promise VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_node_calendar (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  calendar_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  timezone VARCHAR(255) NOT NULL,
  cutoff_time VARCHAR(255) NOT NULL,
  working_days VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (node_id) REFERENCES order_routing_optimization_routing_node(node_id)
);

CREATE TABLE order_routing_optimization_routing_node_service (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  service_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  service_type VARCHAR(255) NOT NULL,
  sla_hours VARCHAR(255) NOT NULL,
  cost_basis DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (node_id) REFERENCES order_routing_optimization_routing_node(node_id)
);

CREATE TABLE order_routing_optimization_routing_node_capacity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  capacity_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  available_units VARCHAR(255) NOT NULL,
  reserved_units VARCHAR(255) NOT NULL,
  forecast_load VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (node_id) REFERENCES order_routing_optimization_routing_node(node_id)
);

CREATE TABLE order_routing_optimization_routing_constraint (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  constraint_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  constraint_type VARCHAR(255) NOT NULL,
  constraint_value VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (rule_id) REFERENCES order_routing_optimization_routing_rule(rule_id)
);

CREATE TABLE order_routing_optimization_routing_cost_component (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  cost_id DECIMAL(18, 4) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  currency VARCHAR(255) NOT NULL,
  total_cost DECIMAL(18, 4) NOT NULL,
  total_carbon VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (decision_id) REFERENCES order_routing_optimization_routing_decision(decision_id)
);

CREATE TABLE order_routing_optimization_routing_promise (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  promise_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) NOT NULL,
  promised_sla_hours VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (decision_id) REFERENCES order_routing_optimization_routing_decision(decision_id)
);

CREATE TABLE order_routing_optimization_split_shipment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  split_shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  allocation_count INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_split_shipment_leg (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  split_leg_id VARCHAR(255) PRIMARY KEY NOT NULL,
  split_shipment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  allocated_units VARCHAR(255) NOT NULL,
  sequence VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (split_shipment_id) REFERENCES order_routing_optimization_split_shipment(split_shipment_id)
);

CREATE TABLE order_routing_optimization_inventory_input_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  input_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_scope VARCHAR(255) NOT NULL,
  available_units VARCHAR(255) NOT NULL,
  input_type VARCHAR(255) NOT NULL,
  source_event_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_transport_input_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  input_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  distance_km VARCHAR(255) NOT NULL,
  base_cost DECIMAL(18, 4) NOT NULL,
  input_type VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_service_input_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  input_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  sla_hours VARCHAR(255) NOT NULL,
  input_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_route_candidate (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  total_cost DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_capacity_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  available_units VARCHAR(255) NOT NULL,
  reserved_units VARCHAR(255) NOT NULL,
  available_to_promise VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  selected_node_ids VARCHAR(255) NOT NULL,
  objective_score DECIMAL(18, 4) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_node_reservation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reservation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  allocated_units VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (decision_id) REFERENCES order_routing_optimization_routing_decision(decision_id)
);

CREATE TABLE order_routing_optimization_route_simulation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  simulation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  current_node VARCHAR(255) NOT NULL,
  proposed_node VARCHAR(255) NOT NULL,
  cost_delta DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_route_simulation_scenario (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  scenario_id VARCHAR(255) PRIMARY KEY NOT NULL,
  simulation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  scenario_type VARCHAR(255) NOT NULL,
  input_hash VARCHAR(255) NOT NULL,
  result_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (simulation_id) REFERENCES order_routing_optimization_route_simulation(simulation_id)
);

CREATE TABLE order_routing_optimization_optimization_run (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  candidate_count INTEGER NOT NULL,
  objective_score DECIMAL(18, 4) NOT NULL,
  selected_candidate_ids VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_optimization_candidate (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  optimization_candidate_id VARCHAR(255) PRIMARY KEY NOT NULL,
  run_id VARCHAR(255) PRIMARY KEY NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  objective_score DECIMAL(18, 4) NOT NULL,
  selected VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (run_id) REFERENCES order_routing_optimization_optimization_run(run_id)
);

CREATE TABLE order_routing_optimization_routing_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  exception_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  recommended_action VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_exception_resolution (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  resolution_id VARCHAR(255) PRIMARY KEY NOT NULL,
  exception_id VARCHAR(255) PRIMARY KEY NOT NULL,
  resolution_action VARCHAR(255) NOT NULL,
  resolved_by VARCHAR(255) NOT NULL,
  resolved_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (exception_id) REFERENCES order_routing_optimization_routing_exception(exception_id)
);

CREATE TABLE order_routing_optimization_routing_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  approval_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  approval_mode VARCHAR(255) NOT NULL,
  approved VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (decision_id) REFERENCES order_routing_optimization_routing_decision(decision_id)
);

CREATE TABLE order_routing_optimization_routing_feedback (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  feedback_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  feedback_source VARCHAR(255) NOT NULL,
  feedback_type VARCHAR(255) NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (decision_id) REFERENCES order_routing_optimization_routing_decision(decision_id)
);

CREATE TABLE order_routing_optimization_routing_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  screening_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision VARCHAR(255) NOT NULL,
  blocked_nodes VARCHAR(255) NOT NULL,
  carbon_budget VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_audit_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  trace_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  trace_type VARCHAR(255) NOT NULL,
  trace_hash VARCHAR(255) NOT NULL,
  public_claims TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  federation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  system_name VARCHAR(255) NOT NULL,
  projection_hash VARCHAR(255) NOT NULL,
  projection_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_carbon_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schedule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  carbon_kg VARCHAR(255) NOT NULL,
  scheduled_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_network_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  optimization_id VARCHAR(255) PRIMARY KEY NOT NULL,
  run_id VARCHAR(255) PRIMARY KEY NOT NULL,
  selected_node_id VARCHAR(255) NOT NULL,
  objective_score DECIMAL(18, 4) NOT NULL,
  demand_units VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_capacity_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  allocation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  allocated_units VARCHAR(255) NOT NULL,
  clearing_bid VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  entropy VARCHAR(255) NOT NULL,
  outlier_count INTEGER NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_exposure_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  expected_exposure VARCHAR(255) NOT NULL,
  tail_risk VARCHAR(255) NOT NULL,
  simulation_count INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  forecast_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  horizon_hours VARCHAR(255) NOT NULL,
  expected_available_units VARCHAR(255) NOT NULL,
  saturation_risk VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_parsed_request (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parsed_request_id VARCHAR(255) PRIMARY KEY NOT NULL,
  order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  region VARCHAR(255) NOT NULL,
  requested_units VARCHAR(255) NOT NULL,
  sla_target_hours VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  seed_id VARCHAR(255) PRIMARY KEY NOT NULL,
  region VARCHAR(255) NOT NULL,
  split_policy VARCHAR(255) NOT NULL,
  substitution_mode VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) PRIMARY KEY NOT NULL,
  table_name VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  control_id VARCHAR(255) PRIMARY KEY NOT NULL,
  assertion VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  tested_at TIMESTAMP NOT NULL,
  severity VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  feature_lineage VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  governance_status VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  scope VARCHAR(255) NOT NULL,
  regions VARCHAR(255) NOT NULL,
  eligible_nodes VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  bounds VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_routing_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) PRIMARY KEY NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  published_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE order_routing_optimization_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

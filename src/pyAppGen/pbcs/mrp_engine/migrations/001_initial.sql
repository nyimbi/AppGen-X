CREATE SCHEMA IF NOT EXISTS mrp_engine;

CREATE TABLE mrp_engine_bill_of_material (
  id INTEGER PRIMARY KEY NOT NULL,
  bom_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parent_item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  current_revision VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_bom_revision (
  id INTEGER PRIMARY KEY NOT NULL,
  revision_id VARCHAR(255) NOT NULL,
  bom_id VARCHAR(255) NOT NULL,
  revision VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  valid_from VARCHAR(255) NOT NULL,
  released_by VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_bom_component (
  id INTEGER PRIMARY KEY NOT NULL,
  component_id VARCHAR(255) NOT NULL,
  bom_id VARCHAR(255) NOT NULL,
  revision_id VARCHAR(255) NOT NULL,
  component_item VARCHAR(255) NOT NULL,
  component_qty VARCHAR(255) NOT NULL,
  scrap_percent VARCHAR(255) NOT NULL,
  sequence VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_bom_alternate (
  id INTEGER PRIMARY KEY NOT NULL,
  alternate_id VARCHAR(255) NOT NULL,
  bom_id VARCHAR(255) NOT NULL,
  alternate_code VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_bom_substitution_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  substitution_id VARCHAR(255) NOT NULL,
  component_item VARCHAR(255) NOT NULL,
  substitute_item VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_item_planning_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  item_type VARCHAR(255) NOT NULL,
  lot_policy VARCHAR(255) NOT NULL,
  lead_time_days VARCHAR(255) NOT NULL,
  planner VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_item_source_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  source_rule_id VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  route VARCHAR(255) NOT NULL,
  supplier_ref VARCHAR(255) NOT NULL,
  work_center_ref VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_material_demand (
  id INTEGER PRIMARY KEY NOT NULL,
  demand_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  need_date TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_demand_projection_line (
  id INTEGER PRIMARY KEY NOT NULL,
  line_id VARCHAR(255) NOT NULL,
  demand_id VARCHAR(255) NOT NULL,
  bucket_start VARCHAR(255) NOT NULL,
  bucket_end VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_demand_forecast_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  forecast_snapshot_id VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  horizon_days VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_sales_order_demand_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  order_projection_id VARCHAR(255) NOT NULL,
  order_ref VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  need_date TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_safety_stock_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  minimum_qty VARCHAR(255) NOT NULL,
  multiplier VARCHAR(255) NOT NULL,
  review_cycle VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_inventory_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  inventory_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  available_qty VARCHAR(255) NOT NULL,
  quality_status VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_inventory_lot_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  lot_projection_id VARCHAR(255) NOT NULL,
  inventory_id VARCHAR(255) NOT NULL,
  lot_ref VARCHAR(255) NOT NULL,
  available_qty VARCHAR(255) NOT NULL,
  expiry_date TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_inventory_reservation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  reservation_id VARCHAR(255) NOT NULL,
  inventory_id VARCHAR(255) NOT NULL,
  demand_id VARCHAR(255) NOT NULL,
  reserved_qty VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_quality_hold_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  hold_projection_id VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  lot_ref VARCHAR(255) NOT NULL,
  release_status VARCHAR(255) NOT NULL,
  event_ref VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_capacity_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  capacity_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  resource VARCHAR(255) NOT NULL,
  capacity_qty VARCHAR(255) NOT NULL,
  bucket_start VARCHAR(255) NOT NULL,
  bucket_end VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_capacity_bucket (
  id INTEGER PRIMARY KEY NOT NULL,
  bucket_id VARCHAR(255) NOT NULL,
  capacity_id VARCHAR(255) NOT NULL,
  bucket_start VARCHAR(255) NOT NULL,
  bucket_end VARCHAR(255) NOT NULL,
  available_capacity VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_work_center_capacity_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  work_center_projection_id VARCHAR(255) NOT NULL,
  work_center_ref VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  available_capacity VARCHAR(255) NOT NULL,
  event_ref VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_supplier_lead_time_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  supplier_projection_id VARCHAR(255) NOT NULL,
  supplier_ref VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  lead_time_days VARCHAR(255) NOT NULL,
  event_ref VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_production_capacity_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  production_projection_id VARCHAR(255) NOT NULL,
  line_ref VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  available_capacity VARCHAR(255) NOT NULL,
  event_ref VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_run (
  id INTEGER PRIMARY KEY NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  horizon_days VARCHAR(255) NOT NULL,
  scenario VARCHAR(255) NOT NULL,
  planner VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  shortage_total VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_run_item (
  id INTEGER PRIMARY KEY NOT NULL,
  run_item_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  gross_requirement VARCHAR(255) NOT NULL,
  net_requirement VARCHAR(255) NOT NULL,
  coverage_status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_run_bucket (
  id INTEGER PRIMARY KEY NOT NULL,
  run_bucket_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  bucket_start VARCHAR(255) NOT NULL,
  bucket_end VARCHAR(255) NOT NULL,
  shortage_qty VARCHAR(255) NOT NULL,
  capacity_gap VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_scenario (
  id INTEGER PRIMARY KEY NOT NULL,
  scenario_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  scenario_name VARCHAR(255) NOT NULL,
  baseline VARCHAR(255) NOT NULL,
  created_by VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_plan_version (
  id INTEGER PRIMARY KEY NOT NULL,
  plan_version_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_planned_order (
  id INTEGER PRIMARY KEY NOT NULL,
  planned_order_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  route VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_planned_order_component (
  id INTEGER PRIMARY KEY NOT NULL,
  planned_component_id VARCHAR(255) NOT NULL,
  planned_order_id VARCHAR(255) NOT NULL,
  component_item VARCHAR(255) NOT NULL,
  required_qty VARCHAR(255) NOT NULL,
  bom_component_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_planned_purchase_suggestion (
  id INTEGER PRIMARY KEY NOT NULL,
  purchase_suggestion_id VARCHAR(255) NOT NULL,
  planned_order_id VARCHAR(255) NOT NULL,
  supplier_ref VARCHAR(255) NOT NULL,
  lead_time_days VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_planned_production_order (
  id INTEGER PRIMARY KEY NOT NULL,
  production_order_id VARCHAR(255) NOT NULL,
  planned_order_id VARCHAR(255) NOT NULL,
  work_center_ref VARCHAR(255) NOT NULL,
  capacity_qty VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_planned_transfer_order (
  id INTEGER PRIMARY KEY NOT NULL,
  transfer_order_id VARCHAR(255) NOT NULL,
  planned_order_id VARCHAR(255) NOT NULL,
  from_site VARCHAR(255) NOT NULL,
  to_site VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_material_shortage (
  id INTEGER PRIMARY KEY NOT NULL,
  shortage_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  shortage_qty VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_shortage_pegging (
  id INTEGER PRIMARY KEY NOT NULL,
  shortage_pegging_id VARCHAR(255) NOT NULL,
  shortage_id VARCHAR(255) NOT NULL,
  demand_id VARCHAR(255) NOT NULL,
  planned_order_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_supply_demand_pegging (
  id INTEGER PRIMARY KEY NOT NULL,
  pegging_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  demand_id VARCHAR(255) NOT NULL,
  supply_ref VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_planning_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  exception_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  exception_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  recommendation VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_exception_resolution_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  resolution_id VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) NOT NULL,
  action VARCHAR(255) NOT NULL,
  owner VARCHAR(255) NOT NULL,
  due_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_release_route (
  id INTEGER PRIMARY KEY NOT NULL,
  release_route_id VARCHAR(255) NOT NULL,
  route VARCHAR(255) NOT NULL,
  target_api VARCHAR(255) NOT NULL,
  idempotency_policy VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_planning_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  screening_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_planning_audit_trace (
  trace_id VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  previous_hash VARCHAR(255) NOT NULL,
  hash VARCHAR(255) NOT NULL,
  actor VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_supply_availability_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  proof_id VARCHAR(255) NOT NULL,
  planned_order_id VARCHAR(255) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  public_claims TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  projection_id VARCHAR(255) NOT NULL,
  planned_order_id VARCHAR(255) NOT NULL,
  system VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_carbon_planning_window (
  id INTEGER PRIMARY KEY NOT NULL,
  window_id VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  window_start VARCHAR(255) NOT NULL,
  window_end VARCHAR(255) NOT NULL,
  carbon_score DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_material_allocation_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  optimization_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  objective_score DECIMAL(18, 4) NOT NULL,
  selected_plan VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_capacity_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  allocation_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  resource VARCHAR(255) NOT NULL,
  allocated_capacity VARCHAR(255) NOT NULL,
  clearing_priority VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_shortage_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  signal_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  entropy VARCHAR(255) NOT NULL,
  outlier_count INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_material_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  auc VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  feature_lineage VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_shortage_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  forecast_id VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  forecast_demand VARCHAR(255) NOT NULL,
  forecast_shortage VARCHAR(255) NOT NULL,
  horizon VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_planning_parsed_instruction (
  id INTEGER PRIMARY KEY NOT NULL,
  instruction_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  action VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  seed_id VARCHAR(255) NOT NULL,
  seed_type VARCHAR(255) NOT NULL,
  key VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  extension_id VARCHAR(255) NOT NULL,
  table_name VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  result VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  tested_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  governed_model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  regulated VARCHAR(255) NOT NULL,
  explainability_required VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_mrp_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_appgen_outbox_event (
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_appgen_inbox_event (
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE mrp_engine_dead_letter_event (
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  failed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

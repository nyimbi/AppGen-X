CREATE TABLE hotel_revenue_management_room_type (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  hotel_id TEXT NOT NULL,
  code TEXT NOT NULL,
  name TEXT NOT NULL,
  physical_rooms INTEGER NOT NULL,
  maintenance_holdback INTEGER NOT NULL DEFAULT 0,
  complimentary_allotment INTEGER NOT NULL DEFAULT 0,
  sellable_rooms INTEGER NOT NULL,
  capacity_adults INTEGER NOT NULL,
  capacity_children INTEGER NOT NULL,
  substitution_targets_json JSON NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_rate_plan (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  hotel_id TEXT NOT NULL,
  room_type_id TEXT NOT NULL,
  code TEXT NOT NULL,
  parent_rate_plan_id TEXT,
  currency TEXT NOT NULL,
  base_rate DECIMAL(18, 2) NOT NULL,
  derived_discount_pct DECIMAL(9, 4) NOT NULL DEFAULT 0,
  effective_rate DECIMAL(18, 2) NOT NULL,
  min_los INTEGER NOT NULL,
  max_los INTEGER NOT NULL,
  member_fence TEXT NOT NULL,
  cancellation_policy TEXT NOT NULL,
  cta_dates_json JSON NOT NULL,
  ctd_dates_json JSON NOT NULL,
  package_components_json JSON NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_channel_inventory (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  hotel_id TEXT NOT NULL,
  room_type_id TEXT NOT NULL,
  rate_plan_id TEXT NOT NULL,
  code TEXT NOT NULL,
  channel_code TEXT NOT NULL,
  stay_date TEXT NOT NULL,
  allotment INTEGER NOT NULL,
  stop_sell BOOLEAN NOT NULL DEFAULT FALSE,
  release_back_hours INTEGER NOT NULL DEFAULT 24,
  blackout_reason TEXT,
  parity_exception_reason TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_demand_forecast (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  hotel_id TEXT NOT NULL,
  room_type_id TEXT NOT NULL,
  code TEXT NOT NULL,
  stay_date TEXT NOT NULL,
  transient_demand INTEGER NOT NULL,
  corporate_demand INTEGER NOT NULL,
  group_demand INTEGER NOT NULL,
  wholesale_demand INTEGER NOT NULL,
  house_use_demand INTEGER NOT NULL,
  forecast_rooms INTEGER NOT NULL,
  confidence DECIMAL(9, 4) NOT NULL,
  pickup_baseline INTEGER NOT NULL,
  event_factor DECIMAL(9, 4) NOT NULL DEFAULT 1,
  manual_override_rooms INTEGER,
  override_reason TEXT,
  approved_by TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_overbooking_policy (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  hotel_id TEXT NOT NULL,
  room_type_id TEXT NOT NULL,
  code TEXT NOT NULL,
  date_class TEXT NOT NULL,
  overbook_limit INTEGER NOT NULL,
  walk_cost DECIMAL(18, 2) NOT NULL,
  no_show_rate DECIMAL(9, 4) NOT NULL,
  cancellation_rate DECIMAL(9, 4) NOT NULL,
  arrival_protection_pct DECIMAL(9, 4) NOT NULL,
  recovery_priority_json JSON NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_yield_decision (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  hotel_id TEXT NOT NULL,
  room_type_id TEXT NOT NULL,
  rate_plan_id TEXT NOT NULL,
  code TEXT NOT NULL,
  stay_date TEXT NOT NULL,
  recommended_rate DECIMAL(18, 2) NOT NULL,
  rate_change_pct DECIMAL(9, 4) NOT NULL,
  channel_action TEXT NOT NULL,
  restriction_action TEXT NOT NULL,
  expected_occupancy DECIMAL(9, 4) NOT NULL,
  expected_adr DECIMAL(18, 2) NOT NULL,
  explanation_json JSON NOT NULL,
  approved_by TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_revenue_snapshot (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  hotel_id TEXT NOT NULL,
  code TEXT NOT NULL,
  stay_date TEXT NOT NULL,
  rooms_sold INTEGER NOT NULL,
  rooms_available INTEGER NOT NULL,
  occupancy_pct DECIMAL(9, 4) NOT NULL,
  adr DECIMAL(18, 2) NOT NULL,
  revpar DECIMAL(18, 2) NOT NULL,
  net_revenue DECIMAL(18, 2) NOT NULL,
  channel_mix_json JSON NOT NULL,
  source_decision_ids_json JSON NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_hotel_revenue_management_policy_rule (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  scope TEXT NOT NULL,
  rule_type TEXT NOT NULL,
  threshold DECIMAL(18, 4),
  expression_json JSON NOT NULL,
  severity TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_hotel_revenue_management_runtime_parameter (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  parameter_key TEXT NOT NULL,
  parameter_value DECIMAL(18, 4) NOT NULL,
  value_type TEXT NOT NULL,
  min_value DECIMAL(18, 4),
  max_value DECIMAL(18, 4),
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_hotel_revenue_management_schema_extension (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  owned_table TEXT NOT NULL,
  extension_fields_json JSON NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_hotel_revenue_management_control_assertion (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  assertion_type TEXT NOT NULL,
  target_record_id TEXT NOT NULL,
  outcome TEXT NOT NULL,
  evidence_json JSON NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_hotel_revenue_management_governed_model (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  model_name TEXT NOT NULL,
  model_version TEXT NOT NULL,
  model_purpose TEXT NOT NULL,
  approval_policy TEXT NOT NULL,
  drift_threshold DECIMAL(9, 4) NOT NULL,
  human_confirmation_required BOOLEAN NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_appgen_outbox_event (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  event_type TEXT NOT NULL,
  topic TEXT NOT NULL,
  aggregate_table TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  payload_json JSON NOT NULL,
  idempotency_key TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_appgen_inbox_event (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  event_type TEXT NOT NULL,
  source_pbc TEXT NOT NULL,
  payload_json JSON NOT NULL,
  idempotency_key TEXT NOT NULL,
  handled_at TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE hotel_revenue_management_appgen_dead_letter_event (
  id TEXT PRIMARY KEY,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  event_type TEXT NOT NULL,
  source_pbc TEXT NOT NULL,
  payload_json JSON NOT NULL,
  idempotency_key TEXT NOT NULL,
  retry_count INTEGER NOT NULL,
  reason TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

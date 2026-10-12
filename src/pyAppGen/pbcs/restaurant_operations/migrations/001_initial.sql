CREATE SCHEMA IF NOT EXISTS restaurant_operations;

CREATE TABLE restaurant_operations_menu_item (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  menu_item_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  concept VARCHAR(255) NOT NULL,
  site_id VARCHAR(255) NOT NULL,
  daypart VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  menu_state VARCHAR(255) NOT NULL,
  price_amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  recipe_version VARCHAR(255) NOT NULL,
  dietary_flags VARCHAR(255) NOT NULL,
  allergen_declaration VARCHAR(255) NOT NULL,
  availability_state VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP,
  effective_to TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE restaurant_operations_recipe (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  recipe_id VARCHAR(255) NOT NULL,
  menu_item_id VARCHAR(255) NOT NULL,
  recipe_version VARCHAR(255) NOT NULL,
  target_yield DECIMAL(18, 4) NOT NULL,
  portion_size DECIMAL(18, 4) NOT NULL,
  yield_unit VARCHAR(255) NOT NULL,
  prep_method VARCHAR(255) NOT NULL,
  store_override VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP,
  effective_to TIMESTAMP,
  locked_for_service BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (menu_item_id) REFERENCES restaurant_operations_menu_item(menu_item_id)
);

CREATE TABLE restaurant_operations_kitchen_ticket (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  kitchen_ticket_id VARCHAR(255) NOT NULL,
  reservation_id VARCHAR(255),
  table_id VARCHAR(255) NOT NULL,
  station_id VARCHAR(255) NOT NULL,
  course_group VARCHAR(255) NOT NULL,
  fire_offset_seconds INTEGER NOT NULL,
  hold_instruction VARCHAR(255) NOT NULL,
  ticket_state VARCHAR(255) NOT NULL,
  allergen_marking VARCHAR(255) NOT NULL,
  fired_at TIMESTAMP,
  plated_at TIMESTAMP,
  handed_off_at TIMESTAMP,
  recalled BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (reservation_id) REFERENCES restaurant_operations_reservation(reservation_id)
);

CREATE TABLE restaurant_operations_reservation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reservation_id VARCHAR(255) NOT NULL,
  guest_name VARCHAR(255) NOT NULL,
  party_size INTEGER NOT NULL,
  table_id VARCHAR(255) NOT NULL,
  daypart VARCHAR(255) NOT NULL,
  service_phase VARCHAR(255) NOT NULL,
  turn_minutes INTEGER NOT NULL,
  accessibility_needs VARCHAR(255) NOT NULL,
  waitlist_state VARCHAR(255) NOT NULL,
  quoted_wait_minutes INTEGER NOT NULL,
  seated_at TIMESTAMP,
  channel VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE restaurant_operations_inventory_prep (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  prep_batch_id VARCHAR(255) NOT NULL,
  recipe_id VARCHAR(255) NOT NULL,
  station_id VARCHAR(255) NOT NULL,
  batch_quantity DECIMAL(18, 4) NOT NULL,
  unit VARCHAR(255) NOT NULL,
  production_at TIMESTAMP NOT NULL,
  expiration_at TIMESTAMP,
  holding_method VARCHAR(255) NOT NULL,
  temperature_checked BOOLEAN NOT NULL,
  approved BOOLEAN NOT NULL,
  discard_reason VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (recipe_id) REFERENCES restaurant_operations_recipe(recipe_id)
);

CREATE TABLE restaurant_operations_food_waste (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  waste_event_id VARCHAR(255) NOT NULL,
  prep_batch_id VARCHAR(255),
  menu_item_id VARCHAR(255),
  station_id VARCHAR(255) NOT NULL,
  waste_reason VARCHAR(255) NOT NULL,
  quantity DECIMAL(18, 4) NOT NULL,
  unit VARCHAR(255) NOT NULL,
  cost_amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  recorded_by VARCHAR(255) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (prep_batch_id) REFERENCES restaurant_operations_inventory_prep(prep_batch_id)
);

CREATE TABLE restaurant_operations_labor_shift (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  labor_shift_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  station_id VARCHAR(255) NOT NULL,
  role_name VARCHAR(255) NOT NULL,
  daypart VARCHAR(255) NOT NULL,
  starts_at TIMESTAMP NOT NULL,
  ends_at TIMESTAMP NOT NULL,
  readiness_confirmed BOOLEAN NOT NULL,
  sanitizer_checked BOOLEAN NOT NULL,
  labor_minutes INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE restaurant_operations_restaurant_operations_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  ambiguity_flag BOOLEAN NOT NULL,
  approver_role VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE restaurant_operations_restaurant_operations_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  effective_from TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE restaurant_operations_restaurant_operations_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) NOT NULL,
  target_table VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  registered_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE restaurant_operations_restaurant_operations_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  assertion_result VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  remediation_task VARCHAR(255) NOT NULL,
  evaluated_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE restaurant_operations_restaurant_operations_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  governance_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE restaurant_operations_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE restaurant_operations_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE restaurant_operations_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

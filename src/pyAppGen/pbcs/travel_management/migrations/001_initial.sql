CREATE SCHEMA IF NOT EXISTS travel_management;

CREATE TABLE travel_management_travel_request (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  traveler_id VARCHAR(255) NOT NULL,
  purpose VARCHAR(255) NOT NULL,
  origin VARCHAR(255) NOT NULL,
  destination VARCHAR(255) NOT NULL,
  departure_date TIMESTAMP NOT NULL,
  return_date TIMESTAMP NOT NULL,
  trip_type VARCHAR(255) NOT NULL,
  cost_estimate DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  risk_level VARCHAR(255) NOT NULL,
  policy_version VARCHAR(255) NOT NULL,
  readiness_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
,
  UNIQUE (trip_request_id));

CREATE TABLE travel_management_travel_booking (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  booking_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  booking_type VARCHAR(255) NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  confirmation_number VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  booking_state VARCHAR(255) NOT NULL,
  cancellation_deadline TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_travel_request(trip_request_id)
);

CREATE TABLE travel_management_travel_itinerary (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  itinerary_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  traveler_id VARCHAR(255) NOT NULL,
  item_count INTEGER NOT NULL,
  start_at TIMESTAMP NOT NULL,
  end_at TIMESTAMP NOT NULL,
  timezone VARCHAR(255) NOT NULL,
  integrity_state VARCHAR(255) NOT NULL,
  conflict_count INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_travel_request(trip_request_id)
,
  UNIQUE (itinerary_id));

CREATE TABLE travel_management_travel_policy_check (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  check_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  policy_version VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  exception_required BOOLEAN NOT NULL,
  severity VARCHAR(255) NOT NULL,
  rationale TEXT NOT NULL,
  evaluated_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_travel_request(trip_request_id)
);

CREATE TABLE travel_management_duty_of_care_alert (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  alert_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  traveler_id VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  location_confidence VARCHAR(255) NOT NULL,
  affected_region VARCHAR(255) NOT NULL,
  contact_attempts INTEGER NOT NULL,
  escalation_owner VARCHAR(255) NOT NULL,
  alert_state VARCHAR(255) NOT NULL,
  acknowledged_at TIMESTAMP,
  closed_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_travel_request(trip_request_id)
);

CREATE TABLE travel_management_supplier_travel_feed (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  feed_id VARCHAR(255) NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  feed_type VARCHAR(255) NOT NULL,
  offer_count INTEGER NOT NULL,
  payload_hash VARCHAR(255) NOT NULL,
  freshness_state VARCHAR(255) NOT NULL,
  scorecard_rating DECIMAL(18, 4) NOT NULL,
  received_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE travel_management_travel_expense_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  handoff_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  expense_report_id VARCHAR(255) NOT NULL,
  approved_budget DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  expected_categories VARCHAR(255) NOT NULL,
  per_diem_eligible BOOLEAN NOT NULL,
  mileage_eligible BOOLEAN NOT NULL,
  handoff_state VARCHAR(255) NOT NULL,
  handed_off_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_travel_request(trip_request_id)
);

CREATE TABLE travel_management_travel_carbon_record (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  carbon_record_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  booking_id VARCHAR(255) NOT NULL,
  transport_mode VARCHAR(255) NOT NULL,
  distance_km DECIMAL(18, 4) NOT NULL,
  carbon_kg DECIMAL(18, 4) NOT NULL,
  data_source VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  assumptions TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_travel_request(trip_request_id)
);

CREATE TABLE travel_management_trip_request (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  traveler_id VARCHAR(255) NOT NULL,
  purpose VARCHAR(255) NOT NULL,
  origin VARCHAR(255) NOT NULL,
  destination VARCHAR(255) NOT NULL,
  departure_date TIMESTAMP NOT NULL,
  return_date TIMESTAMP NOT NULL,
  trip_type VARCHAR(255) NOT NULL,
  cost_estimate DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  risk_level VARCHAR(255) NOT NULL,
  policy_version VARCHAR(255) NOT NULL,
  approval_state VARCHAR(255) NOT NULL,
  readiness_state VARCHAR(255) NOT NULL,
  lifecycle_state VARCHAR(255) NOT NULL,
  business_unit VARCHAR(255) NOT NULL,
  cost_center VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
,
  UNIQUE (trip_request_id));

CREATE TABLE travel_management_traveler_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  traveler_id VARCHAR(255) NOT NULL,
  employee_id VARCHAR(255) NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  home_region VARCHAR(255) NOT NULL,
  preferred_language VARCHAR(255) NOT NULL,
  nationality VARCHAR(255) NOT NULL,
  passport_expiry TIMESTAMP,
  visa_state VARCHAR(255) NOT NULL,
  emergency_contact VARCHAR(255) NOT NULL,
  accessibility_needs VARCHAR(255) NOT NULL,
  loyalty_identifiers VARCHAR(255) NOT NULL,
  notification_preference VARCHAR(255) NOT NULL,
  risk_consent BOOLEAN NOT NULL,
  completeness_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE travel_management_travel_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  policy_name VARCHAR(255) NOT NULL,
  policy_version VARCHAR(255) NOT NULL,
  employee_level VARCHAR(255) NOT NULL,
  business_unit VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  fare_class VARCHAR(255) NOT NULL,
  hotel_cap DECIMAL(18, 4) NOT NULL,
  advance_booking_days INTEGER NOT NULL,
  approval_threshold DECIMAL(18, 4) NOT NULL,
  supplier_category VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE travel_management_travel_approval_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  approval_task_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  approver_id VARCHAR(255) NOT NULL,
  approver_role VARCHAR(255) NOT NULL,
  sequence_number INTEGER NOT NULL,
  decision VARCHAR(255) NOT NULL,
  route_rationale TEXT NOT NULL,
  skipped_approvers VARCHAR(255) NOT NULL,
  delegation VARCHAR(255) NOT NULL,
  escalation_due_at TIMESTAMP,
  emergency_lane BOOLEAN NOT NULL,
  decided_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_trip_request(trip_request_id)
);

CREATE TABLE travel_management_booking_intent (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  booking_intent_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  traveler_id VARCHAR(255) NOT NULL,
  travel_window_start TIMESTAMP NOT NULL,
  travel_window_end TIMESTAMP NOT NULL,
  budget_amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  preferred_supplier VARCHAR(255) NOT NULL,
  policy_constraints VARCHAR(255) NOT NULL,
  risk_constraints VARCHAR(255) NOT NULL,
  booking_deadline TIMESTAMP,
  compared_offer_count INTEGER NOT NULL,
  selected_offer_id VARCHAR(255),
  intent_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_trip_request(trip_request_id)
,
  UNIQUE (booking_intent_id));

CREATE TABLE travel_management_air_booking (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  air_booking_id VARCHAR(255) NOT NULL,
  booking_intent_id VARCHAR(255) NOT NULL,
  ticket_number VARCHAR(255) NOT NULL,
  carrier_code VARCHAR(255) NOT NULL,
  fare_class VARCHAR(255) NOT NULL,
  routing VARCHAR(255) NOT NULL,
  layover_count INTEGER NOT NULL,
  refundable BOOLEAN NOT NULL,
  baggage_allowance VARCHAR(255) NOT NULL,
  change_fee DECIMAL(18, 4) NOT NULL,
  ticketing_deadline TIMESTAMP,
  unused_ticket_eligible BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (booking_intent_id) REFERENCES travel_management_booking_intent(booking_intent_id)
);

CREATE TABLE travel_management_hotel_booking (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  hotel_booking_id VARCHAR(255) NOT NULL,
  booking_intent_id VARCHAR(255) NOT NULL,
  property_name VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  nightly_rate DECIMAL(18, 4) NOT NULL,
  rate_cap DECIMAL(18, 4) NOT NULL,
  total_stay_cost DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  check_in TIMESTAMP NOT NULL,
  check_out TIMESTAMP NOT NULL,
  cancellation_window VARCHAR(255) NOT NULL,
  safety_rating DECIMAL(18, 4) NOT NULL,
  accessible BOOLEAN NOT NULL,
  preferred_supplier BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (booking_intent_id) REFERENCES travel_management_booking_intent(booking_intent_id)
);

CREATE TABLE travel_management_ground_booking (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  ground_booking_id VARCHAR(255) NOT NULL,
  booking_intent_id VARCHAR(255) NOT NULL,
  transport_mode VARCHAR(255) NOT NULL,
  distance_km DECIMAL(18, 4) NOT NULL,
  rate_amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  vehicle_class VARCHAR(255) NOT NULL,
  insurance_included BOOLEAN NOT NULL,
  driver_eligible BOOLEAN NOT NULL,
  pickup_at TIMESTAMP,
  dropoff_at TIMESTAMP,
  carbon_kg DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (booking_intent_id) REFERENCES travel_management_booking_intent(booking_intent_id)
);

CREATE TABLE travel_management_itinerary_item (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  itinerary_item_id VARCHAR(255) NOT NULL,
  itinerary_id VARCHAR(255) NOT NULL,
  item_type VARCHAR(255) NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  confirmation_number VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  timezone VARCHAR(255) NOT NULL,
  starts_at TIMESTAMP NOT NULL,
  ends_at TIMESTAMP NOT NULL,
  depends_on_item_id VARCHAR(255),
  confirmation_state VARCHAR(255) NOT NULL,
  source_evidence VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (itinerary_id) REFERENCES travel_management_travel_itinerary(itinerary_id)
);

CREATE TABLE travel_management_travel_disruption (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  disruption_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  itinerary_item_id VARCHAR(255),
  source VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  traveler_impact VARCHAR(255) NOT NULL,
  options_considered INTEGER NOT NULL,
  selected_option TEXT NOT NULL,
  rejected_rationale TEXT NOT NULL,
  policy_implication VARCHAR(255) NOT NULL,
  expense_impact DECIMAL(18, 4) NOT NULL,
  disruption_state VARCHAR(255) NOT NULL,
  opened_at TIMESTAMP NOT NULL,
  resolved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_trip_request(trip_request_id)
);

CREATE TABLE travel_management_unused_ticket (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  unused_ticket_id VARCHAR(255) NOT NULL,
  traveler_id VARCHAR(255) NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  ticket_number VARCHAR(255) NOT NULL,
  ticket_value DECIMAL(18, 4) NOT NULL,
  residual_value DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  fare_rules VARCHAR(255) NOT NULL,
  transferable BOOLEAN NOT NULL,
  reuse_eligible BOOLEAN NOT NULL,
  expires_at TIMESTAMP,
  owner_id VARCHAR(255) NOT NULL,
  ticket_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE travel_management_travel_expense_link (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  expense_link_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  expense_report_id VARCHAR(255) NOT NULL,
  approved_budget DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  expected_categories VARCHAR(255) NOT NULL,
  per_diem_eligible BOOLEAN NOT NULL,
  mileage_eligible BOOLEAN NOT NULL,
  source_evidence VARCHAR(255) NOT NULL,
  link_state VARCHAR(255) NOT NULL,
  linked_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_trip_request(trip_request_id)
);

CREATE TABLE travel_management_travel_risk_assessment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  risk_assessment_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  traveler_id VARCHAR(255) NOT NULL,
  destination VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  risk_level VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  risk_drivers VARCHAR(255) NOT NULL,
  required_mitigation VARCHAR(255) NOT NULL,
  mitigation_plan TEXT NOT NULL,
  assessed_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_trip_request(trip_request_id)
);

CREATE TABLE travel_management_travel_supplier_offer (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  supplier_offer_id VARCHAR(255) NOT NULL,
  booking_intent_id VARCHAR(255) NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  offer_type VARCHAR(255) NOT NULL,
  base_price DECIMAL(18, 4) NOT NULL,
  taxes DECIMAL(18, 4) NOT NULL,
  fees DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  restrictions VARCHAR(255) NOT NULL,
  refundable BOOLEAN NOT NULL,
  loyalty_accrual VARCHAR(255) NOT NULL,
  baggage_allowance VARCHAR(255) NOT NULL,
  cancellation_terms VARCHAR(255) NOT NULL,
  supplier_rating DECIMAL(18, 4) NOT NULL,
  carbon_estimate DECIMAL(18, 4) NOT NULL,
  source_payload_hash VARCHAR(255) NOT NULL,
  preferred_supplier BOOLEAN NOT NULL,
  offer_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (booking_intent_id) REFERENCES travel_management_booking_intent(booking_intent_id)
);

CREATE TABLE travel_management_travel_exception_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_case_id VARCHAR(255) NOT NULL,
  trip_request_id VARCHAR(255) NOT NULL,
  exception_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  owner_id VARCHAR(255) NOT NULL,
  required_evidence VARCHAR(255) NOT NULL,
  financial_exposure DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  traveler_impact VARCHAR(255) NOT NULL,
  resolution_action VARCHAR(255) NOT NULL,
  closure_proof VARCHAR(255) NOT NULL,
  case_state VARCHAR(255) NOT NULL,
  resolved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (trip_request_id) REFERENCES travel_management_trip_request(trip_request_id)
);

CREATE TABLE travel_management_travel_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  ambiguity_flag BOOLEAN NOT NULL,
  example_text TEXT NOT NULL,
  approver_role VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE travel_management_travel_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE travel_management_travel_schema_extension (
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

CREATE TABLE travel_management_travel_control_assertion (
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

CREATE TABLE travel_management_travel_governed_model (
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

CREATE TABLE travel_management_appgen_outbox_event (
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

CREATE TABLE travel_management_appgen_inbox_event (
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

CREATE TABLE travel_management_appgen_dead_letter_event (
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

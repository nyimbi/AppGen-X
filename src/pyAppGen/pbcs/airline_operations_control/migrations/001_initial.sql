CREATE SCHEMA IF NOT EXISTS airline_operations_control;

CREATE TABLE airline_operations_control_flight_leg (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  flight_leg_id VARCHAR(255) NOT NULL,
  flight_number VARCHAR(255) NOT NULL,
  service_type VARCHAR(255) NOT NULL,
  origin_station VARCHAR(255) NOT NULL,
  destination_station VARCHAR(255) NOT NULL,
  scheduled_departure TIMESTAMP NOT NULL,
  scheduled_arrival TIMESTAMP NOT NULL,
  actual_departure TIMESTAMP,
  actual_arrival TIMESTAMP,
  aircraft_tail VARCHAR(255) NOT NULL,
  gate_position VARCHAR(255) NOT NULL,
  minimum_turn_minutes INTEGER NOT NULL,
  turn_risk_state VARCHAR(255) NOT NULL,
  slot_window VARCHAR(255) NOT NULL,
  curfew_exposure VARCHAR(255) NOT NULL,
  payload_restriction VARCHAR(255) NOT NULL,
  freeze_window_state VARCHAR(255) NOT NULL,
  timeline_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE airline_operations_control_aircraft_rotation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  aircraft_rotation_id VARCHAR(255) NOT NULL,
  aircraft_tail VARCHAR(255) NOT NULL,
  fleet_family VARCHAR(255) NOT NULL,
  rotation_date TIMESTAMP NOT NULL,
  leg_sequence INTEGER NOT NULL,
  previous_leg_id VARCHAR(255) NOT NULL,
  next_leg_id VARCHAR(255) NOT NULL,
  maintenance_stop_state VARCHAR(255) NOT NULL,
  maintenance_due_margin DECIMAL(18, 4) NOT NULL,
  deferred_defect_state VARCHAR(255) NOT NULL,
  spare_substitution_state VARCHAR(255) NOT NULL,
  availability_state VARCHAR(255) NOT NULL,
  swap_option_count INTEGER NOT NULL,
  protected_departure_count INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (previous_leg_id) REFERENCES airline_operations_control_flight_leg(flight_leg_id)
);

CREATE TABLE airline_operations_control_crew_pairing (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  crew_pairing_id VARCHAR(255) NOT NULL,
  pairing_reference VARCHAR(255) NOT NULL,
  crew_role VARCHAR(255) NOT NULL,
  base_station VARCHAR(255) NOT NULL,
  flight_leg_id VARCHAR(255) NOT NULL,
  report_at TIMESTAMP NOT NULL,
  duty_start_at TIMESTAMP NOT NULL,
  duty_end_at TIMESTAMP,
  remaining_duty_margin DECIMAL(18, 4) NOT NULL,
  minimum_rest_hours DECIMAL(18, 4) NOT NULL,
  fdp_limit_hours DECIMAL(18, 4) NOT NULL,
  legality_state VARCHAR(255) NOT NULL,
  standby_state VARCHAR(255) NOT NULL,
  deadhead_state VARCHAR(255) NOT NULL,
  hotel_assignment VARCHAR(255) NOT NULL,
  transport_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (flight_leg_id) REFERENCES airline_operations_control_flight_leg(flight_leg_id)
);

CREATE TABLE airline_operations_control_disruption_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  disruption_event_id VARCHAR(255) NOT NULL,
  disruption_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  source_system VARCHAR(255) NOT NULL,
  station_code VARCHAR(255) NOT NULL,
  flight_leg_id VARCHAR(255) NOT NULL,
  detected_at TIMESTAMP NOT NULL,
  stabilized_at TIMESTAMP,
  closed_at TIMESTAMP,
  relevance_score DECIMAL(18, 4) NOT NULL,
  affected_leg_count INTEGER NOT NULL,
  playbook_name VARCHAR(255) NOT NULL,
  holdover_expiry_at TIMESTAMP,
  deduplication_key VARCHAR(255) NOT NULL,
  disposition_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (flight_leg_id) REFERENCES airline_operations_control_flight_leg(flight_leg_id)
);

CREATE TABLE airline_operations_control_reaccommodation_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reaccommodation_plan_id VARCHAR(255) NOT NULL,
  disruption_event_id VARCHAR(255) NOT NULL,
  passenger_cohort VARCHAR(255) NOT NULL,
  passenger_count INTEGER NOT NULL,
  proposed_option VARCHAR(255) NOT NULL,
  accepted_option VARCHAR(255) NOT NULL,
  protection_boundary VARCHAR(255) NOT NULL,
  interline_scope VARCHAR(255) NOT NULL,
  special_assistance_state VARCHAR(255) NOT NULL,
  overnight_required BOOLEAN NOT NULL,
  ticketing_confirmation VARCHAR(255) NOT NULL,
  uplift_outcome VARCHAR(255) NOT NULL,
  residual_exception_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (disruption_event_id) REFERENCES airline_operations_control_disruption_event(disruption_event_id)
);

CREATE TABLE airline_operations_control_operations_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  operations_decision_id VARCHAR(255) NOT NULL,
  decision_type VARCHAR(255) NOT NULL,
  disruption_event_id VARCHAR(255) NOT NULL,
  flight_leg_id VARCHAR(255) NOT NULL,
  selected_action VARCHAR(255) NOT NULL,
  alternatives_considered TEXT NOT NULL,
  rationale TEXT NOT NULL,
  assumptions TEXT NOT NULL,
  fuel_strategy VARCHAR(255) NOT NULL,
  dispatch_release_state VARCHAR(255) NOT NULL,
  route_compliance_state VARCHAR(255) NOT NULL,
  override_reason VARCHAR(255) NOT NULL,
  override_expires_at TIMESTAMP,
  approver_identity VARCHAR(255) NOT NULL,
  approved_at TIMESTAMP,
  expected_network_effect TEXT NOT NULL,
  actual_outcome_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (disruption_event_id) REFERENCES airline_operations_control_disruption_event(disruption_event_id),
  FOREIGN KEY (flight_leg_id) REFERENCES airline_operations_control_flight_leg(flight_leg_id)
);

CREATE TABLE airline_operations_control_delay_code (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  delay_code_id VARCHAR(255) NOT NULL,
  delay_code VARCHAR(255) NOT NULL,
  code_family VARCHAR(255) NOT NULL,
  primary_cause VARCHAR(255) NOT NULL,
  contributing_causes TEXT NOT NULL,
  reactionary_flag BOOLEAN NOT NULL,
  coding_owner VARCHAR(255) NOT NULL,
  late_change_justification TEXT NOT NULL,
  delay_minutes INTEGER NOT NULL,
  crew_overtime_cost DECIMAL(18, 4) NOT NULL,
  hotel_exposure_cost DECIMAL(18, 4) NOT NULL,
  passenger_care_cost DECIMAL(18, 4) NOT NULL,
  closure_evidence_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE airline_operations_control_airline_operations_control_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  recovery_objective VARCHAR(255) NOT NULL,
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

CREATE TABLE airline_operations_control_airline_operations_control_runtime_parameter (
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

CREATE TABLE airline_operations_control_airline_operations_control_schema_extension (
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

CREATE TABLE airline_operations_control_airline_operations_control_control_assertion (
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

CREATE TABLE airline_operations_control_airline_operations_control_governed_model (
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

CREATE TABLE airline_operations_control_appgen_outbox_event (
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

CREATE TABLE airline_operations_control_appgen_inbox_event (
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

CREATE TABLE airline_operations_control_appgen_dead_letter_event (
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

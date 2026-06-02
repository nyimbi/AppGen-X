CREATE TABLE hospitality_property_operations_room_inventory (
    room_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    room_number TEXT NOT NULL,
    room_class TEXT NOT NULL,
    bed_configuration TEXT NOT NULL,
    zone TEXT NOT NULL,
    floor TEXT NOT NULL,
    accessibility_features_json TEXT NOT NULL,
    amenity_state_json TEXT NOT NULL,
    operational_status TEXT NOT NULL,
    housekeeping_status TEXT NOT NULL,
    inspection_status TEXT NOT NULL,
    maintenance_status TEXT NOT NULL,
    sellable_status TEXT NOT NULL,
    connected_room_id TEXT,
    current_stay_id TEXT,
    last_cleaned_at TEXT,
    last_inspected_at TEXT,
    return_to_service_at TEXT,
    priority_score REAL NOT NULL,
    notes_json TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_reservation (
    reservation_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    reservation_code TEXT NOT NULL,
    guest_name TEXT NOT NULL,
    status TEXT NOT NULL,
    guarantee_status TEXT NOT NULL,
    arrival_date TEXT NOT NULL,
    departure_date TEXT NOT NULL,
    arrival_window TEXT NOT NULL,
    room_class TEXT NOT NULL,
    accessible_required INTEGER NOT NULL,
    adults INTEGER NOT NULL,
    children INTEGER NOT NULL,
    source_channel TEXT NOT NULL,
    assigned_room_id TEXT,
    overbooking_priority REAL NOT NULL,
    cancellation_deadline TEXT NOT NULL,
    special_requests_json TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_guest_stay (
    stay_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    reservation_id TEXT NOT NULL,
    guest_name TEXT NOT NULL,
    lifecycle_state TEXT NOT NULL,
    room_id TEXT NOT NULL,
    check_in_at TEXT NOT NULL,
    check_out_due_at TEXT NOT NULL,
    actual_check_out_at TEXT,
    late_checkout_until TEXT,
    service_flags_json TEXT NOT NULL,
    notes_json TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_housekeeping_task (
    task_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    room_id TEXT NOT NULL,
    task_type TEXT NOT NULL,
    status TEXT NOT NULL,
    zone TEXT NOT NULL,
    shift_code TEXT NOT NULL,
    priority INTEGER NOT NULL,
    due_at TEXT NOT NULL,
    attendant TEXT,
    inspector TEXT,
    arrival_dependency INTEGER NOT NULL,
    expedite INTEGER NOT NULL,
    defect_count INTEGER NOT NULL,
    blocker_reason TEXT,
    evidence_json TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_guest_request (
    request_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    stay_id TEXT,
    room_id TEXT,
    category TEXT NOT NULL,
    urgency TEXT NOT NULL,
    status TEXT NOT NULL,
    promised_by TEXT NOT NULL,
    fulfillment_team TEXT NOT NULL,
    service_recovery INTEGER NOT NULL,
    guest_confirmed INTEGER NOT NULL,
    wait_reason TEXT,
    evidence_json TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_occupancy_snapshot (
    snapshot_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    stay_date TEXT NOT NULL,
    time_bucket TEXT NOT NULL,
    occupied_rooms INTEGER NOT NULL,
    vacant_clean_rooms INTEGER NOT NULL,
    vacant_dirty_rooms INTEGER NOT NULL,
    blocked_rooms INTEGER NOT NULL,
    arrivals_pending INTEGER NOT NULL,
    departures_pending INTEGER NOT NULL,
    stayovers INTEGER NOT NULL,
    same_day_turns INTEGER NOT NULL,
    oversell_risk REAL NOT NULL,
    notes_json TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_rate_plan (
    rate_plan_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    plan_code TEXT NOT NULL,
    room_class TEXT NOT NULL,
    status TEXT NOT NULL,
    closed_to_arrival INTEGER NOT NULL,
    minimum_stay INTEGER NOT NULL,
    maximum_stay INTEGER NOT NULL,
    sell_threshold INTEGER NOT NULL,
    price_delta REAL NOT NULL,
    package_inclusions_json TEXT NOT NULL,
    effective_from TEXT NOT NULL,
    effective_to TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_hospitality_property_operations_policy_rule (
    rule_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    rule_type TEXT NOT NULL,
    status TEXT NOT NULL,
    scope TEXT NOT NULL,
    condition_json TEXT NOT NULL,
    action_json TEXT NOT NULL,
    override_requires_reason INTEGER NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_hospitality_property_operations_runtime_parameter (
    parameter_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_value TEXT NOT NULL,
    min_value REAL NOT NULL,
    max_value REAL NOT NULL,
    status TEXT NOT NULL,
    effective_from TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_hospitality_property_operations_schema_extension (
    extension_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    table_name TEXT NOT NULL,
    field_name TEXT NOT NULL,
    field_type TEXT NOT NULL,
    status TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_hospitality_property_operations_control_assertion (
    assertion_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    assertion_name TEXT NOT NULL,
    subject_ref TEXT NOT NULL,
    status TEXT NOT NULL,
    checked_at TEXT NOT NULL,
    evidence_json TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_hospitality_property_operations_governed_model (
    model_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    model_name TEXT NOT NULL,
    status TEXT NOT NULL,
    use_case TEXT NOT NULL,
    approval_state TEXT NOT NULL,
    metadata_json TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_appgen_outbox_event (
    event_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    idempotency_key TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_appgen_inbox_event (
    event_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    source_pbc TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    idempotency_key TEXT NOT NULL
);

CREATE TABLE hospitality_property_operations_appgen_dead_letter_event (
    dead_letter_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    reason TEXT NOT NULL,
    idempotency_key TEXT NOT NULL
);

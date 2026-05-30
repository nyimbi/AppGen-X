CREATE TABLE defense_readiness_logistics_unit_readiness (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    formation_id TEXT,
    operation_code TEXT,
    unit_code TEXT NOT NULL,
    unit_name TEXT NOT NULL,
    mission_set TEXT NOT NULL,
    readiness_state TEXT NOT NULL,
    reported_state TEXT NOT NULL,
    validation_state TEXT NOT NULL,
    deployment_authorized INTEGER NOT NULL,
    commander_approved INTEGER NOT NULL,
    classification_marking TEXT NOT NULL,
    personnel_available INTEGER NOT NULL,
    personnel_required INTEGER NOT NULL,
    certified_roles_available INTEGER NOT NULL,
    certified_roles_required INTEGER NOT NULL,
    serviceable_assets INTEGER NOT NULL,
    required_assets INTEGER NOT NULL,
    supply_fill_rate REAL NOT NULL,
    minimum_supply_fill_rate REAL NOT NULL,
    ammo_fill_rate REAL NOT NULL,
    minimum_ammo_fill_rate REAL NOT NULL,
    fuel_days REAL NOT NULL,
    required_fuel_days REAL NOT NULL,
    blocker_codes_json TEXT NOT NULL,
    evidence_pack_id TEXT,
    narrative TEXT,
    assessment_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_mission_asset (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    unit_code TEXT NOT NULL,
    asset_code TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    serial_number TEXT,
    lot_batch TEXT,
    serviceability_state TEXT NOT NULL,
    acceptance_state TEXT NOT NULL,
    available_from TEXT,
    available_to TEXT,
    location_code TEXT,
    mission_assignment TEXT,
    controlled_item INTEGER NOT NULL,
    classification_marking TEXT NOT NULL,
    discrepancy_codes_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_supply_request (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    unit_code TEXT NOT NULL,
    mission_set TEXT NOT NULL,
    request_state TEXT NOT NULL,
    criticality TEXT NOT NULL,
    demand_json TEXT NOT NULL,
    on_hand_json TEXT NOT NULL,
    in_transit_json TEXT NOT NULL,
    approved_substitutes_json TEXT NOT NULL,
    shortage_json TEXT NOT NULL,
    readiness_score REAL NOT NULL,
    ammo_lot_code TEXT,
    fuel_required REAL NOT NULL,
    fuel_available REAL NOT NULL,
    required_by TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_maintenance_status (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    asset_code TEXT NOT NULL,
    maintenance_state TEXT NOT NULL,
    fault_codes_json TEXT NOT NULL,
    required_parts_json TEXT NOT NULL,
    available_parts_json TEXT NOT NULL,
    missing_parts_json TEXT NOT NULL,
    deferred_faults_json TEXT NOT NULL,
    safety_critical INTEGER NOT NULL,
    projected_return_at TEXT,
    confidence_score REAL NOT NULL,
    readiness_impact TEXT NOT NULL,
    depot_code TEXT,
    technician_gap INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_deployment_plan (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    unit_code TEXT NOT NULL,
    deployment_code TEXT NOT NULL,
    mission_set TEXT NOT NULL,
    release_state TEXT NOT NULL,
    kit_id TEXT,
    movement_id TEXT,
    movement_mode TEXT,
    departure_window TEXT,
    arrival_window TEXT,
    approval_evidence_json TEXT NOT NULL,
    blocker_codes_json TEXT NOT NULL,
    evidence_pack_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_readiness_inspection (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    unit_code TEXT NOT NULL,
    inspection_type TEXT NOT NULL,
    inspection_state TEXT NOT NULL,
    checklist_score REAL NOT NULL,
    evidence_pack_id TEXT,
    inspector_name TEXT NOT NULL,
    signatures_json TEXT NOT NULL,
    findings_json TEXT NOT NULL,
    corrective_actions_json TEXT NOT NULL,
    performed_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_logistics_movement (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    deployment_code TEXT NOT NULL,
    movement_state TEXT NOT NULL,
    movement_mode TEXT NOT NULL,
    route_code TEXT,
    route_reviewed INTEGER NOT NULL,
    force_protection_reviewed INTEGER NOT NULL,
    lift_confirmed INTEGER NOT NULL,
    fuel_required REAL NOT NULL,
    fuel_available REAL NOT NULL,
    hazardous_cargo INTEGER NOT NULL,
    dangerous_goods_documents INTEGER NOT NULL,
    custody_chain_verified INTEGER NOT NULL,
    load_plan_id TEXT,
    window_code TEXT,
    asset_ids_json TEXT NOT NULL,
    blocker_codes_json TEXT NOT NULL,
    released_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_personnel_qualification (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    unit_code TEXT NOT NULL,
    role_code TEXT NOT NULL,
    certified_count INTEGER NOT NULL,
    required_count INTEGER NOT NULL,
    available_count INTEGER NOT NULL,
    clearance_required INTEGER NOT NULL,
    clearance_gap INTEGER NOT NULL,
    expiry_window_code TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_ammunition_lot (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    unit_code TEXT NOT NULL,
    lot_code TEXT NOT NULL,
    munition_type TEXT NOT NULL,
    on_hand_quantity REAL NOT NULL,
    required_quantity REAL NOT NULL,
    restricted INTEGER NOT NULL,
    restriction_reason TEXT,
    compatibility_code TEXT,
    expiration_date TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_fuel_allocation (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    unit_code TEXT NOT NULL,
    allocation_code TEXT NOT NULL,
    fuel_type TEXT NOT NULL,
    on_hand_quantity REAL NOT NULL,
    required_quantity REAL NOT NULL,
    contingency_reserve REAL NOT NULL,
    refuel_points_json TEXT NOT NULL,
    sufficiency_state TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_movement_load_plan (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    movement_id TEXT NOT NULL,
    weight_total REAL NOT NULL,
    cube_total REAL NOT NULL,
    tie_down_points_required INTEGER NOT NULL,
    tie_down_points_available INTEGER NOT NULL,
    segregation_checked INTEGER NOT NULL,
    hazardous_class_json TEXT NOT NULL,
    validation_state TEXT NOT NULL,
    invalid_reasons_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_theater_support_request (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    operation_code TEXT NOT NULL,
    support_type TEXT NOT NULL,
    support_state TEXT NOT NULL,
    provider_name TEXT,
    support_scope TEXT NOT NULL,
    firm_commitment INTEGER NOT NULL,
    assumption_notes TEXT,
    evidence_ref TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_controlled_item_custody (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    movement_id TEXT NOT NULL,
    custody_item_code TEXT NOT NULL,
    custody_state TEXT NOT NULL,
    assigned_to TEXT,
    transferred_to TEXT,
    acknowledged_at TEXT,
    classification_marking TEXT NOT NULL,
    blocker_reason TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_readiness_exception (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    exception_type TEXT NOT NULL,
    exception_state TEXT NOT NULL,
    owner_role TEXT NOT NULL,
    severity TEXT NOT NULL,
    blocks_deployment INTEGER NOT NULL,
    source_table TEXT NOT NULL,
    source_id TEXT NOT NULL,
    blocker_code TEXT NOT NULL,
    narrative TEXT,
    opened_at TEXT NOT NULL,
    resolved_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_defense_readiness_logistics_policy_rule (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    rule_code TEXT NOT NULL,
    rule_scope TEXT NOT NULL,
    rule_state TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    policy_body_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_defense_readiness_logistics_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_value TEXT NOT NULL,
    parameter_type TEXT NOT NULL,
    min_value REAL,
    max_value REAL,
    parameter_state TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_defense_readiness_logistics_schema_extension (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    table_name TEXT NOT NULL,
    extension_state TEXT NOT NULL,
    field_manifest_json TEXT NOT NULL,
    justification TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_defense_readiness_logistics_control_assertion (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    control_id TEXT NOT NULL,
    control_state TEXT NOT NULL,
    asserted_by TEXT NOT NULL,
    evidence_ref TEXT,
    last_verified_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_defense_readiness_logistics_governed_model (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_state TEXT NOT NULL,
    model_version TEXT NOT NULL,
    approval_required INTEGER NOT NULL,
    citations_required INTEGER NOT NULL,
    redaction_profile TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    fact_type TEXT NOT NULL,
    aggregate_table TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    emitted_at TEXT NOT NULL,
    delivery_state TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    event_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    fact_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    received_at TEXT NOT NULL,
    replay_state TEXT NOT NULL
);

CREATE TABLE defense_readiness_logistics_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    event_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    error_message TEXT NOT NULL,
    retry_count INTEGER NOT NULL,
    dead_lettered_at TEXT NOT NULL,
    resolution_state TEXT NOT NULL
);

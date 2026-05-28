CREATE TABLE IF NOT EXISTS building_information_modeling_ops_bim_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    model_code TEXT NOT NULL,
    discipline TEXT NOT NULL,
    authoring_party TEXT NOT NULL,
    status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_model_version (
    id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    tenant TEXT NOT NULL,
    discipline TEXT NOT NULL,
    issue_purpose TEXT NOT NULL,
    approval_state TEXT NOT NULL,
    coordinate_basis TEXT NOT NULL,
    survey_point_json TEXT NOT NULL,
    project_base_point_json TEXT NOT NULL,
    true_north_degrees REAL NOT NULL,
    elevation_datum TEXT NOT NULL,
    unit_scale REAL NOT NULL,
    spatial_coverage_json TEXT NOT NULL,
    lod_target TEXT NOT NULL,
    checksum TEXT NOT NULL,
    superseded_by_version_id TEXT,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_clash_issue (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    version_id TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_asset_object (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    version_id TEXT NOT NULL,
    asset_tag TEXT NOT NULL,
    system_name TEXT,
    location_code TEXT,
    status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_handover_package (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    federation_id TEXT NOT NULL,
    status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_model_review (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    version_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_digital_twin_link (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    version_id TEXT NOT NULL,
    status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_building_information_modeling_ops_policy_rule (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    rule_code TEXT NOT NULL,
    rule_scope TEXT NOT NULL,
    status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_building_information_modeling_ops_runtime_parameter (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_value TEXT NOT NULL,
    status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_building_information_modeling_ops_schema_extension (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    table_name TEXT NOT NULL,
    field_name TEXT NOT NULL,
    status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_building_information_modeling_ops_control_assertion (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    control_code TEXT NOT NULL,
    target_scope TEXT NOT NULL,
    status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_building_information_modeling_ops_governed_model (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    federation_id TEXT NOT NULL,
    release_status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_appgen_outbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_appgen_inbox_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_information_modeling_ops_appgen_dead_letter_event (
    id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    event_type TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload TEXT NOT NULL,
    failure_reason TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE SCHEMA IF NOT EXISTS composition_engine;

CREATE TABLE composition_engine_composition_workspace (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  workspace_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  owner VARCHAR(255) NOT NULL,
  target VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  selected_pbcs TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_component_registry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  component_id VARCHAR(255) NOT NULL,
  pbc VARCHAR(255) NOT NULL,
  fragment VARCHAR(255) NOT NULL,
  permissions TEXT NOT NULL,
  schemas TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  compatibility VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_ui_fragment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  fragment_id VARCHAR(255) NOT NULL,
  component_id VARCHAR(255) NOT NULL,
  route VARCHAR(255) NOT NULL,
  slots TEXT NOT NULL,
  events TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_layout_binding (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  binding_id VARCHAR(255) NOT NULL,
  workspace_id VARCHAR(255) NOT NULL,
  page VARCHAR(255) NOT NULL,
  slot VARCHAR(255) NOT NULL,
  fragment_id VARCHAR(255) NOT NULL,
  projection VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_dsl_artifact (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  artifact_id VARCHAR(255) NOT NULL,
  workspace_id VARCHAR(255) NOT NULL,
  route_count INTEGER NOT NULL,
  checksum VARCHAR(255) NOT NULL,
  event_contract VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_composition_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  workspace_id VARCHAR(255) NOT NULL,
  selected_pbcs TEXT NOT NULL,
  route_count INTEGER NOT NULL,
  bindings TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_composition_validation_run (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  validation_id VARCHAR(255) NOT NULL,
  workspace_id VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  blockers TEXT NOT NULL,
  missing_fragments TEXT NOT NULL,
  route_count INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_package_registration_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255) NOT NULL,
  workspace_id VARCHAR(255) NOT NULL,
  requested_by VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  side_effect_free VARCHAR(255) NOT NULL,
  writes_performed TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_package_index_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  workspace_id VARCHAR(255) NOT NULL,
  selected_pbcs TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  entry_source VARCHAR(255) NOT NULL,
  indexed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_release_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  workspace_id VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  route_count INTEGER NOT NULL,
  release_risk VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  package_registration_plan TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_composition_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  required_fragments TEXT NOT NULL,
  allowed_meshes TEXT NOT NULL,
  route_policy VARCHAR(255) NOT NULL,
  requires_approval VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_composition_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  key VARCHAR(255) NOT NULL,
  value TEXT NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_composition_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_timezone VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE composition_engine_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

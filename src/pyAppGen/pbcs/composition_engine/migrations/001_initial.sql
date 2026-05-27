CREATE SCHEMA IF NOT EXISTS composition_engine;

CREATE TABLE composition_workspace (
  tenant TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  name TEXT,
  owner TEXT,
  target TEXT,
  version INTEGER,
  status TEXT NOT NULL,
  selected_pbcs TEXT,
  PRIMARY KEY (workspace_id)
);

CREATE TABLE component_registry (
  tenant TEXT NOT NULL,
  component_id TEXT NOT NULL,
  pbc TEXT,
  fragment TEXT,
  permissions TEXT,
  schemas TEXT,
  status TEXT NOT NULL,
  compatibility TEXT,
  PRIMARY KEY (component_id)
);

CREATE TABLE ui_fragment (
  tenant TEXT NOT NULL,
  fragment_id TEXT NOT NULL,
  component_id TEXT,
  route TEXT,
  slots TEXT,
  events TEXT,
  status TEXT NOT NULL,
  PRIMARY KEY (fragment_id)
);

CREATE TABLE layout_binding (
  tenant TEXT NOT NULL,
  binding_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  page TEXT,
  slot TEXT,
  fragment_id TEXT,
  projection TEXT,
  status TEXT NOT NULL,
  PRIMARY KEY (binding_id)
);

CREATE TABLE dsl_artifact (
  tenant TEXT NOT NULL,
  artifact_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  route_count INTEGER,
  checksum TEXT,
  event_contract TEXT,
  status TEXT NOT NULL,
  PRIMARY KEY (artifact_id)
);

CREATE TABLE composition_plan (
  tenant TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  selected_pbcs TEXT,
  route_count INTEGER,
  bindings TEXT,
  status TEXT NOT NULL,
  PRIMARY KEY (workspace_id)
);

CREATE TABLE composition_validation_run (
  tenant TEXT NOT NULL,
  validation_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  decision TEXT,
  blockers TEXT,
  missing_fragments TEXT,
  route_count INTEGER,
  PRIMARY KEY (validation_id)
);

CREATE TABLE package_registration_plan (
  tenant TEXT NOT NULL,
  plan_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  requested_by TEXT,
  status TEXT NOT NULL,
  side_effect_free BOOLEAN,
  writes_performed TEXT,
  PRIMARY KEY (plan_id)
);

CREATE TABLE package_index_entry (
  tenant TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  selected_pbcs TEXT,
  status TEXT NOT NULL,
  entry_source TEXT,
  indexed_at TIMESTAMP,
  PRIMARY KEY (workspace_id)
);

CREATE TABLE release_evidence (
  tenant TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  version INTEGER,
  route_count INTEGER,
  release_risk DECIMAL(12,4),
  status TEXT NOT NULL,
  package_registration_plan TEXT,
  PRIMARY KEY (workspace_id)
);

CREATE TABLE composition_rule (
  tenant TEXT NOT NULL,
  rule_id TEXT NOT NULL,
  scope TEXT,
  required_fragments TEXT,
  allowed_meshes TEXT,
  route_policy TEXT,
  requires_approval BOOLEAN,
  status TEXT NOT NULL,
  PRIMARY KEY (rule_id)
);

CREATE TABLE composition_parameter (
  tenant TEXT NOT NULL,
  parameter_id TEXT NOT NULL,
  key TEXT,
  value TEXT,
  effective_at TIMESTAMP,
  status TEXT NOT NULL,
  PRIMARY KEY (parameter_id)
);

CREATE TABLE composition_configuration (
  tenant TEXT NOT NULL,
  configuration_id TEXT NOT NULL,
  database_backend TEXT,
  event_topic TEXT,
  retry_limit INTEGER,
  default_timezone TEXT,
  status TEXT NOT NULL,
  PRIMARY KEY (configuration_id)
);

CREATE TABLE composition_engine_appgen_outbox_event (
  tenant TEXT NOT NULL,
  event_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  payload TEXT,
  idempotency_key TEXT NOT NULL,
  status TEXT NOT NULL,
  PRIMARY KEY (event_id)
);

CREATE TABLE composition_engine_appgen_inbox_event (
  tenant TEXT NOT NULL,
  event_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  payload TEXT,
  idempotency_key TEXT NOT NULL,
  attempts INTEGER,
  PRIMARY KEY (event_id)
);

CREATE TABLE composition_engine_dead_letter_event (
  tenant TEXT NOT NULL,
  event_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  reason TEXT,
  payload TEXT,
  attempts INTEGER,
  PRIMARY KEY (event_id)
);

-- Relationship: ui_fragment.component_id -> component_registry.component_id
-- Relationship: layout_binding.workspace_id -> composition_workspace.workspace_id
-- Relationship: layout_binding.fragment_id -> ui_fragment.fragment_id
-- Relationship: dsl_artifact.workspace_id -> composition_workspace.workspace_id
-- Relationship: composition_plan.workspace_id -> composition_workspace.workspace_id
-- Relationship: composition_validation_run.workspace_id -> composition_workspace.workspace_id
-- Relationship: package_registration_plan.workspace_id -> composition_workspace.workspace_id
-- Relationship: package_index_entry.workspace_id -> composition_workspace.workspace_id
-- Relationship: release_evidence.workspace_id -> composition_workspace.workspace_id

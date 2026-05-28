CREATE SCHEMA IF NOT EXISTS enterprise_pim;

CREATE TABLE enterprise_pim_product_taxonomy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  taxonomy_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  parent_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_taxonomy_node (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  taxonomy_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  depth VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_taxonomy_relationship (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  relationship_id VARCHAR(255) NOT NULL,
  from_taxonomy_id VARCHAR(255) NOT NULL,
  to_taxonomy_id VARCHAR(255) NOT NULL,
  relationship_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_taxonomy_publication (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  publication_id VARCHAR(255) NOT NULL,
  taxonomy_id VARCHAR(255) NOT NULL,
  channels VARCHAR(255) NOT NULL,
  readiness_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_taxonomy_classification_candidate (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  taxonomy_id VARCHAR(255) NOT NULL,
  entity_ref VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_product_attribute (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  attribute_id VARCHAR(255) NOT NULL,
  taxonomy_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  data_type VARCHAR(255) NOT NULL,
  required VARCHAR(255) NOT NULL,
  effective_value VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_attribute_group (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  group_id VARCHAR(255) NOT NULL,
  taxonomy_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  sequence VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_attribute_value_option (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  option_id VARCHAR(255) NOT NULL,
  attribute_id VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  label VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_attribute_inheritance_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  inheritance_rule_id VARCHAR(255) NOT NULL,
  source_attribute_id VARCHAR(255) NOT NULL,
  target_attribute_id VARCHAR(255) NOT NULL,
  depth VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_attribute_validation_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  validation_rule_id VARCHAR(255) NOT NULL,
  attribute_id VARCHAR(255) NOT NULL,
  data_type VARCHAR(255) NOT NULL,
  required VARCHAR(255) NOT NULL,
  pattern VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_attribute_quality_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  quality_signal_id VARCHAR(255) NOT NULL,
  attribute_id VARCHAR(255) NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_localized_content (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  content_id VARCHAR(255) NOT NULL,
  entity_id VARCHAR(255) NOT NULL,
  entity_type VARCHAR(255) NOT NULL,
  locale VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_localized_content_version (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  content_version_id VARCHAR(255) NOT NULL,
  content_id VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  title VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_translation_memory_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  translation_id VARCHAR(255) NOT NULL,
  source_locale VARCHAR(255) NOT NULL,
  target_locale VARCHAR(255) NOT NULL,
  source_text_hash VARCHAR(255) NOT NULL,
  target_text VARCHAR(255) NOT NULL,
  quality_score DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_locale_fallback_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  fallback_rule_id VARCHAR(255) NOT NULL,
  locale VARCHAR(255) NOT NULL,
  fallback_locale VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_content_completeness_score (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  score_id DECIMAL(18, 4) NOT NULL,
  entity_id VARCHAR(255) NOT NULL,
  locale_count INTEGER NOT NULL,
  attribute_count INTEGER NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_validation_workflow (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  entity_id VARCHAR(255) NOT NULL,
  entity_type VARCHAR(255) NOT NULL,
  requested_by VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  sla_hours VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_validation_workflow_step (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  step_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  approver_role VARCHAR(255) NOT NULL,
  sequence VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_approval_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  approval_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  approver VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  decided_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_publication_readiness_check (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  readiness_check_id VARCHAR(255) NOT NULL,
  entity_id VARCHAR(255) NOT NULL,
  locales_ready VARCHAR(255) NOT NULL,
  attributes_ready VARCHAR(255) NOT NULL,
  dependencies_ready VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_dependency_schema (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  dependency_schema_id VARCHAR(255) NOT NULL,
  dependency VARCHAR(255) NOT NULL,
  schema_version VARCHAR(255) NOT NULL,
  events VARCHAR(255) NOT NULL,
  fields VARCHAR(255) NOT NULL,
  accepted VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_dependency_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) NOT NULL,
  dependency VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  entity_id VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_media_dependency_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_price_dependency_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_tax_dependency_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_inventory_dependency_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_search_dependency_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_catalog_publication_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_channel_publication_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_product_relationship (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_product_bundle_definition (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_product_variant_family (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_product_variant_member (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_assortment_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_data_steward_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_exception_resolution_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_audit_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_master_data_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_carbon_enrichment_window (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_taxonomy_optimization_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_workflow_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_content_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_enrichment_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_enrichment_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_semantic_instruction_parse (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  required_locales VARCHAR(255) NOT NULL,
  required_attributes VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_pim_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_locale VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE SCHEMA IF NOT EXISTS product_catalog_pim;

CREATE TABLE product_catalog_pim_product (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  family_id VARCHAR(255) PRIMARY KEY NOT NULL,
  sku VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  lifecycle_state VARCHAR(255) NOT NULL,
  owner VARCHAR(255) NOT NULL,
  taxonomy VARCHAR(255) NOT NULL,
  completeness VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (family_id) REFERENCES product_catalog_pim_product_family(family_id)
);

CREATE TABLE product_catalog_pim_product_family (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  family_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  taxonomy VARCHAR(255) NOT NULL,
  variant_axes VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_variant (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  variant_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  family_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_product_variant_option (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  variant_option_id VARCHAR(255) PRIMARY KEY NOT NULL,
  variant_id VARCHAR(255) PRIMARY KEY NOT NULL,
  axis VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (variant_id) REFERENCES product_catalog_pim_product_variant(variant_id)
);

CREATE TABLE product_catalog_pim_product_variant_member (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  variant_member_id VARCHAR(255) PRIMARY KEY NOT NULL,
  variant_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) NOT NULL,
  option_signature VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (variant_id) REFERENCES product_catalog_pim_product_variant(variant_id),
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_product_taxonomy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  taxonomy_id VARCHAR(255) PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  parent_taxonomy_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_taxonomy_node (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  node_id VARCHAR(255) PRIMARY KEY NOT NULL,
  taxonomy_id VARCHAR(255) PRIMARY KEY NOT NULL,
  parent_node_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  depth VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_taxonomy_relationship (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  relationship_id VARCHAR(255) PRIMARY KEY NOT NULL,
  from_taxonomy_id VARCHAR(255) PRIMARY KEY NOT NULL,
  to_taxonomy_id VARCHAR(255) NOT NULL,
  relationship_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_category (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  category_id VARCHAR(255) PRIMARY KEY NOT NULL,
  taxonomy_id VARCHAR(255) PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  channel_scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_category_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assignment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  category_id VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id),
  FOREIGN KEY (category_id) REFERENCES product_catalog_pim_product_category(category_id)
);

CREATE TABLE product_catalog_pim_product_attribute_schema (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schema_id VARCHAR(255) PRIMARY KEY NOT NULL,
  family_id VARCHAR(255) PRIMARY KEY NOT NULL,
  attributes VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (family_id) REFERENCES product_catalog_pim_product_family(family_id)
);

CREATE TABLE product_catalog_pim_product_attribute (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  attribute_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  attribute_name VARCHAR(255) NOT NULL,
  attribute_value VARCHAR(255) NOT NULL,
  schema_version VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_product_attribute_validation_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  validation_rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  schema_id VARCHAR(255) PRIMARY KEY NOT NULL,
  attribute_name VARCHAR(255) NOT NULL,
  data_type VARCHAR(255) NOT NULL,
  required VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (schema_id) REFERENCES product_catalog_pim_product_attribute_schema(schema_id)
);

CREATE TABLE product_catalog_pim_product_attribute_value_option (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  value_option_id VARCHAR(255) PRIMARY KEY NOT NULL,
  schema_id VARCHAR(255) PRIMARY KEY NOT NULL,
  attribute_name VARCHAR(255) NOT NULL,
  option_value VARCHAR(255) NOT NULL,
  sort_order VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (schema_id) REFERENCES product_catalog_pim_product_attribute_schema(schema_id)
);

CREATE TABLE product_catalog_pim_product_price (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  price_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  currency VARCHAR(255) NOT NULL,
  list_price VARCHAR(255) NOT NULL,
  cost DECIMAL(18, 4) NOT NULL,
  margin VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_product_channel_price (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  channel_price_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  channel VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  list_price VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_product_media (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  media_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  role VARCHAR(255) NOT NULL,
  asset_ref VARCHAR(255) NOT NULL,
  rights_status VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_product_locale_content (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  content_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  locale VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  seo_slug VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_product_localization_memory (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  translation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_locale VARCHAR(255) NOT NULL,
  target_locale VARCHAR(255) NOT NULL,
  quality_score DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_seo_metadata (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  seo_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  locale VARCHAR(255) NOT NULL,
  title_tag VARCHAR(255) NOT NULL,
  meta_description VARCHAR(255) NOT NULL,
  canonical_url VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_compliance_claim (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  claim_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  region VARCHAR(255) NOT NULL,
  claim_type VARCHAR(255) NOT NULL,
  screening_status VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_product_lifecycle_stage (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  lifecycle_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  stage VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_product_approval_workflow (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  workflow_type VARCHAR(255) NOT NULL,
  required_approvers VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_approval_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  workflow_id VARCHAR(255) PRIMARY KEY NOT NULL,
  approver VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  decided_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (workflow_id) REFERENCES product_catalog_pim_product_approval_workflow(workflow_id)
);

CREATE TABLE product_catalog_pim_product_assortment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assortment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  season VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_assortment_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assignment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  assortment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (assortment_id) REFERENCES product_catalog_pim_product_assortment(assortment_id),
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_catalog_publication (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  publication_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  channels VARCHAR(255) NOT NULL,
  locales VARCHAR(255) NOT NULL,
  readiness_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_catalog_channel_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  channel VARCHAR(255) NOT NULL,
  locale VARCHAR(255) NOT NULL,
  projection_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_catalog_channel_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) PRIMARY KEY NOT NULL,
  channel VARCHAR(255) NOT NULL,
  required_attributes VARCHAR(255) NOT NULL,
  required_media_roles VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_catalog_syndication_feed (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  feed_id VARCHAR(255) PRIMARY KEY NOT NULL,
  channel VARCHAR(255) NOT NULL,
  format VARCHAR(255) NOT NULL,
  cadence VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_catalog_syndication_delivery (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  delivery_id VARCHAR(255) PRIMARY KEY NOT NULL,
  feed_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  delivery_status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (feed_id) REFERENCES product_catalog_pim_catalog_syndication_feed(feed_id),
  FOREIGN KEY (product_id) REFERENCES product_catalog_pim_product(product_id)
);

CREATE TABLE product_catalog_pim_product_enrichment_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  task_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  task_type VARCHAR(255) NOT NULL,
  assignee VARCHAR(255) NOT NULL,
  priority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_data_quality_score (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  quality_score_id DECIMAL(18, 4) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  completeness_score DECIMAL(18, 4) NOT NULL,
  content_score DECIMAL(18, 4) NOT NULL,
  quality_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_data_quality_issue (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  issue_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  issue_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_bundle_definition (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  bundle_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  component_product_ids VARCHAR(255) NOT NULL,
  bundle_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_relationship (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  relationship_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  target_product_id VARCHAR(255) NOT NULL,
  relationship_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_identity_credential (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  credential_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  did VARCHAR(255) NOT NULL,
  issuer VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_graph_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_count INTEGER NOT NULL,
  edge_count INTEGER NOT NULL,
  projection_hash VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_semantic_embedding (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  embedding_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  embedding_model VARCHAR(255) NOT NULL,
  vector_ref VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_readiness_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  forecast_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  forecast_readiness VARCHAR(255) NOT NULL,
  ready_date TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  risk_model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  screening_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  policy_scope VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_publication_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  proof_type VARCHAR(255) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  channel_scope VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_audit_trace (
  tenant VARCHAR(255) NOT NULL,
  trace_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  trace_type VARCHAR(255) NOT NULL,
  trace_hash VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) PRIMARY KEY NOT NULL,
  table_name VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  control_id VARCHAR(255) PRIMARY KEY NOT NULL,
  assertion_type VARCHAR(255) NOT NULL,
  subject_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  tested_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  feature_lineage VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  seed_id VARCHAR(255) PRIMARY KEY NOT NULL,
  seed_type VARCHAR(255) NOT NULL,
  seed_ref VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  loaded_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rule_type VARCHAR(255) NOT NULL,
  allowed_channels VARCHAR(255) NOT NULL,
  allowed_locales VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) PRIMARY KEY NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE product_catalog_pim_product_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) PRIMARY KEY NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_timezone VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

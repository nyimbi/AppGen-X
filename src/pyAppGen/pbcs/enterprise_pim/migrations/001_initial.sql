CREATE SCHEMA IF NOT EXISTS enterprise_pim;

CREATE TABLE enterprise_pim_product_taxonomy (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_pim_taxonomy_node (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_taxonomy_relationship (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_product_attribute (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_attribute_group (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_attribute_validation_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_localized_content (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_localized_content_version (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_validation_workflow (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_validation_workflow_step (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_approval_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_publication_readiness_check (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_dependency_schema (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_dependency_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_pim_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_pim_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_pim_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  product_taxonomy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (product_taxonomy_id) REFERENCES enterprise_pim_product_taxonomy(id)
);

CREATE TABLE enterprise_pim_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE enterprise_pim_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE enterprise_pim_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

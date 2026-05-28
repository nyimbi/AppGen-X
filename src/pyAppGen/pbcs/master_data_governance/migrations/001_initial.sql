CREATE SCHEMA IF NOT EXISTS master_data_governance;

CREATE TABLE master_data_governance_master_record (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE master_data_governance_golden_record (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  master_record_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_record_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_match_candidate (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  master_record_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_record_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_merge_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  master_record_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_record_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_survivorship_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  master_record_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_record_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_data_quality_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  master_record_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_record_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_stewardship_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  master_record_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_record_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_downstream_sync_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  master_record_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_record_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  master_record_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE master_data_governance_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  master_record_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE master_data_governance_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  master_record_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

-- World-class domain depth supplemental tables
CREATE SCHEMA IF NOT EXISTS master_data_governance;

CREATE TABLE master_data_governance_master_record (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE master_data_governance_master_domain (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_source_record_link (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_match_candidate (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_match_decision (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_survivorship_rule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_survivorship_decision (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_golden_record_version (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_hierarchy_node (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_hierarchy_relationship (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_data_quality_rule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_data_quality_observation (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_stewardship_task (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_master_data_approval (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_publication_batch (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_publication_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_master_exception_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_mdm_policy_rule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE master_data_governance_mdm_runtime_parameter (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE master_data_governance_mdm_schema_extension (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE master_data_governance_mdm_control_assertion (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE master_data_governance_mdm_governed_model (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE master_data_governance_appgen_outbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_appgen_inbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

CREATE TABLE master_data_governance_appgen_dead_letter_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  master_data_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (master_data_id) REFERENCES master_data_governance_master_record(id)
);

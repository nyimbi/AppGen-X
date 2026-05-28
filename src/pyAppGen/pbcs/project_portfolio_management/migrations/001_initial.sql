CREATE SCHEMA IF NOT EXISTS project_portfolio_management;

CREATE TABLE project_portfolio_management_portfolio (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE project_portfolio_management_program (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  portfolio_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio(id)
);

CREATE TABLE project_portfolio_management_project (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  portfolio_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio(id)
);

CREATE TABLE project_portfolio_management_project_milestone (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  portfolio_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio(id)
);

CREATE TABLE project_portfolio_management_project_budget (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  portfolio_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio(id)
);

CREATE TABLE project_portfolio_management_resource_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  portfolio_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio(id)
);

CREATE TABLE project_portfolio_management_project_risk (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  portfolio_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio(id)
);

CREATE TABLE project_portfolio_management_benefit_realization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  portfolio_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio(id)
);

CREATE TABLE project_portfolio_management_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  portfolio_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE project_portfolio_management_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  portfolio_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE project_portfolio_management_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  portfolio_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

-- World-class domain depth supplemental tables
CREATE SCHEMA IF NOT EXISTS project_portfolio_management;

CREATE TABLE project_portfolio_management_portfolio_item (
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

CREATE TABLE project_portfolio_management_portfolio_program (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_business_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_portfolio_score (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_prioritization_run (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_stage_gate (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_gate_decision (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_project_dependency (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_resource_demand (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_resource_assignment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_benefit_hypothesis (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_benefit_realization (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_portfolio_risk (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_portfolio_issue (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_change_request (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_portfolio_financial_snapshot (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_portfolio_exception_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_portfolio_policy_rule (
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

CREATE TABLE project_portfolio_management_portfolio_runtime_parameter (
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

CREATE TABLE project_portfolio_management_portfolio_schema_extension (
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

CREATE TABLE project_portfolio_management_portfolio_control_assertion (
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

CREATE TABLE project_portfolio_management_portfolio_governed_model (
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

CREATE TABLE project_portfolio_management_appgen_outbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_appgen_inbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

CREATE TABLE project_portfolio_management_appgen_dead_letter_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  portfolio_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES project_portfolio_management_portfolio_item(id)
);

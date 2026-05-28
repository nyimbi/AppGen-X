PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customer_success_management_customer_success_account (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT,
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_success_plan (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_onboarding_milestone (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_adoption_signal (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_health_score (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_health_score_component (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_success_playbook (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_playbook_task (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_customer_escalation (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_renewal_motion (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_expansion_opportunity (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_executive_business_review (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_customer_objective (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_customer_value_realization (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_churn_risk_signal (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_success_exception_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT REFERENCES customer_success_management_customer_success_account(id),
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_success_policy_rule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT,
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_success_runtime_parameter (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT,
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_success_schema_extension (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT,
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_success_control_assertion (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT,
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_success_governed_model (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT,
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_appgen_outbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT,
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT UNIQUE,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_appgen_inbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT,
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT UNIQUE,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_success_management_appgen_dead_letter_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT,
  owner TEXT,
  status TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  success_account_id TEXT,
  score REAL,
  due_on TEXT,
  event_type TEXT,
  topic TEXT,
  idempotency_key TEXT UNIQUE,
  attempts INTEGER DEFAULT 0,
  last_error TEXT,
  payload TEXT,
  effective_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS customer_success_management_account_tenant_idx
  ON customer_success_management_customer_success_account (tenant, status);

CREATE INDEX IF NOT EXISTS customer_success_management_health_score_account_idx
  ON customer_success_management_health_score (success_account_id, created_at);

CREATE INDEX IF NOT EXISTS customer_success_management_playbook_task_account_idx
  ON customer_success_management_playbook_task (success_account_id, status);

CREATE INDEX IF NOT EXISTS customer_success_management_renewal_motion_account_idx
  ON customer_success_management_renewal_motion (success_account_id, due_on);

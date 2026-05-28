CREATE SCHEMA IF NOT EXISTS field_service_management;

CREATE TABLE field_service_management_field_work_order (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE field_service_management_dispatch_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  field_work_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_work_order_id) REFERENCES field_service_management_field_work_order(id)
);

CREATE TABLE field_service_management_technician_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  field_work_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_work_order_id) REFERENCES field_service_management_field_work_order(id)
);

CREATE TABLE field_service_management_mobile_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  field_work_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_work_order_id) REFERENCES field_service_management_field_work_order(id)
);

CREATE TABLE field_service_management_parts_usage (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  field_work_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_work_order_id) REFERENCES field_service_management_field_work_order(id)
);

CREATE TABLE field_service_management_service_sla (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  field_work_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_work_order_id) REFERENCES field_service_management_field_work_order(id)
);

CREATE TABLE field_service_management_service_history (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  field_work_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_work_order_id) REFERENCES field_service_management_field_work_order(id)
);

CREATE TABLE field_service_management_customer_service_update (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  field_work_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (field_work_order_id) REFERENCES field_service_management_field_work_order(id)
);

CREATE TABLE field_service_management_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  field_work_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE field_service_management_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  field_work_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE field_service_management_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  field_work_order_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

-- World-class domain depth supplemental tables
CREATE SCHEMA IF NOT EXISTS field_service_management;

CREATE TABLE field_service_management_work_order (
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

CREATE TABLE field_service_management_service_request (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_service_appointment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_technician_profile (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_technician_skill (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_dispatch_plan (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_dispatch_assignment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_service_part_requirement (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_part_reservation (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_mobile_work_log (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_service_checklist (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_warranty_entitlement (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_sla_commitment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_sla_observation (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_customer_confirmation (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_repeat_visit_signal (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_field_exception_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_field_policy_rule (
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

CREATE TABLE field_service_management_field_runtime_parameter (
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

CREATE TABLE field_service_management_field_schema_extension (
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

CREATE TABLE field_service_management_field_control_assertion (
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

CREATE TABLE field_service_management_field_governed_model (
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

CREATE TABLE field_service_management_appgen_outbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_appgen_inbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

CREATE TABLE field_service_management_appgen_dead_letter_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  service_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (service_id) REFERENCES field_service_management_work_order(id)
);

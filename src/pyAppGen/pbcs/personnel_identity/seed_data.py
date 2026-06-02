"""Executable seed-data contract for the personnel_identity PBC."""

from __future__ import annotations

from .runtime import PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC


PBC_KEY = "personnel_identity"
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_country": "US",
    "allowed_worker_types": ("employee", "contractor"),
    "allowed_statuses": ("active", "leave", "terminated"),
    "privacy_region": "US",
    "default_identity_assurance": 0.86,
    "workbench_limit": 75,
}
DEFAULT_PARAMETERS = {
    "max_roles_per_worker": 4,
    "access_risk_threshold": 0.7,
    "manager_span_limit": 8,
    "identity_assurance_threshold": 0.75,
    "stale_attribute_age_days": 180,
    "review_cadence_days": 90,
    "lifecycle_grace_days": 14,
    "provisioning_retry_limit": 3,
    "org_depth_limit": 8,
    "workbench_limit": 75,
}
DEFAULT_RULE = {
    "rule_id": "personnel_identity.employee.default",
    "tenant": "tenant_demo",
    "rule_type": "identity",
    "allowed_worker_types": ("employee", "contractor"),
    "allowed_statuses": ("active", "leave", "terminated"),
    "required_attributes": ("email", "government_id"),
    "sensitive_roles": ("payroll_admin", "security_admin"),
    "blocked_role_pairs": (("payroll_admin", "payroll_approver"),),
    "status": "active",
}


def demo_workspace_seed_bundle(tenant: str = "tenant_demo") -> dict:
    department = {"department_id": f"dept_{tenant}_people", "tenant": tenant, "name": "People Operations", "parent_department_id": None, "cost_center": "people"}
    manager = {"employee_id": f"emp_{tenant}_manager", "tenant": tenant, "department_id": department["department_id"], "manager_employee_id": None, "worker_type": "employee", "status": "active", "job": "People Director", "country": "US"}
    employee = {"employee_id": f"emp_{tenant}_001", "tenant": tenant, "department_id": department["department_id"], "manager_employee_id": manager["employee_id"], "worker_type": "employee", "status": "active", "job": "People Analyst", "country": "US"}
    attributes = (("email", f"{employee['employee_id']}@example.com", 0.96), ("government_id", "hash:demo-government-id", 0.91))
    projection_events = (
        {"event_id": f"provision_{tenant}_001", "event_type": "EmployeeProvisioned", "payload": {"tenant": tenant, "employee_id": employee["employee_id"], "system": "directory"}},
        {"event_id": f"policy_{tenant}_001", "event_type": "AccessPolicyChanged", "payload": {"tenant": tenant, "policy_id": f"policy_{tenant}_001", "status": "clear"}},
        {"event_id": f"org_{tenant}_001", "event_type": "OrgUnitChanged", "payload": {"tenant": tenant, "department_id": department["department_id"], "name": department["name"]}},
    )
    seed_rows = (
        {"table": "personnel_identity_personnel_department", "rows": ({"tenant": tenant, "department_id": department["department_id"], "status": "active"},)},
        {"table": "personnel_identity_personnel_employee", "rows": ({"tenant": tenant, "employee_id": manager["employee_id"], "status": "active"}, {"tenant": tenant, "employee_id": employee["employee_id"], "status": "active"})},
        {"table": "personnel_identity_personnel_role_assignment", "rows": ({"tenant": tenant, "assignment_id": f"role_{employee['employee_id']}_employee", "status": "active"},)},
        {"table": "personnel_identity_personnel_identity_attribute", "rows": tuple({"tenant": tenant, "attribute_id": f"{employee['employee_id']}:{name}", "status": "active"} for name, _value, _assurance in attributes)},
        {"table": "personnel_identity_personnel_policy_rule", "rows": ({"tenant": tenant, "record_id": DEFAULT_RULE["rule_id"], "status": "active"},)},
        {"table": "personnel_identity_personnel_parameter", "rows": tuple({"tenant": tenant, "record_id": key, "status": "configured"} for key in DEFAULT_PARAMETERS)},
        {"table": "personnel_identity_personnel_configuration", "rows": ({"tenant": tenant, "record_id": f"cfg_{tenant}", "status": "configured"},)},
    )
    return {"tenant": tenant, "configuration": dict(DEFAULT_CONFIGURATION), "parameters": dict(DEFAULT_PARAMETERS), "rule": {**DEFAULT_RULE, "tenant": tenant}, "department": department, "manager": manager, "employee": employee, "attributes": attributes, "projection_events": projection_events, "seed_rows": seed_rows}


SEED_DATA = demo_workspace_seed_bundle()["seed_rows"]


def seed_plan(tenant: str = "tenant_demo") -> dict:
    """Return deterministic seed rows without applying them."""
    bundle = demo_workspace_seed_bundle(tenant=tenant)
    tables = tuple(dict.fromkeys(item["table"] for item in bundle["seed_rows"]))
    return {"ok": bool(bundle["seed_rows"]), "pbc": PBC_KEY, "tables": tables, "rows": bundle["seed_rows"], "configuration": bundle["configuration"], "parameters": bundle["parameters"], "side_effects": ()}


def validate_seed_data(tenant: str = "tenant_demo") -> dict:
    """Validate seed ownership and minimum row shape."""
    plan = seed_plan(tenant=tenant)
    invalid_tables = tuple(item["table"] for item in plan["rows"] if not item.get("table", "").startswith(f"{PBC_KEY}_"))
    invalid_rows = tuple(row for item in plan["rows"] for row in item.get("rows", ()) if not row.get("tenant") or not any(key in row for key in ("department_id", "employee_id", "assignment_id", "attribute_id", "record_id")))
    return {"ok": plan["ok"] and not invalid_tables and not invalid_rows, "pbc": PBC_KEY, "plan": plan, "invalid_tables": invalid_tables, "invalid_rows": invalid_rows, "side_effects": ()}


def smoke_test() -> dict:
    """Exercise seed validation without writing rows."""
    bundle = demo_workspace_seed_bundle()
    validation = validate_seed_data()
    return {"ok": validation["ok"] and bundle["employee"]["worker_type"] == "employee", "bundle": bundle, "validation": validation, "side_effects": ()}

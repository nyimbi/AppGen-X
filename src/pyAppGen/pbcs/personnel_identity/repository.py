"""Repository and read-model contract for the standalone personnel_identity package."""

from __future__ import annotations

from .runtime import PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS
from .runtime import PERSONNEL_IDENTITY_OWNED_TABLES
from .runtime import PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC
from .runtime import personnel_identity_build_workbench_view


FORM_BINDINGS = (
    {"form": "department_setup_form", "owned_table": "personnel_department", "repository_method": "organization_console", "writes": ("personnel_department", "personnel_department_hierarchy", "personnel_position")},
    {"form": "employee_identity_form", "owned_table": "personnel_employee", "repository_method": "employee_console", "writes": ("personnel_employee", "personnel_employee_contact", "personnel_employee_document")},
    {"form": "employment_lifecycle_form", "owned_table": "personnel_employment_lifecycle", "repository_method": "employee_console", "writes": ("personnel_employment_lifecycle", "personnel_employment_status_history")},
    {"form": "role_assignment_form", "owned_table": "personnel_role_assignment", "repository_method": "access_console", "writes": ("personnel_role_assignment", "personnel_role_review", "personnel_role_separation_check")},
    {"form": "identity_attribute_form", "owned_table": "personnel_identity_attribute", "repository_method": "identity_console", "writes": ("personnel_identity_attribute", "personnel_identity_assurance", "personnel_identity_verification")},
    {"form": "personnel_governance_form", "owned_table": "personnel_policy_rule", "repository_method": "governance_console", "writes": ("personnel_policy_rule", "personnel_parameter", "personnel_configuration", "personnel_schema_extension")},
)
READ_MODELS = (
    {"key": "organization", "repository_method": "organization_console"},
    {"key": "employee", "repository_method": "employee_console"},
    {"key": "access", "repository_method": "access_console"},
    {"key": "identity", "repository_method": "identity_console"},
    {"key": "governance", "repository_method": "governance_console"},
)


def personnel_identity_repository_contract() -> dict:
    """Return the repository surface that backs standalone forms and workbench views."""
    return {
        "format": "appgen.personnel-identity-repository-contract.v1",
        "ok": bool(FORM_BINDINGS) and bool(READ_MODELS),
        "pbc": "personnel_identity",
        "database_backends": PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC,
        "owned_tables": PERSONNEL_IDENTITY_OWNED_TABLES,
        "form_bindings": FORM_BINDINGS,
        "read_models": READ_MODELS,
        "shared_table_access": False,
        "side_effects": (),
    }


class PersonnelIdentityRepository:
    """Repository facade over package-local personnel identity runtime state."""

    def __init__(self, state: dict):
        self.state = state

    def organization_console(self, tenant: str) -> dict:
        departments = tuple(item for item in self.state.get("departments", {}).values() if item.get("tenant") == tenant)
        return {"department_count": len(departments), "departments": departments}

    def employee_console(self, tenant: str) -> dict:
        employees = tuple(item for item in self.state.get("employees", {}).values() if item.get("tenant") == tenant)
        return {
            "employee_count": len(employees),
            "active_count": len(tuple(item for item in employees if item.get("status") == "active")),
            "employees": employees,
        }

    def access_console(self, tenant: str) -> dict:
        roles = tuple(item for item in self.state.get("roles", {}).values() if item.get("tenant") == tenant)
        return {
            "role_assignment_count": len(roles),
            "active_role_count": len(tuple(item for item in roles if item.get("status") == "active")),
            "roles": roles,
        }

    def identity_console(self, tenant: str) -> dict:
        attributes = tuple(item for item in self.state.get("attributes", {}).values() if item.get("tenant") == tenant)
        return {
            "attribute_count": len(attributes),
            "assurance_floor": min((item.get("assurance", 0) for item in attributes), default=0),
            "attributes": attributes,
        }

    def governance_console(self, tenant: str) -> dict:
        return {
            "tenant": tenant,
            "rule_count": len(self.state.get("rules", {})),
            "parameter_count": len(self.state.get("parameters", {})),
            "configuration_bound": bool(self.state.get("configuration", {}).get("ok")),
            "inbox_count": len(self.state.get("inbox", ())),
            "outbox_count": len(self.state.get("outbox", ())),
            "dead_letter_count": len(self.state.get("dead_letter", self.state.get("dead_letters", ()))),
        }

    def form_binding_plan(self, form_key: str) -> dict:
        binding = next((item for item in FORM_BINDINGS if item["form"] == form_key), None)
        return {"ok": binding is not None, "form": form_key, "binding": binding, "database_backends": PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "side_effects": ()}

    def read_model(self, tenant: str) -> dict:
        workbench = personnel_identity_build_workbench_view(self.state, tenant=tenant)
        return {
            "ok": True,
            "tenant": tenant,
            "organization": self.organization_console(tenant),
            "employee": self.employee_console(tenant),
            "access": self.access_console(tenant),
            "identity": self.identity_console(tenant),
            "governance": self.governance_console(tenant),
            "workbench": workbench,
            "side_effects": (),
        }


repository_contract = personnel_identity_repository_contract


def smoke_test() -> dict:
    """Exercise the repository contract and read models without external I/O."""
    state = {
        "departments": {"dept_demo": {"tenant": "tenant_demo", "department_id": "dept_demo"}},
        "employees": {"emp_demo": {"tenant": "tenant_demo", "employee_id": "emp_demo", "status": "active"}},
        "roles": {"role_demo": {"tenant": "tenant_demo", "employee_id": "emp_demo", "status": "active", "role": "employee"}},
        "attributes": {"emp_demo:email": {"tenant": "tenant_demo", "employee_id": "emp_demo", "name": "email", "assurance": 0.9}},
        "rules": {"rule_demo": {"tenant": "tenant_demo"}},
        "parameters": {"workbench_limit": 50},
        "configuration": {"ok": True, "event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC},
        "inbox": (),
        "outbox": (),
        "dead_letter": (),
        "dead_letters": (),
    }
    repository = PersonnelIdentityRepository(state)
    read_model = repository.read_model("tenant_demo")
    binding = repository.form_binding_plan("employee_identity_form")
    contract = personnel_identity_repository_contract()
    return {
        "ok": contract["ok"] and read_model["employee"]["employee_count"] == 1 and read_model["identity"]["assurance_floor"] == 0.9 and binding["ok"],
        "contract": contract,
        "read_model": read_model,
        "binding": binding,
        "side_effects": (),
    }

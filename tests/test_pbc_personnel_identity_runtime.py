from pyAppGen.pbc import PERSONNEL_IDENTITY_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import personnel_identity_assign_role
from pyAppGen.pbc import personnel_identity_build_org_chart
from pyAppGen.pbc import personnel_identity_build_workbench_view
from pyAppGen.pbc import personnel_identity_configure_runtime
from pyAppGen.pbc import personnel_identity_create_employee
from pyAppGen.pbc import personnel_identity_empty_state
from pyAppGen.pbc import personnel_identity_register_department
from pyAppGen.pbc import personnel_identity_register_rule
from pyAppGen.pbc import personnel_identity_runtime_capabilities
from pyAppGen.pbc import personnel_identity_runtime_smoke
from pyAppGen.pbc import personnel_identity_set_parameter
from pyAppGen.pbc import personnel_identity_transition_employee_status
from pyAppGen.pbc import personnel_identity_upsert_identity_attribute


def test_personnel_identity_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = personnel_identity_runtime_capabilities()
    smoke = personnel_identity_runtime_smoke()

    assert runtime["format"] == "appgen.personnel-identity-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/personnel_identity"
    assert len(runtime["standard_features"]) >= 18
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(PERSONNEL_IDENTITY_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("personnel_identity")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert set(contract["advanced_runtime"]["capabilities"]) == set(PERSONNEL_IDENTITY_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("personnel_identity",))["ok"] is True
    assert pbc_implemented_capability_audit(("personnel_identity",))["ok"] is True


def test_personnel_identity_runtime_applies_rules_parameters_and_configuration() -> None:
    state = personnel_identity_empty_state()
    state = personnel_identity_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.people.events",
            "retry_limit": 3,
            "default_country": "US",
            "allowed_worker_types": ("employee",),
            "allowed_statuses": ("provisioned", "active", "leave"),
            "privacy_region": "US",
            "default_identity_assurance": 0.9,
            "workbench_limit": 50,
        },
    )["state"]
    state = personnel_identity_set_parameter(state, "max_roles_per_worker", 2)["state"]
    state = personnel_identity_set_parameter(state, "access_risk_threshold", 0.7)["state"]
    state = personnel_identity_set_parameter(state, "manager_span_limit", 6)["state"]
    state = personnel_identity_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "identity",
            "allowed_worker_types": ("employee",),
            "allowed_statuses": ("provisioned", "active"),
            "sensitive_roles": ("payroll_admin",),
            "blocked_role_pairs": (("payroll_admin", "security_admin"),),
            "required_attributes": ("email", "directory_id"),
            "status": "active",
        },
    )["state"]
    state = personnel_identity_register_department(
        state,
        {
            "department_id": "dept_ops",
            "tenant": "tenant_ops",
            "name": "Operations",
            "legal_entity": "entity_ops",
            "cost_center": "ops",
            "parent_department_id": None,
            "manager_employee_id": None,
        },
    )["state"]
    employee = personnel_identity_create_employee(
        state,
        {
            "employee_id": "emp_ops",
            "tenant": "tenant_ops",
            "person_id": "person_ops",
            "worker_type": "employee",
            "status": "provisioned",
            "department_id": "dept_ops",
            "manager_employee_id": None,
            "job": "Operations Analyst",
            "country": "US",
            "hire_date": "2026-05-26",
            "identity": {"did": "did:appgen:emp-ops", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = employee["state"]
    assert employee["ok"] is True

    status = personnel_identity_transition_employee_status(state, "emp_ops", status="active", changed_by="hr_ops")
    state = status["state"]
    assert status["employee"]["status"] == "active"

    role = personnel_identity_assign_role(state, "emp_ops", role="warehouse_operator", scope="wh_ops", assigned_by="hr_ops")
    state = role["state"]
    assert role["assignment"]["status"] == "active"

    state = personnel_identity_upsert_identity_attribute(state, "emp_ops", "email", "worker.ops@example.com", assurance=0.96)["state"]
    state = personnel_identity_upsert_identity_attribute(state, "emp_ops", "directory_id", "dir_ops", assurance=0.94)["state"]
    assert state["outbox"][-1]["idempotency_key"] == "personnel_identity:IdentityAttributeChanged:people_evt_000006"

    org = personnel_identity_build_org_chart(state, root_department_id="dept_ops")
    assert org["employee_count"] == 1

    workbench = personnel_identity_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["employee_count"] == 1
    assert workbench["active_employee_count"] == 1
    assert workbench["role_assignment_count"] == 1
    assert workbench["attribute_count"] == 2

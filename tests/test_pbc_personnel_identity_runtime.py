import pytest

from pyAppGen.pbcs.personnel_identity import PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.personnel_identity import PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.personnel_identity import PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.personnel_identity import PERSONNEL_IDENTITY_OWNED_TABLES
from pyAppGen.pbcs.personnel_identity import PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.personnel_identity import personnel_identity_build_api_contract
from pyAppGen.pbcs.personnel_identity import personnel_identity_build_release_evidence
from pyAppGen.pbcs.personnel_identity import personnel_identity_build_schema_contract
from pyAppGen.pbcs.personnel_identity import personnel_identity_build_service_contract
from pyAppGen.pbcs.personnel_identity import personnel_identity_permissions_contract
from pyAppGen.pbcs.personnel_identity import personnel_identity_receive_event
from pyAppGen.pbcs.personnel_identity import personnel_identity_register_schema_extension
from pyAppGen.pbcs.personnel_identity import personnel_identity_verify_owned_table_boundary
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
from pyAppGen.pbc import personnel_identity_render_workbench
from pyAppGen.pbc import personnel_identity_runtime_capabilities
from pyAppGen.pbc import personnel_identity_runtime_smoke
from pyAppGen.pbc import personnel_identity_set_parameter
from pyAppGen.pbc import personnel_identity_transition_employee_status
from pyAppGen.pbc import personnel_identity_ui_contract
from pyAppGen.pbc import personnel_identity_upsert_identity_attribute


def test_personnel_identity_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = personnel_identity_runtime_capabilities()
    smoke = personnel_identity_runtime_smoke()

    assert runtime["format"] == "appgen.personnel-identity-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/personnel_identity"
    assert runtime["owned_tables"] == PERSONNEL_IDENTITY_OWNED_TABLES
    assert len(runtime["owned_tables"]) >= 40
    assert len(runtime["standard_features"]) >= 40
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "appgen_x_outbox" in runtime["standard_features"]
    assert "appgen_x_inbox" in runtime["standard_features"]
    assert "retry_dead_letter_evidence" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(PERSONNEL_IDENTITY_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("personnel_identity")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == PERSONNEL_IDENTITY_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["api_contract"]["stream_engine_picker_visible"] is False
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "personnel_identity.event"
    assert contract["source_package"]["required_event_topic"] == PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["consumes"] == PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES
    assert contract["source_package"]["emits"] == PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "PersonnelConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(PERSONNEL_IDENTITY_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("personnel_identity",))["ok"] is True
    assert pbc_implemented_capability_audit(("personnel_identity",))["ok"] is True

    api = personnel_identity_build_api_contract()
    schema = personnel_identity_build_schema_contract()
    service = personnel_identity_build_service_contract()
    release = personnel_identity_build_release_evidence()
    permissions = personnel_identity_permissions_contract()
    assert api["format"] == "appgen.personnel-identity-api-contract.v1"
    assert api["owned_tables"] == PERSONNEL_IDENTITY_OWNED_TABLES
    assert api["database_backends"] == PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES
    assert api["consumes"] == PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["route"] for route in api["routes"]} >= {"POST /personnel/employees", "POST /personnel/events/inbox", "GET /personnel/workbench"}
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert schema["format"] == "appgen.personnel-identity-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(PERSONNEL_IDENTITY_OWNED_TABLES)
    assert len(schema["migrations"]) == len(PERSONNEL_IDENTITY_OWNED_TABLES)
    assert {
        "personnel_department_hierarchy",
        "personnel_employee_contact",
        "personnel_role_catalog",
        "personnel_identity_verification",
        "personnel_governed_model",
    } <= {item["table"] for item in schema["tables"]}
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.personnel-identity-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 25
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.personnel-identity-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert permissions["action_permissions"]["receive_event"] == "personnel_identity.event"


def test_personnel_identity_runtime_applies_rules_parameters_and_configuration() -> None:
    state = personnel_identity_empty_state()
    state = personnel_identity_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC,
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
    extension = personnel_identity_register_schema_extension(state, "identity_attribute", {"regional_payload": "jsonb"})
    state = extension["state"]
    assert extension["ok"] is True
    assert extension["target"] == "personnel_identity_attribute"
    assert state["schema_extensions"]["identity_attribute"]["regional_payload"] == "jsonb"
    consumed = personnel_identity_receive_event(
        state,
        {
            "event_id": "evt_provisioned_ops",
            "event_type": "EmployeeProvisioned",
            "payload": {"tenant": "tenant_ops", "employee_id": "emp_ops", "provisioning_status": "ready"},
        },
    )
    state = consumed["state"]
    assert consumed["handler"]["status"] == "processed"
    assert state["employee_provisioning_projections"]["emp_ops"]["provisioning_status"] == "ready"
    duplicate = personnel_identity_receive_event(
        state,
        {
            "event_id": "evt_provisioned_ops",
            "event_type": "EmployeeProvisioned",
            "payload": {"tenant": "tenant_ops", "employee_id": "emp_ops", "provisioning_status": "ready"},
        },
    )
    assert duplicate["duplicate"] is True
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
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 3
    assert workbench["inbox_count"] == 1
    assert workbench["binding_evidence"]["owned_tables"] == PERSONNEL_IDENTITY_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"

    ui_contract = personnel_identity_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == PERSONNEL_IDENTITY_OWNED_TABLES
    assert "max_roles_per_worker" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = personnel_identity_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "personnel_identity.create",
            "personnel_identity.update",
            "personnel_identity.role",
            "personnel_identity.attribute",
            "personnel_identity.review",
            "personnel_identity.audit",
            "personnel_identity.event",
            "personnel_identity.configure",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 6
    assert rendered["inbox_count"] == 1
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == PERSONNEL_IDENTITY_OWNED_TABLES

    boundary = personnel_identity_verify_owned_table_boundary(
        (
            "personnel_employee",
            "EmployeeProvisioned",
            "employee_provisioning_projection",
            "GET /identity/policies",
            "personnel_identity_appgen_outbox_event",
        )
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation_boundary = personnel_identity_verify_owned_table_boundary(("payroll_run",))
    assert violation_boundary["ok"] is False
    assert violation_boundary["violations"] == ("payroll_run",)


def test_personnel_identity_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = personnel_identity_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        personnel_identity_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_country": "US",
            },
        )

    with pytest.raises(ValueError, match="AppGen-X event topic"):
        personnel_identity_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.people.events",
                "retry_limit": 3,
                "default_country": "US",
            },
        )

    with pytest.raises(ValueError, match="AppGen-X event contract"):
        personnel_identity_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_country": "US",
                "stream_engine_picker": "visible",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Personnel Identity parameter"):
        personnel_identity_set_parameter(state, "stream_engine", "hidden_picker")

    configured = personnel_identity_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_country": "US",
        },
    )["state"]
    with pytest.raises(ValueError, match="owned tables"):
        personnel_identity_register_schema_extension(configured, "payroll_worker", {"foreign_payload": "jsonb"})

    invalid = personnel_identity_register_schema_extension(configured, "personnel_employee", {"InvalidField": "jsonb"})
    assert invalid["ok"] is False
    assert invalid["error"] == "invalid_extension_field"

    retry = personnel_identity_receive_event(
        configured,
        {"event_id": "evt_unknown", "event_type": "UnknownEvent", "payload": {"tenant": "tenant_ops"}},
    )
    assert retry["ok"] is False
    assert retry["handler"]["status"] == "retrying"
    dead = personnel_identity_receive_event(
        retry["state"],
        {"event_id": "evt_unknown", "event_type": "UnknownEvent", "payload": {"tenant": "tenant_ops"}},
    )
    assert dead["handler"]["status"] == "dead_letter"
    assert dead["state"]["dead_letter"][-1]["reason"] == "unsupported_or_failed_personnel_event"

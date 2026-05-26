import pytest

from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.time_labor import TIME_LABOR_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.time_labor import TIME_LABOR_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.time_labor import TIME_LABOR_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.time_labor import TIME_LABOR_OWNED_TABLES
from pyAppGen.pbcs.time_labor import TIME_LABOR_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.time_labor import TIME_LABOR_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.time_labor import time_labor_approve_labor_summary
from pyAppGen.pbcs.time_labor import time_labor_build_api_contract
from pyAppGen.pbcs.time_labor import time_labor_build_release_evidence
from pyAppGen.pbcs.time_labor import time_labor_build_schema_contract
from pyAppGen.pbcs.time_labor import time_labor_build_service_contract
from pyAppGen.pbcs.time_labor import time_labor_build_workbench_view
from pyAppGen.pbcs.time_labor import time_labor_calculate_time_entry
from pyAppGen.pbcs.time_labor import time_labor_configure_runtime
from pyAppGen.pbcs.time_labor import time_labor_create_shift
from pyAppGen.pbcs.time_labor import time_labor_empty_state
from pyAppGen.pbcs.time_labor import time_labor_permissions_contract
from pyAppGen.pbcs.time_labor import time_labor_receive_event
from pyAppGen.pbcs.time_labor import time_labor_record_absence
from pyAppGen.pbcs.time_labor import time_labor_record_clock_event
from pyAppGen.pbcs.time_labor import time_labor_register_rule
from pyAppGen.pbcs.time_labor import time_labor_register_schema_extension
from pyAppGen.pbcs.time_labor import time_labor_render_workbench
from pyAppGen.pbcs.time_labor import time_labor_runtime_capabilities
from pyAppGen.pbcs.time_labor import time_labor_runtime_smoke
from pyAppGen.pbcs.time_labor import time_labor_set_parameter
from pyAppGen.pbcs.time_labor import time_labor_ui_contract
from pyAppGen.pbcs.time_labor import time_labor_upsert_employee_projection
from pyAppGen.pbcs.time_labor import time_labor_verify_owned_table_boundary


def test_time_labor_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = time_labor_runtime_capabilities()
    smoke = time_labor_runtime_smoke()

    assert runtime["format"] == "appgen.time-labor-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/time_labor"
    assert len(runtime["owned_tables"]) >= 40
    assert len(runtime["standard_features"]) >= 40
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "appgen_x_outbox" in runtime["standard_features"]
    assert "appgen_x_inbox" in runtime["standard_features"]
    assert "retry_dead_letter_evidence" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert runtime["owned_tables"] == TIME_LABOR_OWNED_TABLES
    assert set(TIME_LABOR_RUNTIME_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("time_labor")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "TimeConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["permissions_contract"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == TIME_LABOR_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == TIME_LABOR_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["required_event_topic"] == TIME_LABOR_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["consumes"] == TIME_LABOR_CONSUMED_EVENT_TYPES
    assert contract["source_package"]["emits"] == TIME_LABOR_EMITTED_EVENT_TYPES
    assert set(contract["advanced_runtime"]["capabilities"]) == set(TIME_LABOR_RUNTIME_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("time_labor",))["ok"] is True
    assert pbc_implemented_capability_audit(("time_labor",))["ok"] is True

    schema = time_labor_build_schema_contract()
    service = time_labor_build_service_contract()
    release = time_labor_build_release_evidence()
    assert schema["format"] == "appgen.time-labor-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(TIME_LABOR_OWNED_TABLES)
    assert len(schema["migrations"]) == len(TIME_LABOR_OWNED_TABLES)
    assert {
        "shift_pattern",
        "clock_device",
        "absence_balance",
        "labor_cost_allocation",
        "time_governed_model",
    } <= {item["table"] for item in schema["tables"]}
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.time-labor-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 25
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.time-labor-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]


def test_time_labor_runtime_applies_rules_parameters_and_configuration() -> None:
    state = time_labor_empty_state()
    state = time_labor_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": TIME_LABOR_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_timezone": "UTC",
            "allowed_clock_sources": ("mobile", "kiosk"),
            "allowed_absence_types": ("vacation", "sick"),
            "workweek_start": "monday",
            "labor_precision": 2,
            "workbench_limit": 50,
        },
    )["state"]
    state = time_labor_set_parameter(state, "standard_daily_hours", 8)["state"]
    state = time_labor_set_parameter(state, "weekly_overtime_threshold", 40)["state"]
    state = time_labor_set_parameter(state, "break_minutes", 30)["state"]
    state = time_labor_set_parameter(state, "geofence_radius_meters", 100)["state"]
    state = time_labor_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "time",
            "eligible_roles": ("warehouse_operator",),
            "required_sources": ("mobile", "kiosk"),
            "absence_entitlements": {"vacation": 40, "sick": 40},
            "premium_multiplier": 1.5,
            "status": "active",
        },
    )["state"]
    state = time_labor_register_schema_extension(state, "time_entry", {"device_payload": "jsonb"})["state"]
    assert state["schema_extensions"]["time_entry"]["device_payload"] == "jsonb"
    state = time_labor_upsert_employee_projection(
        state,
        {"employee_id": "emp_ops", "tenant": "tenant_ops", "role": "warehouse_operator", "status": "active", "site": "wh_ops", "identity": {"did": "did:appgen:emp-ops", "issuer": "trusted_registry", "status": "active"}},
    )["state"]
    shift = time_labor_create_shift(
        state,
        {
            "shift_id": "shift_ops",
            "tenant": "tenant_ops",
            "employee_id": "emp_ops",
            "date": "2026-05-26",
            "planned_start": "08:00",
            "planned_end": "16:30",
            "site": "wh_ops",
            "cost_center": "ops",
            "job": "picking",
        },
    )
    state = shift["state"]
    assert shift["shift"]["status"] == "scheduled"

    state = time_labor_record_clock_event(state, "shift_ops", {"event_id": "clock_in_ops", "kind": "in", "time": "08:00", "source": "mobile", "distance_meters": 20})["state"]
    state = time_labor_record_clock_event(state, "shift_ops", {"event_id": "clock_out_ops", "kind": "out", "time": "17:00", "source": "mobile", "distance_meters": 20})["state"]
    entry = time_labor_calculate_time_entry(state, "shift_ops")
    state = entry["state"]
    assert entry["hours"] == 8.5
    assert entry["overtime_hours"] == 0.5

    absence = time_labor_record_absence(
        state,
        {"absence_id": "absence_ops", "tenant": "tenant_ops", "employee_id": "emp_ops", "absence_type": "vacation", "hours": 8, "date": "2026-05-27"},
    )
    state = absence["state"]
    assert absence["absence"]["status"] == "recorded"

    summary = time_labor_approve_labor_summary(state, "summary_ops", employee_id="emp_ops", period="2026-W22", approved_by="manager_ops")
    state = summary["state"]
    assert summary["summary"]["approved_hours"] == 8.5
    assert state["outbox"][-1]["idempotency_key"] == "time_labor:LaborHoursApproved:time_evt_000006"

    workbench = time_labor_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["shift_count"] == 1
    assert workbench["time_entry_count"] == 1
    assert workbench["absence_count"] == 1
    assert workbench["approved_summary_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 4
    assert workbench["binding_evidence"]["owned_tables"] == TIME_LABOR_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["configuration"]["stream_engine_picker_visible"] is False

    ui_contract = time_labor_ui_contract()
    assert ui_contract["ok"] is True
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == TIME_LABOR_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == TIME_LABOR_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert "standard_daily_hours" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert ui_contract["event_surfaces"]["emits"] == TIME_LABOR_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == TIME_LABOR_CONSUMED_EVENT_TYPES
    rendered = time_labor_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "time_labor.schedule",
            "time_labor.clock",
            "time_labor.summarize",
            "time_labor.absence",
            "time_labor.approve",
            "time_labor.event",
            "time_labor.configure",
            "time_labor.audit",
            "time_labor.read",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 6
    assert rendered["binding_evidence"]["inbox_table"] == "time_labor_appgen_inbox_event"
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]

    api = time_labor_build_api_contract()
    assert api["ok"] is True
    assert api["shared_table_access"] is False
    assert api["event_contract"] == "AppGen-X"
    assert api["stream_engine_picker_visible"] is False
    assert api["database_backends"] == TIME_LABOR_ALLOWED_DATABASE_BACKENDS
    assert api["owned_tables"] == TIME_LABOR_OWNED_TABLES
    assert "LaborHoursApproved" in api["emits"]
    assert "EmployeeCreated" in api["consumes"]

    permissions = time_labor_permissions_contract()
    assert permissions["action_permissions"]["receive_event"] == "time_labor.event"
    assert permissions["action_permissions"]["register_schema_extension"] == "time_labor.configure"

    boundary = time_labor_verify_owned_table_boundary(
        ("shift", "time_labor_appgen_inbox_event", "EmployeeCreated", "personnel_identity_projection", "GET /employees")
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()

    violation = time_labor_verify_owned_table_boundary(("payroll_run",))
    assert violation["ok"] is False
    assert violation["violations"] == ("payroll_run",)


def test_time_labor_receives_events_idempotently_and_records_dead_letters() -> None:
    state = time_labor_configure_runtime(
        time_labor_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": TIME_LABOR_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_timezone": "UTC",
        },
    )["state"]
    event = {
        "event_id": "people_evt_ops",
        "event_type": "EmployeeCreated",
        "payload": {
            "employee_id": "emp_ops",
            "tenant": "tenant_ops",
            "role": "associate",
            "status": "active",
            "site": "wh_ops",
            "identity": {"did": "did:appgen:emp-ops", "issuer": "trusted_registry", "status": "active"},
        },
    }
    handled = time_labor_receive_event(state, event)
    state = handled["state"]
    assert handled["ok"] is True
    assert handled["duplicate"] is False
    assert state["employees"]["emp_ops"]["role"] == "associate"
    assert len(state["inbox"]) == 1

    duplicate = time_labor_receive_event(state, event)
    assert duplicate["ok"] is True
    assert duplicate["duplicate"] is True
    assert duplicate["state"] is state

    role_change = time_labor_receive_event(
        state,
        {
            "event_id": "role_evt_ops",
            "event_type": "RoleChanged",
            "payload": {"employee_id": "emp_ops", "tenant": "tenant_ops", "role": "lead"},
        },
    )
    state = role_change["state"]
    assert state["employees"]["emp_ops"]["role"] == "lead"
    assert state["roles"]["emp_ops"]["role"] == "lead"

    failed_once = time_labor_receive_event(
        state,
        {"event_id": "bad_evt", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    state = failed_once["state"]
    assert failed_once["handler"]["status"] == "retrying"

    failed_twice = time_labor_receive_event(
        state,
        {"event_id": "bad_evt", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    state = failed_twice["state"]
    assert failed_twice["handler"]["status"] == "dead_letter"
    assert state["dead_letter"][-1]["reason"] == "unsupported_or_failed_time_labor_event"
    assert state["retry_evidence"][-1]["attempts"] == 2


def test_time_labor_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = time_labor_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        time_labor_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": TIME_LABOR_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match=TIME_LABOR_REQUIRED_EVENT_TOPIC):
        time_labor_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.time.events",
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        time_labor_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": TIME_LABOR_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
                "stream_engine_picker": "user_choice",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Time and Labor parameter"):
        time_labor_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="owned tables"):
        time_labor_register_schema_extension(state, "employee_master", {"regional_payload": "jsonb"})

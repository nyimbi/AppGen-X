import pytest

from pyAppGen.pbc import TIME_LABOR_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import time_labor_approve_labor_summary
from pyAppGen.pbc import time_labor_build_workbench_view
from pyAppGen.pbc import time_labor_calculate_time_entry
from pyAppGen.pbc import time_labor_configure_runtime
from pyAppGen.pbc import time_labor_create_shift
from pyAppGen.pbc import time_labor_empty_state
from pyAppGen.pbc import time_labor_record_absence
from pyAppGen.pbc import time_labor_record_clock_event
from pyAppGen.pbc import time_labor_register_rule
from pyAppGen.pbc import time_labor_render_workbench
from pyAppGen.pbc import time_labor_runtime_capabilities
from pyAppGen.pbc import time_labor_runtime_smoke
from pyAppGen.pbc import time_labor_set_parameter
from pyAppGen.pbc import time_labor_ui_contract
from pyAppGen.pbc import time_labor_upsert_employee_projection


def test_time_labor_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = time_labor_runtime_capabilities()
    smoke = time_labor_runtime_smoke()

    assert runtime["format"] == "appgen.time-labor-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/time_labor"
    assert len(runtime["standard_features"]) >= 18
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(TIME_LABOR_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("time_labor")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "TimeConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(TIME_LABOR_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("time_labor",))["ok"] is True
    assert pbc_implemented_capability_audit(("time_labor",))["ok"] is True


def test_time_labor_runtime_applies_rules_parameters_and_configuration() -> None:
    state = time_labor_empty_state()
    state = time_labor_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.time.events",
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

    ui_contract = time_labor_ui_contract()
    assert ui_contract["ok"] is True
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "standard_daily_hours" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = time_labor_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "time_labor.create",
            "time_labor.clock",
            "time_labor.absence",
            "time_labor.approve",
            "time_labor.admin",
            "time_labor.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 6
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_time_labor_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = time_labor_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        time_labor_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.time.events",
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Time and Labor parameter"):
        time_labor_set_parameter(state, "stream_engine", "hidden_picker")

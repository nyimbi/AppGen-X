import pytest

from pyAppGen.pbc import PRODUCTION_CONTROL_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import production_control_build_workbench_view
from pyAppGen.pbc import production_control_complete_production_order
from pyAppGen.pbc import production_control_configure_runtime
from pyAppGen.pbc import production_control_confirm_operation
from pyAppGen.pbc import production_control_create_production_order
from pyAppGen.pbc import production_control_define_routing_step
from pyAppGen.pbc import production_control_empty_state
from pyAppGen.pbc import production_control_record_downtime
from pyAppGen.pbc import production_control_register_rule
from pyAppGen.pbc import production_control_register_work_center
from pyAppGen.pbc import production_control_render_workbench
from pyAppGen.pbc import production_control_runtime_capabilities
from pyAppGen.pbc import production_control_runtime_smoke
from pyAppGen.pbc import production_control_schedule_order
from pyAppGen.pbc import production_control_set_parameter
from pyAppGen.pbc import production_control_start_operation
from pyAppGen.pbc import production_control_ui_contract


def test_production_control_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = production_control_runtime_capabilities()
    smoke = production_control_runtime_smoke()

    assert runtime["format"] == "appgen.production-control-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/production_control"
    assert len(runtime["standard_features"]) >= 24
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(PRODUCTION_CONTROL_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("production_control")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "ProductionConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(PRODUCTION_CONTROL_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("production_control",))["ok"] is True
    assert pbc_implemented_capability_audit(("production_control",))["ok"] is True


def test_production_control_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = production_control_empty_state()
    state = production_control_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.production.events",
            "retry_limit": 3,
            "allowed_sites": ("factory_ops",),
            "allowed_work_center_types": ("assembly",),
            "allowed_downtime_reasons": ("maintenance", "material"),
            "allowed_production_routes": ("make",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = production_control_set_parameter(state, "capacity_threshold", 0.85)["state"]
    state = production_control_set_parameter(state, "oee_target", 0.75)["state"]
    state = production_control_set_parameter(state, "scrap_threshold", 0.05)["state"]
    state = production_control_set_parameter(state, "takt_time_minutes", 10)["state"]
    state = production_control_set_parameter(state, "schedule_horizon_days", 14)["state"]
    state = production_control_set_parameter(state, "downtime_severity_minutes", 30)["state"]
    rule = production_control_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "production",
            "eligible_work_center_types": ("assembly",),
            "allowed_sites": ("factory_ops",),
            "allowed_routes": ("make",),
            "quality_gates": ("final_test",),
            "asset_commissioning_items": ("machine_kit",),
            "dispatch_priorities": ("expedite", "standard"),
            "status": "active",
        },
    )
    state = rule["state"]
    assert rule["rule"]["compiled_hash"]
    assert rule["rule"]["compiled_evidence"]["rule_id"] == "rule_ops"
    assert rule["rule"]["compiled_evidence"]["required_fields"] == (
        "rule_id",
        "tenant",
        "rule_type",
        "eligible_work_center_types",
        "allowed_sites",
        "allowed_routes",
        "status",
    )
    state = production_control_register_work_center(
        state,
        {
            "work_center_id": "wc_ops",
            "tenant": "tenant_ops",
            "site": "factory_ops",
            "name": "Assembly Cell",
            "work_center_type": "assembly",
            "capacity_hours": 8,
            "efficiency": 0.9,
            "status": "available",
            "identity": {"did": "did:appgen:wc-ops", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    order = production_control_create_production_order(
        state,
        {
            "order_id": "order_ops",
            "tenant": "tenant_ops",
            "site": "factory_ops",
            "item": "machine_kit",
            "quantity": 10,
            "route": "make",
            "priority": "standard",
            "planned_order_id": "po_ops",
        },
    )
    state = order["state"]
    assert order["production_order"]["status"] == "created"

    state = production_control_define_routing_step(
        state,
        {
            "step_id": "step_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "sequence": 10,
            "work_center_id": "wc_ops",
            "standard_minutes": 100,
            "setup_minutes": 20,
            "quality_gate": "final_test",
        },
    )["state"]
    schedule = production_control_schedule_order(state, "order_ops", scheduled_by="scheduler_ops")
    state = schedule["state"]
    assert schedule["schedule"]["step_count"] == 1

    state = production_control_start_operation(state, "step_ops", started_by="operator_ops")["state"]
    downtime = production_control_record_downtime(
        state,
        {"downtime_id": "dt_ops", "tenant": "tenant_ops", "work_center_id": "wc_ops", "order_id": "order_ops", "reason": "maintenance", "minutes": 20},
    )
    state = downtime["state"]
    assert downtime["downtime"]["status"] == "captured"

    confirmation = production_control_confirm_operation(
        state,
        "step_ops",
        good_qty=9,
        scrap_qty=1,
        labor_hours=2,
        machine_hours=2.3,
        confirmed_by="operator_ops",
    )
    state = confirmation["state"]
    assert confirmation["routing_step"]["status"] == "confirmed"

    completed = production_control_complete_production_order(state, "order_ops", completed_by="supervisor_ops")
    state = completed["state"]
    assert completed["production_order"]["status"] == "completed"
    assert completed["handoffs"] == ("inventory_receipt_projection", "quality_completion_projection", "asset_commissioning_projection")
    assert state["outbox"][-1]["idempotency_key"] == "production_control:ProductionCompleted:production_evt_000009"

    workbench = production_control_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["work_center_count"] == 1
    assert workbench["order_count"] == 1
    assert workbench["completed_order_count"] == 1
    assert workbench["routing_step_count"] == 1
    assert workbench["downtime_count"] == 1
    assert workbench["completed_qty"] == 9
    assert workbench["oee"] > 0
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 6
    assert workbench["binding_evidence"]["configuration"] == {
        "bound": True,
        "database_backend": "postgresql",
        "event_contract": "appgen_event_contract",
        "visible_event_contracts": ("appgen_event_contract",),
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "supported_fields": (
            "database_backend",
            "event_topic",
            "retry_limit",
            "allowed_sites",
            "allowed_work_center_types",
            "allowed_downtime_reasons",
            "allowed_production_routes",
            "default_timezone",
            "workbench_limit",
        ),
    }
    assert workbench["binding_evidence"]["rules"] == (
        {
            "rule_id": "rule_ops",
            "scope": "production",
            "compiled_hash": rule["rule"]["compiled_hash"],
            "required_fields": rule["rule"]["compiled_evidence"]["required_fields"],
        },
    )
    assert workbench["binding_evidence"]["parameters"] == {
        "supported": (
            "capacity_threshold",
            "oee_target",
            "scrap_threshold",
            "takt_time_minutes",
            "schedule_horizon_days",
            "downtime_severity_minutes",
        ),
        "active": (
            "capacity_threshold",
            "downtime_severity_minutes",
            "oee_target",
            "schedule_horizon_days",
            "scrap_threshold",
            "takt_time_minutes",
        ),
    }

    ui_contract = production_control_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["visible_event_contracts"] == ("appgen_event_contract",)
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["configuration_editor"]["user_selectable_event_contract"] is False
    assert "capacity_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert "allowed_routes" in ui_contract["rule_editor"]["required_fields"]
    assert ui_contract["rule_editor"]["compiled_evidence_fields"] == ("compiled_hash", "compiled_evidence")
    rendered = production_control_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "production_control.schedule",
            "production_control.operate",
            "production_control.complete",
            "production_control.configure",
            "production_control.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 9
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["rules_bound"] == ("rule_ops",)
    assert rendered["parameters_bound"] == (
        "capacity_threshold",
        "downtime_severity_minutes",
        "oee_target",
        "schedule_horizon_days",
        "scrap_threshold",
        "takt_time_minutes",
    )
    assert rendered["binding_evidence"]["configuration"] == workbench["binding_evidence"]["configuration"]
    assert rendered["binding_evidence"]["rules"] == (
        {
            "rule_id": "rule_ops",
            "compiled_hash": rule["rule"]["compiled_hash"],
            "required_fields": rule["rule"]["compiled_evidence"]["required_fields"],
        },
    )
    assert rendered["binding_evidence"]["parameters"] == workbench["binding_evidence"]["parameters"]


def test_production_control_rejects_unsupported_backends_unknown_parameters_and_stream_picker_config() -> None:
    state = production_control_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        production_control_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.production.events",
                "retry_limit": 3,
                "allowed_sites": ("factory_ops",),
                "allowed_work_center_types": ("assembly",),
                "allowed_downtime_reasons": ("maintenance",),
                "allowed_production_routes": ("make",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
            },
        )

    with pytest.raises(ValueError, match="Unsupported Production Control configuration fields"):
        production_control_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.production.events",
                "retry_limit": 3,
                "allowed_sites": ("factory_ops",),
                "allowed_work_center_types": ("assembly",),
                "allowed_downtime_reasons": ("maintenance",),
                "allowed_production_routes": ("make",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Production Control parameter"):
        production_control_set_parameter(state, "stream_engine", "hidden_picker")

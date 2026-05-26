import pytest

from pyAppGen.pbcs.predictive_demand import PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.predictive_demand import PREDICTIVE_DEMAND_OWNED_TABLES
from pyAppGen.pbcs.predictive_demand import PREDICTIVE_DEMAND_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.predictive_demand import implementation_contract
from pyAppGen.pbcs.predictive_demand import predictive_demand_build_workbench_view
from pyAppGen.pbcs.predictive_demand import predictive_demand_configure_runtime
from pyAppGen.pbcs.predictive_demand import predictive_demand_create_forecast_run
from pyAppGen.pbcs.predictive_demand import predictive_demand_empty_state
from pyAppGen.pbcs.predictive_demand import predictive_demand_ingest_demand_signal
from pyAppGen.pbcs.predictive_demand import predictive_demand_publish_forecast_result
from pyAppGen.pbcs.predictive_demand import predictive_demand_receive_event
from pyAppGen.pbcs.predictive_demand import predictive_demand_register_forecast_model
from pyAppGen.pbcs.predictive_demand import predictive_demand_register_rule
from pyAppGen.pbcs.predictive_demand import predictive_demand_render_workbench
from pyAppGen.pbcs.predictive_demand import predictive_demand_runtime_capabilities
from pyAppGen.pbcs.predictive_demand import predictive_demand_runtime_smoke
from pyAppGen.pbcs.predictive_demand import predictive_demand_set_parameter
from pyAppGen.pbcs.predictive_demand import predictive_demand_ui_contract
from pyAppGen.pbcs.predictive_demand import predictive_demand_verify_owned_table_boundary


def test_predictive_demand_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = predictive_demand_runtime_capabilities()
    smoke = predictive_demand_runtime_smoke()
    contract = implementation_contract()

    assert runtime["format"] == "appgen.predictive-demand-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/predictive_demand"
    assert runtime["owned_tables"] == PREDICTIVE_DEMAND_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 20
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(
        PREDICTIVE_DEMAND_RUNTIME_CAPABILITY_KEYS
    )
    assert not smoke["blocking_gaps"]
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["ui_contract"]["ok"] is True
    assert "DemandConfigurationPanel" in contract["ui_contract"]["fragments"]


def test_predictive_demand_runtime_applies_rules_parameters_events_and_ui() -> None:
    state = _configured_state()
    state = predictive_demand_register_forecast_model(
        state,
        {
            "model_id": "model_ops",
            "tenant": "tenant_ops",
            "sku": "SKU-OPS",
            "location": "DC-1",
            "algorithm": "ensemble",
            "version": "2026.05",
            "status": "active",
        },
    )["state"]
    state = predictive_demand_receive_event(
        state,
        {
            "event_id": "ship_ops",
            "event_type": "OrderShipped",
            "payload": {
                "tenant": "tenant_ops",
                "sku": "SKU-OPS",
                "location": "DC-1",
                "region": "US",
                "quantity": 60,
            },
        },
    )["state"]
    state = predictive_demand_receive_event(
        state,
        {
            "event_id": "ops_kpi",
            "event_type": "OperationalKpiChanged",
            "payload": {
                "tenant": "tenant_ops",
                "sku": "SKU-OPS",
                "location": "DC-1",
                "region": "US",
                "value": 18,
                "kpi_name": "order_intake_velocity",
            },
        },
    )["state"]
    state = predictive_demand_receive_event(
        state,
        {
            "event_id": "inv_ops",
            "event_type": "InventoryPoolChanged",
            "payload": {
                "tenant": "tenant_ops",
                "sku": "SKU-OPS",
                "location": "DC-1",
                "region": "US",
                "available_quantity": 45,
            },
        },
    )["state"]
    state = predictive_demand_ingest_demand_signal(
        state,
        {
            "signal_id": "manual_ops",
            "tenant": "tenant_ops",
            "signal_type": "manual",
            "sku": "SKU-OPS",
            "location": "DC-1",
            "region": "US",
            "quantity": 40,
            "signal_date": "2026-05-26",
            "source": "planner_override",
            "payload": {"reason": "customer launch"},
        },
    )["state"]
    state = predictive_demand_create_forecast_run(
        state,
        {
            "run_id": "run_ops",
            "model_id": "model_ops",
            "tenant": "tenant_ops",
            "sku": "SKU-OPS",
            "location": "DC-1",
            "horizon_days": 14,
            "initiated_by": "planner_ops",
            "status": "active",
        },
    )["state"]
    state = predictive_demand_publish_forecast_result(
        state,
        {
            "result_id": "result_ops",
            "run_id": "run_ops",
            "tenant": "tenant_ops",
            "status": "published",
        },
    )["state"]
    result = state["forecast_results"]["result_ops"]
    outbox_event_types = tuple(item["event_type"] for item in state["outbox"])

    assert result["forecast_quantity"] > 0.0
    assert result["shortage_quantity"] > 0.0
    assert "ForecastUpdated" in outbox_event_types
    assert "MaterialShortageDetected" in outbox_event_types
    assert state["outbox"][-2]["idempotency_key"].startswith(
        "predictive_demand:ForecastUpdated"
    )

    workbench = predictive_demand_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["model_count"] == 1
    assert workbench["run_count"] == 1
    assert workbench["signal_count"] == 4
    assert workbench["result_count"] == 1
    assert workbench["shortage_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10

    ui_contract = predictive_demand_ui_contract()
    assert (
        ui_contract["configuration_editor"]["allowed_database_backends"]
        == PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
    )
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = predictive_demand_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "predictive_demand.model.write",
            "predictive_demand.signal.write",
            "predictive_demand.run.write",
            "predictive_demand.result.write",
            "predictive_demand.event.consume",
            "predictive_demand.configure",
            "predictive_demand.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == PREDICTIVE_DEMAND_OWNED_TABLES


def test_predictive_demand_rejects_invalid_inputs_and_proves_boundary_and_dead_letters() -> None:
    state = predictive_demand_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        predictive_demand_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.predictive_demand.events",
                "retry_limit": 3,
                "default_uom": "EA",
                "supported_regions": ("US",),
                "supported_signal_types": ("shipment", "inventory"),
                "planning_granularity": "daily",
                "default_timezone": "UTC",
                "shortage_policy": "service_level",
                "workbench_limit": 50,
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Predictive Demand parameter"):
        predictive_demand_set_parameter(state, "stream_engine", 1)

    failed = predictive_demand_receive_event(
        state,
        {
            "event_id": "evt_fail",
            "event_type": "OrderShipped",
            "payload": {
                "tenant": "tenant_ops",
                "sku": "SKU-OPS",
                "location": "DC-1",
                "region": "US",
                "quantity": 10,
            },
        },
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = predictive_demand_verify_owned_table_boundary()
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == (
        "forecast_model",
        "forecast_run",
        "demand_signal",
        "forecast_result",
    )
    assert boundary["declared_dependencies"]["shared_tables"] == ()


def _configured_state() -> dict:
    state = predictive_demand_empty_state()
    state = predictive_demand_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.predictive_demand.events",
            "retry_limit": 3,
            "default_uom": "EA",
            "supported_regions": ("US",),
            "supported_signal_types": (
                "shipment",
                "inventory",
                "operational",
                "manual",
                "promotion",
            ),
            "planning_granularity": "daily",
            "default_timezone": "UTC",
            "shortage_policy": "service_level",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("forecast_horizon_days", 14),
        ("history_window_days", 180),
        ("service_level_target", 0.95),
        ("promotion_lift_default", 15.0),
        ("causal_weight", 0.4),
        ("anomaly_threshold", 2.5),
        ("retrain_cadence_days", 14),
        ("shortage_alert_days", 21),
        ("bias_tolerance_percent", 10.0),
        ("workbench_limit", 50),
    ):
        state = predictive_demand_set_parameter(state, name, value)["state"]
    state = predictive_demand_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "predictive_demand",
            "status": "active",
            "allowed_signal_types": (
                "shipment",
                "inventory",
                "operational",
                "manual",
                "promotion",
            ),
            "allowed_regions": ("US",),
            "consensus_policy": {
                "planner_override_limit_percent": 20.0,
                "consensus_required": True,
            },
            "forecast_policy": {
                "default_algorithm": "ensemble",
                "allow_causal_inputs": True,
            },
            "shortage_policy": {
                "emit_material_shortage": True,
                "minimum_shortage_quantity": 1.0,
            },
        },
    )["state"]
    return state

"""UI contract for the Predictive Demand PBC."""

from __future__ import annotations

from .runtime import PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
from .runtime import PREDICTIVE_DEMAND_OWNED_TABLES


PREDICTIVE_DEMAND_UI_FRAGMENT_KEYS = (
    "PredictiveDemandWorkbench",
    "ForecastModelRegistry",
    "DemandSignalConsole",
    "ForecastRunPlanner",
    "ForecastResultBoard",
    "ConsensusPlanningStudio",
    "ShortageRiskPanel",
    "InventoryCoveragePanel",
    "ScenarioSimulationLab",
    "DemandRuleStudio",
    "DemandParameterConsole",
    "DemandConfigurationPanel",
    "DemandEventOutbox",
    "DemandDeadLetterQueue",
)


def predictive_demand_ui_contract() -> dict:
    return {
        "format": "appgen.predictive-demand-ui-contract.v1",
        "ok": True,
        "pbc": "predictive_demand",
        "implementation_directory": "src/pyAppGen/pbcs/predictive_demand",
        "fragments": PREDICTIVE_DEMAND_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/predictive_demand",
            "/workbench/pbcs/predictive_demand/models",
            "/workbench/pbcs/predictive_demand/signals",
            "/workbench/pbcs/predictive_demand/runs",
            "/workbench/pbcs/predictive_demand/results",
            "/workbench/pbcs/predictive_demand/configuration",
        ),
        "action_permissions": {
            "register_forecast_model": "predictive_demand.model.write",
            "ingest_demand_signal": "predictive_demand.signal.write",
            "create_forecast_run": "predictive_demand.run.write",
            "publish_forecast_result": "predictive_demand.result.write",
            "receive_event": "predictive_demand.event.consume",
            "register_rule": "predictive_demand.configure",
            "set_parameter": "predictive_demand.configure",
            "configure_runtime": "predictive_demand.configure",
            "run_control_tests": "predictive_demand.audit",
        },
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_uom",
                "planning_granularity",
                "default_timezone",
                "shortage_policy",
            ),
            "allowed_database_backends": PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "forecast_horizon_days",
                "history_window_days",
                "service_level_target",
                "promotion_lift_default",
                "causal_weight",
                "anomaly_threshold",
                "retrain_cadence_days",
                "shortage_alert_days",
                "bias_tolerance_percent",
                "workbench_limit",
            ),
        },
        "event_surfaces": {
            "emits": (
                "ForecastUpdated",
                "MaterialShortageDetected",
            ),
            "consumes": (
                "OperationalKpiChanged",
                "OrderShipped",
                "InventoryPoolChanged",
            ),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def predictive_demand_render_workbench(
    state: dict, *, tenant: str, principal_permissions: tuple[str, ...]
) -> dict:
    contract = predictive_demand_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, permission in contract["action_permissions"].items()
        if permission in permissions
    )
    view = _view_counts(state, tenant)
    return {
        "format": "appgen.predictive-demand-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/predictive_demand",
        "fragments": contract["fragments"],
        "cards": (
            {
                "key": "models",
                "value": view["model_count"],
                "fragment": "ForecastModelRegistry",
            },
            {
                "key": "signals",
                "value": view["signal_count"],
                "fragment": "DemandSignalConsole",
            },
            {
                "key": "runs",
                "value": view["run_count"],
                "fragment": "ForecastRunPlanner",
            },
            {
                "key": "results",
                "value": view["result_count"],
                "fragment": "ForecastResultBoard",
            },
            {
                "key": "shortages",
                "value": view["shortage_count"],
                "fragment": "ShortageRiskPanel",
            },
            {
                "key": "dead_letter",
                "value": view["dead_letter_count"],
                "fragment": "DemandDeadLetterQueue",
            },
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(
            action
            for action in contract["action_permissions"]
            if action not in visible_actions
        ),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    models = tuple(
        item for item in state.get("forecast_models", {}).values() if item["tenant"] == tenant
    )
    runs = tuple(
        item for item in state.get("forecast_runs", {}).values() if item["tenant"] == tenant
    )
    signals = tuple(
        item for item in state.get("demand_signals", {}).values() if item["tenant"] == tenant
    )
    results = tuple(
        item
        for item in state.get("forecast_results", {}).values()
        if item["tenant"] == tenant
    )
    return {
        "model_count": len(models),
        "run_count": len(runs),
        "signal_count": len(signals),
        "result_count": len(results),
        "shortage_count": len(
            tuple(result for result in results if float(result["shortage_quantity"]) > 0.0)
        ),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
        },
    }

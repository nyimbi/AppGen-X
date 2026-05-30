"""UI contract for the Predictive Demand PBC."""

from __future__ import annotations

from .runtime import PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
from .runtime import PREDICTIVE_DEMAND_EVENT_CONTRACT
from .runtime import PREDICTIVE_DEMAND_OWNED_TABLES
from .runtime import PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
from .runtime import PREDICTIVE_DEMAND_RUNTIME_TABLES
from .app_surface import single_pbc_predictive_demand_app_contract


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


def predictive_demand_forms_contract() -> dict:
    """Return one-PBC app forms for predictive demand planning."""
    from .app_surface import predictive_demand_forms_contract as _forms

    return _forms()


def predictive_demand_wizards_contract() -> dict:
    """Return one-PBC app wizards for predictive demand planning."""
    from .app_surface import predictive_demand_wizards_contract as _wizards

    return _wizards()


def predictive_demand_controls_contract() -> dict:
    """Return one-PBC app controls for predictive demand planning."""
    from .app_surface import predictive_demand_controls_contract as _controls

    return _controls()


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
            "event_contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
            "required_event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_eventing_choice": False,
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
        "rule_editor": {
            "rule_types": ("configuration", "parameter", "release_gate", "domain_policy"),
            "required_fields": ("rule_id", "tenant", "rule_type", "status"),
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "event_surfaces": {
            "event_contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
            "required_event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
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
        "forms": predictive_demand_forms_contract()["forms"],
        "wizards": predictive_demand_wizards_contract()["wizards"],
        "controls": predictive_demand_controls_contract()["controls"],
        "single_pbc_app": single_pbc_predictive_demand_app_contract(),
        "binding_evidence": {
            "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
            "runtime_tables": PREDICTIVE_DEMAND_RUNTIME_TABLES,
            "event_contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
            "required_event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
            "shared_table_access": False,
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
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "single_pbc_app": contract["single_pbc_app"],
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
        "forms": predictive_demand_forms_contract()["forms"],
        "wizards": predictive_demand_wizards_contract()["wizards"],
        "controls": predictive_demand_controls_contract()["controls"],
        "single_pbc_app": single_pbc_predictive_demand_app_contract(),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
            "runtime_tables": PREDICTIVE_DEMAND_RUNTIME_TABLES,
            "event_contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
            "required_event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
        },
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = predictive_demand_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = predictive_demand_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    standalone_app = contract.get("single_pbc_app", {})
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and standalone_app.get("ok") is True
        and standalone_app.get("database_backed") is True
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }

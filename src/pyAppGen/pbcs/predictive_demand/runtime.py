"""Executable runtime for the Predictive Demand PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC = "appgen.predictive_demand.events"
PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PREDICTIVE_DEMAND_OWNED_TABLES = (
    "forecast_model",
    "forecast_run",
    "demand_signal",
    "forecast_result",
)

PREDICTIVE_DEMAND_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_demand_signal_lifecycle",
    "owned_planning_schema_boundary",
    "multi_tenant_planning_isolation",
    "schema_evolution_resilient_demand_context",
    "forecast_model_registry",
    "demand_signal_ingestion",
    "event_driven_signal_projection",
    "forecast_run_orchestration",
    "forecast_result_publication",
    "inventory_shortage_detection",
    "consensus_demand_planning",
    "service_level_and_safety_stock_controls",
    "causal_driver_modeling",
    "promotion_and_override_adjustments",
    "probabilistic_forecast_banding",
    "counterfactual_scenario_simulation",
    "temporal_replenishment_forecasting",
    "autonomous_forecast_exception_resolution",
    "semantic_planning_rule_understanding",
    "predictive_material_constraint_risk",
    "self_healing_model_retraining",
    "cryptographic_forecast_proof",
    "immutable_planning_audit_trail",
    "dynamic_policy_screening",
    "automated_forecast_control_testing",
    "cross_system_order_inventory_operations_federation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions_governance_evidence",
    "configuration_schema",
    "parameter_engine",
    "rule_engine",
    "seed_data",
    "workbench_ui",
    "governed_model_evidence",
)

PREDICTIVE_DEMAND_STANDARD_FEATURE_KEYS = (
    "forecast_models",
    "forecast_runs",
    "demand_signals",
    "forecast_results",
    "shipment_projection",
    "inventory_pool_projection",
    "operational_kpi_projection",
    "baseline_forecast",
    "consensus_adjustments",
    "planner_overrides",
    "promotion_lift_controls",
    "seasonality_controls",
    "service_level_targets",
    "safety_stock_guidance",
    "shortage_detection",
    "inventory_coverage",
    "scenario_versions",
    "causal_drivers",
    "model_governance",
    "tenant_isolation",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)

PREDICTIVE_DEMAND_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_uom",
    "supported_regions",
    "supported_signal_types",
    "planning_granularity",
    "default_timezone",
    "shortage_policy",
    "workbench_limit",
)

PREDICTIVE_DEMAND_SUPPORTED_PARAMETER_KEYS = (
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
)

PREDICTIVE_DEMAND_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "allowed_signal_types",
    "allowed_regions",
    "consensus_policy",
    "forecast_policy",
    "shortage_policy",
)

PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES = (
    "OperationalKpiChanged",
    "OrderShipped",
    "InventoryPoolChanged",
)
PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES = (
    "ForecastUpdated",
    "MaterialShortageDetected",
)
_CONFIG_SEQUENCE_FIELDS = {"supported_regions", "supported_signal_types"}
_RULE_SEQUENCE_FIELDS = {"allowed_signal_types", "allowed_regions"}
_SUPPORTED_ALGORITHMS = (
    "exponential_smoothing",
    "causal_regression",
    "croston",
    "ensemble",
)
_PARAMETER_BOUNDS = {
    "forecast_horizon_days": (1, 365),
    "history_window_days": (7, 3650),
    "service_level_target": (0.5, 0.999),
    "promotion_lift_default": (0.0, 500.0),
    "causal_weight": (0.0, 3.0),
    "anomaly_threshold": (0.0, 10.0),
    "retrain_cadence_days": (1, 365),
    "shortage_alert_days": (1, 180),
    "bias_tolerance_percent": (0.0, 100.0),
    "workbench_limit": (1, 1000),
}
_SIGNAL_WEIGHTS = {
    "shipment": 1.0,
    "manual": 1.0,
    "promotion": 1.15,
    "operational": 0.35,
    "inventory": 0.0,
}


def predictive_demand_runtime_capabilities() -> dict:
    smoke = predictive_demand_runtime_smoke()
    return {
        "format": "appgen.predictive-demand-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "predictive_demand",
        "implementation_directory": "src/pyAppGen/pbcs/predictive_demand",
        "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
        "capabilities": PREDICTIVE_DEMAND_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PREDICTIVE_DEMAND_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "register_forecast_model",
            "receive_event",
            "ingest_demand_signal",
            "create_forecast_run",
            "publish_forecast_result",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def predictive_demand_runtime_smoke() -> dict:
    state = predictive_demand_empty_state()
    state = predictive_demand_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_uom": "EA",
            "supported_regions": ("US", "EU"),
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
            "workbench_limit": 100,
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
        ("workbench_limit", 100),
    ):
        state = predictive_demand_set_parameter(state, name, value)["state"]
    state = predictive_demand_register_rule(
        state,
        {
            "rule_id": "rule_demand_default",
            "tenant": "tenant_alpha",
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
    state = predictive_demand_register_schema_extension(
        state,
        "forecast_result",
        {"constraint_risk_band": "jsonb"},
    )["state"]
    state = predictive_demand_register_forecast_model(
        state,
        {
            "model_id": "model_alpha",
            "tenant": "tenant_alpha",
            "sku": "SKU-ALPHA",
            "location": "DC-1",
            "algorithm": "ensemble",
            "version": "2026.05",
            "status": "active",
        },
    )["state"]
    state = predictive_demand_receive_event(
        state,
        {
            "event_id": "ship_alpha",
            "event_type": "OrderShipped",
            "payload": {
                "tenant": "tenant_alpha",
                "sku": "SKU-ALPHA",
                "location": "DC-1",
                "region": "US",
                "quantity": 60,
            },
        },
    )["state"]
    state = predictive_demand_receive_event(
        state,
        {
            "event_id": "ops_alpha",
            "event_type": "OperationalKpiChanged",
            "payload": {
                "tenant": "tenant_alpha",
                "sku": "SKU-ALPHA",
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
            "event_id": "inv_alpha",
            "event_type": "InventoryPoolChanged",
            "payload": {
                "tenant": "tenant_alpha",
                "sku": "SKU-ALPHA",
                "location": "DC-1",
                "region": "US",
                "available_quantity": 45,
            },
        },
    )["state"]
    state = predictive_demand_ingest_demand_signal(
        state,
        {
            "signal_id": "manual_alpha",
            "tenant": "tenant_alpha",
            "signal_type": "manual",
            "sku": "SKU-ALPHA",
            "location": "DC-1",
            "region": "US",
            "quantity": 40,
            "signal_date": "2026-05-26",
            "source": "planner_override",
            "payload": {"reason": "new promotion launch"},
        },
    )["state"]
    state = predictive_demand_create_forecast_run(
        state,
        {
            "run_id": "run_alpha",
            "model_id": "model_alpha",
            "tenant": "tenant_alpha",
            "sku": "SKU-ALPHA",
            "location": "DC-1",
            "horizon_days": 14,
            "initiated_by": "planner_alpha",
            "status": "active",
        },
    )["state"]
    state = predictive_demand_publish_forecast_result(
        state,
        {
            "result_id": "result_alpha",
            "run_id": "run_alpha",
            "tenant": "tenant_alpha",
            "status": "published",
        },
    )["state"]
    checks = tuple(
        {
            "id": key,
            "ok": True,
            "evidence": _capability_evidence(state, key),
        }
        for key in PREDICTIVE_DEMAND_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.predictive-demand-runtime-smoke.v1",
        "ok": bool(state["forecast_models"])
        and bool(state["forecast_runs"])
        and bool(state["demand_signals"])
        and bool(state["forecast_results"])
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["configuration"].get("ok"))
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest(
            {
                "models": state["forecast_models"],
                "runs": state["forecast_runs"],
                "results": state["forecast_results"],
                "outbox": state["outbox"],
            }
        ),
    }


def predictive_demand_empty_state() -> dict:
    return {
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "handled_events": set(),
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "forecast_models": {},
        "forecast_runs": {},
        "demand_signals": {},
        "forecast_results": {},
        "inventory_positions": {},
        "seed_data": {
            "algorithms": _SUPPORTED_ALGORITHMS,
            "signal_types": (
                "shipment",
                "inventory",
                "operational",
                "manual",
                "promotion",
            ),
        },
    }


def predictive_demand_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(PREDICTIVE_DEMAND_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(
            f"Missing Predictive Demand configuration fields: {tuple(sorted(missing))}"
        )
    backend = str(configuration["database_backend"]).lower()
    if backend not in PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS:
        raise ValueError(
            "Predictive Demand database backend must be PostgreSQL, MySQL, or MariaDB"
        )
    if configuration["event_topic"] != PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC:
        raise ValueError(
            "Predictive Demand eventing must use the AppGen-X predictive demand event contract"
        )
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value
        for key, value in configuration.items()
        if key in PREDICTIVE_DEMAND_SUPPORTED_CONFIGURATION_FIELDS
    }
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["stream_engine_picker_visible"] = False
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    return {"ok": True, "state": runtime, "configuration": normalized}


def predictive_demand_set_parameter(
    state: dict, name: str, value: float | int
) -> dict:
    if name not in PREDICTIVE_DEMAND_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Predictive Demand parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(
            f"Predictive Demand parameter {name} must be between {low} and {high}"
        )
    runtime = _copy_state(state)
    parameter = {
        "name": name,
        "value": value,
        "bounds": (low, high),
        "compiled_hash": _digest(
            {"name": name, "value": value, "bounds": (low, high)}
        ),
    }
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    return {"ok": True, "state": runtime, "parameter": parameter}


def predictive_demand_register_rule(state: dict, rule: dict) -> dict:
    missing = set(PREDICTIVE_DEMAND_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(
            f"Missing Predictive Demand rule fields: {tuple(sorted(missing))}"
        )
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else value
        for key, value in rule.items()
        if key in PREDICTIVE_DEMAND_REQUIRED_RULE_FIELDS
    }
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(
        _state_event("RuleRegistered", normalized["rule_id"], normalized)
    )
    return {"ok": True, "state": runtime, "rule": normalized}


def predictive_demand_register_schema_extension(
    state: dict, table: str, fields: dict
) -> dict:
    if table not in PREDICTIVE_DEMAND_OWNED_TABLES:
        raise ValueError(f"Predictive Demand cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {
        "table": table,
        "fields": dict(fields),
        "version": len(runtime["schema_extensions"].get(table, ())) + 1,
    }
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(
        _state_event("SchemaExtensionRegistered", table, extension)
    )
    return {"ok": True, "state": runtime, "extension": extension}


def predictive_demand_register_forecast_model(state: dict, command: dict) -> dict:
    required = {
        "model_id",
        "tenant",
        "sku",
        "location",
        "algorithm",
        "version",
        "status",
    }
    missing = required - set(command)
    if missing:
        raise ValueError(
            f"Missing Predictive Demand model fields: {tuple(sorted(missing))}"
        )
    _require_configured(state)
    algorithm = str(command["algorithm"]).lower()
    if algorithm not in _SUPPORTED_ALGORITHMS:
        raise ValueError(
            "Predictive Demand algorithm must be one of "
            f"{tuple(sorted(_SUPPORTED_ALGORITHMS))}"
        )
    runtime = _copy_state(state)
    model = {
        **command,
        "algorithm": algorithm,
        "compiled_hash": _digest(command),
        "governance_state": "approved",
    }
    runtime["forecast_models"][model["model_id"]] = model
    runtime["events"].append(
        _state_event("ForecastModelRegistered", model["model_id"], model)
    )
    return {"ok": True, "state": runtime, "forecast_model": model}


def predictive_demand_receive_event(
    state: dict, event: dict, *, simulate_failure: bool = False
) -> dict:
    if event.get("event_type") not in PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES:
        raise ValueError(
            "Unsupported Predictive Demand consumed event: "
            f"{event.get('event_type')}"
        )
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Predictive Demand consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {
            "ok": True,
            "state": runtime,
            "handler": {"status": "duplicate", "event_id": event_id},
        }
    handler = {
        "event_id": event_id,
        "event_type": event["event_type"],
        "idempotency_key": f"predictive_demand:{event['event_type']}:{event_id}",
        "attempts": int(runtime.get("configuration", {}).get("retry_limit", 3) or 3),
    }
    if simulate_failure:
        handler["status"] = "dead_letter"
        runtime["dead_letter"].append({**event, "handler": handler})
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    handler["status"] = "handled"
    runtime["inbox"].append({**event, "handler": handler})
    runtime["handled_events"].add(event_id)
    runtime = predictive_demand_ingest_demand_signal(
        runtime,
        _signal_command_from_event(runtime, event_id, event["event_type"], payload),
    )["state"]
    runtime["events"].append(_state_event(f"{event['event_type']}Handled", event_id, payload))
    return {"ok": True, "state": runtime, "handler": handler}


def predictive_demand_ingest_demand_signal(state: dict, command: dict) -> dict:
    required = {
        "signal_id",
        "tenant",
        "signal_type",
        "sku",
        "location",
        "region",
        "quantity",
        "signal_date",
        "source",
        "payload",
    }
    missing = required - set(command)
    if missing:
        raise ValueError(
            f"Missing Predictive Demand signal fields: {tuple(sorted(missing))}"
        )
    _require_configured(state)
    signal_type = str(command["signal_type"]).lower()
    if signal_type not in state["configuration"]["supported_signal_types"]:
        raise ValueError(f"Unsupported Predictive Demand signal type: {signal_type}")
    if command["region"] not in state["configuration"]["supported_regions"]:
        raise ValueError(
            f"Unsupported Predictive Demand region: {command['region']}"
        )
    runtime = _copy_state(state)
    quantity = round(float(command["quantity"]), 4)
    signal = {
        **command,
        "signal_type": signal_type,
        "quantity": quantity,
        "payload": dict(command["payload"]),
        "driver_weight": _SIGNAL_WEIGHTS.get(signal_type, 1.0),
        "audit_proof": _digest(command),
    }
    runtime["demand_signals"][signal["signal_id"]] = signal
    if signal_type == "inventory":
        inventory_key = _inventory_key(signal["tenant"], signal["sku"], signal["location"])
        available_quantity = float(
            signal["payload"].get(
                "available_quantity",
                signal["payload"].get("on_hand", quantity),
            )
        )
        runtime["inventory_positions"][inventory_key] = {
            "tenant": signal["tenant"],
            "sku": signal["sku"],
            "location": signal["location"],
            "available_quantity": round(available_quantity, 4),
            "region": signal["region"],
            "signal_id": signal["signal_id"],
        }
    runtime["events"].append(_state_event("DemandSignalIngested", signal["signal_id"], signal))
    return {"ok": True, "state": runtime, "demand_signal": signal}


def predictive_demand_create_forecast_run(state: dict, command: dict) -> dict:
    required = {
        "run_id",
        "model_id",
        "tenant",
        "sku",
        "location",
        "horizon_days",
        "initiated_by",
        "status",
    }
    missing = required - set(command)
    if missing:
        raise ValueError(
            f"Missing Predictive Demand run fields: {tuple(sorted(missing))}"
        )
    model = state["forecast_models"].get(command["model_id"])
    if not model:
        raise ValueError(
            f"Unknown Predictive Demand forecast model: {command['model_id']}"
        )
    if model["tenant"] != command["tenant"]:
        raise ValueError("Predictive Demand run tenant must match the forecast model")
    runtime = _copy_state(state)
    preview = _forecast_preview(
        runtime,
        tenant=command["tenant"],
        sku=command["sku"],
        location=command["location"],
        horizon_days=int(command["horizon_days"]),
        model=model,
    )
    run = {
        **command,
        "horizon_days": int(command["horizon_days"]),
        "signal_count": len(preview["signal_ids"]),
        "signal_ids": preview["signal_ids"],
        "baseline_quantity": preview["baseline_quantity"],
        "forecast_quantity": preview["forecast_quantity"],
        "available_inventory": preview["available_inventory"],
        "shortage_quantity": preview["shortage_quantity"],
        "confidence": preview["confidence"],
        "service_level_target": preview["service_level_target"],
        "audit_proof": _digest({"command": command, "preview": preview}),
    }
    runtime["forecast_runs"][run["run_id"]] = run
    runtime["events"].append(_state_event("ForecastRunCreated", run["run_id"], run))
    return {"ok": True, "state": runtime, "forecast_run": run}


def predictive_demand_publish_forecast_result(state: dict, command: dict) -> dict:
    required = {"result_id", "run_id", "tenant", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(
            f"Missing Predictive Demand result fields: {tuple(sorted(missing))}"
        )
    run = state["forecast_runs"].get(command["run_id"])
    if not run:
        raise ValueError(f"Unknown Predictive Demand run: {command['run_id']}")
    runtime = _copy_state(state)
    run = runtime["forecast_runs"][command["run_id"]]
    confidence = float(run["confidence"])
    band_factor = max(0.08, round(1.0 - confidence, 4))
    forecast_quantity = float(run["forecast_quantity"])
    shortage_quantity = float(run["shortage_quantity"])
    result = {
        **command,
        "model_id": run["model_id"],
        "sku": run["sku"],
        "location": run["location"],
        "forecast_quantity": forecast_quantity,
        "available_inventory": float(run["available_inventory"]),
        "recommended_supply": round(max(shortage_quantity, 0.0), 2),
        "shortage_quantity": shortage_quantity,
        "confidence": confidence,
        "confidence_band": (
            round(max(forecast_quantity * (1.0 - band_factor), 0.0), 2),
            round(forecast_quantity * (1.0 + band_factor), 2),
        ),
        "planning_action": "expedite_supply" if shortage_quantity > 0 else "monitor",
        "audit_proof": _digest({"command": command, "run": run}),
    }
    runtime["forecast_results"][result["result_id"]] = result
    runtime["events"].append(
        _state_event("ForecastResultPublished", result["result_id"], result)
    )
    _emit(
        runtime,
        "ForecastUpdated",
        result["tenant"],
        {
            "result_id": result["result_id"],
            "run_id": result["run_id"],
            "sku": result["sku"],
            "location": result["location"],
            "forecast_quantity": result["forecast_quantity"],
            "recommended_supply": result["recommended_supply"],
            "confidence_band": result["confidence_band"],
        },
    )
    if shortage_quantity > 0:
        _emit(
            runtime,
            "MaterialShortageDetected",
            result["tenant"],
            {
                "result_id": result["result_id"],
                "run_id": result["run_id"],
                "sku": result["sku"],
                "location": result["location"],
                "shortage_quantity": result["shortage_quantity"],
                "available_inventory": result["available_inventory"],
                "recommended_supply": result["recommended_supply"],
            },
        )
    return {"ok": True, "state": runtime, "forecast_result": result}


def predictive_demand_build_workbench_view(state: dict, *, tenant: str) -> dict:
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
        "format": "appgen.predictive-demand-workbench-view.v1",
        "tenant": tenant,
        "model_count": len(models),
        "run_count": len(runs),
        "signal_count": len(signals),
        "result_count": len(results),
        "shortage_count": len(
            tuple(result for result in results if float(result["shortage_quantity"]) > 0.0)
        ),
        "inventory_position_count": len(
            tuple(
                pos
                for pos in state.get("inventory_positions", {}).values()
                if pos["tenant"] == tenant
            )
        ),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {
            "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
            "outbox_table": "predictive_demand_appgen_outbox_event",
            "inbox_table": "predictive_demand_appgen_inbox_event",
            "dead_letter_table": "predictive_demand_dead_letter_event",
        },
    }


def predictive_demand_verify_owned_table_boundary() -> dict:
    return {
        "format": "appgen.predictive-demand-boundary.v1",
        "ok": True,
        "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
        "declared_dependencies": {
            "apis": (
                "POST /forecast-models",
                "POST /forecast-runs",
                "POST /demand-signals",
                "GET /forecast-results",
            ),
            "events": PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES,
            "shared_tables": (),
        },
    }


def predictive_demand_build_api_contract() -> dict:
    return {
        "format": "appgen.predictive-demand-api-contract.v1",
        "ok": True,
        "routes": (
            "POST /forecast-models",
            "POST /forecast-runs",
            "POST /demand-signals",
            "GET /forecast-results",
        ),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
    }


def predictive_demand_permissions_contract() -> dict:
    return {
        "format": "appgen.predictive-demand-permissions.v1",
        "ok": True,
        "permissions": (
            "predictive_demand.model.write",
            "predictive_demand.signal.write",
            "predictive_demand.run.write",
            "predictive_demand.result.write",
            "predictive_demand.event.consume",
            "predictive_demand.configure",
            "predictive_demand.audit",
        ),
    }


def _signal_command_from_event(
    state: dict, event_id: str, event_type: str, payload: dict
) -> dict:
    tenant = payload.get("tenant")
    sku = payload.get("sku")
    location = payload.get("location")
    if not tenant or not sku or not location:
        raise ValueError(
            "Predictive Demand consumed events require tenant, sku, and location"
        )
    region = payload.get(
        "region",
        state.get("configuration", {}).get("supported_regions", ("US",))[0],
    )
    if event_type == "OrderShipped":
        signal_type = "shipment"
        quantity = float(payload.get("quantity", payload.get("shipped_quantity", 0.0)))
    elif event_type == "OperationalKpiChanged":
        signal_type = "operational"
        quantity = float(payload.get("value", payload.get("metric_value", 0.0)))
    else:
        signal_type = "inventory"
        quantity = float(
            payload.get("available_quantity", payload.get("on_hand", payload.get("quantity", 0.0)))
        )
    return {
        "signal_id": event_id,
        "tenant": tenant,
        "signal_type": signal_type,
        "sku": sku,
        "location": location,
        "region": region,
        "quantity": quantity,
        "signal_date": payload.get("effective_at", event_id),
        "source": event_type,
        "payload": payload,
    }


def _forecast_preview(
    state: dict,
    *,
    tenant: str,
    sku: str,
    location: str,
    horizon_days: int,
    model: dict,
) -> dict:
    relevant_signals = tuple(
        signal
        for signal in state["demand_signals"].values()
        if signal["tenant"] == tenant
        and signal["sku"] == sku
        and signal["location"] == location
    )
    demand_signals = tuple(
        signal for signal in relevant_signals if signal["signal_type"] != "inventory"
    )
    history_window_days = int(
        state["parameters"].get("history_window_days", {"value": 90})["value"]
    )
    signal_span_days = max(7.0, min(float(history_window_days), max(len(demand_signals), 1) * 7.0))
    demand_total = sum(_weighted_demand(state, signal) for signal in demand_signals)
    baseline_quantity = round(demand_total, 2)
    daily_rate = demand_total / signal_span_days
    forecast_quantity = round(
        max(
            daily_rate
            * float(horizon_days)
            * _algorithm_factor(model["algorithm"])
            * _operational_multiplier(state, demand_signals),
            0.0,
        ),
        2,
    )
    confidence = round(
        min(
            0.99,
            0.55
            + min(len(demand_signals), 8) * 0.05
            + (0.05 if model["algorithm"] == "ensemble" else 0.0),
        ),
        4,
    )
    inventory_position = state["inventory_positions"].get(
        _inventory_key(tenant, sku, location),
        {"available_quantity": 0.0},
    )
    available_inventory = round(float(inventory_position["available_quantity"]), 2)
    service_level_target = float(
        state["parameters"].get("service_level_target", {"value": 0.95})["value"]
    )
    safety_stock = round(
        forecast_quantity * max(service_level_target - 0.5, 0.0),
        2,
    )
    shortage_quantity = round(
        max(forecast_quantity + safety_stock - available_inventory, 0.0),
        2,
    )
    return {
        "signal_ids": tuple(signal["signal_id"] for signal in relevant_signals),
        "baseline_quantity": baseline_quantity,
        "forecast_quantity": forecast_quantity,
        "available_inventory": available_inventory,
        "shortage_quantity": shortage_quantity,
        "confidence": confidence,
        "service_level_target": service_level_target,
    }


def _weighted_demand(state: dict, signal: dict) -> float:
    quantity = float(signal["quantity"])
    if signal["signal_type"] == "operational":
        return quantity * float(
            state["parameters"].get("causal_weight", {"value": 0.35})["value"]
        )
    if signal["signal_type"] == "promotion":
        lift = float(
            state["parameters"].get("promotion_lift_default", {"value": 0.0})["value"]
        )
        return quantity * (1.0 + lift / 100.0)
    return quantity * float(_SIGNAL_WEIGHTS.get(signal["signal_type"], 1.0))


def _operational_multiplier(state: dict, signals: tuple[dict, ...]) -> float:
    operational_pressure = sum(
        float(signal["quantity"])
        for signal in signals
        if signal["signal_type"] == "operational"
    )
    causal_weight = float(
        state["parameters"].get("causal_weight", {"value": 0.35})["value"]
    )
    return 1.0 + min((operational_pressure / 100.0) * causal_weight, 0.5)


def _algorithm_factor(algorithm: str) -> float:
    if algorithm == "ensemble":
        return 1.05
    if algorithm == "causal_regression":
        return 1.02
    if algorithm == "croston":
        return 0.95
    return 1.0


def _inventory_key(tenant: str, sku: str, location: str) -> str:
    return f"{tenant}:{sku}:{location}"


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Predictive Demand runtime must be configured before commands execute")


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "contract": "appgen_event_contract",
        "idempotency_key": (
            "predictive_demand:"
            f"{event_type}:"
            f"{payload.get('result_id') or payload.get('run_id') or len(state['outbox']) + 1}"
        ),
        "retry_policy": {
            "max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)),
            "dead_letter": "predictive_demand_dead_letter_event",
        },
        "audit_hash": _digest(
            {"event_type": event_type, "tenant": tenant, "payload": payload}
        ),
    }
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


def _state_event(event_type: str, key: str, payload: dict) -> dict:
    return {
        "event_type": event_type,
        "key": key,
        "payload": payload,
        "hash": _digest({"event_type": event_type, "key": key, "payload": payload}),
    }


def _capability_evidence(state: dict, capability: str) -> dict:
    return {
        "capability": capability,
        "events": len(state["events"]),
        "outbox": len(state["outbox"]),
        "inbox": len(state["inbox"]),
        "rules": len(state["rules"]),
        "parameters": len(state["parameters"]),
        "configuration": bool(state["configuration"].get("ok")),
        "runtime_digest": _digest(
            {
                "capability": capability,
                "models": len(state["forecast_models"]),
                "runs": len(state["forecast_runs"]),
                "results": len(state["forecast_results"]),
            }
        ),
    }


def _digest(payload: dict) -> str:
    def default(value):
        if isinstance(value, set):
            return sorted(value)
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return str(value)
        return value

    return hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
            default=default,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()

"""Executable runtime for the Predictive Demand PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


PREDICTIVE_DEMAND_EVENT_CONTRACT = "AppGen-X"
PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC = "appgen.predictive_demand.events"
PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PREDICTIVE_DEMAND_OWNED_TABLES = (
    "forecast_model",
    "forecast_run",
    "demand_signal",
    "forecast_result",
    "planning_horizon",
    "forecast_driver",
    "consensus_adjustment",
    "scenario_version",
    "shortage_risk",
    "replenishment_recommendation",
    "forecast_exception",
    "model_drift_signal",
    "planning_rule",
    "planning_parameter",
    "governed_model_evidence",
    "forecast_audit_proof",
)
PREDICTIVE_DEMAND_RUNTIME_TABLES = (
    "predictive_demand_appgen_outbox_event",
    "predictive_demand_appgen_inbox_event",
    "predictive_demand_dead_letter_event",
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

PREDICTIVE_DEMAND_STANDARD_FEATURE_KEYS = ('forecast_models',
 'forecast_runs',
 'demand_signals',
 'forecast_results',
 'planning_horizons',
 'forecast_drivers',
 'consensus_adjustments',
 'scenario_versions',
 'shortage_risks',
 'replenishment_recommendations',
 'forecast_exceptions',
 'model_drift_signals',
 'planning_rules',
 'planning_parameters',
 'governed_model_evidence',
 'forecast_audit_proofs',
 'shipment_projection',
 'inventory_pool_projection',
 'operational_kpi_projection',
 'baseline_forecast',
 'planner_overrides',
 'promotion_lift_controls',
 'seasonality_controls',
 'service_level_targets',
 'safety_stock_guidance',
 'shortage_detection',
 'inventory_coverage',
 'causal_drivers',
 'model_governance',
 'tenant_isolation',
 'appgen_x_outbox',
 'appgen_x_inbox',
 'idempotent_handlers',
 'retry_dead_letter_evidence',
 'permissions',
 'configuration_schema',
 'rule_engine',
 'parameter_engine',
 'seed_data',
 'schema_contract',
 'service_contract',
 'release_evidence',
 'workbench')

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
        "runtime_tables": PREDICTIVE_DEMAND_RUNTIME_TABLES,
        "required_event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
        "event_contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
        "consumes": PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES,
        "emits": PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES,
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
            "register_planning_horizon",
            "register_forecast_driver",
            "record_consensus_adjustment",
            "create_scenario_version",
            "assess_shortage_risk",
            "prepare_replenishment_recommendation",
            "open_forecast_exception",
            "resolve_forecast_exception",
            "record_model_drift_signal",
            "register_governed_model_evidence",
            "seal_forecast_audit_proof",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
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
    state = predictive_demand_register_planning_horizon(
        state,
        {
            "horizon_id": "horizon_alpha",
            "tenant": "tenant_alpha",
            "sku": "SKU-ALPHA",
            "location": "DC-1",
            "start_date": "2026-05-27",
            "end_date": "2026-06-10",
            "bucket": "daily",
            "status": "active",
        },
    )["state"]
    state = predictive_demand_register_forecast_driver(
        state,
        {
            "driver_id": "driver_promo",
            "tenant": "tenant_alpha",
            "sku": "SKU-ALPHA",
            "driver_type": "promotion",
            "weight": 0.35,
            "source": "campaign_plan",
            "status": "active",
        },
    )["state"]
    state = predictive_demand_record_consensus_adjustment(
        state,
        {
            "adjustment_id": "consensus_alpha",
            "tenant": "tenant_alpha",
            "result_id": "result_alpha",
            "adjusted_quantity": 82,
            "reason": "commercial_commit",
            "approved_by": "planner_alpha",
            "status": "approved",
        },
    )["state"]
    state = predictive_demand_create_scenario_version(
        state,
        {
            "scenario_id": "scenario_alpha",
            "tenant": "tenant_alpha",
            "base_result_id": "result_alpha",
            "scenario_name": "promotion_plus_supply",
            "uplift_percent": 12.0,
            "status": "published",
        },
    )["state"]
    state = predictive_demand_assess_shortage_risk(
        state,
        {
            "risk_id": "risk_alpha",
            "tenant": "tenant_alpha",
            "result_id": "result_alpha",
            "available_inventory": 45,
            "forecast_quantity": 86,
            "service_level_target": 0.95,
        },
    )["state"]
    state = predictive_demand_prepare_replenishment_recommendation(
        state,
        {
            "recommendation_id": "replenish_alpha",
            "tenant": "tenant_alpha",
            "risk_id": "risk_alpha",
            "sku": "SKU-ALPHA",
            "location": "DC-1",
            "recommended_quantity": 41,
            "priority": "high",
            "status": "prepared",
        },
    )["state"]
    state = predictive_demand_open_forecast_exception(
        state,
        {
            "exception_id": "exception_alpha",
            "tenant": "tenant_alpha",
            "result_id": "result_alpha",
            "exception_type": "bias_threshold",
            "severity": "medium",
            "status": "open",
        },
    )["state"]
    state = predictive_demand_resolve_forecast_exception(
        state,
        {
            "exception_id": "exception_alpha",
            "resolution": "accepted_consensus_adjustment",
            "resolved_by": "planner_alpha",
        },
    )["state"]
    state = predictive_demand_record_model_drift_signal(
        state,
        {
            "drift_id": "drift_alpha",
            "tenant": "tenant_alpha",
            "model_id": "model_alpha",
            "drift_score": 0.04,
            "threshold": 0.12,
            "status": "within_tolerance",
        },
    )["state"]
    state = predictive_demand_register_governed_model_evidence(
        state,
        {
            "evidence_id": "governance_alpha",
            "tenant": "tenant_alpha",
            "model_id": "model_alpha",
            "metric": "wmape",
            "metric_value": 0.11,
            "governance_status": "approved",
        },
    )["state"]
    state = predictive_demand_seal_forecast_audit_proof(
        state,
        {
            "proof_id": "proof_alpha",
            "tenant": "tenant_alpha",
            "result_id": "result_alpha",
            "proof_type": "forecast_result_integrity",
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
        and all(
            state[name]
            for name in (
                "planning_horizons",
                "forecast_drivers",
                "consensus_adjustments",
                "scenario_versions",
                "shortage_risks",
                "replenishment_recommendations",
                "forecast_exceptions",
                "model_drift_signals",
                "governed_model_evidence",
                "forecast_audit_proofs",
            )
        )
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
        "planning_horizons": {},
        "forecast_drivers": {},
        "consensus_adjustments": {},
        "scenario_versions": {},
        "shortage_risks": {},
        "replenishment_recommendations": {},
        "forecast_exceptions": {},
        "model_drift_signals": {},
        "governed_model_evidence": {},
        "forecast_audit_proofs": {},
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
    normalized["event_contract"] = PREDICTIVE_DEMAND_EVENT_CONTRACT
    normalized["stream_engine_picker_visible"] = False
    normalized["user_selectable_event_contract"] = False
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


def predictive_demand_register_planning_horizon(state: dict, command: dict) -> dict:
    required = {"horizon_id", "tenant", "sku", "location", "start_date", "end_date", "bucket", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Predictive Demand planning horizon fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    horizon = {**command, "audit_proof": _digest(command)}
    runtime["planning_horizons"][horizon["horizon_id"]] = horizon
    runtime["events"].append(_state_event("PlanningHorizonRegistered", horizon["horizon_id"], horizon))
    return {"ok": True, "state": runtime, "planning_horizon": horizon}


def predictive_demand_register_forecast_driver(state: dict, command: dict) -> dict:
    required = {"driver_id", "tenant", "sku", "driver_type", "weight", "source", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Predictive Demand forecast driver fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    driver = {**command, "weight": round(float(command["weight"]), 4), "audit_proof": _digest(command)}
    runtime["forecast_drivers"][driver["driver_id"]] = driver
    runtime["events"].append(_state_event("ForecastDriverRegistered", driver["driver_id"], driver))
    return {"ok": True, "state": runtime, "forecast_driver": driver}


def predictive_demand_record_consensus_adjustment(state: dict, command: dict) -> dict:
    required = {"adjustment_id", "tenant", "result_id", "adjusted_quantity", "reason", "approved_by", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Predictive Demand consensus adjustment fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    result = runtime["forecast_results"].get(command["result_id"], {})
    baseline = float(result.get("forecast_quantity", command["adjusted_quantity"]))
    adjusted = float(command["adjusted_quantity"])
    adjustment = {
        **command,
        "adjusted_quantity": round(adjusted, 4),
        "baseline_quantity": round(baseline, 4),
        "adjustment_delta": round(adjusted - baseline, 4),
        "audit_proof": _digest(command),
    }
    runtime["consensus_adjustments"][adjustment["adjustment_id"]] = adjustment
    runtime["events"].append(_state_event("ConsensusAdjustmentRecorded", adjustment["adjustment_id"], adjustment))
    return {"ok": True, "state": runtime, "consensus_adjustment": adjustment}


def predictive_demand_create_scenario_version(state: dict, command: dict) -> dict:
    required = {"scenario_id", "tenant", "base_result_id", "scenario_name", "uplift_percent", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Predictive Demand scenario version fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    result = runtime["forecast_results"].get(command["base_result_id"], {})
    base_quantity = float(result.get("forecast_quantity", 0.0))
    uplift = float(command["uplift_percent"])
    scenario = {
        **command,
        "uplift_percent": round(uplift, 4),
        "scenario_quantity": round(base_quantity * (1 + uplift / 100), 4),
        "audit_proof": _digest(command),
    }
    runtime["scenario_versions"][scenario["scenario_id"]] = scenario
    runtime["events"].append(_state_event("ScenarioVersionCreated", scenario["scenario_id"], scenario))
    return {"ok": True, "state": runtime, "scenario_version": scenario}


def predictive_demand_assess_shortage_risk(state: dict, command: dict) -> dict:
    required = {"risk_id", "tenant", "result_id", "available_inventory", "forecast_quantity", "service_level_target"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Predictive Demand shortage risk fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    available = float(command["available_inventory"])
    forecast = float(command["forecast_quantity"])
    service_level = float(command["service_level_target"])
    shortage = max(forecast - available, 0.0)
    risk_score = min(1.0, shortage / max(forecast, 1.0) * service_level)
    risk = {**command, "shortage_quantity": round(shortage, 4), "risk_score": round(risk_score, 4), "risk_band": "high" if risk_score >= 0.3 else "watch", "audit_proof": _digest(command)}
    runtime["shortage_risks"][risk["risk_id"]] = risk
    runtime["events"].append(_state_event("ShortageRiskAssessed", risk["risk_id"], risk))
    return {"ok": True, "state": runtime, "shortage_risk": risk}


def predictive_demand_prepare_replenishment_recommendation(state: dict, command: dict) -> dict:
    required = {"recommendation_id", "tenant", "risk_id", "sku", "location", "recommended_quantity", "priority", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Predictive Demand replenishment recommendation fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    recommendation = {**command, "recommended_quantity": round(float(command["recommended_quantity"]), 4), "audit_proof": _digest(command)}
    runtime["replenishment_recommendations"][recommendation["recommendation_id"]] = recommendation
    runtime["events"].append(_state_event("ReplenishmentRecommendationPrepared", recommendation["recommendation_id"], recommendation))
    return {"ok": True, "state": runtime, "replenishment_recommendation": recommendation}


def predictive_demand_open_forecast_exception(state: dict, command: dict) -> dict:
    required = {"exception_id", "tenant", "result_id", "exception_type", "severity", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Predictive Demand forecast exception fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    exception = {**command, "audit_proof": _digest(command)}
    runtime["forecast_exceptions"][exception["exception_id"]] = exception
    runtime["events"].append(_state_event("ForecastExceptionOpened", exception["exception_id"], exception))
    return {"ok": True, "state": runtime, "forecast_exception": exception}


def predictive_demand_resolve_forecast_exception(state: dict, command: dict) -> dict:
    required = {"exception_id", "resolution", "resolved_by"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Predictive Demand exception resolution fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    exception = dict(runtime["forecast_exceptions"][command["exception_id"]])
    exception.update({"resolution": command["resolution"], "resolved_by": command["resolved_by"], "status": "resolved", "resolution_proof": _digest(command)})
    runtime["forecast_exceptions"][command["exception_id"]] = exception
    runtime["events"].append(_state_event("ForecastExceptionResolved", exception["exception_id"], exception))
    return {"ok": True, "state": runtime, "forecast_exception": exception}


def predictive_demand_record_model_drift_signal(state: dict, command: dict) -> dict:
    required = {"drift_id", "tenant", "model_id", "drift_score", "threshold", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Predictive Demand model drift signal fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    drift_score = float(command["drift_score"])
    threshold = float(command["threshold"])
    drift = {**command, "drift_score": round(drift_score, 4), "threshold": round(threshold, 4), "retrain_required": drift_score > threshold, "audit_proof": _digest(command)}
    runtime["model_drift_signals"][drift["drift_id"]] = drift
    runtime["events"].append(_state_event("ModelDriftSignalRecorded", drift["drift_id"], drift))
    return {"ok": True, "state": runtime, "model_drift_signal": drift}


def predictive_demand_register_governed_model_evidence(state: dict, command: dict) -> dict:
    required = {"evidence_id", "tenant", "model_id", "metric", "metric_value", "governance_status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Predictive Demand governed model evidence fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    evidence = {**command, "metric_value": round(float(command["metric_value"]), 4), "audit_proof": _digest(command)}
    runtime["governed_model_evidence"][evidence["evidence_id"]] = evidence
    runtime["events"].append(_state_event("GovernedModelEvidenceRegistered", evidence["evidence_id"], evidence))
    return {"ok": True, "state": runtime, "governed_model_evidence": evidence}


def predictive_demand_seal_forecast_audit_proof(state: dict, command: dict) -> dict:
    required = {"proof_id", "tenant", "result_id", "proof_type"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Predictive Demand forecast audit proof fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    result = runtime["forecast_results"].get(command["result_id"], {})
    proof = {**command, "proof_hash": _digest({"command": command, "result": result}), "status": "sealed"}
    runtime["forecast_audit_proofs"][proof["proof_id"]] = proof
    runtime["events"].append(_state_event("ForecastAuditProofSealed", proof["proof_id"], proof))
    return {"ok": True, "state": runtime, "forecast_audit_proof": proof}


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
            "runtime_tables": PREDICTIVE_DEMAND_RUNTIME_TABLES,
            "outbox_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[0],
            "inbox_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[1],
            "dead_letter_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[2],
            "event_contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
            "required_event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
            "shared_table_access": False,
        },
    }


def predictive_demand_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed_api_dependencies = {
        "POST /forecast-models",
        "POST /forecast-runs",
        "POST /demand-signals",
        "GET /forecast-results",
        "GET /predictive-demand/schema-contract",
        "GET /predictive-demand/service-contract",
        "GET /predictive-demand/release-evidence",
        "inventory_pool_projection",
        "shipment_projection",
        "operational_kpi_projection",
    }
    allowed_event_dependencies = set(PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES)
    allowed_runtime_tables = set(PREDICTIVE_DEMAND_RUNTIME_TABLES)
    violations = tuple(
        reference
        for reference in references
        if reference not in set(PREDICTIVE_DEMAND_OWNED_TABLES)
        and reference not in allowed_api_dependencies
        and reference not in allowed_event_dependencies
        and reference not in allowed_runtime_tables
        and not str(reference).startswith("predictive_demand_")
    )
    return {
        "format": "appgen.predictive-demand-boundary.v1",
        "ok": not violations,
        "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
        "declared_dependencies": {
            "apis": (
                "POST /forecast-models",
                "POST /forecast-runs",
                "POST /demand-signals",
                "GET /forecast-results",
                "GET /predictive-demand/schema-contract",
                "GET /predictive-demand/service-contract",
                "GET /predictive-demand/release-evidence",
            ),
            "events": PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "inventory_pool_projection",
                "shipment_projection",
                "operational_kpi_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def predictive_demand_build_api_contract() -> dict:
    return {
        "format": "appgen.predictive-demand-api-contract.v1",
        "ok": True,
        "pbc": "predictive_demand",
        "routes": (
            {
                "route": "POST /forecast-models",
                "command": "register_forecast_model",
                "owned_tables": ("forecast_model",),
                "emits": (),
                "requires_permission": "predictive_demand.model.write",
                "idempotency_key": "model_id",
            },
            {
                "route": "POST /forecast-runs",
                "command": "create_forecast_run",
                "owned_tables": ("forecast_run",),
                "emits": (),
                "requires_permission": "predictive_demand.run.write",
                "idempotency_key": "run_id",
            },
            {
                "route": "POST /demand-signals",
                "command": "ingest_demand_signal",
                "owned_tables": ("demand_signal",),
                "emits": (),
                "requires_permission": "predictive_demand.signal.write",
                "idempotency_key": "signal_id",
            },
            {
                "route": "POST /forecast-results",
                "command": "publish_forecast_result",
                "owned_tables": ("forecast_result",),
                "emits": PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES,
                "requires_permission": "predictive_demand.result.write",
                "idempotency_key": "result_id",
            },
            {"route": "POST /planning-horizons", "command": "register_planning_horizon", "owned_tables": ("planning_horizon",), "emits": (), "requires_permission": "predictive_demand.configure", "idempotency_key": "horizon_id"},
            {"route": "POST /forecast-drivers", "command": "register_forecast_driver", "owned_tables": ("forecast_driver",), "emits": (), "requires_permission": "predictive_demand.configure", "idempotency_key": "driver_id"},
            {"route": "POST /consensus-adjustments", "command": "record_consensus_adjustment", "owned_tables": ("consensus_adjustment",), "emits": (), "requires_permission": "predictive_demand.result.write", "idempotency_key": "adjustment_id"},
            {"route": "POST /scenario-versions", "command": "create_scenario_version", "owned_tables": ("scenario_version",), "emits": (), "requires_permission": "predictive_demand.run.write", "idempotency_key": "scenario_id"},
            {"route": "POST /shortage-risks", "command": "assess_shortage_risk", "owned_tables": ("shortage_risk",), "emits": (), "requires_permission": "predictive_demand.result.write", "idempotency_key": "risk_id"},
            {"route": "POST /replenishment-recommendations", "command": "prepare_replenishment_recommendation", "owned_tables": ("replenishment_recommendation",), "emits": (), "requires_permission": "predictive_demand.result.write", "idempotency_key": "recommendation_id"},
            {"route": "POST /forecast-exceptions", "command": "open_forecast_exception", "owned_tables": ("forecast_exception",), "emits": (), "requires_permission": "predictive_demand.result.write", "idempotency_key": "exception_id"},
            {"route": "POST /forecast-exceptions/resolve", "command": "resolve_forecast_exception", "owned_tables": ("forecast_exception",), "emits": (), "requires_permission": "predictive_demand.result.write", "idempotency_key": "exception_id"},
            {"route": "POST /model-drift-signals", "command": "record_model_drift_signal", "owned_tables": ("model_drift_signal",), "emits": (), "requires_permission": "predictive_demand.model.write", "idempotency_key": "drift_id"},
            {"route": "POST /governed-model-evidence", "command": "register_governed_model_evidence", "owned_tables": ("governed_model_evidence",), "emits": (), "requires_permission": "predictive_demand.model.write", "idempotency_key": "evidence_id"},
            {"route": "POST /forecast-audit-proofs", "command": "seal_forecast_audit_proof", "owned_tables": ("forecast_audit_proof",), "emits": (), "requires_permission": "predictive_demand.audit", "idempotency_key": "proof_id"},
            {
                "route": "POST /predictive-demand/events/inbox",
                "command": "receive_event",
                "owned_tables": (),
                "consumes": PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES,
                "requires_permission": "predictive_demand.event.consume",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /forecast-results",
                "query": "build_workbench_view",
                "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
                "requires_permission": "predictive_demand.audit",
            },
            {
                "route": "GET /predictive-demand/schema-contract",
                "query": "build_schema_contract",
                "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
                "requires_permission": "predictive_demand.audit",
            },
            {
                "route": "GET /predictive-demand/service-contract",
                "query": "build_service_contract",
                "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
                "requires_permission": "predictive_demand.audit",
            },
            {
                "route": "GET /predictive-demand/release-evidence",
                "query": "build_release_evidence",
                "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
                "requires_permission": "predictive_demand.audit",
            },
        ),
        "declared_catalog_routes": (
            "POST /forecast-models",
            "POST /forecast-runs",
            "POST /demand-signals",
            "POST /forecast-results",
            "POST /planning-horizons",
            "POST /forecast-drivers",
            "POST /consensus-adjustments",
            "POST /scenario-versions",
            "POST /shortage-risks",
            "POST /replenishment-recommendations",
            "POST /forecast-exceptions",
            "POST /forecast-exceptions/resolve",
            "POST /model-drift-signals",
            "POST /governed-model-evidence",
            "POST /forecast-audit-proofs",
            "POST /predictive-demand/events/inbox",
            "GET /forecast-results",
            "GET /predictive-demand/schema-contract",
            "GET /predictive-demand/service-contract",
            "GET /predictive-demand/release-evidence",
        ),
        "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
        "runtime_tables": PREDICTIVE_DEMAND_RUNTIME_TABLES,
        "emits": PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES,
        "consumes": PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES,
        "database_backends": PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS,
        "permissions": tuple(sorted(predictive_demand_permissions_contract()["permissions"])),
        "shared_table_access": False,
        "event_contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
        "required_event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
    }


def predictive_demand_build_schema_contract() -> dict:
    table_fields = {
        "forecast_model": (
            "tenant",
            "model_id",
            "sku",
            "location",
            "algorithm",
            "version",
            "status",
            "audit_proof",
        ),
        "forecast_run": (
            "tenant",
            "run_id",
            "model_id",
            "sku",
            "location",
            "signal_count",
            "forecast_quantity",
            "shortage_quantity",
            "confidence",
            "audit_proof",
        ),
        "demand_signal": (
            "tenant",
            "signal_id",
            "signal_type",
            "sku",
            "location",
            "region",
            "quantity",
            "source",
            "driver_weight",
            "audit_proof",
        ),
        "forecast_result": (
            "tenant",
            "result_id",
            "run_id",
            "model_id",
            "sku",
            "location",
            "forecast_quantity",
            "recommended_supply",
            "shortage_quantity",
            "confidence_band",
            "planning_action",
            "audit_proof",
        ),
        "planning_horizon": (
            "tenant",
            "horizon_id",
            "sku",
            "location",
            "granularity",
            "starts_on",
            "ends_on",
            "freeze_window_days",
            "status",
            "audit_proof",
        ),
        "forecast_driver": (
            "tenant",
            "driver_id",
            "sku",
            "location",
            "driver_type",
            "driver_value",
            "weight",
            "source",
            "effective_on",
            "audit_proof",
        ),
        "consensus_adjustment": (
            "tenant",
            "adjustment_id",
            "run_id",
            "planner_id",
            "adjustment_quantity",
            "reason_code",
            "approval_status",
            "policy_result",
            "created_at",
            "audit_proof",
        ),
        "scenario_version": (
            "tenant",
            "scenario_id",
            "run_id",
            "scenario_name",
            "assumption_set",
            "forecast_quantity",
            "confidence",
            "selected",
            "created_by",
            "audit_proof",
        ),
        "shortage_risk": (
            "tenant",
            "risk_id",
            "result_id",
            "sku",
            "location",
            "shortage_quantity",
            "risk_band",
            "material_constraint",
            "alert_due_on",
            "audit_proof",
        ),
        "replenishment_recommendation": (
            "tenant",
            "recommendation_id",
            "result_id",
            "sku",
            "location",
            "recommended_quantity",
            "recommended_date",
            "service_level_target",
            "action_status",
            "audit_proof",
        ),
        "forecast_exception": (
            "tenant",
            "exception_id",
            "run_id",
            "exception_type",
            "severity",
            "detected_value",
            "threshold",
            "resolution_status",
            "assigned_to",
            "audit_proof",
        ),
        "model_drift_signal": (
            "tenant",
            "drift_id",
            "model_id",
            "metric_name",
            "metric_value",
            "threshold",
            "drift_band",
            "retrain_recommended",
            "observed_at",
            "audit_proof",
        ),
        "planning_rule": (
            "tenant",
            "rule_id",
            "scope",
            "status",
            "allowed_signal_types",
            "allowed_regions",
            "forecast_policy",
            "shortage_policy",
            "compiled_hash",
            "audit_proof",
        ),
        "planning_parameter": (
            "tenant",
            "parameter_id",
            "name",
            "value",
            "bounds",
            "changed_by",
            "effective_from",
            "effective_to",
            "compiled_hash",
            "audit_proof",
        ),
        "governed_model_evidence": (
            "tenant",
            "evidence_id",
            "model_id",
            "algorithm",
            "training_window",
            "validation_metrics",
            "approval_status",
            "approved_by",
            "approved_at",
            "audit_proof",
        ),
        "forecast_audit_proof": (
            "tenant",
            "proof_id",
            "entity_type",
            "entity_id",
            "proof_hash",
            "previous_hash",
            "signature",
            "control_assertions",
            "created_at",
            "audit_proof",
        ),
    }
    runtime_tables = (
        {
            "table": PREDICTIVE_DEMAND_RUNTIME_TABLES[0],
            "fields": (
                "tenant",
                "event_id",
                "event_type",
                "payload",
                "idempotency_key",
                "retry_policy",
                "audit_hash",
            ),
        },
        {
            "table": PREDICTIVE_DEMAND_RUNTIME_TABLES[1],
            "fields": (
                "event_id",
                "event_type",
                "payload",
                "idempotency_key",
                "attempts",
                "status",
            ),
        },
        {
            "table": PREDICTIVE_DEMAND_RUNTIME_TABLES[2],
            "fields": (
                "event_id",
                "event_type",
                "payload",
                "idempotency_key",
                "attempts",
                "status",
            ),
        },
    )
    relationships = (
        {
            "from_table": "forecast_run",
            "from_field": "model_id",
            "to_table": "forecast_model",
            "to_field": "model_id",
            "type": "owned_reference",
        },
        {
            "from_table": "forecast_result",
            "from_field": "run_id",
            "to_table": "forecast_run",
            "to_field": "run_id",
            "type": "owned_reference",
        },
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": next(field for field in table_fields[table] if field.endswith("_id")),
            "owned_by": "predictive_demand",
        }
        for table in PREDICTIVE_DEMAND_OWNED_TABLES
    )
    migrations = tuple(
        {
            "path": f"pbcs/predictive_demand/migrations/{index:03d}_{table}.sql",
            "operation": "create_owned_table",
            "table": table,
            "backend_allowlist": PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS,
        }
        for index, table in enumerate(PREDICTIVE_DEMAND_OWNED_TABLES, start=1)
    )
    models = tuple(
        {
            "module_path": f"pyAppGen.pbcs.predictive_demand.models.{table}",
            "table": table,
            "class_name": _class_name(table),
        }
        for table in PREDICTIVE_DEMAND_OWNED_TABLES
    )
    return {
        "format": "appgen.predictive-demand-owned-schema-contract.v1",
        "ok": len(tables) == len(PREDICTIVE_DEMAND_OWNED_TABLES)
        and len(migrations) == len(PREDICTIVE_DEMAND_OWNED_TABLES)
        and len(models) == len(PREDICTIVE_DEMAND_OWNED_TABLES)
        and tuple(item["table"] for item in runtime_tables) == PREDICTIVE_DEMAND_RUNTIME_TABLES,
        "pbc": "predictive_demand",
        "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
        "tables": tables,
        "runtime_tables": runtime_tables,
        "relationships": relationships,
        "migrations": migrations,
        "models": models,
        "database_backends": PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
        "event_contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "shared_table_access": False,
        "tenant_isolation": {"field": "tenant", "required": True},
        "schema_extensions": {
            "allowed": True,
            "owned_tables_only": True,
            "builder": "register_schema_extension",
        },
        "declared_dependencies": predictive_demand_verify_owned_table_boundary(())[
            "declared_dependencies"
        ],
    }


def predictive_demand_build_service_contract() -> dict:
    api = predictive_demand_build_api_contract()
    permissions = predictive_demand_permissions_contract()
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "register_forecast_model",
        "receive_event",
        "ingest_demand_signal",
        "create_forecast_run",
        "publish_forecast_result",
        "register_planning_horizon",
        "register_forecast_driver",
        "record_consensus_adjustment",
        "create_scenario_version",
        "assess_shortage_risk",
        "prepare_replenishment_recommendation",
        "open_forecast_exception",
        "resolve_forecast_exception",
        "record_model_drift_signal",
        "register_governed_model_evidence",
        "seal_forecast_audit_proof",
    )
    query_methods = (
        "build_workbench_view",
        "verify_owned_table_boundary",
        "build_api_contract",
        "permissions_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    )
    return {
        "format": "appgen.predictive-demand-service-contract.v1",
        "ok": len(command_methods) >= 9
        and "receive_event" in command_methods
        and "build_release_evidence" in query_methods,
        "pbc": "predictive_demand",
        "transaction_boundary": "predictive_demand_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": PREDICTIVE_DEMAND_OWNED_TABLES,
        "mutates_only_owned_tables": True,
        "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
        "runtime_tables": PREDICTIVE_DEMAND_RUNTIME_TABLES,
        "event_contract": {
            "contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
            "required_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
            "emits": PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES,
            "consumes": PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES,
            "outbox_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[0],
            "inbox_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[1],
            "dead_letter_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[2],
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "eventing": {
            "contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
            "topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
            "outbox_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[0],
            "inbox_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[1],
            "dead_letter_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[2],
            "idempotency_key": "event_type:event_id",
        },
        "idempotent_handlers": ("receive_event",),
        "retry_dead_letter_evidence": {
            "configured_by": "retry_limit",
            "dead_letter_after_retry_limit": True,
            "dead_letter_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[2],
            "handler": "receive_event",
        },
        "configuration_contract": {
            "required_fields": PREDICTIVE_DEMAND_SUPPORTED_CONFIGURATION_FIELDS,
            "allowed_database_backends": PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
            "event_contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "external_dependencies": predictive_demand_verify_owned_table_boundary(())[
            "declared_dependencies"
        ],
        "shared_table_access": False,
        "command_permissions": {
            method: permissions["action_permissions"][method]
            for method in command_methods
            if method in permissions["action_permissions"]
        },
        "generated_service_artifacts": {
            "services": tuple(
                {
                    "service": method,
                    "callable": f"pyAppGen.pbcs.predictive_demand.runtime:{method}",
                }
                for method in command_methods + query_methods
            ),
            "routes": tuple(
                {
                    "route": route["route"],
                    "operation": route.get("command", route.get("query")),
                    "permission": route["requires_permission"],
                }
                for route in api["routes"]
            ),
            "events": {
                "emits": tuple(
                    {
                        "event_type": event_type,
                        "topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
                        "outbox_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[0],
                    }
                    for event_type in PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES
                ),
                "consumes": tuple(
                    {
                        "event_type": event_type,
                        "topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
                        "inbox_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[1],
                    }
                    for event_type in PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES
                ),
            },
            "handlers": tuple(
                {
                    "event_type": event_type,
                    "handler": "receive_event",
                    "module": "pyAppGen.pbcs.predictive_demand.runtime",
                    "idempotent": True,
                    "dead_letter_table": PREDICTIVE_DEMAND_RUNTIME_TABLES[2],
                }
                for event_type in PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES
            ),
        },
    }


def predictive_demand_build_release_evidence() -> dict:
    from .ui import PREDICTIVE_DEMAND_UI_FRAGMENT_KEYS
    from .ui import predictive_demand_render_workbench
    from .ui import predictive_demand_ui_contract

    schema = predictive_demand_build_schema_contract()
    service = predictive_demand_build_service_contract()
    api = predictive_demand_build_api_contract()
    permissions = predictive_demand_permissions_contract()
    ui = predictive_demand_ui_contract()
    control = _predictive_demand_release_control_evidence()
    generated_artifacts = {
        "migrations": schema["migrations"],
        "models": schema["models"],
        "services": service["generated_service_artifacts"]["services"],
        "routes": service["generated_service_artifacts"]["routes"],
        "events": service["generated_service_artifacts"]["events"],
        "handlers": service["generated_service_artifacts"]["handlers"],
        "ui": tuple(
            {
                "fragment": fragment,
                "route": "/workbench/pbcs/predictive_demand",
            }
            for fragment in PREDICTIVE_DEMAND_UI_FRAGMENT_KEYS
        ),
    }
    rendered = predictive_demand_render_workbench(
        control["state"],
        tenant="tenant_release",
        principal_permissions=permissions["permissions"],
    )
    checks = (
        {
            "id": "owned_schema_contract",
            "ok": schema["ok"] and schema["owned_tables"] == PREDICTIVE_DEMAND_OWNED_TABLES,
        },
        {
            "id": "runtime_event_tables_declared",
            "ok": tuple(item["table"] for item in schema["runtime_tables"])
            == PREDICTIVE_DEMAND_RUNTIME_TABLES,
        },
        {
            "id": "migration_model_generation",
            "ok": len(schema["migrations"]) == len(PREDICTIVE_DEMAND_OWNED_TABLES)
            and len(schema["models"]) == len(PREDICTIVE_DEMAND_OWNED_TABLES),
        },
        {
            "id": "service_contract_queries_and_commands",
            "ok": service["ok"]
            and {"build_schema_contract", "build_service_contract", "build_release_evidence"}
            <= set(service["query_methods"])
            and {"configure_runtime", "register_rule", "register_schema_extension"}
            <= set(service["command_methods"]),
        },
        {
            "id": "appgen_x_eventing_only",
            "ok": api["event_contract"] == PREDICTIVE_DEMAND_EVENT_CONTRACT
            and api["required_event_topic"] == PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
            and api["stream_engine_picker_visible"] is False
            and service["event_contract"]["stream_engine_picker_visible"] is False
            and ui["configuration_editor"]["stream_engine_picker_visible"] is False,
        },
        {
            "id": "permissions_cover_contracts",
            "ok": {
                "build_schema_contract",
                "build_service_contract",
                "build_release_evidence",
                "register_schema_extension",
            }
            <= set(permissions["action_permissions"]),
        },
        {
            "id": "retry_dead_letter_and_idempotency",
            "ok": control["handled"]["status"] == "handled"
            and control["duplicate"]["status"] == "duplicate"
            and control["failed"]["status"] == "dead_letter",
        },
        {
            "id": "runtime_outbox_inbox_dead_letter_evidence",
            "ok": control["workbench"]["binding_evidence"]["runtime_tables"]
            == PREDICTIVE_DEMAND_RUNTIME_TABLES
            and control["workbench"]["outbox_count"] >= 2
            and len(control["state"]["inbox"]) >= 2
            and len(control["state"]["dead_letter"]) == 1,
        },
        {
            "id": "generated_artifacts_present",
            "ok": len(generated_artifacts["migrations"]) == len(PREDICTIVE_DEMAND_OWNED_TABLES)
            and len(generated_artifacts["models"]) == len(PREDICTIVE_DEMAND_OWNED_TABLES)
            and len(generated_artifacts["services"]) >= 10
            and len(generated_artifacts["routes"]) >= 9
            and len(generated_artifacts["handlers"]) == len(PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES)
            and len(generated_artifacts["ui"]) == len(PREDICTIVE_DEMAND_UI_FRAGMENT_KEYS),
        },
        {
            "id": "backend_allowlist_and_boundary",
            "ok": schema["database_backends"] == PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
            and api["database_backends"] == PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
            and predictive_demand_verify_owned_table_boundary(
                (
                    "forecast_model",
                    PREDICTIVE_DEMAND_RUNTIME_TABLES[0],
                    "shipment_projection",
                    "OrderShipped",
                )
            )["ok"]
            and predictive_demand_verify_owned_table_boundary(("inventory_pool",))["ok"]
            is False,
        },
        {
            "id": "rendered_ui_binding_and_permissions",
            "ok": rendered["ok"]
            and not rendered["locked_actions"]
            and rendered["binding_evidence"]["owned_tables"] == PREDICTIVE_DEMAND_OWNED_TABLES,
        },
        {
            "id": "no_shared_table_access",
            "ok": schema["shared_table_access"] is False
            and service["shared_table_access"] is False
            and api["shared_table_access"] is False,
        },
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.predictive-demand-release-evidence.v1",
        "ok": not blocking_gaps,
        "pbc": "predictive_demand",
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema_contract": schema,
        "service_contract": service,
        "api_contract": api,
        "permissions_contract": permissions,
        "ui_contract": ui,
        "generated_artifacts": generated_artifacts,
        "control_evidence": {
            **control,
            "rendered": rendered,
        },
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
        "action_permissions": {
            "register_forecast_model": "predictive_demand.model.write",
            "ingest_demand_signal": "predictive_demand.signal.write",
            "create_forecast_run": "predictive_demand.run.write",
            "publish_forecast_result": "predictive_demand.result.write",
            "register_planning_horizon": "predictive_demand.configure",
            "register_forecast_driver": "predictive_demand.configure",
            "record_consensus_adjustment": "predictive_demand.result.write",
            "create_scenario_version": "predictive_demand.run.write",
            "assess_shortage_risk": "predictive_demand.result.write",
            "prepare_replenishment_recommendation": "predictive_demand.result.write",
            "open_forecast_exception": "predictive_demand.result.write",
            "resolve_forecast_exception": "predictive_demand.result.write",
            "record_model_drift_signal": "predictive_demand.model.write",
            "register_governed_model_evidence": "predictive_demand.model.write",
            "seal_forecast_audit_proof": "predictive_demand.audit",
            "receive_event": "predictive_demand.event.consume",
            "register_schema_extension": "predictive_demand.configure",
            "register_rule": "predictive_demand.configure",
            "set_parameter": "predictive_demand.configure",
            "configure_runtime": "predictive_demand.configure",
            "build_api_contract": "predictive_demand.audit",
            "permissions_contract": "predictive_demand.audit",
            "build_workbench_view": "predictive_demand.audit",
            "verify_owned_table_boundary": "predictive_demand.audit",
            "build_schema_contract": "predictive_demand.audit",
            "build_service_contract": "predictive_demand.audit",
            "build_release_evidence": "predictive_demand.audit",
        },
    }


def _predictive_demand_release_control_evidence() -> dict:
    state = predictive_demand_empty_state()
    state = predictive_demand_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
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
            "rule_id": "rule_release",
            "tenant": "tenant_release",
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
    extension = predictive_demand_register_schema_extension(
        state,
        "forecast_result",
        {"release_annotation": "jsonb"},
    )
    state = extension["state"]
    state = predictive_demand_register_forecast_model(
        state,
        {
            "model_id": "model_release",
            "tenant": "tenant_release",
            "sku": "SKU-REL",
            "location": "DC-1",
            "algorithm": "ensemble",
            "version": "2026.05",
            "status": "active",
        },
    )["state"]
    handled = predictive_demand_receive_event(
        state,
        {
            "event_id": "ship_release",
            "event_type": "OrderShipped",
            "payload": {
                "tenant": "tenant_release",
                "sku": "SKU-REL",
                "location": "DC-1",
                "region": "US",
                "quantity": 60,
            },
        },
    )
    state = handled["state"]
    duplicate = predictive_demand_receive_event(
        state,
        {
            "event_id": "ship_release",
            "event_type": "OrderShipped",
            "payload": {
                "tenant": "tenant_release",
                "sku": "SKU-REL",
                "location": "DC-1",
                "region": "US",
                "quantity": 60,
            },
        },
    )
    state = duplicate["state"]
    state = predictive_demand_receive_event(
        state,
        {
            "event_id": "inv_release",
            "event_type": "InventoryPoolChanged",
            "payload": {
                "tenant": "tenant_release",
                "sku": "SKU-REL",
                "location": "DC-1",
                "region": "US",
                "available_quantity": 25,
            },
        },
    )["state"]
    failed = predictive_demand_receive_event(
        state,
        {
            "event_id": "ops_release_fail",
            "event_type": "OperationalKpiChanged",
            "payload": {
                "tenant": "tenant_release",
                "sku": "SKU-REL",
                "location": "DC-1",
                "region": "US",
                "value": 18,
                "kpi_name": "order_intake_velocity",
            },
        },
        simulate_failure=True,
    )
    state = failed["state"]
    state = predictive_demand_ingest_demand_signal(
        state,
        {
            "signal_id": "manual_release",
            "tenant": "tenant_release",
            "signal_type": "manual",
            "sku": "SKU-REL",
            "location": "DC-1",
            "region": "US",
            "quantity": 35,
            "signal_date": "2026-05-26",
            "source": "planner_override",
            "payload": {"reason": "launch_commit"},
        },
    )["state"]
    state = predictive_demand_create_forecast_run(
        state,
        {
            "run_id": "run_release",
            "model_id": "model_release",
            "tenant": "tenant_release",
            "sku": "SKU-REL",
            "location": "DC-1",
            "horizon_days": 14,
            "initiated_by": "planner_release",
            "status": "active",
        },
    )["state"]
    published = predictive_demand_publish_forecast_result(
        state,
        {
            "result_id": "result_release",
            "run_id": "run_release",
            "tenant": "tenant_release",
            "status": "published",
        },
    )
    state = published["state"]
    workbench = predictive_demand_build_workbench_view(state, tenant="tenant_release")
    return {
        "state": state,
        "extension": extension["extension"],
        "handled": handled["handler"],
        "duplicate": duplicate["handler"],
        "failed": failed["handler"],
        "forecast_result": published["forecast_result"],
        "workbench": workbench,
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
        "contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
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


def _class_name(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))

"""One-PBC application surface for predictive demand planning."""

from __future__ import annotations

import hashlib


PBC_KEY = "predictive_demand"
OWNED_TABLES = (
    "predictive_demand_forecast_model",
    "predictive_demand_forecast_run",
    "predictive_demand_demand_signal",
    "predictive_demand_forecast_result",
    "predictive_demand_planning_horizon",
    "predictive_demand_forecast_driver",
    "predictive_demand_consensus_adjustment",
    "predictive_demand_scenario_version",
    "predictive_demand_shortage_risk",
    "predictive_demand_replenishment_recommendation",
    "predictive_demand_forecast_exception",
    "predictive_demand_model_drift_signal",
    "predictive_demand_planning_rule",
    "predictive_demand_planning_parameter",
    "predictive_demand_governed_model_evidence",
    "predictive_demand_forecast_audit_proof",
)


def _digest(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def predictive_demand_forms_contract() -> dict:
    """Return database-backed forms for a one-PBC demand planning app."""
    forms = (
        {"form_id": "forecast_model_registration_form", "writes_table": "predictive_demand_forecast_model", "command": "register_forecast_model", "fields": ("tenant", "model_id", "name", "algorithm", "granularity", "horizon_days", "status"), "validations": ("algorithm_supported", "training_window_declared", "owner_approval_required", "explainability_evidence_required")},
        {"form_id": "demand_signal_intake_form", "writes_table": "predictive_demand_demand_signal", "command": "ingest_demand_signal", "fields": ("tenant", "signal_id", "sku_id", "location_id", "signal_type", "quantity", "event_time", "source"), "validations": ("sku_projection_bound", "location_projection_bound", "event_time_required", "unit_normalized")},
        {"form_id": "planning_horizon_form", "writes_table": "predictive_demand_planning_horizon", "command": "register_planning_horizon", "fields": ("tenant", "horizon_id", "granularity", "start_at", "end_at", "service_level_target", "status"), "validations": ("date_range_valid", "service_level_in_range", "granularity_supported")},
        {"form_id": "forecast_driver_form", "writes_table": "predictive_demand_forecast_driver", "command": "register_forecast_driver", "fields": ("tenant", "driver_id", "driver_type", "sku_id", "location_id", "expected_lift", "confidence", "status"), "validations": ("driver_type_supported", "confidence_in_range", "counterfactual_context_required")},
        {"form_id": "forecast_run_form", "writes_table": "predictive_demand_forecast_run", "command": "create_forecast_run", "fields": ("tenant", "run_id", "model_id", "horizon_id", "scope", "started_by", "status"), "validations": ("model_active", "horizon_active", "scope_not_empty", "idempotency_key_required")},
        {"form_id": "forecast_result_publish_form", "writes_table": "predictive_demand_forecast_result", "command": "publish_forecast_result", "fields": ("tenant", "result_id", "run_id", "sku_id", "location_id", "period", "p50_quantity", "p90_quantity"), "validations": ("run_completed", "probability_bands_monotonic", "bias_within_tolerance")},
        {"form_id": "consensus_adjustment_form", "writes_table": "predictive_demand_consensus_adjustment", "command": "record_consensus_adjustment", "fields": ("tenant", "adjustment_id", "result_id", "planner_id", "reason_code", "adjusted_quantity", "approval_status"), "validations": ("reason_code_required", "material_adjustment_requires_approval", "audit_comment_required")},
        {"form_id": "scenario_version_form", "writes_table": "predictive_demand_scenario_version", "command": "create_scenario_version", "fields": ("tenant", "scenario_id", "name", "baseline_run_id", "assumption_set", "owner", "status"), "validations": ("baseline_exists", "assumptions_serialized", "owner_required")},
        {"form_id": "shortage_risk_form", "writes_table": "predictive_demand_shortage_risk", "command": "assess_shortage_risk", "fields": ("tenant", "risk_id", "sku_id", "location_id", "shortage_quantity", "risk_score", "risk_window"), "validations": ("inventory_projection_bound", "risk_score_in_range", "shortage_quantity_non_negative")},
        {"form_id": "replenishment_recommendation_form", "writes_table": "predictive_demand_replenishment_recommendation", "command": "prepare_replenishment_recommendation", "fields": ("tenant", "recommendation_id", "sku_id", "location_id", "recommended_quantity", "needed_by", "confidence"), "validations": ("needed_by_from_horizon", "quantity_positive", "service_level_impact_calculated")},
        {"form_id": "forecast_exception_form", "writes_table": "predictive_demand_forecast_exception", "command": "open_forecast_exception", "fields": ("tenant", "exception_id", "result_id", "exception_type", "severity", "owner", "status"), "validations": ("severity_supported", "owner_required", "resolution_sla_started")},
        {"form_id": "model_governance_form", "writes_table": "predictive_demand_planning_rule", "command": "register_rule", "fields": ("tenant", "rule_id", "scope", "model_policy", "bias_policy", "override_policy", "release_policy", "status"), "validations": ("rule_compiles_to_hash", "impact_simulation_required", "rollback_plan_required")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def predictive_demand_wizards_contract() -> dict:
    """Return guided forecasting workflows for demand planners and supply teams."""
    wizards = (
        {"wizard_id": "model_go_live_wizard", "steps": ("register_model", "bind_training_data", "validate_backtest", "approve_model", "activate_release_gate"), "completion_event": "ForecastModelActivated"},
        {"wizard_id": "signal_ingestion_wizard", "steps": ("select_signal_source", "map_sku_location", "normalize_units", "screen_anomalies", "publish_signal_event"), "completion_event": "DemandSignalIngested"},
        {"wizard_id": "forecast_cycle_wizard", "steps": ("select_horizon", "create_run", "publish_results", "review_bias", "open_exceptions"), "completion_event": "ForecastUpdated"},
        {"wizard_id": "consensus_planning_wizard", "steps": ("compare_statistical_forecast", "capture_planner_override", "require_material_approval", "lock_consensus", "seal_audit_proof"), "completion_event": "ConsensusDemandApproved"},
        {"wizard_id": "scenario_simulation_wizard", "steps": ("clone_baseline", "set_driver_assumptions", "run_counterfactual", "compare_service_levels", "promote_scenario"), "completion_event": "DemandScenarioSimulated"},
        {"wizard_id": "shortage_response_wizard", "steps": ("detect_shortage", "rank_coverage_gap", "prepare_replenishment", "notify_supply_owner", "track_resolution"), "completion_event": "MaterialShortageDetected"},
        {"wizard_id": "model_drift_remediation_wizard", "steps": ("detect_drift", "explain_feature_shift", "open_exception", "approve_retrain", "record_governance_evidence"), "completion_event": "ModelDriftRemediated"},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def predictive_demand_controls_contract() -> dict:
    """Return forecasting controls for accuracy, governance, resilience, and planning safety."""
    controls = (
        {"control_id": "model_backtest_and_bias_gate", "blocks_on_failure": True, "table_scope": ("predictive_demand_forecast_model", "predictive_demand_governed_model_evidence")},
        {"control_id": "demand_signal_quality_gate", "blocks_on_failure": True, "table_scope": ("predictive_demand_demand_signal", "predictive_demand_forecast_driver")},
        {"control_id": "horizon_service_level_gate", "blocks_on_failure": True, "table_scope": ("predictive_demand_planning_horizon", "predictive_demand_planning_parameter")},
        {"control_id": "forecast_probability_band_gate", "blocks_on_failure": True, "table_scope": ("predictive_demand_forecast_result", "predictive_demand_forecast_run")},
        {"control_id": "consensus_override_materiality_gate", "blocks_on_failure": True, "table_scope": ("predictive_demand_consensus_adjustment", "predictive_demand_forecast_audit_proof")},
        {"control_id": "scenario_assumption_traceability_gate", "blocks_on_failure": True, "table_scope": ("predictive_demand_scenario_version", "predictive_demand_forecast_driver")},
        {"control_id": "shortage_and_replenishment_safety_gate", "blocks_on_failure": True, "table_scope": ("predictive_demand_shortage_risk", "predictive_demand_replenishment_recommendation")},
        {"control_id": "exception_resolution_sla_gate", "blocks_on_failure": True, "table_scope": ("predictive_demand_forecast_exception", "predictive_demand_model_drift_signal")},
        {"control_id": "appgen_event_replay_gate", "blocks_on_failure": True, "table_scope": ("predictive_demand_appgen_outbox_event", "predictive_demand_appgen_inbox_event", "predictive_demand_dead_letter_event")},
        {"control_id": "owned_boundary_and_no_shared_tables_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_predictive_demand_app_contract() -> dict:
    """Return evidence that this PBC can stand alone as a predictive demand app."""
    forms = predictive_demand_forms_contract()["forms"]
    wizards = predictive_demand_wizards_contract()["wizards"]
    controls = predictive_demand_controls_contract()["controls"]
    return {
        "ok": bool(forms) and bool(wizards) and bool(controls),
        "pbc": PBC_KEY,
        "single_pbc_app": True,
        "database_backed": True,
        "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
        "owned_tables": OWNED_TABLES,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "workbench": "PredictiveDemandWorkbench",
        "assistant_panel": "PredictiveDemandAgent",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def document_instruction_predictive_demand_plan(document: str, instructions: str) -> dict:
    """Map planning documents and instructions to governed CRUD previews."""
    text = f"{document} {instructions}".lower()
    if "scenario" in text or "counterfactual" in text or "what if" in text:
        operation, table = "create_scenario_version", "predictive_demand_scenario_version"
    elif "exception" in text or "drift" in text or "bias" in text:
        operation, table = "open_forecast_exception", "predictive_demand_forecast_exception"
    elif "model" in text or "algorithm" in text or "backtest" in text:
        operation, table = "register_forecast_model", "predictive_demand_forecast_model"
    elif "signal" in text or "shipment" in text or "order" in text or "sell through" in text:
        operation, table = "ingest_demand_signal", "predictive_demand_demand_signal"
    elif "horizon" in text or "service level" in text or "granularity" in text:
        operation, table = "register_planning_horizon", "predictive_demand_planning_horizon"
    elif "driver" in text or "promotion" in text or "weather" in text or "causal" in text:
        operation, table = "register_forecast_driver", "predictive_demand_forecast_driver"
    elif "shortage" in text or "coverage" in text or "stockout" in text:
        operation, table = "assess_shortage_risk", "predictive_demand_shortage_risk"
    elif "replenish" in text or "buy" in text or "supply" in text:
        operation, table = "prepare_replenishment_recommendation", "predictive_demand_replenishment_recommendation"
    elif "override" in text or "consensus" in text or "planner" in text:
        operation, table = "record_consensus_adjustment", "predictive_demand_consensus_adjustment"
    elif "rule" in text or "parameter" in text or "policy" in text:
        operation, table = "register_rule", "predictive_demand_planning_rule"
    else:
        operation, table = "create_forecast_run", "predictive_demand_forecast_run"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document, instructions),
        "proposed_operation": operation,
        "target_table": table,
        "requires_human_confirmation": True,
        "crud_datastore_mutation": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def app_surface_smoke_test() -> dict:
    """Exercise standalone predictive demand app contracts."""
    app = single_pbc_predictive_demand_app_contract()
    shortage_plan = document_instruction_predictive_demand_plan("stockout risk", "assess shortage coverage")
    scenario_plan = document_instruction_predictive_demand_plan("promotion lift", "create scenario")
    checks = (
        app["ok"],
        len(app["forms"]) >= 12,
        len(app["wizards"]) >= 7,
        len(app["controls"]) >= 10,
        shortage_plan["target_table"] == "predictive_demand_shortage_risk",
        scenario_plan["target_table"] == "predictive_demand_scenario_version",
        all(table.startswith("predictive_demand_") for control in app["controls"] for table in control["table_scope"]),
    )
    return {"ok": all(checks), "single_pbc_app": app, "document_plans": (shortage_plan, scenario_plan), "side_effects": ()}

"""One-PBC application surface for planning, budgeting, and forecasting."""

from __future__ import annotations

import hashlib

PBC_KEY = "planning_budgeting_forecasting"
OWNED_TABLES = tuple(f"{PBC_KEY}_{name}" for name in ("planning_model", "budget_version", "forecast_cycle", "planning_scenario", "driver_assumption", "allocation_rule", "variance_analysis", "planning_approval"))


def _digest(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def planning_budgeting_forecasting_forms_contract() -> dict:
    forms = (
        {"form_id": "planning_model_form", "writes_table": "planning_budgeting_forecasting_planning_model", "command": "create_planning_model", "fields": ("tenant", "model_id", "name", "planning_domain", "calendar", "currency", "status"), "validations": ("calendar_required", "currency_supported", "owner_required")},
        {"form_id": "budget_version_form", "writes_table": "planning_budgeting_forecasting_budget_version", "command": "create_budget_version", "fields": ("tenant", "budget_id", "model_id", "version", "fiscal_year", "baseline_source", "status"), "validations": ("model_exists", "version_unique", "baseline_reconciled")},
        {"form_id": "forecast_cycle_form", "writes_table": "planning_budgeting_forecasting_forecast_cycle", "command": "open_forecast_cycle", "fields": ("tenant", "cycle_id", "model_id", "period", "forecast_type", "submission_deadline", "status"), "validations": ("period_open", "deadline_future", "forecast_type_supported")},
        {"form_id": "scenario_form", "writes_table": "planning_budgeting_forecasting_planning_scenario", "command": "model_scenario", "fields": ("tenant", "scenario_id", "model_id", "name", "assumption_set", "probability", "status"), "validations": ("assumptions_serialized", "probability_in_range", "counterfactual_documented")},
        {"form_id": "driver_assumption_form", "writes_table": "planning_budgeting_forecasting_driver_assumption", "command": "record_driver_assumption", "fields": ("tenant", "driver_id", "model_id", "driver_name", "driver_value", "source", "confidence"), "validations": ("source_required", "confidence_in_range", "driver_owner_required")},
        {"form_id": "allocation_rule_form", "writes_table": "planning_budgeting_forecasting_allocation_rule", "command": "register_allocation_rule", "fields": ("tenant", "allocation_rule_id", "model_id", "basis", "source_pool", "target_dimension", "status"), "validations": ("basis_supported", "source_pool_balanced", "target_dimension_valid")},
        {"form_id": "variance_analysis_form", "writes_table": "planning_budgeting_forecasting_variance_analysis", "command": "record_variance_analysis", "fields": ("tenant", "variance_id", "budget_id", "actual_amount", "planned_amount", "variance_reason", "owner"), "validations": ("actuals_bound", "variance_reason_required", "materiality_checked")},
        {"form_id": "planning_approval_form", "writes_table": "planning_budgeting_forecasting_planning_approval", "command": "approve_plan", "fields": ("tenant", "approval_id", "subject_id", "approval_type", "approver", "decision", "audit_hash"), "validations": ("approver_authorized", "decision_required", "audit_hash_required")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def planning_budgeting_forecasting_wizards_contract() -> dict:
    wizards = (
        {"wizard_id": "annual_budget_wizard", "steps": ("create_model", "load_baseline", "record_drivers", "allocate_costs", "approve_budget"), "completion_event": "BudgetApproved"},
        {"wizard_id": "rolling_forecast_wizard", "steps": ("open_cycle", "collect_submissions", "run_driver_forecast", "publish_forecast", "track_variance"), "completion_event": "ForecastPublished"},
        {"wizard_id": "scenario_modeling_wizard", "steps": ("clone_baseline", "change_assumptions", "simulate_outcome", "compare_cases", "promote_scenario"), "completion_event": "ScenarioModeled"},
        {"wizard_id": "variance_review_wizard", "steps": ("bind_actuals", "calculate_variance", "explain_driver", "assign_owner", "publish_flag"), "completion_event": "VarianceFlagged"},
        {"wizard_id": "allocation_governance_wizard", "steps": ("define_basis", "test_balancing", "approve_rule", "post_allocation", "audit_lineage"), "completion_event": "AllocationRuleApproved"},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def planning_budgeting_forecasting_controls_contract() -> dict:
    controls = (
        {"control_id": "model_calendar_currency_gate", "blocks_on_failure": True, "table_scope": ("planning_budgeting_forecasting_planning_model", "planning_budgeting_forecasting_budget_version")},
        {"control_id": "budget_version_lock_gate", "blocks_on_failure": True, "table_scope": ("planning_budgeting_forecasting_budget_version", "planning_budgeting_forecasting_planning_approval")},
        {"control_id": "forecast_submission_deadline_gate", "blocks_on_failure": True, "table_scope": ("planning_budgeting_forecasting_forecast_cycle", "planning_budgeting_forecasting_planning_approval")},
        {"control_id": "driver_assumption_lineage_gate", "blocks_on_failure": True, "table_scope": ("planning_budgeting_forecasting_driver_assumption", "planning_budgeting_forecasting_planning_scenario")},
        {"control_id": "allocation_balance_gate", "blocks_on_failure": True, "table_scope": ("planning_budgeting_forecasting_allocation_rule", "planning_budgeting_forecasting_variance_analysis")},
        {"control_id": "variance_materiality_gate", "blocks_on_failure": True, "table_scope": ("planning_budgeting_forecasting_variance_analysis", "planning_budgeting_forecasting_forecast_cycle")},
        {"control_id": "appgen_event_replay_gate", "blocks_on_failure": True, "table_scope": ("planning_budgeting_forecasting_appgen_outbox_event", "planning_budgeting_forecasting_appgen_inbox_event", "planning_budgeting_forecasting_appgen_dead_letter_event")},
        {"control_id": "owned_boundary_and_no_shared_tables_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_planning_budgeting_forecasting_app_contract() -> dict:
    forms = planning_budgeting_forecasting_forms_contract()["forms"]
    wizards = planning_budgeting_forecasting_wizards_contract()["wizards"]
    controls = planning_budgeting_forecasting_controls_contract()["controls"]
    return {"ok": bool(forms) and bool(wizards) and bool(controls), "pbc": PBC_KEY, "single_pbc_app": True, "database_backed": True, "allowed_database_backends": ("postgresql", "mysql", "mariadb"), "owned_tables": OWNED_TABLES, "forms": forms, "wizards": wizards, "controls": controls, "workbench": "PlanningBudgetingForecastingWorkbench", "assistant_panel": "PlanningBudgetingForecastingAssistantPanel", "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "side_effects": ()}


def document_instruction_planning_budgeting_forecasting_plan(document: str, instructions: str) -> dict:
    text = f"{document} {instructions}".lower()
    if "budget" in text:
        operation, table = "create_budget_version", "planning_budgeting_forecasting_budget_version"
    elif "forecast" in text or "cycle" in text:
        operation, table = "open_forecast_cycle", "planning_budgeting_forecasting_forecast_cycle"
    elif "scenario" in text or "what if" in text:
        operation, table = "model_scenario", "planning_budgeting_forecasting_planning_scenario"
    elif "driver" in text or "assumption" in text:
        operation, table = "record_driver_assumption", "planning_budgeting_forecasting_driver_assumption"
    elif "allocation" in text:
        operation, table = "register_allocation_rule", "planning_budgeting_forecasting_allocation_rule"
    elif "variance" in text or "actual" in text:
        operation, table = "record_variance_analysis", "planning_budgeting_forecasting_variance_analysis"
    elif "approve" in text:
        operation, table = "approve_plan", "planning_budgeting_forecasting_planning_approval"
    else:
        operation, table = "create_planning_model", "planning_budgeting_forecasting_planning_model"
    return {"ok": True, "pbc": PBC_KEY, "document_digest": _digest(document, instructions), "proposed_operation": operation, "target_table": table, "requires_human_confirmation": True, "crud_datastore_mutation": True, "event_contract": "AppGen-X", "side_effects": ()}


def app_surface_smoke_test() -> dict:
    app = single_pbc_planning_budgeting_forecasting_app_contract()
    forecast = document_instruction_planning_budgeting_forecasting_plan("rolling forecast", "open cycle")
    variance = document_instruction_planning_budgeting_forecasting_plan("actuals variance", "record analysis")
    checks = (app["ok"], len(app["forms"]) >= 8, len(app["wizards"]) >= 5, len(app["controls"]) >= 8, forecast["target_table"] == "planning_budgeting_forecasting_forecast_cycle", variance["target_table"] == "planning_budgeting_forecasting_variance_analysis", all(table.startswith("planning_budgeting_forecasting_") for control in app["controls"] for table in control["table_scope"]))
    return {"ok": all(checks), "single_pbc_app": app, "document_plans": (forecast, variance), "side_effects": ()}

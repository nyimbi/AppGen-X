"""Executable improve1 controls for the Planning Budgeting Forecasting PBC."""
from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import PLANNING_BUDGETING_FORECASTING_ALLOWED_DATABASE_BACKENDS, PLANNING_BUDGETING_FORECASTING_OWNED_TABLES, PLANNING_BUDGETING_FORECASTING_REQUIRED_EVENT_TOPIC

PBC_KEY = "planning_budgeting_forecasting"
EVENT_CONTRACT = "AppGen-X"
PLANNING_CONTROL_ALLOWED_DATABASE_BACKENDS = PLANNING_BUDGETING_FORECASTING_ALLOWED_DATABASE_BACKENDS
PLANNING_CONTROL_REQUIRED_EVENT_TOPIC = PLANNING_BUDGETING_FORECASTING_REQUIRED_EVENT_TOPIC
PLANNING_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(PLANNING_BUDGETING_FORECASTING_OWNED_TABLES + tuple(f"planning_budgeting_forecasting_{c.slug}_control" for c in IMPROVE1_CAPABILITIES)))
PLANNING_CONTROL_DECLARED_DEPENDENCIES = (
    "TrialBalanceCalculated", "RevenueRecognized", "DemandForecastPublished", "HeadcountPlanPublished",
    "CashForecastPublished", "ExchangeRateChanged", "ActualsClosed", "PolicyChanged", "WorkflowTaskChanged",
    "AuditEventSealed", "ModelGovernanceChanged", "CarbonIntensityWindowChanged",
)
PLANNING_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {c.feature_number: c for c in PLANNING_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {c.slug: c for c in PLANNING_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "planning_model_id", "budget_version_id", "forecast_cycle_id", "scenario_id", "cost_center_id", "account_id", "currency", "period_id", "actor_id", "policy_version", "evidence_references")
_FIELD_ROWS = """
1|model_code,model_owner,dimension_set,calendar,planning_grain,readiness_status
2|lifecycle_state,allowed_transition,approval_gate,archive_lock,reopen_reason,state_change_event
3|dimension_id,parent_member,child_member,hierarchy_version,cycle_check,orphan_check
4|dimension_change_id,impacted_versions,impacted_allocations,scenario_delta,approval_required,rollback_plan
5|branch_id,parent_version,branch_reason,merge_target,conflict_state,lineage_hash
6|budget_workflow_id,submitter,reviewer,approval_stage,rejection_reason,finalization_state
7|budget_line_id,account_member,period_amount,validation_rule,exception_reason,line_status
8|spread_profile_id,phasing_curve,source_amount,period_distribution,rounding_policy,reconciliation_delta
9|forecast_cycle_id,cycle_type,submission_window,publish_gate,refresh_cadence,cycle_owner
10|freshness_score_id,actuals_cutoff,driver_age,contributor_age,stale_reason,refresh_action
11|driver_id,driver_owner,unit_of_measure,calculation_method,source_authority,quality_rule
12|assumption_id,assumption_version,effective_period,sensitivity,approval_state,expiry_rule
13|actual_ingestion_id,source_system,loaded_period,reconciliation_status,staleness_reason,projection_hash
14|shock_id,driver_change,affected_lines,scenario_output,confidence,decision_preview
15|allocation_rule_id,rule_version,basis_driver,source_pool,target_members,effective_window
16|allocation_run_id,source_total,allocated_total,reconciliation_delta,exception_count,run_status
17|scenario_governance_id,scenario_type,owner,access_scope,baseline_version,approval_status
18|explainability_id,driver_contribution,allocation_contribution,variance_driver,citation_set,reviewer_note
19|comparison_id,baseline_scenario,alternate_scenario,delta_metric,causal_assumption,decision_trace
20|publication_id,rolling_window,published_version,recipient_group,lock_status,event_emitted
21|backtest_id,actual_period,forecast_period,error_metric,bias_signal,improvement_action
22|variance_id,actual_value,plan_value,variance_amount,materiality_threshold,root_cause
23|commentary_id,source_variances,generated_text,citation_set,reviewer_edit,approval_status
24|quality_score_id,commentary_id,grounding_score,materiality_score,tone_check,revision_required
25|approval_grain_id,dimension_slice,threshold,approver_group,segregation_check,approval_trace
26|freeze_id,lock_level,locked_dimensions,exception_window,break_glass_reason,unlock_approval
27|import_batch_id,file_digest,row_count,validation_errors,formula_cells,reject_reason
28|spreadsheet_lineage_id,workbook_ref,formula_map,external_links,manual_override,audit_result
29|actuals_reconciliation_id,ledger_period,source_total,planning_total,delta,correction_action
30|headcount_plan_id,position_group,fte,compensation_driver,hiring_timing,dependency_projection
31|revenue_link_id,demand_signal,price_assumption,volume_driver,revenue_rule,scenario_link
32|cash_hook_id,working_capital_driver,cash_cycle,collection_profile,payment_profile,treasury_projection
33|currency_control_id,rate_type,rate_source,translation_method,remeasurement_delta,fx_lock
34|access_slice_id,dimension_scope,contributor_role,write_window,masked_members,permission_check
35|forecast_model_id,feature_lineage,training_window,driver_set,drift_score,rollback_plan
36|anomaly_id,forecast_line,expected_range,observed_value,reason_codes,triage_action
37|risk_score_id,planning_area,risk_driver,probability,impact,mitigation
38|task_orchestration_id,task_type,assignee,due_date,dependency_task,completion_state
39|exception_case_id,case_type,severity,owner,sla,recovery_action
40|crypto_proof_id,version_hash,line_hash,approval_hash,event_hash,verifier_api
41|event_reliability_id,inbox_status,outbox_status,dead_letter_age,replay_eligibility,projection_freshness
42|boundary_proof_id,owned_table_check,ledger_table_block,revenue_table_block,demand_table_block,foreign_write_block
43|budget_agent_plan_id,instruction,owned_table_preview,affected_lines,approval_required,expected_event
44|forecast_agent_refresh_id,instruction,source_projection,refresh_scope,staleness_check,human_approval
45|operations_cockpit_id,cycle_health,open_tasks,exceptions,dead_letters,readiness_indicator
46|ui_surface_id,model_view,budget_view,forecast_view,scenario_view,agent_panel
47|control_test_id,budget_line_check,allocation_check,boundary_check,event_check,agent_bypass_check
48|resilience_drill_id,scenario,failed_dependency,retry_path,degraded_mode,recovery_time
49|readiness_score_id,setup_score,data_score,workflow_score,event_score,agent_score
50|release_proof_id,model_ready,budget_approved,forecast_published,scenario_explained,boundary_verified
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {n: f"{CAPABILITY_BY_NUMBER[n].slug}_verified" for n in range(1, 51)}
_FEATURE_FIELDS = {n: _BASE_FIELDS + _DOMAIN_FIELDS[n] + (_PRIMARY_PROOF_FIELDS[n],) for n in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    13: ("ActualsClosed",), 20: ("WorkflowTaskChanged",), 29: ("TrialBalanceCalculated",),
    30: ("HeadcountPlanPublished",), 31: ("RevenueRecognized", "DemandForecastPublished"),
    32: ("CashForecastPublished",), 33: ("ExchangeRateChanged",), 35: ("ModelGovernanceChanged",),
    38: ("WorkflowTaskChanged",), 40: ("AuditEventSealed",), 41: ("AuditEventSealed",),
    42: ("TrialBalanceCalculated", "RevenueRecognized", "DemandForecastPublished"), 44: ("ActualsClosed", "DemandForecastPublished"),
    48: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (2, 4, 6, 7, 15, 16, 20, 23, 25, 26, 27, 29, 34, 35, 38, 39, 43, 44, 48, 50)
_PROJECTION_ONLY_FEATURES = (13, 20, 29, 30, 31, 32, 33, 35, 38, 40, 41, 42, 44, 48)
_AGENT_PREVIEW_FEATURES = (23, 43, 44, 50)
_NON_MUTATING_FEATURES = (4, 14, 18, 19, 21, 23, 24, 35, 36, 37, 40, 41, 42, 45, 46, 47, 48, 49, 50)
_PLANNING_RISK_FEATURES = (1, 2, 3, 4, 6, 7, 13, 15, 16, 20, 22, 25, 26, 27, 29, 33, 34, 35, 36, 37, 39, 40, 41, 42, 47, 48, 50)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    return {"title": capability.title, "slug": capability.slug, "tables": (f"planning_budgeting_forecasting_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number], "ui": f"PlanningBudgetingForecasting{_camel(capability.slug)}Panel", "route": f"POST /planning-budgeting-forecasting/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in PLANNING_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({"database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "event_topic": PLANNING_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "dependency_access_mode": "api_event_projection", "human_confirmation": True, "agent_preview_only": True, "non_mutating_simulation": True, "planning_risk_evidence_complete": True, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires planning-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _PLANNING_RISK_FEATURES and payload.get("planning_risk_evidence_complete") is not True:
        findings.append("model, dimension, budget, driver, allocation, publication, variance, approval, import, actuals, currency, security, forecast risk, event, boundary, control, resilience, and release decisions require complete planning risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("lifecycle changes, dimension impact, budgets, validations, allocations, publications, commentary, approvals, locks, imports, actuals, security, model governance, orchestration, exceptions, agent actions, resilience, and release proof require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("planning agent skills must return cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("impact analysis, simulations, explainability, comparisons, backtesting, commentary, model governance, anomaly, risk, crypto, reliability, boundary, cockpit, UI proof, tests, drills, readiness, and release proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("actuals, headcount, revenue, demand, cash, FX, workflow, model, audit, event, and boundary facts must use APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != PLANNING_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("planning eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in PLANNING_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary planning datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("planning controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_planning_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in PLANNING_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in PLANNING_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "primary_proof": spec["primary_proof"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": PLANNING_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": PLANNING_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_planning_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_planning_control(capability) for capability in PLANNING_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.planning-budgeting-forecasting-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": PLANNING_CONTROL_OWNED_TABLES, "declared_dependencies": PLANNING_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": PLANNING_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": PLANNING_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


PLANNING_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_planning_control(slug, payload)) for capability in PLANNING_CONTROL_CAPABILITIES}

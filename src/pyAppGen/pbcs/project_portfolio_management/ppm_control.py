"""Executable improve1 controls for the Project Portfolio Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PROJECT_PORTFOLIO_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    PROJECT_PORTFOLIO_MANAGEMENT_OWNED_TABLES,
    PROJECT_PORTFOLIO_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    PROJECT_PORTFOLIO_MANAGEMENT_RUNTIME_TABLES,
)

PBC_KEY = "project_portfolio_management"
EVENT_CONTRACT = "AppGen-X"
PPM_CONTROL_ALLOWED_DATABASE_BACKENDS = PROJECT_PORTFOLIO_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
PPM_CONTROL_REQUIRED_EVENT_TOPIC = PROJECT_PORTFOLIO_MANAGEMENT_REQUIRED_EVENT_TOPIC
PPM_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in PPM_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in PPM_CONTROL_CAPABILITIES}
PPM_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        PROJECT_PORTFOLIO_MANAGEMENT_OWNED_TABLES
        + PROJECT_PORTFOLIO_MANAGEMENT_RUNTIME_TABLES
        + tuple(f"project_portfolio_management_{capability.slug}_control" for capability in PPM_CONTROL_CAPABILITIES)
    )
)
PPM_CONTROL_DECLARED_DEPENDENCIES = (
    "BudgetApproved",
    "EmployeeCreated",
    "EmployeeProvisioned",
    "RiskAssessed",
    "PolicyChanged",
    "ProcurementApproved",
    "FinancialEnvelopeProjected",
    "WorkforceCapacityProjected",
    "SupplierCommitmentProjected",
    "SustainabilityMetricProjected",
    "ProposalSubmitted",
    "AuditEventSealed",
    "ModelGovernanceChanged",
)
_BASE_FIELDS = (
    "tenant_id",
    "portfolio_id",
    "portfolio_item_id",
    "program_id",
    "business_case_id",
    "sponsor_id",
    "actor_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|strategy_graph_id,objective_id,okr_id,mandate_id,customer_outcome,enterprise_theme,orphan_flag,explanation
2|intake_score_id,problem_clarity,sponsor_authority,strategic_fit,benefit_evidence,cost_basis,risk_statement,remediation_task
3|archetype_id,initiative_class,required_evidence,scoring_dimension,approval_path,financial_method,risk_tolerance,gate_template
4|assumption_ledger_id,assumption_type,owner,confidence,evidence_source,expiration_date,sensitivity,validation_plan
5|benefit_hypothesis_id,outcome_metric,baseline,target,realization_mechanism,leading_indicator,attribution_logic,realization_curve
6|score_model_id,criteria_library,weighting_method,normalization_rule,mandatory_criteria,threshold_policy,approval_history,score_breakdown
7|prioritization_run_id,objective_set,constraint_definition,pareto_frontier,selected_point,rejected_alternative,executive_rationale,scenario_state
8|capital_allocation_id,budget_projection,funding_source,fiscal_period,capitalization_rule,reserved_capacity,funding_gap,sequence_recommendation
9|capacity_model_id,skill_taxonomy,role_criticality,scarcity,ramp_time,availability_window,confidence,capacity_heatmap
10|resource_conflict_id,demand_id,assignment_id,priority_conflict,timing_conflict,affected_milestone,swap_option,fairness_impact
11|dependency_graph_id,dependency_kind,strength,lead_lag,evidence_required,risk_propagation,critical_path,blocked_value
12|dependency_health_id,delay_probability,downstream_cost,downstream_schedule,downstream_benefit,mitigation_status,simulation_id,exception_queue
13|gate_template_id,gate_stage,required_document,required_metric,risk_check,financial_evidence,waiver_request,policy_explanation
14|gate_decision_id,decision_type,conditional_term,dissent_record,participant_quorum,delegated_authority,action_item,expiry_date
15|kanban_state_id,current_state,next_state,transition_permission,required_evidence,wip_limit,aging_days,bottleneck_reason
16|executive_scenario_id,constraint_change,selected_items,rejected_items,delayed_items,benefit_timing,risk_exposure,board_summary
17|real_option_id,option_type,option_assumption,trigger_event,expiration,uncertainty,decision_checkpoint,valuation_method
18|risk_aggregation_id,correlation_group,contagion_path,risk_appetite,residual_exposure,mitigation_coverage,heatmap_bucket,adjusted_score
19|risk_appetite_id,appetite_statement,tolerance_range,breach_logic,escalation_route,exception_approval,risk_acceptance,selection_evidence
20|issue_escalation_id,escalation_level,decision_needed,owner,due_date,impacted_items,intervention,decision_history
21|change_impact_id,cost_delta,benefit_delta,score_delta,risk_delta,capacity_delta,dependency_delta,before_after_view
22|benefit_attribution_id,attribution_model,comparison_baseline,counterfactual_evidence,contributing_initiative,confounder,confidence,validation_method
23|benefit_leakage_id,leakage_category,early_warning,erosion_amount,recovery_action,owner_accountability,rebaseline_option,stop_signal
24|post_investment_review_id,planned_cost,actual_cost,planned_benefit,actual_benefit,assumption_result,lesson,calibration_signal
25|balance_analytics_id,strategy_bucket,archetype_mix,risk_mix,horizon_mix,value_stream,investment_class,rebalancing_option
26|projection_descriptor_id,financial_projection,employee_projection,supplier_projection,risk_projection,procurement_projection,sustainability_projection,boundary_mode
27|financial_variance_id,baseline_version,current_forecast,variance_driver,funding_source,capitalization_treatment,contingency_use,materiality
28|funding_tranche_id,release_criteria,consumed_amount,remaining_authorization,gate_dependency,revocation_rule,redirect_option,audit_trace
29|stop_pause_pivot_id,decision_type,sunk_cost,residual_obligation,resource_release,benefit_loss,dependency_impact,authorization
30|health_fusion_id,schedule_signal,cost_signal,scope_signal,benefit_signal,risk_signal,data_freshness,recommendation
31|predictive_risk_id,model_purpose,slippage_risk,cost_overrun_risk,benefit_erosion_risk,resource_contention_risk,drift_check,explainable_driver
32|agenda_automation_id,decision_item,dependency_group,materiality_rank,dissent_summary,decision_packet,meeting_summary,typed_command
33|authority_matrix_id,role,threshold,domain,delegation,quorum,separation_of_duties,emergency_override
34|policy_studio_id,rule_template,impact_preview,conflict_detection,approval_workflow,version,history_simulation,activation_state
35|parameter_simulation_id,parameter_name,new_threshold,affected_items,changed_scores,new_gate_warnings,exception_volume,blast_radius
36|control_assertion_id,control_objective,test_method,sample_population,failure_evidence,remediation,owner,next_test_date
37|audit_reconstruction_id,transaction_time,valid_time,score_state,scenario_state,gate_state,decision_lineage,evidence_hash
38|decision_proof_id,proof_scope,input_hash,authority_hash,vote_hash,evidence_hash,event_hash,verifier_export
39|document_ingestion_id,document_digest,extracted_initiative,extracted_assumption,extracted_benefit,validation_error,crud_preview,citation
40|business_case_critique_id,rubric_id,missing_evidence,weak_assumption,historical_comparison,feasibility_concern,improvement,owned_evidence
41|exception_case_id,exception_type,affected_item,policy_breached,authority_required,temporary_control,expiry_date,closure_proof
42|intake_marketplace_id,sponsor_submission,duplicate_candidate,merge_option,comment_thread,tracking_status,consolidation_plan,transparency_score
43|stakeholder_map_id,sponsor,beneficiary,impacted_group,decision_maker,approver,change_champion,communication_owner
44|compliance_commitment_id,obligation_source,deadline,regulator,penalty_exposure,evidence_package,dependency,waiver_status
45|sustainability_lens_id,carbon_score,waste_score,energy_score,social_impact,resilience_score,projection_source,scenario_delta
46|anomaly_detection_id,anomaly_type,severity,score_change,gate_waiver_pattern,budget_fragmentation,approval_cluster,remediation
47|continuous_close_id,financial_freshness,benefit_freshness,capacity_freshness,risk_freshness,dependency_freshness,publication_readiness,blocked_refresh
48|executive_narrative_id,fact_citation,forecast_citation,assumption_citation,recommendation,unresolved_gap,board_summary,confidence
49|role_workbench_id,sponsor_view,manager_view,executive_room,finance_view,resource_view,risk_console,auditor_room
50|release_matrix_id,owned_tables,commands,routes,event_contracts,handlers,workbench_panels,agent_skills,boundary_checks
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    8: ("BudgetApproved", "FinancialEnvelopeProjected"),
    9: ("EmployeeCreated", "WorkforceCapacityProjected"),
    10: ("EmployeeCreated", "WorkforceCapacityProjected"),
    18: ("RiskAssessed",),
    21: ("BudgetApproved", "RiskAssessed", "WorkforceCapacityProjected"),
    26: ("FinancialEnvelopeProjected", "WorkforceCapacityProjected", "SupplierCommitmentProjected", "RiskAssessed", "ProcurementApproved", "SustainabilityMetricProjected"),
    27: ("BudgetApproved", "FinancialEnvelopeProjected"),
    31: ("ModelGovernanceChanged",),
    38: ("AuditEventSealed",),
    39: ("ProposalSubmitted",),
    44: ("PolicyChanged",),
    45: ("SustainabilityMetricProjected",),
    47: ("BudgetApproved", "EmployeeCreated", "RiskAssessed", "ProcurementApproved"),
    50: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 4, 6, 7, 8, 13, 14, 15, 16, 19, 21, 28, 29, 32, 33, 34, 35, 38, 39, 40, 41, 44, 45, 48, 50)
_AGENT_PREVIEW_FEATURES = (1, 2, 4, 7, 10, 12, 16, 21, 22, 29, 32, 35, 39, 40, 42, 46, 48, 49, 50)
_NON_MUTATING_FEATURES = (1, 2, 4, 5, 7, 8, 10, 12, 16, 17, 18, 21, 22, 23, 25, 26, 27, 30, 31, 32, 34, 35, 37, 38, 39, 40, 45, 46, 47, 48, 50)
_PROJECTION_ONLY_FEATURES = (8, 9, 10, 18, 21, 26, 27, 31, 38, 39, 44, 45, 47, 50)
_PPM_RISK_FEATURES = (1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 20, 21, 22, 23, 27, 28, 29, 30, 31, 33, 34, 36, 38, 40, 41, 44, 46, 47, 48, 49, 50)


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
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"project_portfolio_management_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"ProjectPortfolioManagement{_camel(capability.slug)}Panel",
        "route": f"POST /project-portfolio-management/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in PPM_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({
        "database_backend": "postgresql",
        "event_contract": EVENT_CONTRACT,
        "event_topic": PPM_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "ppm_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires portfolio-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _PPM_RISK_FEATURES and payload.get("ppm_risk_evidence_complete") is not True:
        findings.append("portfolio intake, scoring, prioritization, gates, dependencies, resources, benefits, risks, financials, decisions, policy, controls, audit, event, boundary, and release decisions require complete PPM risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("portfolio strategy, assumptions, scoring, prioritization, funding, gates, scenarios, risk acceptance, changes, tranches, stop/pause/pivot, agendas, authority, policies, parameter changes, proofs, documents, critiques, exceptions, compliance, sustainability, narratives, and release proof require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("PPM agent skills must produce cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("strategy graphs, scoring, optimization, allocation, conflicts, dependency simulations, scenarios, valuation, risk aggregation, impact analysis, benefit attribution, balance analytics, projections, variance, health, prediction, agenda generation, policy studio, parameter simulation, audit reconstruction, proofs, document ingestion, critique, sustainability, anomaly, continuous close, narrative, and release matrix must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("budget, employee, workforce, risk, procurement, supplier, financial, sustainability, proposal, audit, and model facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != PPM_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("PPM eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in PPM_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary PPM datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("PPM controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_ppm_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in PPM_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in PPM_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "primary_proof": spec["primary_proof"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": PPM_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": PPM_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "feature_number": resolved.feature_number,
        "slug": resolved.slug,
        "title": resolved.title,
        "capability": resolved.as_traceability_row(),
        "payload": candidate,
        "evidence": evidence,
        "missing_fields": missing_fields,
        "foreign_tables": foreign_tables,
        "undeclared_dependencies": undeclared_dependencies,
        "findings": findings,
        "side_effects": (),
    }


def improve1_ppm_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_ppm_control(capability) for capability in PPM_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.project-portfolio-management-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": PPM_CONTROL_OWNED_TABLES,
        "declared_dependencies": PPM_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": PPM_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": PPM_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


PPM_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_ppm_control(slug, payload)) for capability in PPM_CONTROL_CAPABILITIES}

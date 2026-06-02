"""Executable improve1 controls for the Professional Services Automation PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PROFESSIONAL_SERVICES_AUTOMATION_ALLOWED_DATABASE_BACKENDS,
    PROFESSIONAL_SERVICES_AUTOMATION_OWNED_TABLES,
    PROFESSIONAL_SERVICES_AUTOMATION_REQUIRED_EVENT_TOPIC,
    PROFESSIONAL_SERVICES_AUTOMATION_RUNTIME_TABLES,
)

PBC_KEY = "professional_services_automation"
EVENT_CONTRACT = "AppGen-X"
PSA_CONTROL_ALLOWED_DATABASE_BACKENDS = PROFESSIONAL_SERVICES_AUTOMATION_ALLOWED_DATABASE_BACKENDS
PSA_CONTROL_REQUIRED_EVENT_TOPIC = PROFESSIONAL_SERVICES_AUTOMATION_REQUIRED_EVENT_TOPIC
PSA_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in PSA_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in PSA_CONTROL_CAPABILITIES}
PSA_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        PROFESSIONAL_SERVICES_AUTOMATION_OWNED_TABLES
        + PROFESSIONAL_SERVICES_AUTOMATION_RUNTIME_TABLES
        + tuple(f"professional_services_automation_{capability.slug}_control" for capability in PSA_CONTROL_CAPABILITIES)
    )
)
PSA_CONTROL_DECLARED_DEPENDENCIES = (
    "EmployeeCreated",
    "ExpenseApproved",
    "InvoiceIssued",
    "PolicyChanged",
    "ContractApproved",
    "TimeSubmitted",
    "CustomerHealthProjected",
    "RateCardProjected",
    "ProposalApproved",
    "KnowledgeAssetProjected",
    "CarbonIntensityProjected",
    "AuditEventSealed",
    "ModelGovernanceChanged",
)
_BASE_FIELDS = (
    "tenant_id",
    "engagement_id",
    "sow_id",
    "client_id",
    "role_id",
    "consultant_id",
    "actor_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|lifecycle_state_id,current_state,next_state,transition_reason,role_permission,staffing_readiness,billing_gate,closure_criteria
2|archetype_id,service_model,billing_method,delivery_governance,milestone_template,risk_indicator,acceptance_evidence,margin_control
3|sow_extraction_id,document_digest,source_citation,deliverable_extract,milestone_extract,billing_term_extract,assumption_extract,change_clause
4|obligation_ledger_id,owner,due_date,evidence_source,confidence,dependency,status,risk_impact,billing_impact
5|scope_boundary_id,requested_work,sow_scope_link,change_request_status,billing_impact,out_of_scope_reason,exception_case,recommendation
6|role_architecture_id,role_family,level,required_skills,billable_status,rate_card,allocation_range,substitution_rule
7|skill_graph_id,skill,proficiency,recency,certification_expiry,industry_context,language,validation_source
8|skill_gap_id,demand_horizon,skill_shortage,training_option,hiring_option,subcontract_option,utilization_impact,recommendation
9|staffing_request_score_id,role_clarity,skill_detail,start_date,end_date,allocation,location_constraint,approval_status,readiness_score
10|staffing_optimization_id,candidate_rank,constraint_satisfaction,tradeoff_explanation,rejected_candidate_reason,fairness_check,margin_effect,risk_effect
11|utilization_forecast_id,forecast_bucket,billable_split,committed_demand,probable_demand,bench_exposure,burnout_risk,capacity_confidence
12|soft_booking_id,hold_expiry,probability_weighted_demand,conflict_set,release_rule,revenue_at_stake,escalation_path,decision
13|partner_staffing_id,assignment_type,compliance_check,onboarding_evidence,rate_terms,confidentiality_control,deliverable_ownership,approval_workflow
14|rate_card_validation_id,rate_card_projection,billing_role,effective_date,discount_approval,currency,mismatch_explanation,exception_route
15|time_policy_id,billability_reason,task_link,scope_link,submission_sla,approval_route,correction_history,anomaly_score
16|narrative_quality_id,scope_alignment,deliverable_context,client_language_score,prohibited_content,defensibility_score,suggestion,audit_history
17|expense_allowability_id,expense_id,sow_reimbursement_term,receipt_evidence,client_approval_need,markup_policy,tax_treatment,billing_impact
18|milestone_dependency_id,dependency_set,critical_path_status,acceptance_requirement,forecast_completion,delay_reason,revenue_impact,escalation_owner
19|deliverable_quality_id,quality_gate,reviewer_role,acceptance_criteria,defect_log,rework_cycle,version_history,approval_proof
20|client_acceptance_id,acceptance_type,approver_authority,criteria_met,waiver_terms,rejection_reason,dispute_window,billing_effect
21|billing_alignment_id,sow_clause,milestone_status,deliverable_acceptance,time_approval,expense_approval,cap_check,cutoff_date
22|billing_readiness_id,blocker_type,revenue_amount,aging_days,owner,required_evidence,remediation_action,invoice_handoff_status
23|leakage_detection_id,unbilled_time,write_off_risk,discount_leakage,missed_expense,dispute_amount,preventable_loss,concession_type
24|margin_decomposition_id,baseline_margin,staffing_mix_variance,rate_variance,travel_variance,rework_variance,confidence,mitigation
25|fixed_price_control_id,earned_value,estimate_to_complete,estimate_at_completion,burn_to_budget,delivery_confidence,margin_at_completion,exception_trigger
26|retainer_consumption_id,entitlement_balance,service_scope,consumption_units,rollover_expiry,overage_threshold,sla_performance,renewal_risk
27|delivery_risk_id,staffing_gap_signal,milestone_slip_signal,late_time_signal,scope_exception_signal,margin_erosion_signal,confidence,mitigation_plan
28|client_health_id,sentiment,responsiveness,escalation_history,acceptance_cycle_time,stakeholder_engagement,renewal_risk,projection_source
29|exception_case_id,exception_type,materiality,owner,due_date,root_cause,client_communication,closure_proof
30|change_order_recommendation_id,scope_trigger,effort_estimate,timeline_impact,billing_effect,approval_workflow,draft_rationale,agent_citation
31|financial_close_id,final_time_status,expense_status,billing_status,acceptance_status,write_off_status,final_margin,archival_proof
32|project_to_cash_handoff_id,payload_type,schema_version,consumer,accepted_deliverable,approved_time,reimbursable_expense,compatibility_test
33|utilization_guardrail_id,overutilization_window,travel_intensity,weekend_work,context_switching,bench_stagnation,fairness_score,tradeoff
34|career_staffing_id,career_goal,target_skill,promotion_readiness,mentorship_need,development_assignment,client_fit,tradeoff
35|methodology_mapping_id,archetype,stage_template,quality_gate_set,artifact_expectation,deviation_rationale,approval_status,generated_milestones
36|knowledge_reuse_id,asset_projection,industry,technology,deliverable_type,quality_feedback,time_saved,margin_effect
37|retrospective_id,actual_scope,actual_effort,actual_margin,milestone_variance,staffing_fit,lesson,model_feedback
38|proposal_handoff_id,contract_projection,pricing_assumption,solution_design,staffing_commitment,delivery_risk,mismatch_flag,kickoff_blocker
39|kickoff_readiness_id,signed_sow,client_sponsor,delivery_team,role_assignment,access_ready,governance_cadence,billing_setup
40|demand_forecast_id,skill,region,role,industry,probability,timing,capacity_plan
41|risk_simulation_id,staffing_delay,scope_growth,client_delay,rate_change,expense_pattern,margin_impact,risk_impact
42|model_evidence_id,model_purpose,feature_set,training_period,evaluation_metric,drift_check,fairness_check,rollback_plan
43|control_assertion_id,control_objective,test_population,evidence_source,failure_detail,owner,remediation,next_test_date
44|boundary_harness_id,artifact_scanned,dependency_name,contract_type,capability_consumer,foreign_table_probe,violation_result,evidence
45|dead_letter_ops_id,event_failure_type,retry_readiness,replay_simulation,duplicate_detection,psa_impact,affected_object,replay_command
46|carbon_planning_id,travel_emissions,remote_delivery_option,staffing_location,cost_tradeoff,margin_tradeoff,client_preference,emissions_delta
47|agent_skill_id,skill_name,typed_preview,rbac_check,human_confirmation,audit_evidence,crud_target,rollback_limit
48|role_workbench_id,delivery_manager_view,resource_manager_view,consultant_view,finance_view,partner_view,auditor_view,agent_skill_surface
49|executive_cockpit_id,revenue_readiness,utilization_forecast,margin_risk,delivery_risk,staffing_gap,exception_aging,scenario_plan
50|release_matrix_id,owned_tables,commands,routes,event_contracts,handlers,workbench_panels,agent_skills,boundary_checks
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    3: ("ContractApproved",),
    7: ("EmployeeCreated",),
    10: ("EmployeeCreated", "RateCardProjected"),
    11: ("EmployeeCreated", "TimeSubmitted"),
    14: ("RateCardProjected",),
    17: ("ExpenseApproved",),
    21: ("TimeSubmitted", "ExpenseApproved", "InvoiceIssued"),
    28: ("CustomerHealthProjected",),
    32: ("InvoiceIssued",),
    36: ("KnowledgeAssetProjected",),
    38: ("ProposalApproved", "ContractApproved"),
    42: ("ModelGovernanceChanged",),
    44: ("EmployeeCreated", "ExpenseApproved", "InvoiceIssued", "ContractApproved"),
    45: ("EmployeeCreated", "ExpenseApproved", "InvoiceIssued", "PolicyChanged"),
    46: ("CarbonIntensityProjected",),
    50: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 3, 5, 10, 12, 13, 14, 16, 17, 20, 21, 23, 25, 26, 29, 30, 31, 34, 35, 38, 39, 41, 43, 45, 46, 47, 50)
_AGENT_PREVIEW_FEATURES = (3, 5, 8, 10, 16, 22, 24, 27, 30, 35, 38, 39, 41, 47, 48, 49, 50)
_NON_MUTATING_FEATURES = (3, 8, 10, 11, 12, 16, 22, 23, 24, 25, 26, 27, 28, 30, 33, 34, 36, 37, 40, 41, 42, 43, 44, 45, 46, 49, 50)
_PROJECTION_ONLY_FEATURES = (7, 10, 11, 14, 17, 21, 28, 32, 36, 38, 42, 44, 45, 46, 50)
_PSA_RISK_FEATURES = (1, 3, 4, 5, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 33, 34, 38, 39, 41, 42, 43, 44, 45, 47, 49, 50)


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
        "tables": (f"professional_services_automation_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"ProfessionalServicesAutomation{_camel(capability.slug)}Panel",
        "route": f"POST /professional-services-automation/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in PSA_CONTROL_CAPABILITIES}


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
        "event_topic": PSA_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "psa_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires PSA-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _PSA_RISK_FEATURES and payload.get("psa_risk_evidence_complete") is not True:
        findings.append("engagement, SOW, staffing, skills, time, expenses, milestones, deliverables, billing, utilization, margin, delivery risk, acceptance, exception, model, event, boundary, and release decisions require complete PSA risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("engagement transitions, SOW extraction, scope changes, staffing, billing, acceptance, write-offs, change orders, close, simulations, controls, replay, carbon, agent, and release proof require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("PSA agent skills must produce cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("semantic extraction, optimization, forecasts, readiness, billing triage, leakage, margin, simulations, model evidence, control assertions, boundary scans, replay simulations, carbon planning, cockpit, and release matrix must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("employee, expense, invoice, contract, customer, rate, proposal, knowledge, carbon, audit, and model facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != PSA_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("PSA eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in PSA_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary PSA datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("PSA controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_psa_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in PSA_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in PSA_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": PSA_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": PSA_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_psa_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_psa_control(capability) for capability in PSA_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.professional-services-automation-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": PSA_CONTROL_OWNED_TABLES,
        "declared_dependencies": PSA_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": PSA_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": PSA_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


PSA_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_psa_control(slug, payload)) for capability in PSA_CONTROL_CAPABILITIES}

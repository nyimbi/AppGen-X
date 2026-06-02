"""Executable improve1 controls for the Revenue Recognition PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    REVENUE_RECOGNITION_ALLOWED_DATABASE_BACKENDS,
    REVENUE_RECOGNITION_CONSUMED_EVENT_TYPES,
    REVENUE_RECOGNITION_OWNED_TABLES,
    REVENUE_RECOGNITION_REQUIRED_EVENT_TOPIC,
    REVENUE_RECOGNITION_RUNTIME_TABLES,
)

PBC_KEY = "revenue_recognition"
EVENT_CONTRACT = "AppGen-X"
REVENUE_ALLOWED_DATABASE_BACKENDS = REVENUE_RECOGNITION_ALLOWED_DATABASE_BACKENDS
REVENUE_REQUIRED_EVENT_TOPIC = REVENUE_RECOGNITION_REQUIRED_EVENT_TOPIC
REVENUE_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in REVENUE_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in REVENUE_CAPABILITIES}
REVENUE_OWNED_TABLES = tuple(
    dict.fromkeys(
        REVENUE_RECOGNITION_OWNED_TABLES
        + REVENUE_RECOGNITION_RUNTIME_TABLES
        + tuple(f"revenue_recognition_{capability.slug}_control" for capability in REVENUE_CAPABILITIES)
    )
)
REVENUE_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        REVENUE_RECOGNITION_CONSUMED_EVENT_TYPES
        + (
            "OrderCompleted",
            "SubscriptionActivated",
            "InvoiceIssued",
            "InvoiceCorrected",
            "PaymentCaptured",
            "PaymentFailed",
            "CustomerCreditRiskChanged",
            "ContractApproved",
            "ContractAmended",
            "PolicyChanged",
            "UsageMeasured",
            "DeliveryAccepted",
            "FulfillmentCompleted",
            "TaxClassificationChanged",
            "CurrencyRatePublished",
            "AuditEventSealed",
            "CloseCalendarChanged",
            "DisclosureRequirementChanged",
            "DocumentExtracted",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "entity_id",
    "contract_id",
    "customer_projection_id",
    "policy_version",
    "accounting_standard",
    "effective_period",
    "evidence_references",
)
_FIELD_ROWS = """
1|intake_gate_id,customer_identity_status,commercial_substance_result,collectability_indicator,required_attachment_set,cancellation_term_summary,readiness_decision
2|line_normalization_id,line_category,source_projection,quantity_basis,service_period,price_component_set,unresolved_exception_state
3|obligation_workbench_id,candidate_obligation_group,distinctness_rationale,bundle_relationship,series_treatment,policy_citation,reviewer_approval
4|semantic_extraction_id,source_document_hash,extracted_promise,acceptance_clause,termination_right,uncertainty_score,human_confirmation_state
5|material_right_id,option_value,exercise_probability,ssp_evidence_reference,customer_economics,allocation_impact,schedule_implication
6|ssp_registry_id,product_scope,region_scope,currency_code,effective_interval,ssp_method,evidence_confidence
7|ssp_estimation_id,estimation_method,assumption_set,data_set_reference,outlier_policy,confidence_interval,approval_evidence
8|transaction_price_component_id,component_type,probability_weight,constraint_status,timing_basis,tax_exclusion_flag,allocation_treatment
9|variable_estimate_version_id,estimate_method,input_snapshot,probability_distribution,constraint_assessment,update_trigger,true_up_policy
10|reversal_risk_id,risk_driver,score_threshold,refund_right_indicator,acceptance_uncertainty,history_volatility,required_action
11|allocation_trace_id,total_contract_price,exclusion_amount,ssp_weight,discount_assignment,rounding_policy,allocated_amount
12|discount_rebate_control_id,allocation_basis,specific_obligation_scope,rebate_cap,portfolio_treatment,alternative_policy_simulation,approval_state
13|satisfaction_pattern_id,pattern_type,progress_measure,service_period_basis,acceptance_event_required,usage_input_required,schedule_generation_method
14|satisfaction_event_gate_id,source_event_id,delivery_or_usage_evidence,customer_acceptance_state,quantity_satisfied,event_date,idempotency_key
15|usage_evidence_id,measurement_source,billing_period,usage_type,estimate_actual_status,cutoff_policy,correction_event_reference
16|subscription_activation_control_id,activation_event_id,entitlement_period,plan_version,term_alignment,cancellation_rights,projection_freshness
17|invoice_reconciliation_id,invoice_line_projection,contract_line_reference,tax_exclusion_check,over_under_billing_amount,deferral_match_state,mismatch_resolution
18|collectability_signal_id,payment_projection_id,aging_bucket,dispute_state,failed_payment_pattern,credit_hold_state,exception_trigger
19|schedule_generation_id,obligation_reference,recognition_method,period_calendar,allocation_trace_reference,hold_state,deferral_link
20|schedule_version_id,recalculation_reason,affected_periods,cumulative_catchup_amount,prospective_treatment,reviewer_reference,reversal_schedule_link
21|recognition_entry_control_id,open_period_check,approved_schedule_line,materiality_check,duplicate_entry_key,entry_hash,posting_batch
22|deferral_lifecycle_id,source_invoice_reference,liability_classification,release_schedule,balance_rollforward,recognition_link,reconciliation_state
23|modification_classifier_id,added_distinct_goods,price_change_assessment,remaining_obligation_state,termination_rights,effective_date,classification_rationale
24|modification_simulation_id,scenario_type,prospective_result,retrospective_result,cumulative_catchup_result,disclosure_impact,policy_warning
25|contract_combination_id,related_contract_set,negotiated_package_evidence,cross_discount_indicator,dependent_obligation_set,candidate_flag,reviewer_disposition
26|portfolio_expedient_id,portfolio_grouping_rule,homogeneity_check,materiality_test,sample_validation_result,reassessment_frequency,tolerance_result
27|hold_workbench_id,hold_type,trigger_source,owner_user,affected_schedule_set,release_criteria,aging_days
28|adjustment_trueup_id,adjustment_type,source_period_treatment,materiality_assessment,entry_reversal_link,disclosure_effect,preview_financial_impact
29|close_readiness_id,close_period,unapproved_contract_count,missing_ssp_count,open_hold_count,unposted_entry_count,signoff_evidence
30|continuous_close_monitor_id,daily_control_run,new_contract_risk,activation_event_risk,invoice_mismatch_trend,predicted_blocker,remediation_link
31|disclosure_packet_id,packet_version,remaining_obligation_summary,judgment_disclosure,contract_balance_rollforward,reviewer_signoff,supporting_proof
32|exception_case_id,exception_type,severity,owner_sla,financial_exposure,evidence_checklist,closure_criteria
33|policy_version_id,effective_date_scope,compiled_rule_hash,migration_guidance,test_fixture_set,approver_set,supersession_link
34|policy_impact_analysis_id,policy_change_id,affected_obligation_count,revenue_impact_amount,recalculation_requirement,disclosure_change,approval_decision
35|anomaly_detection_id,anomaly_type,schedule_amount_signal,entry_timing_signal,estimate_swing_signal,invoice_mismatch_signal,exception_route
36|predictive_risk_score_id,evidence_completeness_score,variable_consideration_score,modification_history_score,hold_exposure_score,driver_explanation,remediation_recommendation
37|currency_control_id,contract_currency,functional_currency,reporting_currency,rate_source,rate_date,remeasurement_policy
38|non_revenue_exclusion_id,source_line_reference,legal_basis,tax_fee_type,refundable_status,allocation_exclusion_state,policy_approval
39|contract_balance_rollforward_id,period_key,beginning_balance,billings_amount,recognized_amount,adjustments_amount,ending_balance
40|recognition_proof_id,hash_chain_position,redacted_payload_fingerprint,source_event_hash,schedule_version_hash,policy_version_hash,verifier_export
41|event_reliability_id,event_type,schema_version,idempotency_key,ordering_assumption,retry_envelope,dead_letter_taxonomy
42|boundary_proof_id,external_dependency,api_projection_name,cached_field_set,staleness_rule,retention_rule,shared_table_scan_result
43|agent_contract_review_id,document_digest,cited_source_span,candidate_obligation_set,variable_term_flag,risk_flag,human_approval_state
44|agent_close_remediation_id,close_failure_group,root_cause_cluster,remediation_plan,financial_impact_preview,evidence_request_draft,service_command_preview
45|workbench_drilldown_id,dashboard_metric,contract_portfolio_path,obligation_map_path,schedule_calendar_path,audit_proof_path,permission_scope
46|ui_surface_proof_id,capability_surface,form_reference,wizard_reference,control_reference,agent_tool_reference,coverage_result
47|control_test_library_id,control_name,owner_role,frequency,latest_result,remediation_evidence,continuous_assertion
48|resilience_drill_id,drill_type,recovery_time_target,financial_exposure_estimate,data_loss_estimate,corrective_action,replay_result
49|readiness_score_id,contract_completeness_score,obligation_approval_score,ssp_evidence_score,event_health_score,agent_safety_score,blocker_link
50|release_proof_id,intake_to_disclosure_trace,document_intake_result,allocation_result,schedule_result,recognition_entry_result,close_disclosure_result
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("ContractApproved", "DocumentExtracted"),
    2: ("OrderCompleted", "InvoiceIssued"),
    4: ("DocumentExtracted",),
    14: ("DeliveryAccepted", "FulfillmentCompleted"),
    15: ("UsageMeasured",),
    16: ("SubscriptionActivated",),
    17: ("InvoiceIssued", "InvoiceCorrected"),
    18: ("PaymentCaptured", "PaymentFailed", "CustomerCreditRiskChanged"),
    23: ("ContractAmended",),
    33: ("PolicyChanged",),
    34: ("PolicyChanged",),
    37: ("CurrencyRatePublished",),
    38: ("TaxClassificationChanged",),
    40: ("AuditEventSealed",),
    41: ("OrderCompleted", "SubscriptionActivated", "InvoiceIssued", "PaymentCaptured", "PolicyChanged"),
    42: ("OrderCompleted", "SubscriptionActivated", "InvoiceIssued", "PaymentCaptured", "ContractApproved", "PolicyChanged"),
    48: ("InvoiceIssued", "SubscriptionActivated", "PolicyChanged"),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 3, 4, 5, 7, 10, 12, 14, 23, 24, 25, 27, 28, 29, 31, 33, 34, 43, 44, 48, 50)
_APPROVAL_REQUIRED_FEATURES = (1, 3, 5, 7, 10, 12, 21, 23, 24, 27, 28, 31, 33, 34, 38, 43, 44, 48, 50)
_AGENT_PREVIEW_FEATURES = (1, 4, 24, 29, 30, 35, 36, 43, 44, 49, 50)
_NON_MUTATING_FEATURES = (1, 3, 4, 5, 7, 10, 11, 12, 24, 25, 26, 29, 30, 31, 34, 35, 36, 40, 42, 43, 44, 45, 46, 48, 49, 50)
_FINANCIAL_INTEGRITY_FEATURES = (5, 6, 7, 8, 9, 10, 11, 12, 19, 20, 21, 22, 23, 24, 25, 26, 28, 37, 38, 39, 49, 50)
_CLOSE_DISCLOSURE_FEATURES = (21, 22, 27, 28, 29, 30, 31, 32, 39, 46, 47, 49, 50)
_EVENT_BOUNDARY_FEATURES = (14, 15, 16, 17, 18, 33, 34, 37, 38, 40, 41, 42, 48, 50)
_POLICY_GOVERNANCE_FEATURES = (7, 10, 12, 23, 24, 26, 33, 34, 38, 40, 43, 47, 50)
_PROJECTION_ONLY_FEATURES = (1, 2, 14, 15, 16, 17, 18, 37, 38, 41, 42, 48)


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
        "tables": (f"revenue_recognition_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"RevenueRecognition{_camel(capability.slug)}Panel",
        "route": f"POST /revenue-recognition/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in REVENUE_CAPABILITIES}


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
        "event_topic": REVENUE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "financial_integrity_evidence_complete": True,
        "close_disclosure_evidence_complete": True,
        "event_boundary_evidence_complete": True,
        "policy_governance_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned revenue model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _FINANCIAL_INTEGRITY_FEATURES and payload.get("financial_integrity_evidence_complete") is not True:
        findings.append("SSP, variable consideration, allocation, reversal risk, schedules, entries, deferrals, modifications, currency, exclusions, rollforwards, readiness, and release proof require financial integrity evidence")
    if number in _CLOSE_DISCLOSURE_FEATURES and payload.get("close_disclosure_evidence_complete") is not True:
        findings.append("recognition entries, deferrals, holds, adjustments, close readiness, continuous close, disclosures, exceptions, UI coverage, control testing, readiness score, and end-to-end proof require close disclosure evidence")
    if number in _EVENT_BOUNDARY_FEATURES and payload.get("event_boundary_evidence_complete") is not True:
        findings.append("satisfaction, usage, subscription, invoice, collectability, policy, currency, tax, audit, reliability, boundary, resilience, and release proof require event boundary evidence")
    if number in _POLICY_GOVERNANCE_FEATURES and payload.get("policy_governance_evidence_complete") is not True:
        findings.append("estimation, reversal risk, discount/rebate, modification, portfolio, policy versioning, policy impact, exclusions, proof, agent review, control testing, and release proof require policy governance evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("revenue judgments, obligation extraction, material rights, estimates, reversal holds, modifications, close signoff, disclosures, policies, agent recommendations, resilience drills, and release proof require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk revenue actions require separated approval for intake, obligations, SSP estimates, reversal risk, allocation exceptions, postings, modifications, holds, adjustments, disclosures, policy migrations, exclusions, agent CRUD, resilience drills, and release gates")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("revenue assistant skills must cite evidence, preview financial impact, prepare service commands only, and remain approval-gated before CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("intake plans, obligation workbench, document extraction, material rights, SSP estimation, risk scoring, allocation proofs, simulations, close dashboards, disclosures, anomaly/risk models, audit proofs, boundary proofs, agent plans, UI proofs, resilience drills, readiness scores, and release gates must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("orders, subscriptions, invoices, payments, contracts, policies, tax, currency, audit, and document context must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != REVENUE_REQUIRED_EVENT_TOPIC:
        findings.append("revenue recognition eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in REVENUE_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary revenue datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("revenue recognition controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_revenue_recognition_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in REVENUE_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in REVENUE_DECLARED_DEPENDENCIES)
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
        "required_event_topic": REVENUE_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": REVENUE_ALLOWED_DATABASE_BACKENDS,
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


def improve1_revenue_recognition_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_revenue_recognition_control(capability) for capability in REVENUE_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.revenue-recognition-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": REVENUE_OWNED_TABLES,
        "declared_dependencies": REVENUE_DECLARED_DEPENDENCIES,
        "allowed_database_backends": REVENUE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": REVENUE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


REVENUE_RECOGNITION_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_revenue_recognition_control(slug, payload))
    for capability in REVENUE_CAPABILITIES
}

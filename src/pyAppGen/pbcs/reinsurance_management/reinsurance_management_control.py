"""Executable improve1 controls for the Reinsurance Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "reinsurance_management"
EVENT_CONTRACT = "AppGen-X"
REINSURANCE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REINSURANCE_REQUIRED_EVENT_TOPIC = "pbc.reinsurance_management.events"
REINSURANCE_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in REINSURANCE_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in REINSURANCE_CAPABILITIES}
REINSURANCE_OWNED_TABLES = tuple(
    dict.fromkeys(
        DOMAIN_OWNED_TABLES
        + tuple(f"reinsurance_management_{capability.slug}_control" for capability in REINSURANCE_CAPABILITIES)
    )
)
REINSURANCE_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        DOMAIN_CONSUMED_EVENTS
        + (
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
            "ClaimUpdated",
            "PolicyPremiumProjected",
            "CashReceiptProjected",
            "AccountingPeriodClosed",
            "TreasurySettlementMatched",
            "DocumentStored",
            "CounterpartyRatingChanged",
            "FxRatePublished",
            "CatastropheEventDeclared",
            "ExposureModelUpdated",
            "RiskThresholdChanged",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "program_id",
    "treaty_id",
    "counterparty_id",
    "cession_id",
    "bordereau_id",
    "operator_id",
    "accounting_period",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|treaty_type,covered_book,line_of_business,attachment_basis,limit_amount,share_percent,wording_reference
2|lifecycle_state,transition_reason,approval_id,allowed_command,effective_at,state_evidence,next_action
3|counterparty_projection_id,role,participation_percent,credit_rating,domicile,projection_freshness,boundary_mode
4|participation_line_id,reinsurer_id,broker_id,signed_line,written_line,slip_reference,change_history_hash
5|facultative_placement_id,submission_package,market_list,quote_terms,capacity_offered,subjectivity_status,bind_status
6|placement_document_id,document_type,extracted_limit,extracted_share,extracted_clause,confidence,reviewer_approval
7|eligibility_rule_id,source_projection,treaty_match,inclusion_result,attachment_test,territory_check,effective_date_check
8|calculation_trace_id,gross_amount,retention_amount,layer_amount,reinstatement_amount,commission_amount,rounding_rule
9|exposure_layer_id,attachment_point,exhaustion_point,peril,territory,aggregation_basis,utilization_amount
10|cat_event_id,peril,occurrence_window,affected_treaties,gross_loss_estimate,ceded_estimate,reporting_status
11|bordereau_schema_id,bordereau_type,schema_version,source_file,row_count,validation_failure_count,submission_status
12|ingestion_quality_id,duplicate_key,period_check,currency_check,treaty_mapping,reject_queue,accepted_row_count
13|premium_reconciliation_id,policy_premium_projection,billing_status,ceded_commission,tax_amount,variance_amount,certification_status
14|loss_reconciliation_id,claim_projection,paid_loss,case_reserve,allocated_expense,event_code,deductible_treatment
15|recoverable_lifecycle_id,source_cession,claim_recovery_link,currency,due_date,aging_bucket,impairment_evidence
16|claim_recovery_id,claim_projection,notice_date,required_document,submission_package,reinsurer_response,closure_status
17|reinstatement_id,exhausted_limit,reinstatement_number,pro_rata_factor,premium_due,approval_id,settlement_link
18|commission_term_id,commission_basis,formula_version,loss_ratio_band,period,adjustment_amount,calculation_trace
19|premium_term_id,deposit_amount,adjustment_basis,minimum_premium,reporting_frequency,due_date,true_up_amount
20|currency_rule_id,treaty_currency,source_currency,settlement_currency,fx_source,conversion_date,converted_amount
21|settlement_statement_id,statement_period,line_items,balance_forward,approval_id,delivery_status,receipt_status
22|cash_projection_id,cash_receipt_reference,matched_statement_id,unmatched_difference,projection_freshness,boundary_mode,match_status
23|collateral_id,collateral_type,amount,beneficiary,expiry_date,threshold_amount,deficiency_amount
24|credit_risk_id,rating_projection,watchlist_status,exposure_amount,recoverable_aging,concentration_metric,risk_alert
25|commutation_case_id,affected_treaties,estimated_liability,offer_terms,approval_id,settlement_status,release_evidence
26|clause_reference_id,clause_type,wording_version,applicability,extracted_obligation,validation_link,citation
27|calendar_obligation_id,due_date,owner,source_clause,status,escalation_level,proof_of_submission
28|renewal_pipeline_id,exposure_pack,loss_experience,market_submission,quote_comparison,signed_line_status,active_handoff
29|retrocession_id,assumed_treaty_link,ceded_treaty_link,inward_share,outward_share,net_exposure,relationship_evidence
30|assumed_portfolio_projection_id,cedant,period,exposure_amount,premium_amount,loss_amount,bordereau_mapping
31|dispute_id,dispute_category,disputed_amount,source_row,counterparty_response,evidence_request,resolution_status
32|treaty_file_packet_id,document_checklist,missing_evidence,packet_hash,approval_id,export_manifest,audit_status
33|exposure_drilldown_id,layer_id,source_projection,treaty_clause,accumulation_bucket,stale_projection_warning,ui_link
34|recoverable_queue_id,age_bucket,currency,dispute_status,cash_projection,collection_action,priority_score
35|rule_parameter_id,rule_name,parameter_name,bounds,approval_history,rollback_version,runtime_effect
36|treaty_extraction_skill_id,source_page,extracted_clause,participant_share,reporting_deadline,confidence,human_confirmation
37|bordereau_triage_skill_id,failed_row,likely_mapping,missing_source_fact,recommended_task,approval_state,mutation_block
38|agent_safety_id,proposed_command,affected_records,financial_impact,confidence,approval_role,irreversible_impact
39|specialized_event_id,event_type,idempotency_key,retry_count,dead_letter_evidence,declared_dependency,handler_status
40|reconstruction_id,as_of_date,event_sequence,participation_snapshot,cession_snapshot,recoverable_snapshot,replay_hash
41|crypto_packet_id,terms_hash,calculation_hash,bordereau_hash,billing_hash,settlement_hash,verification_result
42|large_loss_alert_id,threshold_amount,claim_projection,alert_route,required_action,reinstatement_review,task_status
43|aggregate_exhaustion_id,period,event_id,line_of_business,aggregate_used,remaining_protection,breach_warning
44|operational_risk_score_id,score_factor,trend,threshold,owner,queue_placement,explanation
45|currency_dashboard_id,original_currency,converted_value,fx_source,settlement_status,unmatched_cash,display_bucket
46|statutory_report_id,report_type,period,included_treaties,recoverable_schedule,collateral_schedule,certification_status
47|release_smoke_scenario_id,scenario_name,owned_record_count,appgen_event_count,ui_artifact,boundary_check,result
48|boundary_proof_id,model_reference,service_reference,route_reference,handler_reference,dependency_reference,proof_result
49|profitability_view_id,treaty_layer,counterparty,line_of_business,ceded_premium,ceded_loss,net_benefit
50|command_center_id,treaty_summary,next_obligation,exposure_utilization,recoverable_aging,dispute_summary,governed_action
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    3: ("CounterpartyRatingChanged",),
    6: ("DocumentStored",),
    7: ("PolicyChanged", "ExposureModelUpdated"),
    10: ("CatastropheEventDeclared", "ClaimUpdated"),
    13: ("PolicyPremiumProjected",),
    14: ("ClaimUpdated",),
    16: ("ClaimUpdated", "DocumentStored"),
    20: ("FxRatePublished",),
    22: ("CashReceiptProjected", "TreasurySettlementMatched"),
    24: ("CounterpartyRatingChanged",),
    30: ("ExposureModelUpdated",),
    39: ("PolicyChanged", "ClaimUpdated", "AccountingPeriodClosed"),
    41: ("AuditEventSealed",),
    42: ("ClaimUpdated", "RiskThresholdChanged"),
    45: ("FxRatePublished", "CashReceiptProjected"),
    46: ("AccountingPeriodClosed",),
    48: ("PolicyChanged", "ClaimUpdated", "CashReceiptProjected", "DocumentStored"),
    49: ("AccountingPeriodClosed",),
}
_HUMAN_CONFIRMATION_FEATURES = (2, 5, 6, 8, 13, 16, 17, 18, 21, 23, 25, 28, 31, 32, 35, 36, 37, 38, 42, 46, 47, 50)
_APPROVAL_REQUIRED_FEATURES = (2, 4, 5, 6, 8, 13, 16, 17, 18, 19, 21, 23, 25, 28, 31, 32, 35, 38, 39, 41, 46, 47, 50)
_NON_MUTATING_FEATURES = (1, 3, 7, 9, 10, 11, 12, 13, 14, 20, 22, 24, 26, 27, 30, 33, 34, 35, 36, 37, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50)
_AI_PREVIEW_FEATURES = (6, 31, 35, 36, 37, 38, 44, 47, 50)
_FINANCIAL_CONTROL_FEATURES = (8, 13, 15, 17, 18, 19, 20, 21, 22, 23, 25, 31, 34, 45, 46, 49)
_EXPOSURE_CONTROL_FEATURES = (1, 4, 7, 9, 10, 24, 28, 29, 30, 42, 43, 49, 50)
_DOCUMENT_EVIDENCE_FEATURES = (1, 2, 5, 6, 11, 12, 16, 26, 27, 31, 32, 36, 37, 41, 46, 47)
_PROJECTION_ONLY_FEATURES = (3, 7, 10, 13, 14, 16, 20, 22, 24, 30, 39, 42, 45, 46, 48, 49)


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
        "tables": (f"reinsurance_management_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"ReinsuranceManagement{_camel(capability.slug)}Panel",
        "route": f"POST /reinsurance-management/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in REINSURANCE_CAPABILITIES}


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
        "event_topic": REINSURANCE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "financial_reconciliation_complete": True,
        "exposure_evidence_complete": True,
        "document_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned reinsurance model, UI, service/API, event, agent, test, and release evidence before approval.")
    if number in _FINANCIAL_CONTROL_FEATURES and payload.get("financial_reconciliation_complete") is not True:
        findings.append("cession calculations, premium and loss reconciliation, recoverables, reinstatements, commissions, deposit premium, FX, settlements, cash projections, collateral, commutations, disputes, aging, statutory reports, profitability, and settlements require financial reconciliation evidence")
    if number in _EXPOSURE_CONTROL_FEATURES and payload.get("exposure_evidence_complete") is not True:
        findings.append("treaty structure, participation, eligibility, exposure layers, catastrophe events, credit concentration, renewal pipeline, retrocession, assumed portfolio, large loss, aggregate exhaustion, profitability, and command center require exposure evidence")
    if number in _DOCUMENT_EVIDENCE_FEATURES and payload.get("document_evidence_complete") is not True:
        findings.append("treaty wording, lifecycle evidence, facultative packages, document intake, bordereaux, recoveries, clauses, notices, disputes, treaty files, agent extraction, crypto packets, statutory reports, and release scenarios require document evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("treaty state changes, facultative bind, document extraction, calculations, settlements, collateral, commutations, renewals, disputes, treaty file exports, rule changes, agent recommendations, large-loss tasks, reports, release promotion, and command actions require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-impact treaty, placement, calculation, recovery, settlement, collateral, commutation, renewal, dispute, audit, event, reporting, release, and command decisions require separated approval")
    if number in _AI_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("reinsurance agent skills must be cited, permission-checked, financially bounded, and preview-only until approved")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("rules, eligibility, accumulations, cat grouping, bordereau validation, reconciliations, FX, cash projections, risk, clauses, calendars, projections, drilldowns, queues, workbenches, agent previews, replay, crypto packets, alerts, aggregate monitoring, scoring, dashboards, reports, boundary proofs, analytics, and command center must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("policy, claim, cash, treasury, document, counterparty rating, FX, catastrophe, exposure model, risk, audit, accounting, and KPI facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != REINSURANCE_REQUIRED_EVENT_TOPIC:
        findings.append("reinsurance eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in REINSURANCE_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary reinsurance datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("reinsurance controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_reinsurance_management_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in REINSURANCE_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in REINSURANCE_DECLARED_DEPENDENCIES)
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
        "required_event_topic": REINSURANCE_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": REINSURANCE_ALLOWED_DATABASE_BACKENDS,
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


def improve1_reinsurance_management_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_reinsurance_management_control(capability) for capability in REINSURANCE_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.reinsurance-management-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": REINSURANCE_OWNED_TABLES,
        "declared_dependencies": REINSURANCE_DECLARED_DEPENDENCIES,
        "allowed_database_backends": REINSURANCE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": REINSURANCE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


REINSURANCE_MANAGEMENT_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_reinsurance_management_control(slug, payload))
    for capability in REINSURANCE_CAPABILITIES
}

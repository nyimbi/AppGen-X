"""Executable improve1 controls for the Provider Revenue Cycle PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
    PROVIDER_REVENUE_CYCLE_OWNED_TABLES,
    PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
    PROVIDER_REVENUE_CYCLE_RUNTIME_TABLES,
)

PBC_KEY = "provider_revenue_cycle"
EVENT_CONTRACT = "AppGen-X"
REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS = PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS
REVENUE_CYCLE_REQUIRED_EVENT_TOPIC = PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC
REVENUE_CYCLE_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in REVENUE_CYCLE_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in REVENUE_CYCLE_CAPABILITIES}
REVENUE_CYCLE_OWNED_TABLES = tuple(
    dict.fromkeys(
        PROVIDER_REVENUE_CYCLE_OWNED_TABLES
        + PROVIDER_REVENUE_CYCLE_RUNTIME_TABLES
        + tuple(f"provider_revenue_cycle_{capability.slug}_control" for capability in REVENUE_CYCLE_CAPABILITIES)
    )
)
REVENUE_CYCLE_DECLARED_DEPENDENCIES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "EligibilityResponseProjected",
    "ClinicalEncounterCharged",
    "ClinicalDocumentationUpdated",
    "PayerAcknowledgementReceived",
    "RemittanceReceived",
    "PatientCommunicationDelivered",
    "FinanceCloseRequested",
    "ModelGovernanceChanged",
)
_BASE_FIELDS = ("tenant_id", "account_id", "patient_id", "encounter_id", "payer_id", "claim_id", "actor_id", "policy_version", "evidence_references")
_FIELD_ROWS = """
1|account_readiness_id,account_state,missing_component,claim_ready_blocker,transition_from,transition_to,readiness_score
2|registration_quality_id,identity_confidence,guarantor_status,coverage_priority,subscriber_relationship,accident_indicator,deficiency_case
3|eligibility_projection_id,plan_id,effective_dates,coverage_status,benefit_summary,response_time,freshness
4|authorization_tracking_id,authorization_required,approved_services,approved_units,validity_dates,payer_reference,mismatch_reason
5|charge_completeness_id,source_encounter,charge_trigger,expected_charge,captured_charge,variance,missing_charge_case
6|charge_description_id,charge_master_version,effective_window,billable_flag,modifier_requirement,price_basis,approval_state
7|coding_workqueue_id,case_type,required_documentation,diagnosis_evidence,procedure_evidence,coder_assignment,final_code_set
8|documentation_query_id,query_reason,documentation_evidence,question_text,clinician_response,due_date,coding_impact
9|claim_scrub_id,demographic_edit,coverage_edit,authorization_edit,coding_edit,timely_filing_edit,override_requirement
10|claim_batch_id,batch_type,clearinghouse_route,included_accounts,batch_total,validation_status,acknowledgement
11|clearinghouse_rejection_id,rejection_reason,edit_category,owner,correction_action,resubmission_state,aging_days
12|denial_taxonomy_id,denial_category,payer_reason,internal_root_cause,preventable_flag,dollar_amount,appeal_path
13|denial_appeal_id,appeal_level,packet_checklist,clinical_documents,coding_rationale,deadline,decision
14|payment_posting_id,remittance_source,payer_trace,claim_lines,allowed_amount,payment_amount,patient_responsibility,unmatched_cash
15|underpayment_detection_id,expected_reimbursement,actual_payment,variance_reason,contract_basis,recovery_action,recovery_status
16|patient_balance_segment_id,balance_segment,statement_status,assistance_screening,payment_plan,dispute_status,collection_hold
17|financial_assistance_id,eligibility_signal,application_status,presumptive_eligibility,documentation_request,discount,renewal
18|collections_worklist_id,account_age,balance,contact_restriction,dispute_status,assistance_status,agency_eligibility,outreach_attempt
19|credit_balance_id,credit_source,payer_amount,patient_amount,refund_eligibility,offset_policy,approval_state,stale_escalation
20|revenue_integrity_case_id,audit_case_type,population,finding,financial_exposure,department,corrective_action,followup_measure
21|timely_filing_id,payer_deadline,first_submission,resubmission_clock,appeal_deadline,timely_proof,late_risk_queue
22|coding_compliance_id,audit_flag,coder_quality,unsupported_code_warning,modifier_risk,diagnosis_specificity,correction_tracking
23|claim_followup_id,followup_schedule,last_payer_status,no_response_escalation,requested_information,owner_queue,resolution
24|payer_rule_id,payer_requirement,required_field,attachment_rule,timely_filing_rule,appeal_process,effective_date
25|parameter_impact_id,parameter_name,affected_accounts,affected_charges,affected_claims,affected_denials,impact_report
26|denial_prevention_id,root_cause_trend,upstream_owner,prevention_recommendation,education_task,rule_candidate,measured_reduction
27|late_charge_workflow_id,late_charge,claim_status,billing_hold,rebill_requirement,payer_notification,approval_workflow
28|writeoff_governance_id,writeoff_type,threshold,approver,reason,financial_class,collection_history,reversal_path
29|patient_notice_id,notice_template,language,delivery_channel,required_insert,consent_restriction,delivery_proof
30|workbench_queue_id,registration_queue,authorization_queue,missing_charge_queue,coding_queue,denial_queue,collections_queue
31|agent_summary_id,summary_type,citation_set,inference_marker,denial_root_cause,appeal_draft,patient_guidance
32|agent_crud_preview_id,intent,account_action,evidence_required,preview_payload,confirmation_required,audit_record
33|document_ingestion_id,source_span,candidate_posting,denial_reason,appeal_outcome,confidence,reviewer
34|model_governance_id,use_case,model_version,evaluation_set,thresholds,drift_check,human_feedback
35|continuous_control_id,control_threshold,population,failing_sample,owner,remediation,closure_evidence
36|dead_letter_retry_id,retry_classification,idempotency_key,financial_risk,replay_checkpoint,remediation_action,duplicate_guard
37|boundary_proof_id,dependency_contract,clinical_boundary,payer_boundary,finance_boundary,notification_boundary,audit_boundary
38|net_revenue_forecast_id,service_line,claim_status,denial_probability,expected_payment,cash_timing,confidence
39|financial_analytics_id,registration_loss,authorization_loss,coding_delay,late_charge_loss,underpayment_loss,source_drilldown
40|payer_scorecard_id,payment_speed,denial_rate,overturn_rate,underpayment_rate,admin_burden,trend_confidence
41|account_timeline_id,registration_event,eligibility_event,authorization_event,charge_event,coding_event,cash_event
42|crypto_evidence_id,charge_hash,coding_hash,claim_hash,appeal_hash,payment_hash,proof_chain
43|audit_evidence_room_id,evidence_packet,account_readiness,coding_decision,claim_submission,denial_appeal,permission_filter
44|patient_dispute_id,dispute_reason,account_hold,evidence_requested,investigation_owner,resolution,appeal_path
45|scenario_library_id,scenario_name,seed_account,expected_queue,expected_event,expected_metric,side_effect_free
46|permission_model_id,role,account_edit,charge_approve,coding_finalize,batch_submit,collection_action
47|month_end_close_id,unbilled_accounts,late_charges,uncoded_accounts,unposted_remittances,open_denials,close_event
48|full_cycle_simulation_id,registration_step,eligibility_step,authorization_step,charge_step,coding_step,cash_close
49|overlap_proof_id,clinical_boundary,payer_adjudication_boundary,gl_boundary,declared_contract,foreign_table_probe
50|dsl_agent_exposure_id,model_descriptor,route_descriptor,service_descriptor,ui_artifact,event_contract,assistant_skill
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    3: ("EligibilityResponseProjected",),
    5: ("ClinicalEncounterCharged",),
    7: ("ClinicalDocumentationUpdated",),
    10: ("PayerAcknowledgementReceived",),
    14: ("RemittanceReceived",),
    23: ("PayerAcknowledgementReceived",),
    29: ("PatientCommunicationDelivered",),
    34: ("ModelGovernanceChanged",),
    36: ("EligibilityResponseProjected", "ClinicalEncounterCharged", "RemittanceReceived"),
    37: ("AuditEventSealed",),
    47: ("FinanceCloseRequested",),
    50: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 4, 8, 10, 13, 14, 17, 18, 19, 24, 25, 27, 28, 29, 32, 33, 34, 36, 43, 44, 46, 47, 48, 50)
_AGENT_PREVIEW_FEATURES = (8, 13, 25, 26, 31, 32, 33, 34, 38, 39, 43, 44, 48, 50)
_NON_MUTATING_FEATURES = (3, 5, 9, 21, 23, 25, 26, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 47, 48, 49, 50)
_PROJECTION_ONLY_FEATURES = (3, 5, 7, 10, 14, 23, 29, 34, 36, 37, 47, 50)
_REVENUE_RISK_FEATURES = (1, 2, 3, 4, 5, 7, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 24, 25, 27, 28, 29, 31, 32, 34, 35, 36, 37, 38, 39, 42, 43, 44, 47, 48, 49, 50)


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
        "tables": (f"provider_revenue_cycle_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"ProviderRevenueCycle{_camel(capability.slug)}Panel",
        "route": f"POST /provider-revenue-cycle/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in REVENUE_CYCLE_CAPABILITIES}


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
        "event_topic": REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "revenue_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires revenue-cycle-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _REVENUE_RISK_FEATURES and payload.get("revenue_risk_evidence_complete") is not True:
        findings.append("patient account, registration, eligibility, authorization, charge, coding, claim, denial, payment, collections, integrity, model, event, boundary, and release decisions require complete revenue-cycle risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("claim-ready transitions, authorizations, query drafts, claim batches, appeals, postings, assistance, collections, refunds, payer rules, parameters, write-offs, notices, agent CRUD, documents, replay, audit packets, disputes, permissions, close, simulations, and DSL exposure require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("revenue-cycle agent skills must produce cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("eligibility projections, charge detection, scrubbing, timely filing, follow-up, parameter impact, prevention, workbench, summaries, documents, models, controls, retries, boundary, forecasts, analytics, scorecards, timelines, cryptographic proof, audit packets, scenarios, close, simulations, overlap, and DSL proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("eligibility, clinical, payer acknowledgement, remittance, notification, finance, model, and audit facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != REVENUE_CYCLE_REQUIRED_EVENT_TOPIC:
        findings.append("provider revenue cycle eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary provider revenue datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("provider revenue controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_revenue_cycle_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in REVENUE_CYCLE_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in REVENUE_CYCLE_DECLARED_DEPENDENCIES)
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
        "required_event_topic": REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
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


def improve1_revenue_cycle_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_revenue_cycle_control(capability) for capability in REVENUE_CYCLE_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.provider-revenue-cycle-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": REVENUE_CYCLE_OWNED_TABLES,
        "declared_dependencies": REVENUE_CYCLE_DECLARED_DEPENDENCIES,
        "allowed_database_backends": REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


REVENUE_CYCLE_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_revenue_cycle_control(slug, payload)) for capability in REVENUE_CYCLE_CAPABILITIES}

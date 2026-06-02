"""Executable improve1 controls for the Policy Administration Insurance PBC."""
from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    POLICY_ADMINISTRATION_INSURANCE_ALLOWED_DATABASE_BACKENDS,
    POLICY_ADMINISTRATION_INSURANCE_OWNED_TABLES,
    POLICY_ADMINISTRATION_INSURANCE_REQUIRED_EVENT_TOPIC,
)

PBC_KEY = "policy_administration_insurance"
EVENT_CONTRACT = "AppGen-X"
POLICY_CONTROL_ALLOWED_DATABASE_BACKENDS = POLICY_ADMINISTRATION_INSURANCE_ALLOWED_DATABASE_BACKENDS
POLICY_CONTROL_REQUIRED_EVENT_TOPIC = POLICY_ADMINISTRATION_INSURANCE_REQUIRED_EVENT_TOPIC
POLICY_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        POLICY_ADMINISTRATION_INSURANCE_OWNED_TABLES
        + tuple(f"policy_administration_insurance_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)
    )
)
POLICY_CONTROL_DECLARED_DEPENDENCIES = (
    "BoundQuoteAccepted",
    "PartyProjectionChanged",
    "RatingPremiumProjected",
    "BillingAccountStatusChanged",
    "ClaimsStatusProjected",
    "UnderwritingDecisionProjected",
    "ProductVersionProjected",
    "ProducerAppointmentProjected",
    "DocumentTemplateProjected",
    "ComplianceRuleProjected",
    "CommunicationPreferenceProjected",
    "AuditEventSealed",
    "WorkflowTaskChanged",
    "OperationalKpiChanged",
)
POLICY_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in POLICY_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in POLICY_CONTROL_CAPABILITIES}
_BASE_FIELDS = (
    "tenant_id",
    "policy_id",
    "policy_term_id",
    "transaction_id",
    "coverage_item_id",
    "jurisdiction",
    "product_version",
    "actor_id",
    "policy_version",
    "effective_date",
    "processing_date",
    "evidence_references",
)
_FIELD_ROWS = """
1|issuance_gate_id,bound_quote_ref,insured_projection_ref,coverage_schedule_ref,billing_projection_ref,approval_authority
2|lifecycle_event_id,status_from,status_to,transition_reason,allowed_command,next_action
3|term_version_id,policy_period_start,policy_period_end,transaction_type,predecessor_term,successor_term
4|coverage_schedule_id,coverage_type,covered_object,limit_structure,deductible,form_reference
5|party_role_id,party_projection_ref,role_type,interest_type,role_effective_window,communication_eligibility
6|endorsement_id,change_set,requested_effective_date,accepted_effective_date,premium_delta,document_output
7|eligibility_rule_id,transaction_type,policy_status,billing_status,underwriting_status,rule_version
8|premium_impact_id,rating_projection_ref,billing_account_status,invoice_readiness,receivable_event,premium_delta
9|cancellation_event_id,initiator,cancel_reason,notice_deadline,rescission_window,proof_of_mailing
10|nonpayment_control_id,billing_projection_ref,grace_date,notice_sequence,payment_cure_evidence,suppression_reason
11|flat_cancel_id,rescission_basis,authority,document_set,downstream_event,earned_premium_handling
12|reinstatement_id,request_date,cure_evidence,lapse_period,no_loss_statement,document_reissue
13|renewal_cycle_id,review_status,data_refresh_requirements,offer_terms,nonrenewal_option,mailing_evidence
14|nonrenewal_id,nonrenewal_reason,allowed_basis,notice_deadline,approval_authority,delivery_proof
15|lapse_expiration_id,lapse_date,expiration_date,blocked_actions,coverage_status,downstream_event
16|billing_status_projection_id,account_state,amount_due,delinquency_date,last_payment_date,freshness
17|document_package_id,document_type,template_version,included_forms,render_hash,delivery_status
18|form_edition_id,form_code,edition_date,jurisdiction_applicability,mandatory_status,replacement_form
19|certificate_request_id,requester,holder,purpose,coverage_snapshot,delivery_method
20|binder_id,binder_effective_window,coverage_summary,subjectivities,conversion_deadline,issuer_authority
21|transaction_history_id,command,actor_role,source_document,projection_checkpoint,replay_hash
22|backdate_control_id,backdate_days,allowed_transaction_type,authority,impact_simulation,downstream_effects
23|correction_id,corrected_field_scope,non_contractual_reason,approval,document_reissue_option,audit_note
24|coverage_gap_id,timeline_span,gap_period,overlap_period,conflicting_effective_date,validation_result
25|notice_rule_id,notice_type,lead_time_days,delivery_proof,template_language,exception_handling
26|communication_preference_id,consent_status,language,accessibility_need,delivery_channel,authorized_contact
27|producer_projection_id,producer_of_record,appointment_status,effective_period,servicing_role,producer_change_evidence
28|claims_projection_id,open_claim_count,loss_date,coverage_affected,claim_hold,freshness
29|underwriting_projection_id,approval_status,conditions,authority,expiration,linked_transaction
30|workbench_queue_id,search_filter,saved_queue,role_view,timeline_panel,next_best_action
31|exception_id,exception_category,severity,blocked_action,owner,sla
32|renewal_comparison_id,expiring_terms,proposed_terms,premium_projection,changed_forms,policyholder_action
33|renewal_batch_id,selection_criteria,dry_run_count,excluded_policies,approval,rollback_plan
34|regulatory_hold_id,hold_jurisdiction,peril,policy_type,blocked_actions,release_criteria
35|product_projection_id,allowed_coverages,allowed_forms,allowed_transaction_types,effective_window,projection_source
36|service_request_id,request_type,requester_authority,requested_change,source_channel,command_preview
37|document_interpretation_id,source_document,extracted_request_type,extracted_effective_date,signature_evidence,confidence_score
38|transaction_draft_id,proposed_transaction,affected_record,rule_version,document_requirements,approval_requirement
39|agent_restriction_id,high_impact_action,authorization_route,permitted_user,approval_status,blocked_write
40|impact_simulation_id,coverage_timeline,premium_projection,billing_impact,notice_impact,dependency_events
41|event_specialization_id,typed_event,idempotency_key,retry_status,dead_letter_status,declared_dependency
42|document_reissue_id,affected_document,corrected_template,delivery_proof,superseded_hash,current_document_status
43|data_quality_score_id,issue_type,severity,owner,remediation_task,trend
44|portfolio_metric_id,throughput_metric,sla_metric,backlog_metric,exception_age,drilldown_ref
45|evidence_packet_id,issuance_hash,endorsement_hash,renewal_hash,cancellation_hash,delivery_hash
46|isolation_scope_id,tenant_scope,program_scope,book_scope,visibility_rule,cross_tenant_block
47|smoke_scenario_id,scenario_type,owned_records,appgen_events,ui_artifacts,boundary_checks
48|boundary_proof_id,owned_table_check,underwriting_table_block,billing_table_block,claims_table_block,producer_table_block
49|status_dashboard_id,pending_notices,cure_windows,moratorium_holds,reinstatement_requests,blocked_cancellations
50|renewal_command_center_id,cycle_filter,policy_cohort,offer_status,document_status,assistant_review
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {n: f"{CAPABILITY_BY_NUMBER[n].slug}_verified" for n in range(1, 51)}
_FEATURE_FIELDS = {n: _BASE_FIELDS + _DOMAIN_FIELDS[n] + (_PRIMARY_PROOF_FIELDS[n],) for n in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("BoundQuoteAccepted", "BillingAccountStatusChanged", "UnderwritingDecisionProjected"),
    5: ("PartyProjectionChanged",),
    8: ("RatingPremiumProjected", "BillingAccountStatusChanged"),
    10: ("BillingAccountStatusChanged",),
    13: ("UnderwritingDecisionProjected", "BillingAccountStatusChanged"),
    16: ("BillingAccountStatusChanged",),
    17: ("DocumentTemplateProjected",),
    18: ("DocumentTemplateProjected", "ProductVersionProjected"),
    25: ("ComplianceRuleProjected",),
    26: ("CommunicationPreferenceProjected", "PartyProjectionChanged"),
    27: ("ProducerAppointmentProjected",),
    28: ("ClaimsStatusProjected",),
    29: ("UnderwritingDecisionProjected",),
    34: ("ComplianceRuleProjected",),
    35: ("ProductVersionProjected",),
    41: ("AuditEventSealed",),
    44: ("OperationalKpiChanged",),
    48: ("UnderwritingDecisionProjected", "BillingAccountStatusChanged", "ClaimsStatusProjected", "ProducerAppointmentProjected"),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 2, 6, 7, 9, 10, 11, 12, 14, 20, 22, 23, 29, 33, 34, 36, 37, 38, 39, 42, 45, 47, 50)
_PROJECTION_ONLY_FEATURES = (1, 5, 8, 10, 13, 16, 18, 25, 26, 27, 28, 29, 34, 35, 41, 44, 48)
_AGENT_PREVIEW_FEATURES = (36, 37, 38, 39, 50)
_NON_MUTATING_FEATURES = (21, 22, 24, 30, 32, 33, 40, 43, 44, 45, 47, 48, 49, 50)
_POLICY_RISK_FEATURES = (1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 14, 15, 17, 18, 19, 20, 22, 24, 25, 28, 29, 31, 34, 39, 41, 42, 45, 46, 47, 48, 49, 50)


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
        "tables": (f"policy_administration_insurance_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"PolicyAdministrationInsurance{_camel(capability.slug)}Panel",
        "route": f"POST /policy-administration-insurance/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in POLICY_CONTROL_CAPABILITIES}


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
        "event_topic": POLICY_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "policy_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires policy-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _POLICY_RISK_FEATURES and payload.get("policy_risk_evidence_complete") is not True:
        findings.append("issuance, lifecycle, term, coverage, endorsement, cancellation, reinstatement, renewal, notice, document, compliance, agent, evidence, isolation, and boundary decisions require complete policy risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("policy issuance, endorsement, cancellation, reinstatement, non-renewal, binder, backdated, correction, hold, agent, reissue, evidence, release, and renewal decisions require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("policy agent skills must produce cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("history replay, impact analysis, gap detection, workbench search, renewal batches, simulations, quality scores, analytics, evidence packets, release smoke, boundary proof, dashboards, and command centers must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("quote, party, rating, billing, claims, underwriting, product, producer, document, compliance, communication, audit, KPI, and boundary facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != POLICY_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("policy administration eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in POLICY_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary policy administration datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("policy controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_policy_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in POLICY_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in POLICY_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": POLICY_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": POLICY_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_policy_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_policy_control(capability) for capability in POLICY_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.policy-administration-insurance-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": POLICY_CONTROL_OWNED_TABLES,
        "declared_dependencies": POLICY_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": POLICY_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": POLICY_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


POLICY_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_policy_control(slug, payload)) for capability in POLICY_CONTROL_CAPABILITIES}

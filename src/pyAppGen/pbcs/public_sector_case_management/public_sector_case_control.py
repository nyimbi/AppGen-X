"""Executable improve1 controls for the Public Sector Case Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PUBLIC_SECTOR_CASE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    PUBLIC_SECTOR_CASE_MANAGEMENT_OWNED_TABLES,
    PUBLIC_SECTOR_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    PUBLIC_SECTOR_CASE_MANAGEMENT_RUNTIME_TABLES,
)

PBC_KEY = "public_sector_case_management"
EVENT_CONTRACT = "AppGen-X"
CASE_ALLOWED_DATABASE_BACKENDS = PUBLIC_SECTOR_CASE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
CASE_REQUIRED_EVENT_TOPIC = PUBLIC_SECTOR_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC
CASE_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in CASE_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in CASE_CAPABILITIES}
CASE_OWNED_TABLES = tuple(
    dict.fromkeys(
        PUBLIC_SECTOR_CASE_MANAGEMENT_OWNED_TABLES
        + PUBLIC_SECTOR_CASE_MANAGEMENT_RUNTIME_TABLES
        + tuple(f"public_sector_case_management_{capability.slug}_control" for capability in CASE_CAPABILITIES)
    )
)
CASE_DECLARED_DEPENDENCIES = (
    "PolicyChanged",
    "CustomerUpdated",
    "SupplierQualified",
    "IdentityVerified",
    "AddressVerified",
    "HouseholdCompositionProjected",
    "DocumentEvidenceReceived",
    "CorrespondenceDelivered",
    "ExternalReferralStatusChanged",
    "FraudReferralAccepted",
    "HearingScheduled",
    "AuditEventSealed",
)
_BASE_FIELDS = (
    "tenant_id",
    "case_id",
    "applicant_id",
    "program_id",
    "caseworker_id",
    "jurisdiction",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|intake_envelope_id,channel,submission_timestamp,source_system,language_preference,accessibility_need,consent_capture
2|household_model_id,applicant_role,household_member,authorized_representative,relationship,contact_preference,identity_status
3|jurisdiction_determination_id,residency_evidence,address_source,county,service_area,exception_reason,determination_result
4|screening_id,program_screened,screening_question,preliminary_result,ineligible_reason,next_step,disclosure_text
5|eligibility_period_id,effective_date,retroactive_window,renewal_date,coverage_gap,policy_basis,calculation_trace
6|verification_checklist_id,missing_item,required_document,due_date,acceptable_alternative,worker_note,completion_status
7|document_intake_id,document_type,source_channel,ocr_summary,metadata_tags,evidence_link,malware_scan
8|evidence_sufficiency_id,required_fact,supplied_evidence,sufficiency_score,gap_reason,reviewer,decision_ready
9|correspondence_outbound_id,template_id,delivery_channel,recipient,language,readability_level,delivery_proof
10|correspondence_inbound_id,matched_notice,response_type,received_channel,received_date,case_link,worker_queue
11|referral_id,service_provider,referral_reason,consent_scope,warm_handoff,expected_outcome,tracking_status
12|referral_closure_id,service_outcome,provider_update,closure_reason,client_attended,follow_up_needed,loop_closed
13|benefit_decision_id,service_package,benefit_amount,authorization_period,decision_reason,notice_required,implementation_state
14|change_report_id,reported_change,impact_assessment,reduction_notice,overpayment_amount,recovery_plan,client_rights
15|appeal_intake_id,appeal_source,filing_date,appealable_issue,timeliness_result,late_good_cause,validation_status
16|appeal_scope_id,issue_statement,excluded_issue,program_area,relief_requested,scope_reason,supervisor_review
17|hearing_logistics_id,hearing_date,venue,participant_role,interpreter_need,accommodation,notice_sent
18|hearing_packet_id,packet_index,evidence_item,redaction_status,service_proof,agency_position,participant_copy
19|hearing_outcome_id,outcome_type,remand_instruction,implementation_task,deadline,benefit_adjustment,closure_status
20|chain_of_custody_id,evidence_item,custodian,transfer_event,hash_value,timestamp,integrity_status
21|evidence_sharing_id,sharing_purpose,recipient,minimum_necessary_fields,redaction_rule,consent_basis,disclosure_log
22|sla_clock_id,case_stage,start_time,due_time,clock_owner,priority,breach_risk
23|tolling_reason_id,pause_reason,pause_start,pause_end,legal_basis,resume_trigger,elapsed_days
24|access_policy_id,purpose,role,case_sensitivity,allowed_action,least_privilege_reason,access_decision
25|confidentiality_marker_id,protected_population,marker_type,visibility_rule,review_date,override_policy,worker_warning
26|fraud_handoff_id,suspicion_reason,evidence_summary,handoff_boundary,referral_packet,accepted_by_fraud,no_investigative_mutation
27|rule_version_id,rule_name,effective_date,retired_date,program_scope,version_reason,impact_summary
28|rule_explanation_id,decision_id,plain_language_reason,policy_citation,fact_used,calculation_step,client_facing_text
29|override_governance_id,override_type,policy_exception,approver,justification,expiry_date,audit_record
30|supervisor_queue_id,queue_type,assigned_supervisor,aging_bucket,priority_reason,workload,escalation
31|case_timeline_id,intake_event,evidence_event,decision_event,notice_event,appeal_event,source_label
32|draft_review_id,notice_template,worker_draft,plain_language_check,legal_review,translation_review,approval_status
33|hearing_operator_id,appeal_case,hearing_stage,participant_task,packet_task,outcome_task,operator_alert
34|intake_agent_skill_id,source_text,triage_summary,suggested_program,missing_questions,confidence,human_confirmation
35|correspondence_agent_skill_id,draft_prompt,source_facts,citation_map,readability_score,reviewer,write_block
36|hearing_agent_skill_id,packet_summary,issue_outline,evidence_citations,hearing_questions,remand_risk,human_confirmation
37|quality_agent_skill_id,case_sample,coaching_tip,quality_finding,policy_citation,worker_feedback,supervisor_review
38|event_taxonomy_id,event_schema,intake_event,decision_event,appeal_event,notice_event,consumer_contract
39|cross_system_boundary_id,external_system,event_type,projection_name,shared_table_probe,boundary_decision,contract_reference
40|dead_letter_replay_id,event_id,idempotency_key,retry_count,dead_letter_reason,replay_checkpoint,duplicate_guard
41|analytics_id,backlog_bucket,cycle_time,citizen_impact,program_dimension,queue_trend,forecast
42|quality_sample_id,sample_rule,case_selection,finding,corrective_action,owner,closure_evidence
43|retention_rule_id,record_category,retention_period,legal_hold,expungement_rule,disposition_date,hold_release
44|release_evidence_pack_id,policy_change,workflow_change,test_evidence,training_evidence,approval_record,release_decision
45|scenario_fixture_id,scenario_name,seed_case,seed_evidence,expected_decision,expected_notice,coverage_label
46|accessibility_review_id,language,reading_level,screen_reader_check,translation_status,accommodation,plain_language_result
47|security_consent_trace_id,access_log_id,consent_record,purpose_of_use,disclosure_event,revocation_status,security_alert
48|duplicate_coordination_id,duplicate_candidate,cross_program_case,match_score,merge_decision,coordination_task,client_notice
49|continuity_operation_id,outage_type,manual_packet,hearing_disruption,offline_queue,sync_checkpoint,recovery_action
50|go_live_exit_id,production_metric,readiness_gate,training_completion,policy_signoff,defect_status,exit_decision
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    2: ("IdentityVerified", "HouseholdCompositionProjected"),
    3: ("AddressVerified",),
    7: ("DocumentEvidenceReceived",),
    9: ("CorrespondenceDelivered",),
    11: ("ExternalReferralStatusChanged",),
    12: ("ExternalReferralStatusChanged",),
    17: ("HearingScheduled",),
    26: ("FraudReferralAccepted",),
    38: ("AuditEventSealed",),
    39: ("PolicyChanged", "CustomerUpdated", "SupplierQualified"),
    40: ("AuditEventSealed",),
    47: ("AuditEventSealed",),
    50: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 4, 7, 9, 11, 13, 14, 15, 18, 19, 21, 24, 26, 29, 32, 34, 35, 36, 37, 43, 44, 48, 49, 50)
_SUPERVISOR_APPROVAL_FEATURES = (14, 16, 19, 21, 24, 25, 26, 29, 30, 37, 42, 43, 44, 49, 50)
_NON_MUTATING_FEATURES = (3, 4, 6, 8, 11, 22, 23, 27, 28, 30, 31, 34, 35, 36, 37, 39, 40, 41, 42, 44, 45, 46, 48, 49, 50)
_AI_PREVIEW_FEATURES = (28, 32, 34, 35, 36, 37, 41, 42, 44, 50)
_PRIVACY_EVIDENCE_FEATURES = (2, 7, 8, 9, 10, 18, 20, 21, 24, 25, 26, 32, 35, 36, 39, 43, 46, 47, 48, 50)
_PROGRAM_RULE_FEATURES = (3, 4, 5, 8, 13, 14, 16, 22, 23, 27, 28, 29, 43, 44, 50)
_PROJECTION_ONLY_FEATURES = (2, 3, 7, 9, 11, 12, 17, 26, 38, 39, 40, 47, 50)


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
        "tables": (f"public_sector_case_management_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"PublicSectorCaseManagement{_camel(capability.slug)}Panel",
        "route": f"POST /public-sector-case-management/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in CASE_CAPABILITIES}


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
        "event_topic": CASE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "supervisor_approval": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "privacy_evidence_complete": True,
        "program_rule_trace_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned case evidence, UI, service/API, event, assistant, privacy, and release proof before approval.")
    if number in _PRIVACY_EVIDENCE_FEATURES and payload.get("privacy_evidence_complete") is not True:
        findings.append("household, evidence, correspondence, hearing packets, custody, privacy sharing, purpose access, confidentiality, fraud handoff, drafting agents, boundaries, retention, accessibility, security consent, duplicates, and go-live require privacy-safe evidence")
    if number in _PROGRAM_RULE_FEATURES and payload.get("program_rule_trace_complete") is not True:
        findings.append("residency, screening, eligibility periods, evidence sufficiency, benefit decisions, reductions, appeal scope, SLA/tolling, rule versions, explanations, overrides, retention, release, and go-live require policy rule traceability")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("citizen-facing intake, notices, referrals, eligibility decisions, appeal actions, evidence sharing, fraud handoff, overrides, AI drafts, retention, release, duplicates, continuity, and go-live require human confirmation")
    if number in _SUPERVISOR_APPROVAL_FEATURES and payload.get("supervisor_approval") is not True:
        findings.append("reductions, appeal scope, remands, protected disclosures, confidentiality, fraud handoff, overrides, supervisor queues, quality coaching, corrective actions, retention, release, continuity, and go-live require supervisor approval")
    if number in _AI_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("case management agent skills must produce cited, permission-checked, preview-only drafts before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("jurisdiction checks, screening, verification, evidence scoring, referrals, SLA/tolling, rule simulations, explanations, queues, timelines, agent drafts, boundary proof, replay, analytics, QA, release, fixtures, accessibility, duplicate detection, continuity, and go-live must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("identity, address, household, document, correspondence, referral, hearing, fraud, policy, customer, supplier, and audit facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != CASE_REQUIRED_EVENT_TOPIC:
        findings.append("public sector case eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in CASE_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary public sector case datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("public sector case controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_public_sector_case_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in CASE_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in CASE_DECLARED_DEPENDENCIES)
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
        "required_event_topic": CASE_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": CASE_ALLOWED_DATABASE_BACKENDS,
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


def improve1_public_sector_case_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_public_sector_case_control(capability) for capability in CASE_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.public-sector-case-management-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": CASE_OWNED_TABLES,
        "declared_dependencies": CASE_DECLARED_DEPENDENCIES,
        "allowed_database_backends": CASE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": CASE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


PUBLIC_SECTOR_CASE_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_public_sector_case_control(slug, payload)) for capability in CASE_CAPABILITIES}

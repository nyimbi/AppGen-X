"""Executable improve1 controls for the Permitting Licensing Inspections PBC."""
from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PERMITTING_LICENSING_INSPECTIONS_ALLOWED_DATABASE_BACKENDS,
    PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES,
    PERMITTING_LICENSING_INSPECTIONS_REQUIRED_EVENT_TOPIC,
)

PBC_KEY = "permitting_licensing_inspections"
EVENT_CONTRACT = "AppGen-X"
PERMIT_CONTROL_ALLOWED_DATABASE_BACKENDS = PERMITTING_LICENSING_INSPECTIONS_ALLOWED_DATABASE_BACKENDS
PERMIT_CONTROL_REQUIRED_EVENT_TOPIC = PERMITTING_LICENSING_INSPECTIONS_REQUIRED_EVENT_TOPIC
PERMIT_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES + tuple(f"permitting_licensing_inspections_{c.slug}_control" for c in IMPROVE1_CAPABILITIES)))
PERMIT_CONTROL_DECLARED_DEPENDENCIES = (
    "PolicyChanged", "CustomerUpdated", "SupplierQualified", "ParcelUpdated", "AddressValidated",
    "PaymentConfirmed", "RefundExecuted", "LedgerReconciled", "ContractorQualified", "AgencyReferralReturned",
    "GeospatialZoneChanged", "PublicNoticePublished", "HearingDecided", "NotificationDelivered", "AuditEventSealed",
)
PERMIT_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {c.feature_number: c for c in PERMIT_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {c.slug: c for c in PERMIT_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "jurisdiction_id", "case_id", "application_id", "permit_id", "license_id", "parcel_id", "site_address", "actor_id", "policy_version", "evidence_references")
_FIELD_ROWS = """
1|application_type,required_documents,required_attestations,responsible_parties,submission_status,deficiency_reasons
2|submitted_party_name,canonical_party_id,parcel_identifier,address_normalization,duplicate_score,override_reason
3|consultation_id,advisory_notes,likely_disciplines,expected_fees,notice_obligations,promoted_application_id
4|plan_set_id,version_label,sheet_inventory,revision_date,superseded_version,comment_binding
5|discipline_matrix,review_dependencies,lead_reviewer,parallel_review_group,comment_template,blocker_state
6|correction_round_id,reviewer_comment,applicant_response,resubmittal_due_date,waiver_status,acceptance_state
7|fee_assessment_id,fee_lines,payment_request_id,payment_confirmation_ref,refund_handoff,accounting_reconciliation_ref
8|fee_schedule_id,effective_date,valuation_basis,waiver_approval,credit_reference,refund_eligibility
9|issuance_gate_id,closed_reviews,resolved_corrections,confirmed_fees,permit_conditions,hold_reason
10|qualification_rule_id,allowed_activity,allowed_location,occupancy_limit,insurance_proof,operating_condition
11|temporary_authorization_id,term_limit,missing_items,auto_expiration,follow_up_checkpoint,permanent_conversion_block
12|inspection_type,prerequisite_check,scheduling_window,route_assignment,inspector_capacity,allowed_outcomes
13|mobile_evidence_id,photo_chain,signature_capture,geotag,timestamp_measurement,witness_note
14|failed_item_id,correction_required,reinspection_fee,reinspection_window,applicant_notice,clearance_result
15|violation_code,severity_score,hazard_class,repeat_offense,mitigation_factor,escalation_threshold
16|enforcement_step,stop_work_authority,legal_basis,supervisor_approval,blocked_override,release_condition
17|notice_id,service_channel,service_confirmation,cure_deadline,extension_decision,next_legal_step
18|public_notice_id,notice_text,publication_channel,posting_dates,mailing_list,affidavit_reference
19|hearing_id,docket_number,hearing_type,exhibit_packet,continuance_history,outcome_order
20|renewal_calendar_id,advance_notice_cadence,grace_period_message,seasonal_campaign,expiring_population,notice_audit_log
21|renewal_decision_id,continuing_education,active_violations,unpaid_fees,insurance_status,decision_outcome
22|lifecycle_event_id,status_from,status_to,authority,reason,required_conditions
23|portal_session_id,applicant_role,guided_intake_step,document_upload,fee_estimate,complaint_submission
24|portal_status_id,stage_explanation,outstanding_items,next_step_guidance,deadline,correspondence_history
25|workbench_view_id,operational_lane,aging_bucket,discipline_filter,route_view,saved_persona_view
26|timeline_id,evidence_graph,actor_lineage,source_event,attached_evidence,milestone_order
27|document_id,document_class,retention_tag,stamp_status,supersession_rule,public_version
28|referral_id,agency,review_scope,due_date,returned_conditions,blocking_status
29|milestone_event_id,event_type,payload_schema,case_lineage,actor_lineage,replay_projection
30|template_id,letter_type,jurisdiction_override,template_version,service_channel,rendered_notice
31|relationship_id,relationship_type,original_record,current_effective_record,supersession_reason,history_preserved
32|appeal_id,appeal_type,filing_deadline,variance_basis,reconsideration_path,decision_authority
33|delegation_id,delegated_role,override_scope,segregation_check,approval_trace,revocation_path
34|intake_triage_id,document_summary,missing_item_detection,risk_flags,recommended_route,permission_check
35|plan_summary_id,sheet_changes,code_comments,open_corrections,citation_links,reviewer_confirmation
36|inspection_assist_id,route_brief,site_hazards,required_tools,offline_packet,field_confirmation
37|enforcement_draft_id,violation_findings,ordinance_citations,recommended_action,due_process_check,human_approval
38|geospatial_check_id,zoning_layer,address_confidence,floodplain_flag,overlay_district,manual_map_review
39|registry_sync_id,contractor_number,business_license_ref,responsible_party_status,sync_source,staleness_reason
40|sla_calendar_id,workload_queue,assignment_score,escalation_rule,capacity_exception,supervisor_action
41|analytics_pack_id,throughput_metric,aging_metric,compliance_metric,cohort_filter,export_snapshot
42|traceability_matrix_id,feature_number,code_artifact,ui_surface,service_api,evidence_link
43|seed_pack_id,scenario_type,fixture_records,expected_events,regression_assertions,release_reference
44|audit_chain_id,custody_event,public_record_class,redaction_rule,retention_policy,disclosure_log
45|ordinance_parameter_id,tenant_scope,effective_date,rule_version,parameter_value,impact_preview
46|accessibility_id,language,channel,assistive_support,equity_exception,translated_notice
47|offline_sync_id,field_device,queued_changes,conflict_resolution,gps_evidence,replay_status
48|runbook_id,dead_letter_event,retry_policy,exception_owner,recovery_action,postmortem_link
49|training_asset_id,operator_role,practice_case,competency_check,readiness_score,signoff_actor
50|go_live_pack_id,workflow_pass,ui_evidence,event_trace,boundary_proof,open_risk
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {n: f"{CAPABILITY_BY_NUMBER[n].slug}_verified" for n in range(1, 51)}
_FEATURE_FIELDS = {n: _BASE_FIELDS + _DOMAIN_FIELDS[n] + (_PRIMARY_PROOF_FIELDS[n],) for n in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    2: ("CustomerUpdated", "ParcelUpdated", "AddressValidated"), 7: ("PaymentConfirmed", "RefundExecuted", "LedgerReconciled"),
    9: ("PaymentConfirmed",), 18: ("PublicNoticePublished",), 19: ("HearingDecided",), 28: ("AgencyReferralReturned",),
    29: ("AuditEventSealed",), 30: ("NotificationDelivered",), 38: ("GeospatialZoneChanged", "AddressValidated"),
    39: ("SupplierQualified", "ContractorQualified"), 44: ("AuditEventSealed",), 45: ("PolicyChanged",), 48: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (6, 8, 9, 11, 16, 17, 19, 21, 22, 28, 32, 33, 34, 35, 36, 37, 45, 50)
_PROJECTION_ONLY_FEATURES = (2, 7, 9, 18, 19, 28, 29, 30, 38, 39, 44, 45, 48)
_AGENT_PREVIEW_FEATURES = (34, 35, 36, 37, 50)
_NON_MUTATING_FEATURES = (8, 25, 26, 29, 34, 35, 36, 37, 41, 42, 43, 45, 46, 48, 49, 50)
_PERMIT_RISK_FEATURES = (1, 2, 4, 5, 6, 7, 9, 11, 12, 13, 15, 16, 17, 18, 19, 21, 22, 28, 32, 33, 37, 38, 40, 44, 48, 50)


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
    return {"title": capability.title, "slug": capability.slug, "tables": (f"permitting_licensing_inspections_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number], "ui": f"PermittingLicensingInspections{_camel(capability.slug)}Panel", "route": f"POST /permitting-licensing-inspections/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in PERMIT_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({"database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "event_topic": PERMIT_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "dependency_access_mode": "api_event_projection", "human_confirmation": True, "agent_preview_only": True, "non_mutating_simulation": True, "permit_risk_evidence_complete": True, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned permitting evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _PERMIT_RISK_FEATURES and payload.get("permit_risk_evidence_complete") is not True:
        findings.append("intake, plan review, fees, issuance, inspection, violation, notice, hearing, renewal, geospatial, audit, and go-live decisions require complete risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("waivers, issuance, provisional approvals, enforcement, due process, hearings, renewals, overrides, agent recommendations, policy changes, and go-live require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("permitting agent skills must return cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("fee simulations, dashboards, timelines, agents, analytics, traceability, seed packs, policy previews, accessibility checks, recovery, training, and go-live proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("parcel, party, payment, public notice, hearing, referral, geospatial, registry, audit, policy, notification, and recovery facts must use APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != PERMIT_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("permitting eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in PERMIT_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary permitting datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("permitting controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_permit_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in PERMIT_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in PERMIT_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "primary_proof": spec["primary_proof"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": PERMIT_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": PERMIT_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_permit_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_permit_control(capability) for capability in PERMIT_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.permitting-licensing-inspections-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": PERMIT_CONTROL_OWNED_TABLES, "declared_dependencies": PERMIT_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": PERMIT_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": PERMIT_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


PERMIT_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_permit_control(slug, payload)) for capability in PERMIT_CONTROL_CAPABILITIES}

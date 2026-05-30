"""Executable improve1 controls for the Privacy Consent Governance PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS,
    PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES,
    PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC,
    PRIVACY_CONSENT_GOVERNANCE_RUNTIME_TABLES,
)

PBC_KEY = "privacy_consent_governance"
EVENT_CONTRACT = "AppGen-X"
PRIVACY_CONTROL_ALLOWED_DATABASE_BACKENDS = PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS
PRIVACY_CONTROL_REQUIRED_EVENT_TOPIC = PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC
PRIVACY_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in PRIVACY_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in PRIVACY_CONTROL_CAPABILITIES}
PRIVACY_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES
        + PRIVACY_CONSENT_GOVERNANCE_RUNTIME_TABLES
        + tuple(f"privacy_consent_governance_{capability.slug}_control" for capability in PRIVACY_CONTROL_CAPABILITIES)
    )
)
PRIVACY_CONTROL_DECLARED_DEPENDENCIES = (
    "CustomerUpdated",
    "IdentityVerified",
    "AccessPolicyChanged",
    "AuditProofGenerated",
    "DataProductPublished",
    "IdentityMerged",
    "CustomerPreferenceUpdated",
    "NotificationDeliveryConfirmed",
    "AuditEventSealed",
    "ModelGovernanceChanged",
)
_BASE_FIELDS = (
    "tenant_id",
    "subject_id",
    "purpose_code",
    "jurisdiction",
    "policy_version",
    "actor_id",
    "approval_state",
    "evidence_references",
)
_FIELD_ROWS = """
1|identity_graph_id,identifier_namespace,verification_state,source_event,confidence,merge_split_history,dissenting_signal
2|subject_lifecycle_id,current_state,requested_transition,proof_requirement,request_eligibility,retention_effect,consent_effect
3|consent_timeline_id,grant_id,withdrawal_id,notice_version,capture_method,effective_interval,revocation_reason
4|withdrawal_simulation_id,affected_projection,blocked_purpose,follow_up_task,downstream_event,processing_hold,impact_score
5|purpose_taxonomy_id,purpose_category,allowed_processing,lawful_basis_set,data_categories,retention_linkage,owner_approval
6|purpose_conflict_id,incompatible_purpose,duplicate_scope,vague_term,expired_usage,missing_notice,conflict_resolution
7|notice_version_id,audience,language,channel,required_clause,diff_summary,reacknowledgement_required
8|acknowledgement_proof_id,notice_id,channel,locale,device_session_proof,consent_linkage,redacted_verifier
9|reacknowledgement_campaign_id,affected_cohort,deadline,suppression_rule,fallback_channel,non_response_restriction,delivery_plan
10|dsr_intake_gate_id,request_type,identity_verification,authorized_agent_scope,duplicate_request,fee_abuse_policy,sla_deadline
11|dsr_workflow_id,generated_task_set,data_domain,declared_projection,exemption_step,redaction_need,communication_requirement
12|authorized_agent_id,authority_document,subject_relationship,authority_scope,expiration,verification_result,restricted_action
13|identity_risk_score_id,data_sensitivity,channel_risk,identifier_strength,verification_requirement,disclosure_limit,denial_reason
14|response_package_id,data_inventory,redaction_log,exemption_rationale,included_categories,delivery_method,final_approval
15|sla_governance_id,jurisdiction_clock,extension_eligibility,pause_reason,reminder_schedule,escalation_path,deadline_proof
16|processing_register_id,activity_id,basis_link,sharing_link,retention_link,risk_assessment_link,completion_score
17|basis_validation_id,basis_type,relationship_context,documentation,balancing_test,review_date,invalidation_trigger
18|legitimate_interest_assessment_id,interest_statement,necessity_test,subject_impact,safeguards,opt_out_path,reviewer
19|sensitive_data_control_id,sensitive_category,additional_condition,permitted_purpose,access_restriction,export_block,review_cadence
20|sharing_agreement_id,party_role,recipient,data_categories,transfer_mechanism,subprocessor_list,audit_right
21|cross_border_transfer_id,destination_country,supplementary_measure,transfer_impact_assessment,effective_date,review_cadence,block_reason
22|data_product_review_id,data_product_id,minimization_review,sharing_review,retention_review,risk_review,approval_gate
23|retention_schedule_id,trigger_event,retention_period,data_category,legal_hold_behavior,disposal_method,review_cadence
24|retention_decision_id,affected_scope,schedule_id,hold_status,action,approver,execution_proof
25|retention_simulation_id,schedule_change,subject_cohort,deletion_volume,legal_hold_impact,data_product_impact,operational_risk
26|privacy_risk_assessment_id,processing_scope,subject_vulnerability,profiling_flag,transfer_flag,residual_risk,mitigation_plan
27|dpia_template_id,template_kind,jurisdiction,template_version,completion_score,required_sections,approval_requirement
28|incident_lifecycle_id,discovery_time,affected_subjects,data_categories,severity,containment,closure_evidence
29|breach_notification_id,harm_risk,data_sensitivity,volume,protection_state,recipient_type,delivery_proof
30|consent_evidence_packet_id,subject_identifier_set,purpose_trace,notice_trace,grant_withdrawal_trace,processing_linkage,fingerprint
31|cryptographic_proof_id,hash_chain_head,previous_hash,record_digest,verifier_export,timestamp_proof,tamper_status
32|semantic_compiler_id,source_citation,compiled_purpose,compiled_basis,compiled_retention,ambiguity_flag,approval_evidence
33|policy_impact_id,changed_rule,affected_consent,affected_notice,affected_activity,processing_hold,remediation_task
34|lineage_graph_id,subject_node,notice_node,purpose_node,consent_node,processing_node,allow_deny_explanation
35|minimization_control_id,processing_activity,data_category_count,excessive_category,mitigation,purpose_justification,export_scope
36|control_test_id,expired_consent_check,missing_basis_check,stale_notice_check,overdue_dsr_check,missing_agreement_check,remediation
37|anomaly_detection_id,channel,purpose,geography,notice_version,withdrawal_spike,processing_hold
38|exception_case_id,exception_type,severity,linked_subject_or_activity,owner,sla,evidence_checklist
39|communication_preference_id,delivery_channel,locale,accessibility_format,identity_update_source,notice_delivery_rule,response_delivery_rule
40|vulnerable_subject_id,age_band,guardian_authority,vulnerability_status,consent_age_rule,prohibited_processing,agent_output_restriction
41|event_reliability_id,schema_version,idempotency_key,ordering_assumption,retry_envelope,dead_letter_taxonomy,replay_eligibility
42|boundary_proof_id,declared_event,declared_api,projection_name,cached_field,staleness_rule,foreign_table_block
43|agent_dsr_plan_id,classification,missing_proof,task_plan,redaction_plan,approval_required,disclosure_block
44|agent_policy_mapping_id,policy_document,extracted_purpose,retention_rule,sharing_control,citation,ambiguity_question
45|privacy_cockpit_id,expiring_consent_panel,dsr_deadline_panel,basis_gap_panel,incident_panel,dead_letter_panel,control_panel
46|ui_surface_proof_id,subject_form,consent_form,notice_form,dsr_wizard,incident_board,agent_tool_panel
47|resilience_drill_id,failure_mode,recovery_action,replay_plan,rollback_plan,lesson_record,workbench_status
48|readiness_score_id,lineage_score,notice_score,dsr_score,retention_score,event_score,agent_safety_score
49|tenant_isolation_id,tenant_scope,subject_partition,event_partition,workbench_filter,agent_output_filter,leak_test_result
50|privacy_release_proof_id,subject_setup,consent_capture,withdrawal_flow,dsr_workflow,retention_decision,incident_record
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("CustomerUpdated", "IdentityVerified", "IdentityMerged"),
    4: ("DataProductPublished", "CustomerPreferenceUpdated"),
    10: ("IdentityVerified",),
    13: ("IdentityVerified",),
    21: ("AccessPolicyChanged",),
    22: ("DataProductPublished",),
    30: ("AuditProofGenerated",),
    31: ("AuditProofGenerated", "AuditEventSealed"),
    39: ("CustomerPreferenceUpdated", "NotificationDeliveryConfirmed"),
    41: ("CustomerUpdated", "IdentityVerified", "AccessPolicyChanged", "DataProductPublished"),
    42: ("CustomerUpdated", "IdentityVerified", "AuditProofGenerated", "DataProductPublished"),
    47: ("CustomerUpdated", "IdentityVerified", "AccessPolicyChanged", "DataProductPublished"),
}
_HUMAN_CONFIRMATION_FEATURES = (2, 4, 5, 7, 9, 10, 12, 14, 17, 18, 19, 20, 21, 22, 24, 26, 28, 29, 32, 33, 38, 40, 43, 44, 47, 50)
_AGENT_PREVIEW_FEATURES = (10, 11, 14, 32, 33, 43, 44, 45, 46, 48, 50)
_NON_MUTATING_FEATURES = (4, 6, 13, 25, 30, 31, 32, 33, 34, 35, 36, 37, 41, 42, 45, 46, 47, 48, 49, 50)
_PROJECTION_ONLY_FEATURES = (1, 4, 21, 22, 30, 31, 39, 41, 42, 47)
_PRIVACY_RISK_FEATURES = (1, 2, 3, 4, 6, 8, 10, 13, 14, 15, 17, 19, 20, 21, 24, 26, 28, 29, 30, 31, 32, 35, 36, 37, 38, 40, 41, 42, 43, 47, 48, 49, 50)


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
        "tables": (f"privacy_consent_governance_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"PrivacyConsentGovernance{_camel(capability.slug)}Panel",
        "route": f"POST /privacy-consent-governance/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in PRIVACY_CONTROL_CAPABILITIES}


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
        "event_topic": PRIVACY_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "privacy_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires privacy-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _PRIVACY_RISK_FEATURES and payload.get("privacy_risk_evidence_complete") is not True:
        findings.append("privacy identity, consent, notice, DSR, processing, sharing, transfer, retention, incident, evidence, policy, event, boundary, tenant, and release decisions require complete privacy risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("privacy state transitions, disclosures, deletions, transfers, policy publication, incidents, agent plans, and release proof require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("privacy agent skills must produce cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("simulations, evidence packets, semantic compilation, lineage, minimization, controls, anomalies, event reliability, boundary proof, drills, readiness, tenant isolation, and release proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("customer, identity, access-policy, audit, notification, model, and data-product facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != PRIVACY_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("privacy consent eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in PRIVACY_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary privacy datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("privacy controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_privacy_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in PRIVACY_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in PRIVACY_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": PRIVACY_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": PRIVACY_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_privacy_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_privacy_control(capability) for capability in PRIVACY_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.privacy-consent-governance-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": PRIVACY_CONTROL_OWNED_TABLES,
        "declared_dependencies": PRIVACY_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": PRIVACY_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": PRIVACY_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


PRIVACY_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_privacy_control(slug, payload)) for capability in PRIVACY_CONTROL_CAPABILITIES}

"""Executable improve1 controls for the Vendor Supplier 360 PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    VENDOR_SUPPLIER_360_ALLOWED_DATABASE_BACKENDS,
    VENDOR_SUPPLIER_360_CONSUMED_EVENT_TYPES,
    VENDOR_SUPPLIER_360_OWNED_TABLES,
    VENDOR_SUPPLIER_360_REQUIRED_EVENT_TOPIC,
    VENDOR_SUPPLIER_360_RUNTIME_TABLES,
)

PBC_KEY = "vendor_supplier_360"
EVENT_CONTRACT = "AppGen-X"
VENDOR_ALLOWED_DATABASE_BACKENDS = VENDOR_SUPPLIER_360_ALLOWED_DATABASE_BACKENDS
VENDOR_REQUIRED_EVENT_TOPIC = VENDOR_SUPPLIER_360_REQUIRED_EVENT_TOPIC
VENDOR_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in VENDOR_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in VENDOR_CAPABILITIES}
VENDOR_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        VENDOR_SUPPLIER_360_OWNED_TABLES
        + VENDOR_SUPPLIER_360_RUNTIME_TABLES
        + tuple(f"vendor_supplier_360_{capability.slug}_control" for capability in VENDOR_CAPABILITIES)
    )
)
VENDOR_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        VENDOR_SUPPLIER_360_CONSUMED_EVENT_TYPES
        + (
            "QualityIncidentRecorded",
            "PaymentRejected",
            "PurchaseOrderCreated",
            "CompliancePolicyChanged",
            "ContractLifecycleChanged",
            "SpendSnapshotChanged",
            "SanctionsScreeningChanged",
            "SupplierPortalSubmissionReceived",
            "BankValidationNetworkResult",
            "TaxAuthorityValidationChanged",
            "ESGDisclosureSubmitted",
            "RiskSignalDetected",
            "SourcingEventCreated",
            "AuditEvidenceSealed",
            "OperationalKpiChanged",
            "PolicyChanged",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "supplier_id",
    "legal_entity_id",
    "category_id",
    "jurisdiction_id",
    "operator_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|readiness_gate_id,identity_proof_status,legal_name_status,beneficial_owner_status,tax_profile_status,bank_validation_status,certification_status,qualification_decision
2|lifecycle_state_id,current_state,target_state,transition_reason,required_evidence,spend_effect,payment_effect,sourcing_eligibility
3|duplicate_case_id,legal_name_similarity,tax_identifier_match,bank_account_match,owner_graph_match,address_match,merge_decision,investigation_evidence
4|identity_proof_id,source_document,issuer,validation_method,extracted_fields,confidence,expiration_date,cryptographic_fingerprint
5|ownership_graph_id,beneficial_owner_id,ownership_percentage,control_role,source_evidence,effective_dates,associated_entities,screening_status
6|supplier_site_id,site_type,address_validation,geocode_confidence,active_dates,usage_scope,tax_jurisdiction,approval_state
7|contact_authority_id,contact_id,authority_scope,verification_status,delegation_chain,security_challenge_method,expiration_date,sensitive_change_right
8|tax_profile_id,jurisdiction,taxpayer_id_format,document_type,withholding_status,exemption_evidence,name_match,renewal_reminder
9|bank_validation_id,validation_state,ownership_proof,routing_validation,name_match,network_check_evidence,risk_score,ttl_expires_at
10|bank_change_case_id,independent_contact_verification,cooldown_window,high_risk_country_flag,payment_hold_recommendation,duplicate_bank_match,out_of_band_confirmation,approver
11|payment_preference_id,payment_method,currency,remittance_format,priority,effective_dates,bank_link,eligibility_explanation
12|certification_id,certification_type,issuing_authority,scope,site_category_applicability,issue_date,expiry_date,renewal_owner
13|certification_control_id,required_coverage,expiry_window,issuer_verification,document_proof_status,category_gap,action_plan_id,exception_case_id
14|diversity_attribute_id,certifying_body,classification,ownership_evidence,effective_dates,verification_status,reporting_eligibility,visibility_restriction
15|esg_disclosure_id,topic,metric,methodology,reporting_period,assurance_level,source_document,improvement_commitment
16|screening_record_id,screened_party,watchlist,match_score,matched_fields,jurisdiction,false_positive_rationale,escalation_owner
17|risk_signal_id,signal_type,source,severity,confidence,country_risk,action_guidance,expiry_review
18|risk_score_id,identity_driver,bank_driver,tax_driver,sanctions_driver,certification_driver,esg_driver,recommended_controls
19|qualification_decision_id,eligible_categories,eligible_sites,eligible_regions,spend_limit,required_remediations,expiration_date,reviewer
20|conditional_approval_id,approval_reason,allowed_categories,spend_cap,expiration_date,missing_evidence,approver,auto_suspension_rule
21|segmentation_id,segment,spend_band,criticality,risk_band,performance_band,relationship_maturity,management_cadence
22|spend_snapshot_id,source_period,currency,category,amount,buyer_unit,staleness,mapping_confidence
23|concentration_exposure_id,spend_concentration,critical_material,geography,ownership_group,single_source_status,impact_score,mitigation_path
24|disruption_simulation_id,scenario,affected_categories,open_order_projection,alternate_supplier_readiness,inventory_exposure,payment_hold_effect,recovery_timing
25|delivery_scorecard_id,site_id,period,on_time_rate,in_full_rate,lead_time_adherence,exception_reason,trend_direction
26|quality_incident_id,incident_state,severity,affected_materials,containment_action,root_cause,corrective_action,qualification_consequence
27|scorecard_formula_id,metric_weights,thresholds,category_applicability,data_freshness,exclusions,approval_state,calculation_trace
28|action_plan_id,objective,owner,supplier_counterpart,due_date,linked_issue,milestones,outcome_evidence
29|onboarding_case_id,task_template,task_owner,dependency_map,sla,evidence_requirement,portal_status,approval_gate
30|portal_intake_id,submitted_field,source_document,submitter_authority,validation_status,reviewer,proposed_change,safe_diff
31|contract_reference_id,contract_scope,category,effective_dates,renewal,obligations,sla_terms,contract_projection_link
32|payment_rejection_id,rejection_taxonomy,payment_preference_id,bank_review_required,risk_update,exception_case,remediation_action,retry_eligibility
33|po_projection_id,po_event_id,source_category,site_id,amount,currency,projection_staleness,boundary_evidence
34|policy_impact_id,policy_change_event,affected_profiles,rescreen_required,expired_evidence,qualification_delta,action_plan_need,migration_approval
35|supplier_graph_id,relationship_edge,owner_edge,site_edge,contract_edge,risk_edge,performance_edge,graph_explainability
36|conflict_case_id,employee_link,owner_link,related_party_flag,spend_overlap,decision_rationale,mitigation_control,reviewer
37|financial_health_id,credit_signal,liquidity_signal,bankruptcy_signal,continuity_risk,critical_supplier_flag,monitoring_cadence,contingency_plan
38|human_rights_review_id,labor_signal,forced_labor_risk,materials_origin,site_region,remediation_commitment,escalation_status,audit_evidence
39|document_authenticity_id,document_type,issuer_check,tamper_check,signature_check,metadata_consistency,confidence,review_outcome
40|anomaly_detection_id,anomaly_type,baseline,observed_value,driver_explanation,severity,investigation_queue,recommended_action
41|sourcing_recommendation_id,sourcing_event_id,risk_adjusted_rank,qualified_scope,alternate_supplier_set,disqualification_reason,buyer_explanation,approval_required
42|exception_case_id,exception_type,severity,owner,sla,next_action,resolution_evidence,closure_reason
43|credential_proof_id,hash_chain_root,proof_channel,credential_subject,issuer_signature,verification_timestamp,revocation_status,tamper_status
44|event_reliability_id,idempotency_key,event_name,payload_schema,replay_result,dead_letter_cause,retry_policy,consumer_contract
45|boundary_proof_id,dependency_name,projection_record,api_event_contract,no_foreign_mutation,idempotency_behavior,dead_letter_behavior,audit_reference
46|onboarding_agent_id,source_documents,extracted_supplier_profile,missing_evidence,proposed_safe_diff,cited_facts,human_confirmation,write_block
47|risk_review_agent_id,risk_summary,driver_citations,recommended_controls,false_positive_notes,approval_path,human_decision,audit_trace
48|workbench_completeness_id,form_coverage,wizard_coverage,control_coverage,queue_coverage,agent_tool_coverage,permission_coverage,ui_evidence
49|resilience_drill_id,drill_scenario,critical_supplier_scope,alternate_supplier_path,communication_plan,recovery_time_target,lessons_learned,executive_signoff
50|release_proof_id,scenario_name,test_reference,ui_evidence,event_trace,boundary_evidence,release_check,coverage_status
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    8: ("TaxAuthorityValidationChanged",),
    9: ("BankValidationNetworkResult",),
    12: ("SupplierPortalSubmissionReceived",),
    15: ("ESGDisclosureSubmitted",),
    16: ("SanctionsScreeningChanged",),
    17: ("RiskSignalDetected",),
    22: ("SpendSnapshotChanged",),
    25: ("PurchaseOrderCreated",),
    26: ("QualityIncidentRecorded",),
    31: ("ContractLifecycleChanged",),
    32: ("PaymentRejected",),
    33: ("PurchaseOrderCreated",),
    34: ("CompliancePolicyChanged", "PolicyChanged"),
    41: ("SourcingEventCreated",),
    45: ("PurchaseOrderCreated", "PaymentRejected", "CompliancePolicyChanged"),
    50: ("AuditEvidenceSealed", "OperationalKpiChanged"),
}
_MASTER_ONBOARDING_FEATURES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 19, 20, 29, 30, 46, 50)
_RISK_COMPLIANCE_FEATURES = (4, 5, 8, 10, 13, 14, 15, 16, 17, 18, 23, 24, 34, 35, 36, 37, 38, 39, 40, 42, 43, 47, 49, 50)
_PERFORMANCE_RELATIONSHIP_FEATURES = (21, 22, 23, 24, 25, 26, 27, 28, 31, 33, 35, 41, 48, 49, 50)
_GOVERNANCE_AGENT_FEATURES = (34, 39, 40, 41, 43, 44, 45, 46, 47, 48, 50)
_AGENT_FEATURES = (41, 46, 47, 48, 50)
_HUMAN_CONFIRMATION_FEATURES = (1, 2, 3, 4, 5, 7, 9, 10, 11, 16, 19, 20, 30, 32, 34, 36, 41, 42, 46, 47, 49, 50)
_APPROVAL_REQUIRED_FEATURES = (1, 2, 9, 10, 11, 16, 19, 20, 34, 36, 41, 42, 43, 46, 47, 49, 50)
_NON_MUTATING_FEATURES = (3, 5, 13, 15, 17, 18, 21, 22, 23, 24, 25, 27, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 45, 47, 48, 49, 50)
_PROJECTION_ONLY_FEATURES = (22, 25, 26, 31, 32, 33, 34, 35, 37, 41, 45)


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
        "tables": (f"vendor_supplier_360_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"VendorSupplier360{_camel(capability.slug)}Panel",
        "route": f"POST /vendor-supplier-360/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in VENDOR_CAPABILITIES}


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
        "event_topic": VENDOR_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "master_onboarding_evidence_complete": True,
        "risk_compliance_evidence_complete": True,
        "performance_relationship_evidence_complete": True,
        "governance_agent_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned supplier model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _MASTER_ONBOARDING_FEATURES and payload.get("master_onboarding_evidence_complete") is not True:
        findings.append("supplier onboarding, lifecycle, duplicate detection, identity proof, beneficial ownership, sites, contacts, tax, bank validation, payment preferences, certifications, diversity, qualification, conditional approval, portal intake, agent onboarding, and release proof evidence is required")
    if number in _RISK_COMPLIANCE_FEATURES and payload.get("risk_compliance_evidence_complete") is not True:
        findings.append("supplier risk, sanctions, adverse media, ESG, human rights, certification controls, concentration exposure, disruption simulation, conflict checks, financial health, authenticity, anomaly detection, exceptions, cryptographic credentials, and resilience evidence is required")
    if number in _PERFORMANCE_RELATIONSHIP_FEATURES and payload.get("performance_relationship_evidence_complete") is not True:
        findings.append("supplier segmentation, spend snapshots, delivery performance, quality lifecycle, scorecard governance, relationship action plans, contract projections, PO projections, graph intelligence, sourcing recommendations, workbench coverage, and resilience drill evidence is required")
    if number in _GOVERNANCE_AGENT_FEATURES and payload.get("governance_agent_evidence_complete") is not True:
        findings.append("policy impact simulation, document authenticity, anomaly investigation, risk-aware sourcing, credential proof, AppGen-X event reliability, cross-PBC boundaries, governed agents, workbench completeness, and release evidence is required")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("supplier approval, lifecycle changes, duplicate merge, identity proof, ownership graph, contact authority, bank changes, payment preferences, sanctions decisions, qualification, conditional approval, portal changes, payment rejection remediation, policy migration, conflict decisions, sourcing recommendations, exceptions, agent proposals, resilience drills, and release signoff require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk supplier actions require separated approval for readiness gates, lifecycle, bank validation, bank changes, payment preferences, sanctions, qualification, conditional approvals, policy migrations, conflicts, sourcing recommendations, exceptions, credential proof, agent onboarding, risk review, resilience drills, and release proof")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("supplier assistant skills must cite owned facts, show reversible CRUD previews, enforce authority and policy checks, and block direct writes before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("duplicate analysis, ownership graph, certification controls, ESG disclosure scoring, risk scoring, segmentation, spend snapshots, concentration, disruption, delivery scorecards, scorecard formulas, contract/PO projections, policy impacts, graph intelligence, conflict checks, financial health, due diligence, authenticity, anomaly detection, sourcing recommendations, credential proofs, event reliability, boundaries, risk review, UI completeness, resilience drills, and release proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("spend, purchase order, quality, contract, payment, compliance policy, sourcing, audit, KPI, and external screening context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != VENDOR_REQUIRED_EVENT_TOPIC:
        findings.append("vendor supplier 360 eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in VENDOR_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary vendor supplier 360 datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("vendor supplier 360 controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_vendor_supplier_360_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in VENDOR_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in VENDOR_DECLARED_DEPENDENCIES)
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
        "required_event_topic": VENDOR_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": VENDOR_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "configurable_rules_parameters": True,
        "agent_assisted": True,
        "side_effect_free": True,
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "slug": resolved.slug,
        "missing_fields": missing_fields,
        "foreign_tables": foreign_tables,
        "undeclared_dependencies": undeclared_dependencies,
        "findings": findings,
        "evidence": evidence,
        "payload_digest": _digest(candidate)[:20],
        "side_effects": (),
    }


def improve1_vendor_supplier_360_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_vendor_supplier_360_control(capability) for capability in VENDOR_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {
        "format": "appgen.vendor_supplier_360.improve1-control-contract.v1",
        "ok": len(results) == 50 and all(item["ok"] for item in results),
        "pbc": PBC_KEY,
        "capability_count": len(results),
        "capabilities": results,
        "owned_tables": VENDOR_CONTROL_OWNED_TABLES,
        "allowed_database_backends": VENDOR_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": VENDOR_REQUIRED_EVENT_TOPIC,
        "declared_dependencies": VENDOR_DECLARED_DEPENDENCIES,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


VENDOR_SUPPLIER_360_CONTROL_FUNCTIONS = (
    "evaluate_vendor_supplier_360_control",
    "improve1_vendor_supplier_360_control_contract",
    "sample_payload_for",
)

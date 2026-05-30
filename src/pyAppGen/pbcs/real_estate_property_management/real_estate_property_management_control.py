"""Executable improve1 controls for the Real Estate Property Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .standalone import (
    REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES,
    REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES,
    REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_TABLES,
)

PBC_KEY = "real_estate_property_management"
EVENT_CONTRACT = "AppGen-X"
REAL_ESTATE_ALLOWED_DATABASE_BACKENDS = REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
REAL_ESTATE_REQUIRED_EVENT_TOPIC = REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC
REAL_ESTATE_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in REAL_ESTATE_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in REAL_ESTATE_CAPABILITIES}
REAL_ESTATE_OWNED_TABLES = tuple(
    dict.fromkeys(
        REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES
        + REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_TABLES
        + tuple(f"real_estate_property_management_{capability.slug}_control" for capability in REAL_ESTATE_CAPABILITIES)
    )
)
REAL_ESTATE_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES
        + (
            "PolicyChanged",
            "CustomerUpdated",
            "SupplierQualified",
            "VendorQualified",
            "DocumentStored",
            "PaymentReceived",
            "PaymentReversed",
            "IdentityVerified",
            "ResidentCommunicationDelivered",
            "UtilityMeterReadReceived",
            "InsuranceCertificateUpdated",
            "MarketRentIndexChanged",
            "AccountingPeriodClosed",
            "AuditEventSealed",
            "AnomalySignalRaised",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "portfolio_id",
    "property_id",
    "unit_id",
    "lease_id",
    "operator_id",
    "operating_period",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|portfolio_code,owner_entity,management_company,building_code,floor_code,rentable_area_id,reporting_boundary
2|unit_inventory_id,unit_type,bedroom_count,bathroom_count,square_feet,occupancy_status,rent_ready_date
3|completeness_rule_id,required_attribute,jurisdiction,attribute_source,blocking_reason,score,leaseable_decision
4|lease_abstract_id,clause_type,renewal_option,break_clause,notice_window_days,rent_step,source_document_id
5|household_registry_id,party_role,identity_state,move_in_date,move_out_date,communication_preference,privacy_classification
6|rent_roll_snapshot_id,snapshot_date,contracted_rent,concession_amount,arrears_balance,deposit_balance,drill_through_key
7|charge_schedule_id,charge_type,recurrence_rule,proration_formula,source_lease_version,calculated_amount,explanation
8|collections_case_id,aging_bucket,promise_to_pay_state,collector_id,dispute_flag,late_fee_policy,next_action_date
9|deposit_lifecycle_id,trust_account,receipt_reference,interest_rule,holdback_amount,refund_approval_id,dispute_state
10|move_in_packet_id,checklist_template,meter_read_key,key_inventory,appliance_serials,condition_media_id,resident_signature
11|move_out_reconciliation_id,condition_delta,outstanding_rent,utility_balance,damage_charge,forwarding_address,disposition_amount
12|renewal_pipeline_id,renewal_stage,offer_rent,market_guidance,acceptance_probability,expiry_date,future_charge_plan
13|notice_registry_id,notice_type,lead_time_days,service_method,proof_of_service_id,cure_period_days,jurisdiction_basis
14|service_request_id,category,severity,affected_asset,resident_access_constraint,after_hours_flag,triage_decision
15|work_order_id,assignment_type,scheduled_window,labor_estimate,material_estimate,vendor_acceptance,completion_signoff
16|preventive_schedule_id,building_system,cadence,next_due_date,vendor_template,proof_requirement,overdue_state
17|inspection_program_id,inspection_type,checklist_template,failed_item_severity,remediation_requirement,reinspection_date,linked_request_id
18|compliance_obligation_id,license_type,permit_reference,disclosure_required,safety_certificate,posting_rule,obligation_status
19|contractor_qualification_id,vendor_id,insurance_expiry,trade_license,resident_access_approval,property_restriction,eligibility_decision
20|vacancy_turn_id,notice_received_date,move_out_date,make_ready_stage,marketing_ready_date,lease_ready_date,blocker_reason
21|make_ready_budget_id,scope_line,budget_amount,approval_threshold,actual_labor,actual_materials,recoverable_damage_amount
22|utility_responsibility_id,utility_type,meter_id,move_in_read,move_out_read,recovery_rule,pass_through_charge_id
23|payment_exception_id,exception_type,original_payment_id,reversal_amount,unapplied_credit,collector_followup,balance_after
24|concession_control_id,credit_type,reason_code,amount,approval_path,denial_reason,posting_decision
25|lease_amendment_id,effective_date,superseded_term,resident_acknowledgment,rent_impact,notice_impact,deposit_impact
26|occupancy_board_id,unit_status,next_milestone,days_in_status,attached_lease,attached_notice,reconciliation_status
27|ancillary_asset_id,asset_type,assignment_history,billing_rule,renewal_rule,reclaim_action,linked_lease_term
28|detail_ui_id,timeline_section,unit_link,arrears_panel,service_request_panel,inspection_panel,pending_approval_panel
29|assistant_skill_id,skill_namespace,leasing_action,collections_action,maintenance_action,human_confirmation,foreign_mutation_block
30|document_intake_id,document_classification,candidate_target_table,entity_match_confidence,ambiguity_warning,review_screen,extraction_sample
31|domain_event_catalog_id,event_type,appgen_envelope_schema,projection_target,replay_key,consumer_contract,backward_compatibility
32|inbox_playbook_id,idempotency_key,duplicate_policy,dead_letter_reason,retry_action,operator_guidance,closure_reason_code
33|dossier_timeline_id,entity_type,record_milestone,event_reference,redaction_policy,export_token,audit_view
34|owner_statement_id,reporting_period,rent_billed,rent_collected,maintenance_spend,occupancy_rate,lineage_snapshot
35|budget_variance_id,budget_category,budget_amount,actual_amount,variance_threshold,late_adjustment,exception_event_id
36|anomaly_review_id,risk_type,feature_vector,explanation,review_queue,approval_block,false_positive_label
37|tenant_isolation_id,owner_scope,portfolio_scope,visibility_rule,cross_tenant_privilege,projection_filter,isolation_evidence
38|approval_matrix_id,action_type,amount_band,risk_rating,initiator_id,approver_role,segregation_decision
39|conversion_batch_id,source_system,row_number,target_table,mapping_status,error_bucket,opening_balance_reconciliation
40|search_resolution_id,search_term,entity_type,match_score,duplicate_candidate,survivor_rule,merge_review_state
41|release_scenario_id,scenario_type,scenario_artifact,code_path,test_name,domain_outcome,blocking_gate
42|workflow_test_id,workflow_name,stage_name,input_fixture,expected_event,assertion_name,release_evidence_link
43|route_normalization_id,canonical_route,legacy_alias,deprecation_state,advertised_endpoint,compatibility_result,client_impact
44|schema_evolution_id,target_table,new_field,backfill_plan,compatibility_check,projection_replay_state,migration_sequence
45|queue_workbench_id,queue_type,kpi_card,deadline_metric,triage_link,edge_case_bucket,side_effect_free_render
46|mobile_field_flow_id,offline_packet_id,cached_checklist,photo_capture,signature_capture,sync_event_id,upload_status
47|communication_log_id,channel,template_id,delivery_state,response_summary,linked_notice,latest_contact_citation
48|audit_replay_proof_id,hash_chain_root,projection_name,schema_version,replay_result,drift_metric,proof_export
49|governed_recommendation_id,recommendation_type,confidence,explanation_text,approval_capture,accepted_by,rejected_reason
50|go_live_pack_id,readiness_area,readiness_score,blocking_gap,linked_artifact,exit_criterion,promotion_decision
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    5: ("CustomerUpdated", "IdentityVerified"),
    13: ("PolicyChanged", "ResidentCommunicationDelivered"),
    15: ("SupplierQualified", "VendorQualified"),
    19: ("SupplierQualified", "VendorQualified", "InsuranceCertificateUpdated"),
    22: ("UtilityMeterReadReceived",),
    23: ("PaymentReceived", "PaymentReversed"),
    29: ("DocumentStored",),
    30: ("DocumentStored",),
    31: ("AuditEventSealed",),
    32: ("PolicyChanged",),
    34: ("AccountingPeriodClosed",),
    36: ("AnomalySignalRaised",),
    40: ("CustomerUpdated",),
    48: ("AuditEventSealed",),
    49: ("PolicyChanged", "AnomalySignalRaised"),
    50: ("AuditEventSealed", "AccountingPeriodClosed"),
}
_HUMAN_CONFIRMATION_FEATURES = (4, 7, 9, 11, 12, 13, 15, 18, 20, 21, 23, 24, 25, 29, 30, 36, 38, 39, 40, 44, 46, 49, 50)
_APPROVAL_REQUIRED_FEATURES = (3, 9, 11, 13, 19, 21, 23, 24, 25, 34, 35, 36, 38, 39, 44, 48, 49, 50)
_NON_MUTATING_FEATURES = (1, 3, 6, 7, 8, 12, 13, 16, 18, 19, 22, 26, 28, 29, 30, 32, 33, 34, 35, 36, 37, 40, 41, 43, 44, 45, 48, 49, 50)
_AI_RECOMMENDATION_FEATURES = (4, 12, 14, 17, 23, 24, 28, 29, 30, 36, 40, 41, 49, 50)
_FINANCIAL_CONTROL_FEATURES = (6, 7, 8, 9, 11, 21, 23, 24, 34, 35, 38, 48, 50)
_COMPLIANCE_CONTROL_FEATURES = (3, 10, 13, 17, 18, 19, 32, 37, 38, 39, 44, 46, 48, 50)
_FIELD_OPERATIONS_FEATURES = (10, 14, 15, 16, 17, 20, 21, 22, 45, 46, 47)
_PROJECTION_ONLY_FEATURES = (5, 6, 8, 13, 15, 19, 22, 23, 30, 31, 32, 34, 36, 40, 48, 49, 50)


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
        "tables": (f"real_estate_property_management_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"RealEstatePropertyManagement{_camel(capability.slug)}Panel",
        "route": f"POST /real-estate-property-management/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in REAL_ESTATE_CAPABILITIES}


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
        "event_topic": REAL_ESTATE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "financial_reconciliation_complete": True,
        "compliance_evidence_complete": True,
        "field_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned real-estate model, UI, service/API, event, agent, test, and release evidence before approval.")
    if number in _FINANCIAL_CONTROL_FEATURES and payload.get("financial_reconciliation_complete") is not True:
        findings.append("rent roll, charge scheduling, arrears, deposits, move-out disposition, make-ready budget, payment exceptions, concessions, owner statements, budget variance, approval matrix, audit replay, and go-live require financial reconciliation evidence")
    if number in _COMPLIANCE_CONTROL_FEATURES and payload.get("compliance_evidence_complete") is not True:
        findings.append("property completeness, move-in evidence, notices, inspections, compliance obligations, vendor qualification, inbox playbooks, tenant isolation, approvals, conversion, schema evolution, mobile sync, audit replay, and go-live require compliance evidence")
    if number in _FIELD_OPERATIONS_FEATURES and payload.get("field_evidence_complete") is not True:
        findings.append("move-in, service triage, work orders, preventive maintenance, inspections, vacancy turns, make-ready, utilities, queue navigation, mobile field flows, and communication logs require field operations evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("lease abstracts, rent charges, deposits, move-out decisions, renewal offers, statutory notices, vendor dispatch, compliance, vacancy, budgets, payment exceptions, credits, amendments, assistant skills, document intake, anomaly review, approvals, conversion, merge, schema, mobile sync, AI recommendations, and go-live require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("leaseability, deposits, dispositions, statutory notices, vendor eligibility, budgets, payment reversals, credits, amendments, owner reports, variances, anomaly approvals, segregation controls, conversion, schema evolution, audit proofs, AI recommendations, and go-live require separated approval")
    if number in _AI_RECOMMENDATION_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("real estate assistant skills must be cited, permission-checked, explainable, and preview-only until confirmed by property staff")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("analytics, rules, snapshots, schedules, queues, document classification, playbooks, dossiers, statements, variances, anomaly scoring, isolation checks, search, release evidence, routes, schema, workbench, replay, AI, and go-live evidence must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("customer, identity, supplier, vendor, document, payment, utility, insurance, market, accounting, audit, anomaly, and policy facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != REAL_ESTATE_REQUIRED_EVENT_TOPIC:
        findings.append("real estate property management eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in REAL_ESTATE_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary real estate datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("real estate controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_real_estate_property_management_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in REAL_ESTATE_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in REAL_ESTATE_DECLARED_DEPENDENCIES)
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
        "required_event_topic": REAL_ESTATE_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": REAL_ESTATE_ALLOWED_DATABASE_BACKENDS,
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


def improve1_real_estate_property_management_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_real_estate_property_management_control(capability) for capability in REAL_ESTATE_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.real-estate-property-management-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": REAL_ESTATE_OWNED_TABLES,
        "declared_dependencies": REAL_ESTATE_DECLARED_DEPENDENCIES,
        "allowed_database_backends": REAL_ESTATE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": REAL_ESTATE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


REAL_ESTATE_PROPERTY_MANAGEMENT_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_real_estate_property_management_control(slug, payload))
    for capability in REAL_ESTATE_CAPABILITIES
}

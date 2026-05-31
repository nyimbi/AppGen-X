"""Executable improve1 controls for the Tax Administration Public Sector PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    TAX_ADMINISTRATION_PUBLIC_SECTOR_ALLOWED_DATABASE_BACKENDS,
    TAX_ADMINISTRATION_PUBLIC_SECTOR_CONSUMED_EVENT_TYPES,
    TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES,
    TAX_ADMINISTRATION_PUBLIC_SECTOR_REQUIRED_EVENT_TOPIC,
    TAX_ADMINISTRATION_PUBLIC_SECTOR_RUNTIME_TABLES,
)

PBC_KEY = "tax_administration_public_sector"
EVENT_CONTRACT = "AppGen-X"
TAX_ADMIN_ALLOWED_DATABASE_BACKENDS = TAX_ADMINISTRATION_PUBLIC_SECTOR_ALLOWED_DATABASE_BACKENDS
TAX_ADMIN_REQUIRED_EVENT_TOPIC = TAX_ADMINISTRATION_PUBLIC_SECTOR_REQUIRED_EVENT_TOPIC
TAX_ADMIN_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in TAX_ADMIN_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in TAX_ADMIN_CAPABILITIES}
TAX_ADMIN_OWNED_TABLES = tuple(
    dict.fromkeys(
        TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES
        + TAX_ADMINISTRATION_PUBLIC_SECTOR_RUNTIME_TABLES
        + tuple(f"tax_administration_public_sector_{capability.slug}_control" for capability in TAX_ADMIN_CAPABILITIES)
    )
)
TAX_ADMIN_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        TAX_ADMINISTRATION_PUBLIC_SECTOR_CONSUMED_EVENT_TYPES
        + (
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
            "PaymentConfirmed",
            "PaymentReversed",
            "PaymentReconciliationFailed",
            "TreasurySettlementConfirmed",
            "BankAccountVerified",
            "NoticeDeliveryUpdated",
            "ThirdPartyStatementReceived",
            "CourtHearingScheduled",
            "IdentityProofVerified",
            "LegacyBalanceImported",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "jurisdiction_id",
    "taxpayer_account_id",
    "tax_type",
    "tax_period",
    "policy_version",
    "caseworker_id",
    "evidence_references",
)
_FIELD_ROWS = """
1|tin_lifecycle_id,provisional_identifier,final_tin,duplicate_detection,merge_split_operation,successor_liability,effective_dated_contact
2|registration_case_id,legal_form,residency,tax_role,start_date,approval_checkpoint,outcome_code
3|establishment_registration_id,parent_account_id,branch_id,local_jurisdiction,effective_date,closure_reason,obligation_override
4|filing_obligation_id,frequency,due_date,grace_period,threshold_rule,cessation_event,nil_return_flag
5|return_intake_id,channel,period_reference,currency_precision,schedule_total,preparer_detail,attachment_digest
6|return_validation_id,filing_type,overlap_check,nil_eligibility,amendment_reason,superseded_version,statutory_cutoff
7|assessment_engine_id,assessment_type,basis_record,effective_date,statutory_authority,liability_amount,reversal_chain
8|penalty_interest_id,penalty_type,rate_version,calendar_rule,waiver_status,appeal_stay,recalculation_basis
9|statement_projection_id,opening_balance,charge_set,credit_set,payment_set,refund_set,closing_balance
10|payment_boundary_id,payment_reference,receipt_evidence,allocation_instruction,settlement_confirmation,reversal_status,reconciliation_result
11|allocation_control_id,allocation_rule,debt_priority,taxpayer_reference,legal_priority,reallocation_reason,approval_threshold
12|suspense_credit_id,receipt_status,unmatched_reason,aged_queue,identification_action,offset_action,resolution_evidence
13|refund_screening_id,refund_claim,offset_against_debt,risk_score,bank_verification,document_requirement,maker_checker_approval
14|certificate_governance_id,certificate_type,legal_basis,effective_period,limit_amount,expiry,revocation_trigger
15|notice_template_id,notice_type,statutory_clause,policy_version,jurisdiction_clause,approval_state,render_snapshot
16|notice_delivery_id,delivery_channel,delivery_attempt,bounce_status,address_quality,reservice_action,service_evidence
17|audit_selection_id,source_trigger,risk_factor_set,third_party_discrepancy,random_sample_flag,campaign_id,materiality_score
18|audit_workpaper_id,evidence_request,field_visit,interview_note,third_party_confirmation,sample_test,tamper_history_hash
19|audit_outcome_id,finding_id,assessment_adjustment,penalty_trigger,notice_trigger,refund_reconsideration,overturn_reversal
20|objection_intake_id,challenged_decision,date_served,date_received,grounds,requested_relief,stay_effect
21|appeal_lifecycle_id,forum_type,forum_reference,hearing_date,remand_status,settlement_status,decision_implementation
22|collection_strategy_id,debt_age,risk_band,next_action,legal_blocker,override_reason,treatment_stage
23|installment_relief_id,agreement_type,affordability_evidence,installment_schedule,broken_plan_detection,redefault_logic,compromise_decision
24|enforcement_gate_id,service_evidence,debt_certification,appeal_status,approval_threshold,legal_hold,block_reason
25|account_hold_id,hold_type,start_date,end_date,reason,approving_actor,blocked_action
26|discrepancy_case_id,feed_type,third_party_statement,return_comparison,variance,taxpayer_response,resolution_outcome
27|risk_score_id,risk_type,feature_manifest,calibration_report,explanation,feedback_loop,drift_alert
28|debt_treatment_id,materiality,collectability,appeal_posture,asset_indicator,expected_recovery,recommendation_decision
29|event_catalog_id,event_type,schema_version,originating_record,actor_id,producer_contract,consumer_contract
30|idempotency_control_id,business_key,request_identifier,duplicate_command,repeated_event,dead_letter_conflict,no_duplicate_posting
31|exception_taxonomy_id,exception_type,severity,taxpayer_impact,legal_impact,retry_eligibility,remediation_playbook
32|workbench_queue_id,function_role,queue_type,filter_set,bulk_action,error_state,stale_data_indicator
33|account_detail_id,identity_history,registration_set,obligation_calendar,account_statement,linked_cases,role_access
34|policy_owner_ui_id,rule_version,parameter_promotion,impact_preview,rollback_token,approval_state,operational_impact
35|account_assistant_skill_id,taxpayer_summary,overdue_obligation,active_dispute,next_step_draft,citation_set,restricted_action_block
36|intake_assistant_skill_id,document_type,extracted_registration_fact,extracted_return_figure,source_span_citation,confidence,human_confirmation
37|notice_assistant_skill_id,template_reference,period_data,balance_data,due_date,service_channel,human_approval
38|research_assistant_skill_id,chronology,disputed_issue,linked_evidence,prior_decision,deadline_warning,unsupported_claim_block
39|manifest_trace_id,manifest_item,test_reference,scenario_seed,api_contract,event_contract,release_check
40|seed_journey_id,journey_type,record_sequence,event_sequence,ui_snapshot,replay_log,consistency_check
41|tenant_isolation_id,jurisdiction_scope,rule_scope,template_scope,parameter_scope,risk_model_scope,leakage_check
42|privacy_control_id,field_classification,masking_rule,export_approval,retention_clock,legal_hold,assistant_redaction
43|compliance_campaign_id,campaign_type,tax_type_segment,geography_segment,risk_band,reminder_frequency,obligation_history_link
44|api_completeness_id,api_operation,query_contract,correction_command,simulation_endpoint,export_endpoint,versioning_check
45|counterfactual_simulation_id,policy_parameter,baseline_outcome,simulated_outcome,revenue_impact,queue_impact,non_mutation_proof
46|migration_backfill_id,legacy_account,legacy_obligation,legacy_assessment,legacy_payment,variance_explanation,opening_balance
47|operational_metric_id,metric_name,data_lineage,queue_age,breach_rate,threshold,sla_alert
48|accessibility_localization_id,locale,amount_format,date_format,address_format,screen_reader_label,keyboard_flow
49|continuous_control_id,control_assertion,maker_checker_check,stayed_debt_block,refund_threshold,notice_service_check,proof_hash
50|go_live_gate_id,seeded_journey_check,api_contract_check,event_contract_check,ui_check,assistant_check,rollback_drill
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("IdentityProofVerified",),
    8: ("PolicyChanged",),
    10: ("PaymentConfirmed", "PaymentReversed", "PaymentReconciliationFailed"),
    13: ("BankAccountVerified", "TreasurySettlementConfirmed"),
    16: ("NoticeDeliveryUpdated",),
    21: ("CourtHearingScheduled",),
    26: ("ThirdPartyStatementReceived",),
    29: ("PolicyChanged", "AuditEventSealed"),
    40: ("OperationalKpiChanged",),
    46: ("LegacyBalanceImported",),
    49: ("AuditEventSealed",),
    50: ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"),
}
_REGISTRATION_FILING_FEATURES = (1, 2, 3, 4, 5, 6, 14, 40, 41, 43, 46, 50)
_ASSESSMENT_PAYMENT_FEATURES = (7, 8, 9, 10, 11, 12, 13, 27, 28, 45, 47, 50)
_AUDIT_APPEAL_COLLECTION_FEATURES = (17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 31, 32, 33, 50)
_GOVERNANCE_AGENT_FEATURES = (15, 16, 29, 30, 34, 35, 36, 37, 38, 39, 42, 44, 48, 49, 50)
_AGENT_FEATURES = (35, 36, 37, 38, 44, 45, 50)
_HUMAN_CONFIRMATION_FEATURES = (1, 2, 5, 6, 8, 11, 13, 14, 15, 19, 20, 21, 23, 24, 25, 34, 35, 36, 37, 38, 45, 46, 50)
_APPROVAL_REQUIRED_FEATURES = (2, 8, 11, 13, 14, 15, 19, 21, 23, 24, 25, 34, 37, 45, 46, 50)
_NON_MUTATING_FEATURES = (9, 27, 28, 35, 36, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50)
_PROJECTION_ONLY_FEATURES = (10, 13, 16, 21, 26, 43, 46)


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
        "tables": (f"tax_administration_public_sector_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"TaxAdministrationPublicSector{_camel(capability.slug)}Panel",
        "route": f"POST /tax-administration-public-sector/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in TAX_ADMIN_CAPABILITIES}


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
        "event_topic": TAX_ADMIN_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "registration_filing_evidence_complete": True,
        "assessment_payment_evidence_complete": True,
        "audit_appeal_collection_evidence_complete": True,
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
        findings.append(f"{capability.title} requires owned tax administration model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _REGISTRATION_FILING_FEATURES and payload.get("registration_filing_evidence_complete") is not True:
        findings.append("registration and filing evidence is required for taxpayer identity, registration roles, establishments, filing obligations, return intake, validation, certificates, seeded journeys, tenant isolation, outreach, migration, and go-live proof")
    if number in _ASSESSMENT_PAYMENT_FEATURES and payload.get("assessment_payment_evidence_complete") is not True:
        findings.append("assessment, penalty, statement, payment boundary, allocation, suspense, refund, risk, debt treatment, simulation, metrics, and go-live evidence is required")
    if number in _AUDIT_APPEAL_COLLECTION_FEATURES and payload.get("audit_appeal_collection_evidence_complete") is not True:
        findings.append("audit, workpaper, post-audit adjustment, objection, appeal, collection strategy, hardship, enforcement, hold, discrepancy, exception, queue, detail, and go-live evidence is required")
    if number in _GOVERNANCE_AGENT_FEATURES and payload.get("governance_agent_evidence_complete") is not True:
        findings.append("notice governance, delivery proof, event catalog, idempotency, policy UI, assistant skills, traceability, privacy, API completeness, accessibility, continuous controls, and release evidence require governance and agent evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("legally material taxpayer identity, registration, return, penalty, allocation, refund, certificate, notice, audit, objection, appeal, collection, hold, policy, assistant, simulation, migration, and release actions require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk public revenue actions require separated approval for registrations, penalties, allocations, refunds, certificates, notices, audit adjustments, appeals, relief, enforcement, holds, policy changes, notice assistant output, simulations, migration, and go-live")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("tax administration assistant skills must cite owned records, show reversible previews, enforce secrecy controls, and block direct CRUD before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("statements, risk, debt recommendations, assistants, traceability, journeys, isolation, privacy, API snapshots, simulations, migration dry-runs, metrics, accessibility, controls, and release gates must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("payments, banking, delivery, courts, third-party feeds, outreach, and legacy migration context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != TAX_ADMIN_REQUIRED_EVENT_TOPIC:
        findings.append("tax administration eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in TAX_ADMIN_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary tax administration datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("tax administration controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_tax_administration_public_sector_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in TAX_ADMIN_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in TAX_ADMIN_DECLARED_DEPENDENCIES)
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
        "required_event_topic": TAX_ADMIN_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": TAX_ADMIN_ALLOWED_DATABASE_BACKENDS,
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


def improve1_tax_administration_public_sector_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_tax_administration_public_sector_control(capability) for capability in TAX_ADMIN_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {
        "format": "appgen.tax_administration_public_sector.improve1-control-contract.v1",
        "ok": len(results) == 50 and all(item["ok"] for item in results),
        "pbc": PBC_KEY,
        "capability_count": len(results),
        "capabilities": results,
        "owned_tables": TAX_ADMIN_OWNED_TABLES,
        "allowed_database_backends": TAX_ADMIN_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": TAX_ADMIN_REQUIRED_EVENT_TOPIC,
        "declared_dependencies": TAX_ADMIN_DECLARED_DEPENDENCIES,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


TAX_ADMINISTRATION_PUBLIC_SECTOR_CONTROL_FUNCTIONS = (
    "evaluate_tax_administration_public_sector_control",
    "improve1_tax_administration_public_sector_control_contract",
    "sample_payload_for",
)

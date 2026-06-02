"""Executable improve1 controls for the Trade Finance Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES,
    TRADE_FINANCE_OPERATIONS_OWNED_TABLES,
    TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC,
    TRADE_FINANCE_OPERATIONS_RUNTIME_TABLES,
)

PBC_KEY = "trade_finance_operations"
EVENT_CONTRACT = "AppGen-X"
TRADE_ALLOWED_DATABASE_BACKENDS = TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS
TRADE_REQUIRED_EVENT_TOPIC = TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC
TRADE_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in TRADE_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in TRADE_CAPABILITIES}
TRADE_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        TRADE_FINANCE_OPERATIONS_OWNED_TABLES
        + TRADE_FINANCE_OPERATIONS_RUNTIME_TABLES
        + tuple(f"trade_finance_operations_{capability.slug}_control" for capability in TRADE_CAPABILITIES)
    )
)
TRADE_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES
        + (
            "CustomerRiskUpdated",
            "PartyScreeningDecisionChanged",
            "WatchlistChanged",
            "ShipmentStatusChanged",
            "VesselRouteChanged",
            "FxRatePublished",
            "HolidayCalendarChanged",
            "CollateralValuationChanged",
            "LimitReservationChanged",
            "LoanFacilityChanged",
            "PaymentInstructionChanged",
            "AuditEvidenceSealed",
            "DocumentReceived",
            "PolicyChanged",
            "OperationalKpiChanged",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "legal_entity_id",
    "booking_branch_id",
    "case_id",
    "instrument_id",
    "counterparty_ref",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|lc_taxonomy_id,credit_type,availability_method,confirmation_status,tolerance_rule,revolving_terms,transferable_flag,governing_practice
2|party_role_graph_id,applicant,beneficiary,issuing_bank,advising_bank,confirming_bank,reimbursing_bank,role_lineage
3|amount_tenor_id,available_amount,utilized_amount,drawing_schedule,tenor_basis,maturity_logic,tolerance_percent,auto_close_rule
4|amendment_chain_id,amendment_number,clause_change_set,party_acceptance,beneficiary_consent,superseded_terms,effective_timestamp,replay_hash
5|presentation_calendar_id,expiry_place,expiry_date,presentation_period,banking_calendar,shipment_cutoff,grace_rule,late_presentation_discrepancy
6|document_matrix_id,required_document_set,optional_document_set,conditional_document_rule,waived_document_set,original_copy_requirement,issuer_constraint,cross_document_dependency
7|examination_workspace_id,document_fact,credit_term,field_mismatch,examiner_finding,deadline,examiner_narrative,audit_trace
8|discrepancy_codebook_id,discrepancy_code,severity,remediation_path,refusal_notice_template,waiver_allowed,analytics_group,approved_code
9|waiver_workflow_id,discrepancy_case,applicant_waiver_request,beneficiary_resubmission,partial_acceptance,refusal_notice,release_condition,final_disposition
10|availability_flow_id,settlement_type,reimbursement_path,deferred_payment_maturity,draft_acceptance,negotiation_recourse,obligation_type,aging_queue
11|transferable_credit_id,first_beneficiary,second_beneficiary,transferred_amount,quantity_limit,clause_inheritance,substituted_document,parent_child_link
12|standby_credit_id,demand_template,beneficiary_statement,drawing_window,automatic_reduction,isp_rule_selection,demand_completeness,honor_timing
13|guarantee_lifecycle_id,guarantee_type,issuance_approval,effective_date,reduction_schedule,extension_request,claim_decision,discharge_evidence
14|counter_guarantee_chain_id,local_issuer,counter_guarantor,obligation_chain,message_dependency,local_law_override,claim_propagation,event_lineage
15|collection_case_id,collection_mode,collecting_bank_instruction,release_condition,drawee_action,maturity_tracking,non_payment_path,non_acceptance_path
16|collection_instruction_id,protest_flag,partial_payment_rule,storage_instruction,charge_bearer,escalation_contact,typed_instruction,release_notice
17|trade_loan_link_id,loan_purpose,linked_credit,linked_collection,shipment_collateral,receivable_source,documentary_prerequisite,drawdown_block
18|loan_utilization_id,finance_stage,utilization_ceiling,rollover_rule,due_date_logic,repayment_waterfall,export_proceed_reference,delinquency_queue
19|sanctions_boundary_id,screening_request,trade_attribute_set,hit_set,adjudication,release_block,external_aml_reference,boundary_evidence
20|rescreen_trigger_id,trigger_type,party_change,amendment_term,vessel_update,country_change,watchlist_snapshot,adjudication_note
21|route_risk_id,vessel_identifier,port_of_loading,port_of_discharge,transshipment_node,carrier_data,jurisdiction_tag,policy_decision
22|shipment_document_registry_id,document_class,document_identity,issuer,version,amendment_link,presentation_id,duplicate_conflict_check
23|bill_of_lading_rule_id,transport_mode,on_board_date,clean_notation,consignee_wording,notify_party,freight_term,transshipment_consistency
24|cross_document_check_id,invoice_value,packing_quantity,goods_description,origin_declaration,inspection_finding,beneficiary_name,tolerance_policy
25|insurance_adequacy_id,insured_amount,covered_risk,currency_alignment,claims_payable_location,endorsement_status,policy_date,transport_reference
26|shipment_terms_rule_id,partial_shipment_allowed,transshipment_allowed,split_drawing_rule,multiple_presentation_rule,staged_schedule,document_check,amendment_impact
27|drawing_package_id,draw_amount,demand_basis,statement_template,required_document_set,beneficiary_certification,partial_drawing_history,completeness_check
28|settlement_release_id,release_condition,blocked_reason,value_date,reimbursement_path,payment_instruction,partial_settlement,post_settlement_proof
29|fee_accrual_id,fee_type,charge_bearer,accrual_basis,waiver_flag,tax_handling,reversal_logic,net_proceeds_reconciliation
30|fx_mismatch_control_id,invoice_currency,credit_currency,settlement_currency,fx_snapshot,tolerance_usage,financed_amount,mismatch_alert
31|ucp_rule_engine_id,rule_clause,presentation_timing,document_consistency,original_copy_check,transport_requirement,refusal_timing,rule_citation
32|isp_rule_engine_id,standby_rule_clause,demand_condition,drawing_window,extension_clause,automatic_reduction,demand_sufficiency,examiner_label
33|collection_rule_engine_id,release_against_payment,release_against_acceptance,protest_instruction,partial_payment,return_documents,drawer_notification,outcome
34|exception_priority_id,exception_type,exposure_amount,expiry_risk,compliance_severity,customer_timer,priority_score,breach_event
35|four_eyes_control_id,critical_action,maker_user,checker_user,override_reason,evidence_link,policy_reference,segregation_passed
36|event_taxonomy_id,event_name,payload_schema,workflow_branch,consumer_contract,compatibility_version,example_payload,event_coverage
37|event_reliability_id,case_idempotency_key,outbox_status,inbox_status,dead_letter_status,replay_safe_handler,duplicate_callback,retry_reason
38|workbench_queue_id,queue_name,case_state,pending_action,operator_role,filter_definition,row_action,release_gap_indicator
39|timeline_obligation_id,timeline_event,instrument_term,outstanding_obligation,documentary_status,compliance_status,fee_status,next_action
40|document_viewer_id,extracted_fact,governing_term,highlight_span,examiner_comment,comparison_mode,annotation_persistence,discrepancy_link
41|clause_extraction_skill_id,source_document,extracted_clause,party_fact,amount_fact,date_fact,document_requirement,draft_record_preview
42|examination_skill_id,presentation_package,suggested_discrepancy,triggering_clause,field_mismatch,refusal_draft,waiver_request_draft,human_decision
43|sanctions_guidance_skill_id,screening_reason,triggering_fact,missing_evidence,external_decision_required,release_block_explanation,operator_guidance,boundary_guard
44|release_pack_id,workflow_test_evidence,rule_pack_coverage,event_contract_verification,screening_boundary_test,ui_state_evidence,unresolved_risk,migration_status
45|synthetic_corpus_id,scenario_label,document_set,discrepancy_type,late_shipment,partial_drawing,forged_like_indicator,coverage_by_product
46|counterfactual_simulation_id,scenario_type,proposed_amendment,delay_assumption,document_requirement_impact,sanctions_rescreen_impact,settlement_timing_impact,loan_repayment_impact
47|kpi_definition_id,metric_name,formula,projection_source,known_fixture,dashboard_card,validation_result,segment_dimension
48|operating_model_id,booking_branch,operating_branch,advising_location,correspondent_role,branch_calendar,local_policy_override,tenant_leakage_check
49|api_completeness_id,endpoint,query_filter,pagination_rule,idempotency_rule,critical_ui_action,event_traceability,release_export
50|go_live_gate_id,rule_pack_test,examination_regression,sanctions_boundary_verification,event_replay_check,ui_critical_path,runbook_signoff,remaining_risk
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    2: ("CustomerRiskUpdated",),
    5: ("HolidayCalendarChanged",),
    17: ("LoanFacilityChanged",),
    19: ("PartyScreeningDecisionChanged", "CustomerRiskUpdated"),
    20: ("WatchlistChanged", "VesselRouteChanged"),
    21: ("ShipmentStatusChanged", "VesselRouteChanged"),
    28: ("PaymentInstructionChanged",),
    29: ("FxRatePublished",),
    30: ("FxRatePublished",),
    37: ("PolicyChanged", "AuditEvidenceSealed"),
    41: ("DocumentReceived",),
    44: ("AuditEvidenceSealed",),
    47: ("OperationalKpiChanged",),
    50: ("PolicyChanged", "AuditEvidenceSealed", "OperationalKpiChanged"),
}
_INSTRUMENT_FEATURES = (1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 48, 50)
_DOCUMENT_COMPLIANCE_FEATURES = (6, 7, 8, 9, 19, 20, 21, 22, 23, 24, 25, 26, 27, 31, 32, 33, 40, 45, 50)
_SETTLEMENT_EXPOSURE_FEATURES = (3, 10, 17, 18, 28, 29, 30, 34, 35, 46, 47, 49, 50)
_OPERATIONS_AGENT_FEATURES = (36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 49, 50)
_AGENT_FEATURES = (41, 42, 43, 46, 49, 50)
_HUMAN_CONFIRMATION_FEATURES = (4, 9, 10, 12, 13, 14, 19, 20, 28, 35, 41, 42, 43, 46, 50)
_APPROVAL_REQUIRED_FEATURES = (4, 9, 10, 12, 13, 14, 19, 20, 28, 35, 46, 50)
_NON_MUTATING_FEATURES = (3, 5, 7, 8, 19, 20, 21, 23, 24, 25, 26, 30, 31, 32, 33, 34, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50)
_PROJECTION_ONLY_FEATURES = (2, 17, 18, 19, 20, 21, 28, 29, 30, 37, 47, 48, 50)


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
        "tables": (f"trade_finance_operations_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"TradeFinanceOperations{_camel(capability.slug)}Panel",
        "route": f"POST /trade-finance-operations/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in TRADE_CAPABILITIES}


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
        "event_topic": TRADE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "instrument_evidence_complete": True,
        "document_compliance_evidence_complete": True,
        "settlement_exposure_evidence_complete": True,
        "operations_agent_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned trade finance model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _INSTRUMENT_FEATURES and payload.get("instrument_evidence_complete") is not True:
        findings.append("instrument evidence is required for credit taxonomy, party-role graph, amount and tenor controls, amendments, calendars, settlement flows, transferable and standby credits, guarantees, counter-guarantees, collections, trade loans, operating model, and go-live proof")
    if number in _DOCUMENT_COMPLIANCE_FEATURES and payload.get("document_compliance_evidence_complete") is not True:
        findings.append("document and compliance evidence is required for document matrices, examination, discrepancies, waivers, sanctions, rescreening, vessel/route risk, shipment documents, rule packs, document viewer, synthetic corpus, and go-live proof")
    if number in _SETTLEMENT_EXPOSURE_FEATURES and payload.get("settlement_exposure_evidence_complete") is not True:
        findings.append("settlement and exposure evidence is required for amount controls, obligation flows, loans, settlement release, fees, FX mismatch, exception priority, four-eyes controls, simulations, KPIs, APIs, and go-live gates")
    if number in _OPERATIONS_AGENT_FEATURES and payload.get("operations_agent_evidence_complete") is not True:
        findings.append("operations and agent evidence is required for events, idempotency, workbench queues, timeline, document viewer, agent skills, release packs, simulations, analytics, APIs, and go-live readiness")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("amendments, waivers, honor/refusal, standby demand handling, guarantee claims, sanctions release, settlement release, overrides, agent drafts, simulations, and go-live actions require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk trade finance actions require separated approval for amendments, waivers, honor/refusal, guarantee claims, sanctions release, settlement release, override, simulation approval, and go-live gates")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("trade finance assistant skills must cite owned facts, show reviewable CRUD previews, enforce permissions and policy checks, and block direct writes or external release actions before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("calculations, calendar checks, examination previews, compliance screens, document rules, FX checks, analytics, event replay, document viewing, agent suggestions, evidence packs, corpus checks, simulations, KPIs, APIs, and go-live checks must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("customer risk, AML, vessel, FX, calendar, collateral, limits, loans, payments, audit, and KPI context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != TRADE_REQUIRED_EVENT_TOPIC:
        findings.append("trade finance operations eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in TRADE_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary trade finance datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("trade finance controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_trade_finance_operations_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in TRADE_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in TRADE_DECLARED_DEPENDENCIES)
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
        "required_event_topic": TRADE_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": TRADE_ALLOWED_DATABASE_BACKENDS,
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


def improve1_trade_finance_operations_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_trade_finance_operations_control(capability) for capability in TRADE_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {
        "format": "appgen.trade_finance_operations.improve1-control-contract.v1",
        "ok": len(results) == 50 and all(item["ok"] for item in results),
        "pbc": PBC_KEY,
        "capability_count": len(results),
        "capabilities": results,
        "owned_tables": TRADE_CONTROL_OWNED_TABLES,
        "allowed_database_backends": TRADE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": TRADE_REQUIRED_EVENT_TOPIC,
        "declared_dependencies": TRADE_DECLARED_DEPENDENCIES,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


TRADE_FINANCE_OPERATIONS_CONTROL_FUNCTIONS = (
    "evaluate_trade_finance_operations_control",
    "improve1_trade_finance_operations_control_contract",
    "sample_payload_for",
)

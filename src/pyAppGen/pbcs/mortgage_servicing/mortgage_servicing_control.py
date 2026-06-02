"""Executable improve1 controls for the Mortgage Servicing PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "mortgage_servicing"
EVENT_CONTRACT = "AppGen-X"
MORTGAGE_SERVICING_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
MORTGAGE_SERVICING_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.mortgage_servicing.events"
_BASE_OWNED_TABLES = (
    "mortgage_servicing_mortgage_loan",
    "mortgage_servicing_escrow_account",
    "mortgage_servicing_payment_event",
    "mortgage_servicing_servicing_statement",
    "mortgage_servicing_loss_mitigation_case",
    "mortgage_servicing_investor_report",
    "mortgage_servicing_foreclosure_milestone",
    "mortgage_servicing_policy_rule",
    "mortgage_servicing_runtime_parameter",
    "mortgage_servicing_schema_extension",
    "mortgage_servicing_control_assertion",
    "mortgage_servicing_governed_model",
    "mortgage_servicing_appgen_outbox_event",
    "mortgage_servicing_appgen_inbox_event",
    "mortgage_servicing_appgen_dead_letter_event",
)
MORTGAGE_SERVICING_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"mortgage_servicing_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
MORTGAGE_SERVICING_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys((
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "BorrowerProjectionChanged",
    "PropertyProjectionChanged",
    "InvestorProjectionChanged",
    "PaymentRailEventReceived",
    "DocumentExtractionCompleted",
    "ComplianceDeterminationChanged",
    "PropertyServiceProjectionChanged",
    "AccountingPostingRequested",
)))
MORTGAGE_SERVICING_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in MORTGAGE_SERVICING_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in MORTGAGE_SERVICING_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "loan_id", "servicing_cycle_id", "borrower_projection_id", "property_projection_id", "policy_version", "actor_id", "audit_trail", "evidence_references")
_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: 'loan_boarding_data_quality_gate_verified',
    2: 'servicing_transfer_reconciliation_verified',
    3: 'mortgage_loan_lifecycle_state_machine_verified',
    4: 'payment_application_waterfall_verified',
    5: 'suspense_handling_controls_verified',
    6: 'late_charge_assessment_rules_verified',
    7: 'interest_accrual_and_amortization_schedule_verified',
    8: 'adjustable_rate_mortgage_change_controls_verified',
    9: 'escrow_account_lifecycle_verified',
    10: 'escrow_analysis_engine_verified',
    11: 'tax_and_insurance_disbursement_controls_verified',
    12: 'force_placed_insurance_workflow_verified',
    13: 'flood_zone_monitoring_boundary_verified',
    14: 'servicing_statement_generation_verified',
    15: 'borrower_notice_schedule_verified',
    16: 'communication_preference_and_language_controls_verified',
    17: 'delinquency_aging_buckets_verified',
    18: 'collections_contact_strategy_verified',
    19: 'bankruptcy_servicing_controls_verified',
    20: 'military_and_protected_status_controls_verified',
    21: 'loss_mitigation_intake_verified',
    22: 'document_driven_assistance_package_review_verified',
    23: 'workout_option_decisioning_verified',
    24: 'trial_payment_plan_tracking_verified',
    25: 'loan_modification_term_generation_verified',
    26: 'foreclosure_referral_controls_verified',
    27: 'foreclosure_milestone_management_verified',
    28: 'foreclosure_hold_and_restart_governance_verified',
    29: 'payoff_quote_generation_verified',
    30: 'loan_payoff_and_release_tracking_verified',
    31: 'investor_remittance_reporting_verified',
    32: 'advance_tracking_verified',
    33: 'fee_assessment_and_waiver_governance_verified',
    34: 'property_inspection_and_preservation_boundary_verified',
    35: 'disaster_assistance_workflow_verified',
    36: 'complaint_and_dispute_linkage_verified',
    37: 'credit_reporting_furnishing_controls_verified',
    38: 'compliance_rule_and_parameter_workbench_verified',
    39: 'exception_taxonomy_and_queues_verified',
    40: 'borrower_facing_account_timeline_verified',
    41: 'agent_assisted_payment_research_verified',
    42: 'agent_assisted_loss_mitigation_checklist_verified',
    43: 'agent_safety_and_authority_limits_verified',
    44: 'appgen_x_event_specialization_verified',
    45: 'point_in_time_servicing_reconstruction_verified',
    46: 'cryptographic_servicing_audit_packet_verified',
    47: 'operational_risk_scoring_verified',
    48: 'release_smoke_scenarios_verified',
    49: 'cross_pbc_boundary_proof_verified',
    50: 'end_to_end_borrower_assistance_workbench_verified',
}
_DOMAIN_FIELDS: dict[int, tuple[str, ...]] = {
    1: ('loan_id', 'note_terms_verified', 'payment_due_date', 'interest_method', 'escrow_status', 'investor_projection_id', 'borrower_projection_id', 'property_projection_id', 'boarding_exception_reason'),
    2: ('transfer_id', 'prior_servicer_balance', 'payment_history_file', 'escrow_ledger_file', 'open_item_count', 'borrower_notice_set', 'reconciliation_variance', 'approval_status'),
    3: ('loan_state', 'allowed_transition', 'effective_date', 'reason_code', 'approval_id', 'event_emission_id', 'next_allowed_actions'),
    4: ('payment_event_id', 'application_order', 'payment_source', 'effective_date', 'reversal_link', 'principal_allocation', 'interest_allocation', 'escrow_allocation', 'fee_allocation', 'suspense_allocation'),
    5: ('suspense_bucket_id', 'receipt_source', 'matching_status', 'borrower_instruction', 'aging_days', 'release_rule', 'exception_workflow_id'),
    6: ('late_charge_rule_id', 'grace_days', 'fee_calculation', 'waiver_authority', 'fee_cap', 'protected_status', 'rule_version', 'audit_evidence'),
    7: ('amortization_schedule_id', 'scheduled_principal', 'scheduled_interest', 'unpaid_principal_balance', 'interest_method', 'curtailment_amount', 'recast_flag', 'variance_detection'),
    8: ('arm_change_id', 'index_projection_id', 'margin', 'cap_test', 'floor_rate', 'lookback_days', 'payment_change', 'notice_schedule', 'borrower_explanation'),
    9: ('escrow_account_id', 'lifecycle_status', 'tax_line_items', 'insurance_line_items', 'cushion_parameters', 'analysis_date', 'shortage_option', 'surplus_disposition', 'waiver_rule'),
    10: ('escrow_analysis_id', 'analysis_type', 'line_items', 'projected_balance', 'minimum_balance', 'shortage_amount', 'surplus_amount', 'borrower_options', 'approval_id'),
    11: ('disbursement_id', 'payee_projection_id', 'due_date', 'invoice_evidence', 'payment_status', 'exception_reason', 'stop_payment_status', 'duplicate_check'),
    12: ('coverage_gap_id', 'notice_sequence', 'placement_status', 'premium_projection', 'borrower_evidence_review', 'cancellation_status', 'refund_workflow'),
    13: ('flood_projection_id', 'determination_date', 'map_status', 'required_coverage', 'appeal_status', 'freshness_timestamp', 'projection_source'),
    14: ('statement_id', 'statement_period', 'line_items', 'message_blocks', 'disclosure_set', 'delivery_method', 'suppression_reason', 'render_evidence'),
    15: ('notice_requirement_id', 'trigger_event', 'deadline', 'template_version', 'delivery_channel', 'language', 'proof_of_delivery', 'suppression_rule'),
    16: ('communication_projection_id', 'preferred_channel', 'consent_status', 'language', 'accessibility_requirement', 'contact_restriction_status', 'authorized_contact'),
    17: ('delinquency_calc_id', 'due_date', 'paid_through_date', 'days_delinquent', 'aging_bucket', 'rolling_status', 'cure_amount', 'trend'),
    18: ('contact_strategy_id', 'allowed_action', 'suppression_reason', 'next_contact_date', 'script_version', 'contact_outcome', 'compliance_evidence'),
    19: ('bankruptcy_projection_id', 'chapter', 'filing_date', 'stay_status', 'claim_deadline', 'payment_handling_rule', 'attorney_contact_control'),
    20: ('protected_status_id', 'status_type', 'effective_dates', 'evidence_source', 'applicable_protections', 'required_approval', 'violation_block'),
    21: ('loss_mitigation_case_id', 'application_status', 'hardship_reason', 'required_documents', 'received_documents', 'missing_items', 'review_deadline'),
    22: ('document_review_id', 'document_type', 'extracted_fields', 'confidence', 'source_page', 'field_mapping', 'reviewer_approval', 'mutation_preview'),
    23: ('workout_evaluation_id', 'option_type', 'eligibility_rules', 'waterfall_order', 'investor_constraint', 'trial_requirement', 'payment_impact', 'decision_rationale'),
    24: ('trial_plan_id', 'due_dates', 'required_amounts', 'payment_matching', 'missed_payment_consequence', 'completion_evidence'),
    25: ('modification_package_id', 'new_principal', 'new_rate', 'new_term', 'new_maturity', 'escrow_change', 'deferred_balance', 'borrower_acceptance', 'document_status'),
    26: ('foreclosure_referral_id', 'prerequisite_validations', 'approval_authority', 'attorney_projection_id', 'referral_package', 'hold_reasons'),
    27: ('foreclosure_milestone_id', 'milestone_type', 'jurisdiction', 'due_date', 'actual_date', 'responsible_party', 'hold_status', 'outcome', 'evidence'),
    28: ('foreclosure_hold_id', 'hold_reason', 'effective_date', 'blocked_actions', 'owner', 'review_date', 'release_criteria', 'restart_evidence'),
    29: ('payoff_quote_id', 'good_through_date', 'component_lines', 'per_diem', 'delivery_evidence', 'quote_status', 'wire_instructions'),
    30: ('payoff_completion_id', 'received_funds', 'balance_zeroed', 'escrow_refund', 'lien_release_milestones', 'recording_status', 'closure_event'),
    31: ('investor_report_id', 'reporting_period', 'investor_projection_id', 'pool_id', 'remittance_lines', 'certification', 'exception_list', 'submission_evidence'),
    32: ('advance_id', 'advance_type', 'amount', 'recoverability', 'investor_eligibility', 'reimbursement_status', 'write_off_approval'),
    33: ('fee_record_id', 'fee_type', 'trigger', 'rule_version', 'amount', 'waiver_authority', 'reversal_reason', 'borrower_notice_link'),
    34: ('property_service_projection_id', 'inspection_result', 'preservation_recommendation', 'cost_estimate', 'completion_status', 'declared_dependency'),
    35: ('disaster_projection_id', 'affected_property_flag', 'assistance_request', 'relief_option', 'suppression_rules', 'review_dates'),
    36: ('complaint_projection_id', 'category', 'due_date', 'related_records', 'response_status', 'operational_hold_effects'),
    37: ('credit_snapshot_id', 'reporting_period', 'status_code', 'suppression_reason', 'dispute_flag', 'correction_evidence'),
    38: ('compliance_rule_id', 'rule_family', 'parameter_bounds', 'approval_history', 'rollback_target', 'runtime_effect'),
    39: ('exception_id', 'exception_category', 'severity', 'impacted_action', 'owner_queue', 'sla', 'escalation', 'closure_evidence', 'reopen_reason'),
    40: ('timeline_projection_id', 'event_order', 'source_links', 'document_links', 'notice_links', 'exception_links', 'decision_links', 'event_type_filter'),
    41: ('payment_research_skill_id', 'receipt_comparison', 'bank_file_reference', 'suspense_review', 'reversal_review', 'proposed_correction', 'confirmation_required'),
    42: ('loss_mitigation_skill_id', 'borrower_instruction_parse', 'checklist_draft', 'missing_evidence_explanation', 'eligible_paths', 'case_update_preview'),
    43: ('agent_authority_id', 'command', 'affected_records', 'rule_checks', 'confidence', 'source_evidence', 'approval_role', 'irreversible_impact_flag'),
    44: ('event_schema_id', 'event_type', 'idempotency_key', 'retry_policy', 'dead_letter_evidence', 'declared_dependency_use'),
    45: ('reconstruction_id', 'as_of_date', 'balance_snapshot', 'escrow_snapshot', 'delinquency_snapshot', 'notice_snapshot', 'loss_mitigation_snapshot', 'foreclosure_snapshot'),
    46: ('audit_packet_id', 'packet_type', 'hash_chain', 'payment_application_evidence', 'escrow_analysis_evidence', 'decision_evidence', 'tamper_check'),
    47: ('risk_score_id', 'escrow_shortage_factor', 'payment_dispute_factor', 'missed_notice_factor', 'delinquency_roll_factor', 'foreclosure_breach_factor', 'investor_variance_factor', 'explanation'),
    48: ('smoke_scenario_id', 'boarding_scenario', 'payment_scenario', 'escrow_scenario', 'statement_scenario', 'delinquency_scenario', 'loss_mitigation_scenario', 'foreclosure_hold_scenario', 'payoff_scenario'),
    49: ('boundary_proof_id', 'owned_model_check', 'service_reference_check', 'route_reference_check', 'handler_reference_check', 'projection_reference_check', 'agent_command_check'),
    50: ('borrower_assistance_workspace_id', 'borrower_timeline', 'checklist', 'eligibility_results', 'payment_history', 'next_action', 'compliance_clock', 'assistant_panel'),
}
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {feature_number: _BASE_FIELDS + _DOMAIN_FIELDS[feature_number] + (primary_proof,) for feature_number, primary_proof in _PRIMARY_PROOF_FIELDS.items()}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    1: ("BorrowerProjectionChanged", "PropertyProjectionChanged", "InvestorProjectionChanged"),
    13: ("ComplianceDeterminationChanged",),
    16: ("BorrowerProjectionChanged",),
    19: ("ComplianceDeterminationChanged",),
    20: ("ComplianceDeterminationChanged",),
    22: ("DocumentExtractionCompleted",),
    31: ("InvestorProjectionChanged",),
    34: ("PropertyServiceProjectionChanged",),
    36: ("ComplianceDeterminationChanged",),
    44: ("AuditEventSealed",),
    49: ("PolicyChanged", "AuditEventSealed"),
    50: ("BorrowerProjectionChanged", "DocumentExtractionCompleted"),
}
_DOMAIN_MESSAGES: dict[int, str] = {
    1: 'Add boarding checks for note terms, payment due date, interest method, escrow status, investor projection, borrower projection, property projection, and exception reason.',
    2: 'Add transfer-in records with prior-servicer trial balance, payment history, escrow ledger, open items, borrower notices, and reconciliation variance workflow.',
    3: 'Add explicit `mortgage_loan` states, allowed transitions, effective dates, reason codes, required approvals, and AppGen-X event emission.',
    4: 'Expand `payment_event` with configurable application order, payment source, effective date, reversal link, component allocations, and reason evidence.',
    5: 'Add suspense buckets with receipt source, matching status, borrower instruction, aging, release rule, and exception workflow.',
    6: 'Add late-charge rules with grace days, fee calculation, waiver authority, cap, protected status, and audit evidence.',
    7: 'Add amortization projections with scheduled principal, interest, unpaid principal balance, interest method, recast flag, and variance detection.',
    8: 'Add ARM change records with index projection, rate calculation, cap test, payment change, notice schedule, and borrower-facing explanation.',
    9: 'Expand `escrow_account` with lifecycle status, tax/insurance lines, cushion parameters, analysis date, shortage option, surplus disposition, and waiver rules.',
    10: 'Add annual and short-year analysis calculations with line items, projected balance, minimum balance, borrower options, and approval.',
    11: 'Add disbursement schedules, payee projection, due dates, invoice evidence, payment status, exception reason, and stop-payment handling.',
    12: 'Add coverage gap records, notice sequence, placement status, premium projection, borrower evidence review, and cancellation/refund workflow.',
    13: 'Store flood-zone projections with determination date, map status, required coverage, appeal status, and freshness.',
    14: 'Expand `servicing_statement` with statement period, line items, message blocks, disclosure set, delivery method, suppression reason, and render evidence.',
    15: 'Add notice requirements with trigger, deadline, template version, delivery channel, language, proof of delivery, and suppression rules.',
    16: 'Store borrower communication projections, preferred channel, consent, language, accessibility requirement, and contact restriction status.',
    17: 'Add delinquency calculations with due date, paid-through date, days delinquent, rolling status, cure amount, and trend.',
    18: 'Add contact strategies with allowed action, suppression reason, next contact date, script version, outcome, and compliance evidence.',
    19: 'Add bankruptcy status projection, chapter, filing date, stay status, claim deadline, payment handling rule, and attorney contact controls.',
    20: 'Add protected-status projections with effective dates, evidence source, applicable protections, and required approvals.',
    21: 'Expand `loss_mitigation_case` with application status, hardship reason, required documents, received documents, missing items, and review deadline.',
    22: 'Add agent-assisted document extraction with confidence, source page, field mapping, reviewer approval, and mutation preview.',
    23: 'Add workout option evaluations with eligibility rules, waterfall order, investor constraint, trial requirement, payment impact, and decision rationale.',
    24: 'Add trial plan records with due dates, required amounts, payment matching, missed-payment consequences, and completion evidence.',
    25: 'Add modification term package with calculation trace, approval, borrower acceptance, document status, and boarding event.',
    26: 'Add referral checklist with prerequisite validations, approval authority, attorney projection, referral package, and hold reasons.',
    27: 'Expand `foreclosure_milestone` with milestone type, jurisdiction, due date, actual date, responsible party, hold, outcome, and evidence.',
    28: 'Add hold records with reason, effective date, blocked actions, owner, review date, release criteria, and restart evidence.',
    29: 'Add payoff quote records with good-through date, component lines, per diem, delivery evidence, and quote cancellation.',
    30: 'Add payoff completion workflow with received funds, balance zeroing, escrow refund, lien-release milestones, and closure event.',
    31: 'Expand `investor_report` with reporting period, investor projection, pool, remittance lines, certification, exception list, and submission evidence.',
    32: 'Add advance records with type, amount, recoverability, investor eligibility, reimbursement status, and write-off approval.',
    33: 'Add fee records with type, trigger, rule version, amount, waiver authority, reversal reason, and borrower notice link.',
    34: 'Store property-service projections, inspection results, preservation recommendations, cost estimates, and completion status from declared dependencies.',
    35: 'Add disaster-zone projection, affected-property flag, borrower assistance request, relief option, suppression rules, and review dates.',
    36: 'Add complaint/dispute projections with category, due date, related records, response status, and operational hold effects.',
    37: 'Add credit-reporting snapshot with reporting period, status code, suppression reason, dispute flag, and correction evidence.',
    38: 'Add workbench editors for late fees, notices, escrow cushions, loss-mitigation waterfalls, foreclosure preconditions, and contact limits.',
    39: 'Add exception categories, severity, impacted action, owner queue, SLA, escalation, closure evidence, and reopen reason.',
    40: 'Add a timeline projection that orders servicing events, documents, notices, exceptions, and decisions with source links.',
    41: 'Add assistant skills that summarize payment history, identify likely misapplications, propose corrections, and require confirmation.',
    42: 'Add assistant prompts that parse borrower instructions, build checklist drafts, explain missing evidence, and generate governed case updates.',
    43: 'Require agent proposals to state command, affected records, rule checks, confidence, source evidence, approval role, and irreversible-impact flag.',
    44: 'Define typed events for loan boarded, payment applied, escrow analyzed, notice sent, loss mitigation decisioned, foreclosure held, and investor report certified.',
    45: 'Add event-sourced reconstruction for balances, escrow, delinquency, notices, loss mitigation, and foreclosure status.',
    46: 'Add hash-linked packets for payment application, escrow analysis, loss-mitigation decision, foreclosure referral, and payoff closure.',
    47: 'Add risk scores for escrow shortage, payment dispute, missed notice, delinquency roll, foreclosure breach, and investor-report variance.',
    48: 'Add smoke scenarios for boarding, payment application, escrow analysis, statement generation, delinquency, loss mitigation, foreclosure hold, and payoff.',
    49: 'Add automated proof that generated models, services, routes, handlers, projections, and agent commands use only owned tables plus declared APIs/events.',
    50: 'Add a loss-mitigation workspace with borrower timeline, checklist, eligibility results, payment history, next action, compliance clock, and assistant panel.',
}
_HUMAN_CONFIRMATION_FEATURES = (2, 3, 8, 12, 18, 22, 23, 25, 26, 28, 30, 33, 38, 41, 42, 43, 50)
_PROJECTION_ONLY_FEATURES = (1, 13, 16, 19, 20, 22, 31, 34, 36, 44, 49, 50)
_AGENT_PREVIEW_FEATURES = (22, 41, 42, 43, 50)
_NON_MUTATING_FEATURES = (38, 45, 46, 48, 49)
BORROWER_IMPACT_FEATURES = (4, 6, 8, 10, 12, 14, 15, 18, 20, 21, 23, 25, 26, 28, 29, 30, 33, 37, 41, 42, 43, 50)


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
    proof = _PRIMARY_PROOF_FIELDS[capability.feature_number]
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"mortgage_servicing_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": proof,
        "ui": f"MortgageServicing{_camel(capability.slug)}Panel",
        "route": f"POST /mortgage-servicing/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in MORTGAGE_SERVICING_CONTROL_CAPABILITIES}


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
        "event_topic": MORTGAGE_SERVICING_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "borrower_impact_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    feature_number = capability.feature_number
    spec = CONTROL_SPECS[feature_number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[feature_number])
    if feature_number in BORROWER_IMPACT_FEATURES and payload.get("borrower_impact_evidence_complete") is not True:
        findings.append("borrower-impacting servicing actions require complete rule, notice, approval, and evidence context")
    if feature_number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("mortgage servicing decisions with borrower, foreclosure, fee, assistance, or irreversible impact require human approval before mutation")
    if feature_number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("mortgage servicing assistant skills must produce preview-only drafts with source evidence and approval gates")
    if feature_number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("compliance simulations, reconstruction, audit packets, smoke scenarios, and boundary proofs must be side-effect-free artifacts")
    if feature_number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("borrower, property, investor, document, compliance, payment rail, accounting, and audit context must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != MORTGAGE_SERVICING_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("mortgage servicing eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in MORTGAGE_SERVICING_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary mortgage servicing datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("mortgage servicing controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_mortgage_servicing_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in MORTGAGE_SERVICING_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in MORTGAGE_SERVICING_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": MORTGAGE_SERVICING_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": MORTGAGE_SERVICING_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_mortgage_servicing_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_mortgage_servicing_control(capability) for capability in MORTGAGE_SERVICING_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.mortgage-servicing-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": MORTGAGE_SERVICING_CONTROL_OWNED_TABLES, "declared_dependencies": MORTGAGE_SERVICING_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": MORTGAGE_SERVICING_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": MORTGAGE_SERVICING_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


MORTGAGE_SERVICING_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_mortgage_servicing_control(slug, payload)) for capability in MORTGAGE_SERVICING_CONTROL_CAPABILITIES}

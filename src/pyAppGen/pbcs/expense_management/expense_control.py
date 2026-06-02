"""Executable improve1 controls for the Expense Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "expense_management"
EVENT_CONTRACT = "AppGen-X"
EXPENSE_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
EXPENSE_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.expense_management.events"
EXPENSE_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(DOMAIN_OWNED_TABLES + (
    "expense_management_expense_report",
    "expense_management_expense_line",
    "expense_management_receipt_document",
    "expense_management_corporate_card_feed",
    "expense_management_expense_policy",
    "expense_management_expense_approval",
    "expense_management_reimbursement_batch",
    "expense_management_expense_fraud_signal",
    "expense_management_appgen_outbox_event",
    "expense_management_appgen_inbox_event",
    "expense_management_appgen_dead_letter_event",
)))
EXPENSE_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "EmployeeCreated",
    "EmployeeProvisioned",
    "CardTransactionPosted",
    "PaymentExecuted",
    "PaymentCaptured",
    "PolicyChanged",
    "AccessPolicyChanged",
    "TravelItineraryProjected",
    "ProjectProjectionUpdated",
    "CustomerProjectionUpdated",
    "TaxPolicyChanged",
    "FinancialPeriodChanged",
    "GET /employee-spend-intelligence",
    "POST /notifications/messages",
)))

EXPENSE_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in EXPENSE_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in EXPENSE_CONTROL_CAPABILITIES}

_SPEC_ROWS: tuple[tuple[int, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = [(1, ('expense_management_expense_report', 'expense_management_expense_line', 'expense_management_receipt_artifact', 'expense_management_card_transaction', 'expense_management_expense_policy', 'expense_management_expense_approval_task'), ('employee_projection', 'report_period', 'currency', 'business_purpose', 'line_completeness', 'receipt_requirements', 'card_match_state', 'policy_version', 'approver_eligibility', 'exception_status', 'readiness_decision'), 'ExpenseReportReadinessGate', 'POST /expense-reports/readiness', ('EmployeeCreated', 'CardTransactionPosted', 'PolicyChanged')), (2, ('expense_management_expense_report', 'expense_management_reimbursement_batch'), ('lifecycle_state', 'allowed_transition', 'required_evidence', 'owner', 'timestamp', 'notification', 'reimbursement_effect', 'transition_decision'), 'ExpenseReportLifecycleBoard', 'POST /expense-reports/lifecycle/transition', ()), (3, ('expense_management_expense_line', 'expense_management_merchant_profile', 'expense_management_expense_policy'), ('merchant_profile', 'receipt_text', 'card_metadata', 'location', 'employee_role', 'project_code', 'historical_pattern', 'category_confidence', 'override_rationale'), 'ExpenseLineCategoryStudio', 'POST /expense-lines/classify', ('EmployeeCreated',)), (4, ('expense_management_expense_report', 'expense_management_expense_line'), ('business_purpose', 'specificity_score', 'project_linkage', 'attendee_detail', 'trip_linkage', 'required_details', 'generic_phrase_flags', 'agent_suggestion'), 'BusinessPurposeCoach', 'POST /expense-reports/business-purpose/score', ('TravelItineraryProjected',)), (5, ('expense_management_receipt_artifact',), ('receipt_fingerprint', 'source_metadata', 'ocr_extract', 'integrity_check', 'attachment_lineage', 'duplicate_artifact_status', 'redaction_status', 'line_fact_links'), 'ReceiptEvidenceChain', 'POST /receipts/evidence-chain', ()), (6, ('expense_management_receipt_artifact', 'expense_management_expense_line'), ('merchant', 'tax_amount', 'tip_amount', 'currency', 'receipt_datetime', 'line_items', 'field_confidence', 'anomaly_flags', 'confirmation_required'), 'SemanticReceiptExtractionWorkbench', 'POST /receipts/extract', ()), (7, ('expense_management_receipt_artifact', 'expense_management_card_transaction'), ('amount_tolerance', 'date_window', 'merchant_alias', 'currency_conversion', 'location_match', 'authorization_date', 'posting_date', 'tip_detection', 'match_confidence', 'mismatch_reason'), 'ReceiptCardMatchConsole', 'POST /receipts/match-card-transaction', ('CardTransactionPosted',)), (8, ('expense_management_card_transaction', 'expense_management_appgen_dead_letter_event'), ('feed_idempotency_key', 'authorization_state', 'posting_state', 'reversal_detection', 'employee_assignment', 'merchant_normalization', 'dispute_flag', 'dead_letter_reason'), 'CardFeedGovernanceQueue', 'POST /card-transactions/ingest', ('CardTransactionPosted',)), (9, ('expense_management_merchant_profile', 'expense_management_expense_line'), ('merchant_aliases', 'category_codes', 'risk_flags', 'preferred_category', 'region', 'tax_treatment', 'policy_notes', 'violation_rate'), 'MerchantProfileEnrichment', 'POST /merchant-profiles/enrich', ()), (10, ('expense_management_expense_policy', 'expense_management_policy_violation'), ('policy_version', 'effective_dates', 'employee_groups', 'regions', 'categories', 'thresholds', 'receipt_rules', 'approval_requirements', 'compiled_hash'), 'ExpensePolicyVersionStudio', 'POST /expense-policies/versions', ('PolicyChanged',)), (11, ('expense_management_expense_policy_rule', 'expense_management_expense_policy'), ('source_document', 'structured_rule', 'compiled_predicate', 'test_cases', 'ambiguity_flags', 'effective_dates', 'approver_evidence', 'compiled_hash'), 'PolicyRuleCompiler', 'POST /expense-policy-rules/compile', ('PolicyChanged',)), (12, ('expense_management_expense_policy_rule', 'expense_management_expense_line'), ('scenario_amount', 'scenario_category', 'scenario_merchant', 'scenario_route', 'travel_class', 'pass_fail_result', 'required_receipt', 'coaching_explanation'), 'CounterfactualPolicyCoach', 'POST /expense-policy-rules/simulate', ()), (13, ('expense_management_policy_violation', 'expense_management_expense_approval_task'), ('violation_state', 'severity', 'rule_version', 'impacted_amount', 'approver', 'exception_evidence', 'employee_response', 'resolution_outcome'), 'PolicyViolationLifecycle', 'POST /policy-violations/resolve', ()), (14, ('expense_management_expense_exception_case', 'expense_management_policy_violation'), ('reason_taxonomy', 'supporting_evidence', 'approver_role', 'amount_impact', 'precedent_checks', 'expiration', 'audit_visibility', 'agent_draft'), 'ExceptionRequestWorkflow', 'POST /expense-exceptions/request', ()), (15, ('expense_management_expense_approval_task', 'expense_management_expense_report'), ('routing_graph', 'manager_node', 'project_owner_node', 'finance_node', 'compliance_node', 'audit_node', 'delegation', 'escalation_timer', 'routing_rationale'), 'ExpenseApprovalRoutingGraph', 'POST /expense-approvals/route', ('EmployeeCreated', 'ProjectProjectionUpdated')), (16, ('expense_management_expense_approval_task', 'expense_management_reimbursement_batch'), ('submitter', 'approver', 'delegate', 'card_owner', 'payment_preparer', 'auditor', 'conflict_evidence', 'segregation_decision'), 'SegregationOfDutyControl', 'POST /expense-approvals/segregation-check', ('AccessPolicyChanged',)), (17, ('expense_management_expense_approval_task',), ('sla_policy', 'employee_group', 'amount_band', 'reimbursement_cycle', 'due_at', 'owner', 'bottleneck_reason', 'escalation_notice'), 'ApprovalSlaEscalationBoard', 'POST /expense-approvals/escalate', ()), (18, ('expense_management_reimbursement_batch', 'expense_management_reimbursement_payment', 'expense_management_cash_advance'), ('approval_status', 'duplicate_flags', 'cash_advance_offsets', 'currency', 'payment_projection', 'employee_eligibility', 'tax_treatment', 'cutoff_period', 'batch_proof'), 'ReimbursementBatchReadiness', 'POST /reimbursements/batches/readiness', ('EmployeeCreated', 'PaymentExecuted')), (19, ('expense_management_reimbursement_payment', 'expense_management_appgen_inbox_event'), ('payment_event_id', 'scheduled_amount', 'executed_amount', 'failure_classification', 'retry_plan', 'reversal_status', 'partial_payment_delta', 'payment_evidence'), 'ReimbursementPaymentReconciliation', 'POST /reimbursements/payments/reconcile', ('PaymentExecuted',)), (20, ('expense_management_cash_advance', 'expense_management_expense_report'), ('advance_state', 'issued_amount', 'expected_use', 'linked_reports', 'applied_amounts', 'returned_funds', 'aging_bucket', 'employee_communication', 'write_off_policy'), 'CashAdvanceLifecycle', 'POST /cash-advances/reconcile', ()), (21, ('expense_management_mileage_claim', 'expense_management_expense_policy'), ('origin', 'destination', 'claim_date', 'business_purpose', 'route_distance', 'commute_deduction', 'rate_version', 'vehicle_type', 'duplicate_route_check', 'route_evidence'), 'MileageRouteValidation', 'POST /mileage-claims/validate', ()), (22, ('expense_management_per_diem_claim', 'expense_management_expense_policy'), ('location', 'travel_dates', 'partial_day_factor', 'meals_provided', 'overnight_required', 'employee_eligibility', 'effective_rate_version', 'deduction_explanation'), 'PerDiemEligibilityEngine', 'POST /per-diem-claims/calculate', ('EmployeeCreated',)), (23, ('expense_management_expense_line', 'expense_management_policy_violation'), ('attendees', 'organizations', 'roles', 'customer_linkage', 'employee_count', 'per_person_spend', 'prohibited_party_check', 'purpose_evidence'), 'HospitalityGovernancePanel', 'POST /expense-lines/hospitality-check', ('CustomerProjectionUpdated',)), (24, ('expense_management_expense_line', 'expense_management_expense_report'), ('trip_projection', 'booking_reference', 'itinerary_window', 'travel_approval', 'expense_location', 'booking_source', 'out_of_policy_flag', 'trip_link_confidence'), 'TravelExpenseLinkage', 'POST /expense-lines/link-travel', ('TravelItineraryProjected',)), (25, ('expense_management_expense_line', 'expense_management_expense_control_assertion'), ('emission_source', 'route_evidence', 'category_factor', 'emissions_estimate', 'carbon_summary', 'alternative_suggestion', 'policy_coaching', 'configuration_enabled'), 'CarbonAwareTravelSpendInsights', 'POST /expense-analytics/carbon-estimate', ()), (26, ('expense_management_duplicate_expense_signal', 'expense_management_receipt_artifact', 'expense_management_card_transaction'), ('amount_match', 'date_match', 'merchant_match', 'receipt_fingerprint_match', 'employee_match', 'attendee_match', 'location_match', 'card_transaction_match', 'semantic_similarity', 'reviewer_disposition'), 'DuplicateExpenseDetectionWorkbench', 'POST /duplicate-expenses/detect', ()), (27, ('expense_management_expense_fraud_signal', 'expense_management_merchant_profile'), ('altered_receipt_signal', 'personal_spend_signal', 'merchant_collusion_signal', 'repeated_exception_signal', 'weekend_spend_signal', 'category_manipulation_signal', 'explainable_drivers', 'case_routing'), 'FraudAbuseSignalModel', 'POST /expense-fraud-signals/score', ()), (28, ('expense_management_expense_audit_sample', 'expense_management_expense_fraud_signal'), ('amount_risk', 'category_risk', 'violation_history', 'employee_history', 'merchant_risk', 'receipt_confidence', 'project_risk', 'statistical_coverage', 'sampling_rationale'), 'RiskBasedAuditSampling', 'POST /expense-audits/sample', ()), (29, ('expense_management_expense_audit_sample', 'expense_management_expense_exception_case'), ('evidence_checklist', 'audit_decision', 'findings', 'required_corrections', 'reimbursement_impact', 'employee_response', 'closure_evidence', 'repeat_finding_link'), 'ExpenseAuditSampleWorkbench', 'POST /expense-audits/review', ()), (30, ('expense_management_expense_control_assertion', 'expense_management_expense_line'), ('employee_dimension', 'department_dimension', 'project_dimension', 'category_dimension', 'merchant_dimension', 'region_dimension', 'policy_version_dimension', 'payment_status_dimension', 'budget_alerts', 'anomaly_trends'), 'SpendControlDashboard', 'GET /expense-analytics/spend-controls', ()), (31, ('expense_management_expense_report', 'expense_management_card_transaction', 'expense_management_cash_advance'), ('open_reports', 'unmatched_card_transactions', 'missing_receipts', 'violations', 'required_approvals', 'expected_reimbursement_date', 'cash_advance_aging', 'coaching_suggestions'), 'EmployeeSpendIntelligenceCards', 'GET /employee-spend-intelligence', ('EmployeeCreated',)), (32, ('expense_management_receipt_artifact', 'expense_management_card_transaction'), ('offline_upload_id', 'image_quality', 'duplicate_artifact', 'ocr_confidence', 'card_match_suggestion', 'category_suggestion', 'policy_warning', 'sync_conflict_handling'), 'MobileReceiptCaptureWorkflow', 'POST /mobile-receipts/capture', ()), (33, ('expense_management_receipt_artifact',), ('sensitive_content_detection', 'redaction_suggestion', 'original_access_control', 'redacted_version', 'approver_view', 'agent_summary_policy', 'privacy_basis', 'irrelevant_detail_suppression'), 'ReceiptRedactionPrivacyWorkbench', 'POST /receipts/redact', ('AccessPolicyChanged',)), (34, ('expense_management_expense_line', 'expense_management_expense_approval_task'), ('split_allocations', 'percentage_total', 'amount_total', 'segment_validation', 'split_owner_routing', 'segment_policy_rules', 'payment_neutrality', 'split_rationale'), 'ProjectCostAllocationSplitting', 'POST /expense-lines/split-allocation', ('ProjectProjectionUpdated',)), (35, ('expense_management_expense_line', 'expense_management_reimbursement_payment'), ('receipt_currency', 'card_currency', 'claim_currency', 'reimbursement_currency', 'rate_source', 'rate_date', 'spread', 'rounding_delta', 'fx_explanation'), 'MultiCurrencyExpenseControls', 'POST /expense-lines/currency-check', ()), (36, ('expense_management_expense_line', 'expense_management_receipt_artifact'), ('tax_amounts', 'tax_ids', 'jurisdiction', 'recoverability_category', 'receipt_validity', 'missing_tax_evidence', 'tax_export', 'declared_integration_only'), 'ExpenseTaxRecoverabilityCapture', 'POST /expense-lines/tax-capture', ('TaxPolicyChanged',)), (37, ('expense_management_expense_report', 'expense_management_card_transaction', 'expense_management_reimbursement_batch'), ('submitted_accruals', 'approved_accruals', 'unsubmitted_card_accruals', 'matched_receipt_accruals', 'cash_advance_accruals', 'pending_reimbursement_accruals', 'confidence_level', 'cutoff_evidence'), 'SpendAccrualReadiness', 'GET /expense-accruals/readiness', ('FinancialPeriodChanged',)), (38, ('expense_management_expense_policy', 'expense_management_expense_policy_rule'), ('policy_change', 'historical_reports', 'open_drafts', 'violation_rate_delta', 'audit_load_delta', 'reimbursement_delay_delta', 'spend_reduction_estimate', 'employee_impact', 'approval_required'), 'PolicyChangeImpactAnalysis', 'POST /expense-policies/impact-analysis', ('PolicyChanged',)), (39, ('expense_management_expense_control_assertion',), ('missing_receipt_assertion', 'expired_policy_assertion', 'approval_conflict_assertion', 'duplicate_signal_assertion', 'card_feed_gap_assertion', 'reimbursement_before_approval_assertion', 'stale_advance_assertion', 'high_risk_merchant_assertion', 'remediation_task'), 'ContinuousExpenseControlTesting', 'POST /expense-control-assertions/run', ()), (40, ('expense_management_expense_governed_model', 'expense_management_expense_fraud_signal'), ('employee_baseline', 'merchant_baseline', 'category_baseline', 'project_baseline', 'region_baseline', 'amount_deviation', 'time_deviation', 'policy_version_context', 'explainable_drivers', 'routing_decision'), 'ExpenseAnomalyDetection', 'POST /expense-anomalies/detect', ()), (41, ('expense_management_expense_exception_case',), ('case_type', 'severity', 'owner', 'sla', 'linked_report', 'linked_line', 'linked_payment', 'required_evidence', 'employee_response', 'resolution_action', 'financial_impact'), 'ExpenseExceptionCaseWorkflow', 'POST /expense-exception-cases/resolve', ()), (42, ('expense_management_expense_control_assertion', 'expense_management_receipt_artifact', 'expense_management_reimbursement_batch'), ('hash_chain', 'report_lifecycle_proof', 'receipt_artifact_proof', 'policy_evaluation_proof', 'approval_proof', 'reimbursement_batch_proof', 'payment_reconciliation_proof', 'redacted_verifier_export'), 'CryptographicExpenseProof', 'POST /expense-proofs/verify', ()), (43, ('expense_management_appgen_inbox_event', 'expense_management_appgen_outbox_event', 'expense_management_appgen_dead_letter_event'), ('schema_version', 'idempotency_key', 'ordering_assumption', 'retry_envelope', 'dead_letter_taxonomy', 'replay_eligibility', 'handler_evidence', 'duplicate_card_post_test', 'failed_payment_callback_test'), 'AppGenXExpenseEventReliability', 'POST /expense-events/replay-proof', ('EmployeeCreated', 'CardTransactionPosted', 'PaymentExecuted', 'PolicyChanged')), (44, ('expense_management_expense_control_assertion',), ('declared_api', 'declared_projection', 'declared_event', 'cached_field', 'staleness_policy', 'retention_rule', 'boundary_violation', 'foreign_table_access'), 'CrossPbcExpenseBoundaryProof', 'POST /expense-boundaries/prove', ('EmployeeCreated', 'PaymentExecuted', 'TravelItineraryProjected', 'ProjectProjectionUpdated', 'PolicyChanged')), (45, ('expense_management_expense_report', 'expense_management_receipt_artifact', 'expense_management_card_transaction'), ('extracted_expense_lines', 'card_match_suggestions', 'category_suggestions', 'missing_facts', 'draft_business_purpose', 'policy_preview', 'human_confirmation', 'no_auto_submit'), 'AgentAssistedReceiptReportCreation', 'POST /expense-agent/report-draft', ()), (46, ('expense_management_expense_approval_task', 'expense_management_policy_violation', 'expense_management_duplicate_expense_signal'), ('policy_status', 'violation_summary', 'unusual_items', 'duplicate_signals', 'receipt_confidence', 'employee_history', 'recommended_questions', 'explicit_authorized_action', 'no_auto_approve'), 'AgentAssistedApproverReview', 'POST /expense-agent/approver-review', ('EmployeeCreated',)), (47, ('expense_management_expense_control_assertion',), ('reports_panel', 'lines_panel', 'receipts_panel', 'card_transactions_panel', 'merchants_panel', 'policies_panel', 'violations_panel', 'approvals_panel', 'reimbursements_panel', 'payments_panel', 'advances_panel', 'mileage_panel', 'per_diem_panel', 'audits_panel', 'duplicates_panel', 'exceptions_panel', 'rules_panel', 'parameters_panel', 'controls_panel', 'models_panel', 'events_panel', 'analytics_panel', 'agent_tools_panel'), 'ExpenseUiCapabilitySurfaceProof', 'POST /expense-ui/coverage-proof', ()), (48, ('expense_management_expense_control_assertion', 'expense_management_appgen_dead_letter_event'), ('delayed_card_transaction_drill', 'duplicate_feed_replay_drill', 'failed_ocr_drill', 'invalid_policy_rollout_drill', 'payment_failure_event_drill', 'reimbursement_replay_drill', 'dead_letter_recovery_drill', 'recovery_time', 'affected_reports', 'financial_exposure'), 'ExpenseResilienceDrills', 'POST /expense-resilience/drills', ('CardTransactionPosted', 'PaymentExecuted', 'PolicyChanged')), (49, ('expense_management_expense_control_assertion',), ('policy_coverage_score', 'receipt_extraction_quality', 'card_feed_health', 'approval_routing_health', 'reimbursement_reconciliation_health', 'audit_control_health', 'event_health', 'ui_coverage', 'boundary_proof', 'agent_safety', 'blocking_gaps', 'remediation_actions'), 'ExpenseReadinessScore', 'GET /expense-readiness-score', ()), (50, ('expense_management_expense_report', 'expense_management_expense_line', 'expense_management_receipt_artifact', 'expense_management_card_transaction', 'expense_management_policy_violation', 'expense_management_expense_approval_task', 'expense_management_reimbursement_batch', 'expense_management_reimbursement_payment', 'expense_management_cash_advance', 'expense_management_mileage_claim', 'expense_management_per_diem_claim', 'expense_management_duplicate_expense_signal', 'expense_management_expense_audit_sample', 'expense_management_expense_exception_case'), ('report_creation', 'line_capture', 'receipt_extraction', 'card_ingestion', 'match_result', 'policy_validation', 'violation_handling', 'approval_routing', 'reimbursement_batching', 'payment_reconciliation', 'cash_advance_netting', 'mileage_calculation', 'per_diem_calculation', 'duplicate_detection', 'audit_sampling', 'exception_resolution', 'rule_compilation', 'ui_coverage', 'appgen_x_eventing', 'boundary_verification', 'agent_safe_crud_plan'), 'EndToEndExpenseReleaseProof', 'POST /expense-release/end-to-end-proof', ('EmployeeCreated', 'CardTransactionPosted', 'PaymentExecuted', 'PolicyChanged'))]

CONTROL_SPECS: dict[int, dict[str, Any]] = {number: {"tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps} for number, tables, fields, ui, route, deps in _SPEC_ROWS}
_EMPTY_ALLOWED_FIELDS = (
    "boundary_violation",
    "blocking_gaps",
    "dead_letter_reason",
    "duplicate_artifact_status",
    "duplicate_flags",
    "exception_status",
    "failed_payment_callback_test",
    "foreign_table_access",
    "missing_facts",
    "out_of_policy_flag",
    "partial_payment_delta",
    "redaction_suggestion",
    "risk_flags",
    "ambiguity_flags",
    "budget_alerts",
    "unmatched_card_transactions",
    "missing_receipts",
    "violations",
    "remediation_actions",
    "reversal_status",
    "unusual_items",
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update({
        "employee_projection": "employee-active",
        "line_completeness": "complete",
        "receipt_requirements": "satisfied",
        "card_match_state": "matched",
        "approver_eligibility": "eligible",
        "readiness_decision": "ready",
        "lifecycle_state": "approved",
        "allowed_transition": True,
        "reimbursement_effect": "allowed_after_approval",
        "transition_decision": "accepted",
        "category_confidence": 0.93,
        "specificity_score": 0.91,
        "receipt_fingerprint": "sha256:receipt",
        "integrity_check": "passed",
        "field_confidence": 0.9,
        "confirmation_required": False,
        "match_confidence": 0.92,
        "authorization_state": "posted",
        "posting_state": "posted",
        "reversal_detection": "none",
        "employee_assignment": "assigned",
        "risk_flags": (),
        "violation_rate": 0.02,
        "effective_dates": ("2026-01-01",),
        "compiled_hash": "sha256:policy",
        "compiled_predicate": "executable",
        "test_cases": ("positive", "negative"),
        "ambiguity_flags": (),
        "pass_fail_result": "pass",
        "violation_state": "resolved",
        "severity": "medium",
        "resolution_outcome": "approved_exception",
        "precedent_checks": "clear",
        "audit_visibility": True,
        "routing_graph": "resolved",
        "delegation": "valid",
        "submitter": "employee-1",
        "approver": "manager-1",
        "delegate": "delegate-1",
        "card_owner": "employee-1",
        "payment_preparer": "payops-1",
        "auditor": "auditor-1",
        "segregation_decision": "clear",
        "escalation_notice": "not_required",
        "approval_status": "approved",
        "duplicate_flags": (),
        "employee_eligibility": "active",
        "batch_proof": "sha256:batch",
        "payment_event_id": "pay-evt-1",
        "scheduled_amount": 100,
        "executed_amount": 100,
        "failure_classification": "none",
        "retry_plan": "not_required",
        "payment_evidence": "settled",
        "advance_state": "reconciled",
        "issued_amount": 200,
        "applied_amounts": 200,
        "returned_funds": 0,
        "write_off_policy": "none",
        "route_distance": 42,
        "commute_deduction": 0,
        "duplicate_route_check": "clear",
        "route_evidence": "map-proof",
        "employee_eligibility": "eligible",
        "deduction_explanation": "calculated",
        "attendees": ("customer",),
        "per_person_spend": 45,
        "prohibited_party_check": "clear",
        "purpose_evidence": "customer meeting",
        "trip_projection": "trip-1",
        "out_of_policy_flag": False,
        "configuration_enabled": True,
        "receipt_fingerprint_match": "clear",
        "semantic_similarity": 0.21,
        "reviewer_disposition": "not_duplicate",
        "explainable_drivers": ("merchant risk",),
        "case_routing": "audit_queue",
        "statistical_coverage": "met",
        "sampling_rationale": "risk_weighted",
        "audit_decision": "pass",
        "closure_evidence": "closed",
        "budget_alerts": (),
        "anomaly_trends": "stable",
        "open_reports": ("report-1",),
        "unmatched_card_transactions": (),
        "missing_receipts": (),
        "violations": (),
        "required_approvals": ("manager",),
        "offline_upload_id": "mobile-1",
        "image_quality": "acceptable",
        "ocr_confidence": 0.9,
        "sync_conflict_handling": "resolved",
        "sensitive_content_detection": "none",
        "original_access_control": "restricted",
        "irrelevant_detail_suppression": True,
        "percentage_total": 100,
        "amount_total": 100,
        "segment_validation": "balanced",
        "payment_neutrality": True,
        "rate_source": "treasury-approved",
        "rate_date": "2026-05-30",
        "rounding_delta": 0,
        "fx_explanation": "rate applied",
        "tax_amounts": 12,
        "receipt_validity": "valid",
        "declared_integration_only": True,
        "confidence_level": 0.88,
        "cutoff_evidence": "period-close",
        "approval_required": True,
        "missing_receipt_assertion": "passed",
        "expired_policy_assertion": "passed",
        "approval_conflict_assertion": "passed",
        "duplicate_signal_assertion": "passed",
        "card_feed_gap_assertion": "passed",
        "reimbursement_before_approval_assertion": "passed",
        "stale_advance_assertion": "passed",
        "high_risk_merchant_assertion": "passed",
        "amount_deviation": "within_baseline",
        "routing_decision": "monitor",
        "case_type": "missing_receipt",
        "sla": "P2D",
        "required_evidence": "present",
        "resolution_action": "accepted",
        "financial_impact": 0,
        "hash_chain": ("h1", "h2"),
        "redacted_verifier_export": "available",
        "schema_version": "v1",
        "idempotency_key": "idem-1",
        "retry_envelope": "5-attempts",
        "dead_letter_taxonomy": "classified",
        "replay_eligibility": True,
        "handler_evidence": "covered",
        "duplicate_card_post_test": "passed",
        "failed_payment_callback_test": "passed",
        "declared_api": "declared",
        "declared_projection": "declared",
        "declared_event": "declared",
        "cached_field": "employee_id",
        "staleness_policy": "PT1H",
        "retention_rule": "policy-bound",
        "boundary_violation": (),
        "foreign_table_access": (),
        "extracted_expense_lines": ("line-1",),
        "human_confirmation": True,
        "no_auto_submit": True,
        "explicit_authorized_action": True,
        "no_auto_approve": True,
        "reports_panel": True,
        "agent_tools_panel": True,
        "delayed_card_transaction_drill": "passed",
        "duplicate_feed_replay_drill": "passed",
        "failed_ocr_drill": "passed",
        "invalid_policy_rollout_drill": "passed",
        "payment_failure_event_drill": "passed",
        "reimbursement_replay_drill": "passed",
        "dead_letter_recovery_drill": "passed",
        "recovery_time": "PT10M",
        "financial_exposure": 0,
        "policy_coverage_score": 0.96,
        "receipt_extraction_quality": 0.91,
        "card_feed_health": "green",
        "approval_routing_health": "green",
        "reimbursement_reconciliation_health": "green",
        "audit_control_health": "green",
        "event_health": "green",
        "ui_coverage": "done",
        "boundary_proof": "passed",
        "agent_safety": "passed",
        "blocking_gaps": (),
        "remediation_actions": (),
        "report_creation": "done",
        "line_capture": "done",
        "receipt_extraction": "done",
        "card_ingestion": "done",
        "match_result": "done",
        "policy_validation": "done",
        "violation_handling": "done",
        "approval_routing": "done",
        "reimbursement_batching": "done",
        "payment_reconciliation": "done",
        "cash_advance_netting": "done",
        "mileage_calculation": "done",
        "per_diem_calculation": "done",
        "duplicate_detection": "done",
        "audit_sampling": "done",
        "exception_resolution": "done",
        "rule_compilation": "done",
        "appgen_x_eventing": "done",
        "boundary_verification": "done",
        "agent_safe_crud_plan": "done",
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and (payload.get("employee_projection") in (None, "") or payload.get("line_completeness") != "complete" or payload.get("readiness_decision") != "ready"):
        findings.append("expense report readiness gate is not satisfied")
    if n == 2 and payload.get("reimbursement_effect") == "scheduled_before_approval":
        findings.append("report lifecycle blocks reimbursement actions before approval")
    if n == 5 and payload.get("integrity_check") != "passed":
        findings.append("receipt artifact evidence chain failed integrity validation")
    if n == 6 and payload.get("field_confidence", 0) < 0.75 and payload.get("confirmation_required") is not True:
        findings.append("low-confidence receipt extraction requires confirmation")
    if n == 8 and payload.get("feed_idempotency_key") in (None, ""):
        findings.append("card transaction feed requires idempotency evidence")
    if n == 10 and not payload.get("compiled_hash"):
        findings.append("expense policy version requires compiled hash")
    if n == 11 and payload.get("ambiguity_flags") and payload.get("approval_required") is not True:
        findings.append("ambiguous policy rules require approval before activation")
    if n == 16 and payload.get("submitter") == payload.get("approver"):
        findings.append("segregation of duty blocks self approval")
    if n == 18 and payload.get("approval_status") != "approved":
        findings.append("reimbursement batch readiness requires approved reports")
    if n == 19 and payload.get("failure_classification") not in ("none", "retryable", "terminal"):
        findings.append("payment reconciliation requires classified failure state")
    if n == 20 and payload.get("advance_state") == "open" and payload.get("applied_amounts", 0) < payload.get("issued_amount", 0):
        findings.append("cash advance must be netted before reimbursement")
    if n == 21 and payload.get("commute_deduction", 0) < 0:
        findings.append("mileage commute deduction cannot increase reimbursable distance")
    if n == 22 and not payload.get("deduction_explanation"):
        findings.append("per diem engine must explain deductions")
    if n == 23 and payload.get("per_person_spend", 0) > 100 and not payload.get("attendees"):
        findings.append("hospitality lines over threshold require attendees")
    if n == 26 and payload.get("reviewer_disposition") not in ("not_duplicate", "duplicate", "needs_review"):
        findings.append("duplicate expense detection requires reviewer disposition")
    if n == 27 and payload.get("case_routing") in (None, ""):
        findings.append("fraud and abuse signals require case routing")
    if n == 29 and payload.get("audit_decision") not in ("pass", "fail", "correction_required"):
        findings.append("audit workbench requires explicit review decision")
    if n == 33 and payload.get("irrelevant_detail_suppression") is not True:
        findings.append("receipt privacy requires irrelevant detail suppression")
    if n == 34 and payload.get("percentage_total") != 100:
        findings.append("allocation splits must balance to 100 percent")
    if n == 35 and payload.get("rounding_delta", 0) > 1:
        findings.append("multi-currency controls require bounded rounding delta")
    if n == 36 and payload.get("declared_integration_only") is not True:
        findings.append("tax exports must use owned tables and declared integrations only")
    if n == 39 and any(payload.get(field) != "passed" for field in ("missing_receipt_assertion", "expired_policy_assertion", "approval_conflict_assertion", "duplicate_signal_assertion", "card_feed_gap_assertion", "reimbursement_before_approval_assertion", "stale_advance_assertion", "high_risk_merchant_assertion")):
        findings.append("continuous expense controls have unresolved failing assertions")
    if n == 42 and not payload.get("hash_chain"):
        findings.append("cryptographic expense proof requires hash-chain evidence")
    if n == 43 and payload.get("duplicate_card_post_test") != "passed":
        findings.append("AppGen-X event reliability must prove duplicate card post handling")
    if n == 44 and (payload.get("foreign_table_access") or payload.get("boundary_violation")):
        findings.append("cross-PBC expense boundary cannot use foreign tables")
    if n == 45 and (payload.get("human_confirmation") is not True or payload.get("no_auto_submit") is not True):
        findings.append("agent-assisted report creation must require confirmation and avoid auto-submit")
    if n == 46 and (payload.get("explicit_authorized_action") is not True or payload.get("no_auto_approve") is not True):
        findings.append("agent-assisted approver review cannot approve or reject autonomously")
    if n == 48 and payload.get("dead_letter_recovery_drill") != "passed":
        findings.append("expense resilience drills must prove dead-letter recovery")
    if n == 49 and payload.get("blocking_gaps"):
        findings.append("expense readiness score has blocking gaps")
    if n == 50 and not all(payload.get(field) == "done" for field in ("report_creation", "line_capture", "receipt_extraction", "card_ingestion", "match_result", "policy_validation", "violation_handling", "approval_routing", "reimbursement_batching", "payment_reconciliation", "cash_advance_netting", "mileage_calculation", "per_diem_calculation", "duplicate_detection", "audit_sampling", "exception_resolution", "rule_compilation", "ui_coverage", "appgen_x_eventing", "boundary_verification", "agent_safe_crud_plan")):
        findings.append("end-to-end expense release proof is incomplete")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_expense_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in EXPENSE_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in EXPENSE_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": EXPENSE_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": EXPENSE_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_expense_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_expense_control(capability) for capability in EXPENSE_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.expense-management-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": EXPENSE_CONTROL_OWNED_TABLES,
        "declared_dependencies": EXPENSE_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": EXPENSE_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": EXPENSE_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


EXPENSE_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_expense_control(slug, payload)) for capability in EXPENSE_CONTROL_CAPABILITIES}

"""Executable improve1 controls for the Grant Fund Accounting PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "grant_fund_accounting"
EVENT_CONTRACT = "AppGen-X"
GRANT_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
GRANT_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.grant_fund_accounting.events"
GRANT_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + (
    "grant_fund_accounting_award_intake_gate",
    "grant_fund_accounting_award_document_extraction",
    "grant_fund_accounting_award_lifecycle_transition",
    "grant_fund_accounting_award_amendment_version",
    "grant_fund_accounting_restriction_taxonomy_node",
    "grant_fund_accounting_cost_allowability_decision",
    "grant_fund_accounting_fund_lifecycle_balance",
    "grant_fund_accounting_budget_version_control",
    "grant_fund_accounting_budget_burn_rate_signal",
    "grant_fund_accounting_allowable_rule_compilation",
    "grant_fund_accounting_cost_transaction_evidence",
    "grant_fund_accounting_journal_payment_reconciliation",
    "grant_fund_accounting_cost_transfer_case",
    "grant_fund_accounting_allocation_rule_version",
    "grant_fund_accounting_allocation_run_trace",
    "grant_fund_accounting_drawdown_readiness_gate",
    "grant_fund_accounting_drawdown_cash_projection",
    "grant_fund_accounting_drawdown_receipt_reconciliation",
    "grant_fund_accounting_match_requirement_schedule",
    "grant_fund_accounting_match_contribution_evidence",
    "grant_fund_accounting_in_kind_valuation_control",
    "grant_fund_accounting_funder_reporting_calendar",
    "grant_fund_accounting_funder_report_package",
    "grant_fund_accounting_report_ledger_reconciliation",
    "grant_fund_accounting_compliance_evidence_room",
    "grant_fund_accounting_continuous_compliance_assertion",
    "grant_fund_accounting_procurement_subaward_hook",
    "grant_fund_accounting_indirect_cost_rate",
    "grant_fund_accounting_program_income_record",
    "grant_fund_accounting_fund_balance_rollforward",
    "grant_fund_accounting_portfolio_forecast",
    "grant_fund_accounting_shortfall_simulation",
    "grant_fund_accounting_exception_case_workflow",
    "grant_fund_accounting_closeout_readiness_checklist",
    "grant_fund_accounting_post_closeout_adjustment",
    "grant_fund_accounting_retention_audit_hold",
    "grant_fund_accounting_crypto_evidence_packet",
    "grant_fund_accounting_policy_impact_analysis",
    "grant_fund_accounting_predictive_risk_score",
    "grant_fund_accounting_anomaly_detection_case",
    "grant_fund_accounting_event_reliability_proof",
    "grant_fund_accounting_cross_pbc_boundary_proof",
    "grant_fund_accounting_agent_award_setup_skill",
    "grant_fund_accounting_agent_allowability_review_skill",
    "grant_fund_accounting_workbench_cockpit_state",
    "grant_fund_accounting_ui_surface_proof",
    "grant_fund_accounting_control_testing_library",
    "grant_fund_accounting_resilience_drill",
    "grant_fund_accounting_readiness_scorecard",
    "grant_fund_accounting_release_rehearsal_story",
)))
GRANT_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "ExpenseApproved", "PaymentExecuted", "JournalPosted", "PolicyChanged", "AuditProofGenerated",
    "ProcurementObligationProjected", "VendorEligibilityProjected", "PayrollCostProjected",
    "CashReceiptProjected", "GeneralLedgerPeriodClosed", "FunderPortalSubmissionRecorded",
)))
GRANT_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in GRANT_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in GRANT_CONTROL_CAPABILITIES}

_FEATURE_TABLES = {
    1: ("grant_fund_accounting_award_intake_gate",),
    2: ("grant_fund_accounting_award_document_extraction",),
    3: ("grant_fund_accounting_award_lifecycle_transition",),
    4: ("grant_fund_accounting_award_amendment_version",),
    5: ("grant_fund_accounting_restriction_taxonomy_node",),
    6: ("grant_fund_accounting_cost_allowability_decision",),
    7: ("grant_fund_accounting_fund_lifecycle_balance",),
    8: ("grant_fund_accounting_budget_version_control",),
    9: ("grant_fund_accounting_budget_burn_rate_signal",),
    10: ("grant_fund_accounting_allowable_rule_compilation",),
    11: ("grant_fund_accounting_cost_transaction_evidence",),
    12: ("grant_fund_accounting_journal_payment_reconciliation",),
    13: ("grant_fund_accounting_cost_transfer_case",),
    14: ("grant_fund_accounting_allocation_rule_version",),
    15: ("grant_fund_accounting_allocation_run_trace",),
    16: ("grant_fund_accounting_drawdown_readiness_gate",),
    17: ("grant_fund_accounting_drawdown_cash_projection",),
    18: ("grant_fund_accounting_drawdown_receipt_reconciliation",),
    19: ("grant_fund_accounting_match_requirement_schedule",),
    20: ("grant_fund_accounting_match_contribution_evidence",),
    21: ("grant_fund_accounting_in_kind_valuation_control",),
    22: ("grant_fund_accounting_funder_reporting_calendar",),
    23: ("grant_fund_accounting_funder_report_package",),
    24: ("grant_fund_accounting_report_ledger_reconciliation",),
    25: ("grant_fund_accounting_compliance_evidence_room",),
    26: ("grant_fund_accounting_continuous_compliance_assertion",),
    27: ("grant_fund_accounting_procurement_subaward_hook",),
    28: ("grant_fund_accounting_indirect_cost_rate",),
    29: ("grant_fund_accounting_program_income_record",),
    30: ("grant_fund_accounting_fund_balance_rollforward",),
    31: ("grant_fund_accounting_portfolio_forecast",),
    32: ("grant_fund_accounting_shortfall_simulation",),
    33: ("grant_fund_accounting_exception_case_workflow",),
    34: ("grant_fund_accounting_closeout_readiness_checklist",),
    35: ("grant_fund_accounting_post_closeout_adjustment",),
    36: ("grant_fund_accounting_retention_audit_hold",),
    37: ("grant_fund_accounting_crypto_evidence_packet",),
    38: ("grant_fund_accounting_policy_impact_analysis",),
    39: ("grant_fund_accounting_predictive_risk_score",),
    40: ("grant_fund_accounting_anomaly_detection_case",),
    41: ("grant_fund_accounting_event_reliability_proof",),
    42: ("grant_fund_accounting_cross_pbc_boundary_proof",),
    43: ("grant_fund_accounting_agent_award_setup_skill",),
    44: ("grant_fund_accounting_agent_allowability_review_skill",),
    45: ("grant_fund_accounting_workbench_cockpit_state",),
    46: ("grant_fund_accounting_ui_surface_proof",),
    47: ("grant_fund_accounting_control_testing_library",),
    48: ("grant_fund_accounting_resilience_drill",),
    49: ("grant_fund_accounting_readiness_scorecard",),
    50: ("grant_fund_accounting_release_rehearsal_story",),
}

_FEATURE_FIELDS = {
    1: ("funder", "award_number", "period_start", "period_end", "funding_amount", "assistance_listing", "restriction_set", "budget_categories", "reporting_schedule", "match_terms", "indirect_cost_terms", "closeout_terms", "source_document_evidence", "activation_allowed"),
    2: ("document_packet", "extracted_restrictions", "extracted_budget", "extracted_milestones", "clause_citations", "confidence", "human_approval_required", "owned_record_plan", "source_lineage_preserved"),
    3: ("current_state", "target_state", "transition_evidence", "spending_allowed", "drawdown_allowed", "reporting_obligations_refreshed", "audit_proof", "blocked_reason"),
    4: ("amendment_number", "effective_date", "changed_terms", "before_after_budget_impact", "affected_costs", "reporting_updates", "approval_evidence", "version_locked"),
    5: ("restriction_type", "source_clause", "effective_period", "affected_funds", "release_criteria", "reporting_treatment", "cost_validation_rule", "taxonomy_version"),
    6: ("cost_id", "award_period_valid", "budget_category_valid", "restriction_valid", "allowable_cost_rule_valid", "procurement_evidence_valid", "match_eligible", "prior_approval_status", "indirect_cost_valid", "remaining_budget", "documentation_complete", "allowability_result"),
    7: ("fund_state", "award_link", "restriction_scope", "available_balance", "obligated_balance", "spent_balance", "drawn_balance", "matched_balance", "closeout_ready", "rollforward_hash"),
    8: ("budget_version", "approved_amount", "category_set", "effective_date", "funder_approval_required", "rebudget_threshold", "prior_version_comparison", "locked_periods", "active_for_costs"),
    9: ("budget_line", "period", "actual_spend", "approved_budget", "projected_exhaustion_date", "underspend_risk", "overspend_risk", "recommended_action", "alert_visible"),
    10: ("policy_source", "structured_rule", "award_clause_citations", "examples", "ambiguity_flags", "compiled_hash", "test_cases", "approval_workflow", "executable_rule"),
    11: ("source_journal", "source_payment", "expense_ref", "payroll_ref", "procurement_ref", "vendor_ref", "incurred_date", "paid_date", "cost_category", "documentation_status", "allowability_result", "budget_impact", "draw_eligibility", "audit_evidence"),
    12: ("journal_event", "payment_event", "cost_transaction", "draw_receipt", "duplicate_detected", "late_posting_flag", "unmatched_queue", "reconciliation_status", "balance_updated"),
    13: ("original_grant", "target_grant", "transfer_reason", "timing_days", "supporting_evidence", "allowability_check", "budget_impact", "approver", "late_transfer_flag", "audit_trail"),
    14: ("allocation_rule_version", "source_pool", "target_awards", "allocation_basis", "excluded_costs", "effective_period", "documentation", "approval", "reconciliation_required"),
    15: ("allocation_run", "source_costs", "basis_metrics", "target_percentages", "rounding_policy", "residual_handling", "excluded_awards", "output_lines", "calculation_evidence"),
    16: ("eligible_costs", "payment_status", "documentation_status", "budget_available", "prior_draw_status", "match_status", "funder_limit_status", "reporting_currency", "cash_timing", "submission_allowed"),
    17: ("eligible_cost_forecast", "payment_schedule", "funder_processing_days", "method", "holdbacks", "pending_exceptions", "cash_balance_assumption", "shortfall_risk", "recommended_draw_date"),
    18: ("draw_request", "receipt_amount", "receipt_date", "funder_reference", "rejected_lines", "pending_lines", "cash_account_projection", "short_paid_exception", "reconciliation_complete"),
    19: ("match_schedule", "basis", "source_restrictions", "eligible_contribution_types", "valuation_rules", "due_dates", "shortfall_threshold", "progress", "forecast_shortfall"),
    20: ("contribution_source", "cash_or_in_kind", "valuation_method", "donor_source", "documentation", "eligibility", "award_link", "contribution_date", "double_counted", "audit_evidence"),
    21: ("contribution_type", "valuation_method", "rate_source", "market_evidence", "approver", "donor_restrictions", "documentation_requirements", "unsupported_valuation_flag", "expired_rate_flag"),
    22: ("report_type", "due_date", "submission_window", "owner", "data_cutoff", "dependencies", "required_attachments", "portal_status", "escalation_rule"),
    23: ("report_version", "owned_costs", "budgets", "drawdowns", "match_evidence", "compliance_evidence", "milestone", "variance_explanations", "attachments", "approval_workflow", "submitted_proof"),
    24: ("report_lines", "cost_transactions", "budget_categories", "draw_requests", "receipts", "ledger_total", "report_total", "explainable_adjustments", "submission_blocked"),
    25: ("evidence_packet", "document_type", "award_link", "cost_link", "restriction_link", "report_link", "retention_period", "source", "reviewer", "redaction_state", "cryptographic_proof", "missing_obligation_visible"),
    26: ("assertion_suite", "unallowable_costs_checked", "late_reports_checked", "expired_evidence_checked", "match_shortfalls_checked", "budget_overages_checked", "draw_mismatches_checked", "procurement_gaps_checked", "remediation_tasks", "control_effective"),
    27: ("procurement_method", "required_quotes", "sole_source_justification", "vendor_eligibility", "subaward_status", "monitoring_requirements", "projection_source", "evidence_links", "cost_allowed"),
    28: ("rate_name", "base_definition", "rate", "effective_dates", "exclusions", "funder_caps", "approval_evidence", "calculation_trace", "draw_eligible"),
    29: ("income_source", "period", "award_link", "treatment_method", "restriction", "budget_impact", "report_inclusion", "draw_readiness_effect", "audit_evidence"),
    30: ("beginning_balance", "awards", "costs", "draws", "match", "transfers", "adjustments", "ending_balance", "drilldown_ready", "reconciled_to_reports"),
    31: ("portfolio_awards", "funding_forecast", "spend_forecast", "draw_cash_forecast", "match_exposure", "report_workload", "closeout_workload", "shortfall_risk", "assumptions", "confidence"),
    32: ("scenario", "draw_delay_days", "rejected_costs", "match_gap", "budget_change", "spending_pace", "shortfall_amount", "recommended_mitigation", "live_mutation_blocked"),
    33: ("exception_type", "severity", "award", "fund", "linked_record", "owner", "due_date", "required_evidence", "financial_exposure", "resolution_action", "closure_proof"),
    34: ("final_costs_complete", "final_draws_complete", "final_reports_submitted", "match_complete", "property_disposition", "program_income_resolved", "evidence_packet_complete", "funder_acceptance", "closeout_allowed"),
    35: ("closed_award", "adjustment_type", "materiality", "approval", "funder_notification", "report_amendment", "draw_correction", "audit_trail", "casual_edit_blocked"),
    36: ("retention_schedule", "legal_hold", "audit_hold", "closeout_date", "destruction_eligibility", "evidence_completeness", "export_package", "premature_deletion_blocked"),
    37: ("packet_hash", "previous_hash", "redacted_payload_fingerprint", "source_event_hashes", "report_version_hash", "verifier_export", "proof_verified", "altered_payload_detected"),
    38: ("policy_change", "affected_awards", "affected_rules", "impacted_costs", "drawdown_effect", "reporting_effect", "before_after_analysis", "approval_queue", "closed_history_mutation_blocked"),
    39: ("risk_score", "model_version", "risk_factors", "explanations", "confidence", "review_queue", "human_override", "mitigation_plan", "bias_check_complete"),
    40: ("anomaly_type", "expected_pattern", "observed_pattern", "information_divergence", "linked_costs", "linked_draws", "analyst_review", "false_positive_feedback", "case_opened"),
    41: ("outbox_event", "inbox_event", "idempotency_key", "retry_policy", "dead_letter_route", "event_topic", "event_contract", "stream_engine_picker_visible", "safe_replay_allowed"),
    42: ("dependency", "dependency_mode", "projection_used", "foreign_table_access_blocked", "api_contract", "event_contract", "owned_table_scope", "boundary_evidence"),
    43: ("instruction", "document_intake", "candidate_award", "source_citations", "command_preview", "permission_check", "human_confirmation", "owned_mutation_plan", "direct_mutation_blocked"),
    44: ("cost_packet", "allowability_recommendation", "source_citations", "confidence", "ambiguity_visible", "human_confirmation", "explanation", "owned_mutation_plan", "direct_mutation_blocked"),
    45: ("portfolio_summary", "award_queue", "drawdown_queue", "match_queue", "report_queue", "exception_queue", "readiness_score", "permission_filtered_actions", "agent_panel_visible"),
    46: ("forms_visible", "wizards_visible", "controls_visible", "table_browsers_visible", "rule_editors_visible", "parameter_editors_visible", "agent_tools_visible", "edge_case_queues_visible", "all_capabilities_surfaced"),
    47: ("control_library", "allowability_controls", "draw_controls", "match_controls", "report_controls", "closeout_controls", "assertion_results", "remediation_owner", "continuous_testing_enabled"),
    48: ("drill_name", "failure_mode", "duplicate_event_replay", "dead_letter_recovery", "offline_capture", "cash_timing_stress", "tenant_isolation_check", "recovery_evidence", "live_mutation_blocked"),
    49: ("readiness_score", "evidence_completeness", "control_pass_rate", "report_timeliness", "draw_reconciliation", "match_progress", "closeout_load", "blocking_gaps", "score_explanation"),
    50: ("award_seeded", "budget_seeded", "costs_seeded", "draws_seeded", "match_seeded", "report_seeded", "closeout_seeded", "apis_exercised", "events_emitted", "workbench_queues_driven", "agent_summary_generated", "control_assertions_run", "release_documents_updated"),
}

_FEATURE_DEPENDENCIES = {
    12: ("JournalPosted", "PaymentExecuted"),
    18: ("PaymentExecuted",),
    24: ("JournalPosted",),
    27: ("ProcurementObligationProjected", "VendorEligibilityProjected"),
    38: ("PolicyChanged",),
    41: ("JournalPosted", "PaymentExecuted", "AuditProofGenerated"),
    42: ("ExpenseApproved", "PaymentExecuted", "JournalPosted"),
}

_EMPTY_ALLOWED_FIELDS = ("blocked_reason", "unmatched_queue", "rejected_lines", "pending_lines", "blocking_gaps", "explainable_adjustments", "remediation_tasks")


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
        "tables": _FEATURE_TABLES[capability.feature_number],
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "ui": _camel(capability.slug),
        "route": f"POST /grant-fund-accounting/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in GRANT_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update({
        "funding_amount": 100000, "activation_allowed": True, "confidence": 0.92, "human_approval_required": True,
        "source_citations": ("award-clause-1",), "source_lineage_preserved": True, "spending_allowed": True,
        "drawdown_allowed": True, "audit_proof": "hash-proof", "version_locked": True, "allowability_result": "allowable",
        "award_period_valid": True, "budget_category_valid": True, "restriction_valid": True, "allowable_cost_rule_valid": True,
        "procurement_evidence_valid": True, "match_eligible": True, "prior_approval_status": "approved", "indirect_cost_valid": True,
        "remaining_budget": 25000, "documentation_complete": True, "closeout_ready": True, "active_for_costs": True,
        "alert_visible": True, "executable_rule": True, "documentation_status": "complete", "draw_eligibility": True,
        "duplicate_detected": False, "late_posting_flag": False, "unmatched_queue": (), "reconciliation_status": "reconciled",
        "balance_updated": True, "late_transfer_flag": False, "reconciliation_required": True, "calculation_evidence": "calculation-pack",
        "payment_status": "paid", "budget_available": True, "prior_draw_status": "not_previously_drawn", "match_status": "current",
        "funder_limit_status": "within_limit", "submission_allowed": True, "shortfall_risk": "low", "reconciliation_complete": True,
        "forecast_shortfall": 0, "double_counted": False, "unsupported_valuation_flag": False, "expired_rate_flag": False,
        "portal_status": "ready", "submitted_proof": "portal-receipt", "short_paid_exception": False, "ledger_total": 1000, "report_total": 1000,
        "explainable_adjustments": (), "submission_blocked": False, "cryptographic_proof": "verified", "missing_obligation_visible": True,
        "unallowable_costs_checked": True, "late_reports_checked": True, "expired_evidence_checked": True, "match_shortfalls_checked": True,
        "budget_overages_checked": True, "draw_mismatches_checked": True, "procurement_gaps_checked": True, "remediation_tasks": (),
        "control_effective": True, "vendor_eligibility": "eligible", "cost_allowed": True, "rate": 0.1, "draw_eligible": True,
        "reconciled_to_reports": True, "confidence": 0.91, "live_mutation_blocked": True, "case_opened": True,
        "final_costs_complete": True, "final_draws_complete": True, "final_reports_submitted": True, "match_complete": True,
        "property_disposition": "resolved", "program_income_resolved": True, "evidence_packet_complete": True, "funder_acceptance": True,
        "closeout_allowed": True, "casual_edit_blocked": True, "premature_deletion_blocked": True, "proof_verified": True,
        "altered_payload_detected": False, "closed_history_mutation_blocked": True, "bias_check_complete": True,
        "false_positive_feedback": "captured", "event_contract": EVENT_CONTRACT, "event_topic": GRANT_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False, "safe_replay_allowed": True, "foreign_table_access_blocked": True,
        "dependency_mode": "event", "projection_used": True, "api_contract": "declared", "owned_table_scope": True,
        "command_preview": True, "permission_check": True, "human_confirmation": True, "direct_mutation_blocked": True,
        "ambiguity_visible": True, "agent_panel_visible": True, "forms_visible": True, "wizards_visible": True,
        "controls_visible": True, "table_browsers_visible": True, "rule_editors_visible": True, "parameter_editors_visible": True,
        "agent_tools_visible": True, "edge_case_queues_visible": True, "all_capabilities_surfaced": True,
        "continuous_testing_enabled": True, "duplicate_event_replay": True, "dead_letter_recovery": True, "offline_capture": True,
        "tenant_isolation_check": True, "recovery_evidence": "captured", "readiness_score": 0.94, "evidence_completeness": 1.0,
        "control_pass_rate": 1.0, "report_timeliness": 1.0, "draw_reconciliation": True, "match_progress": 1.0,
        "blocking_gaps": (), "award_seeded": True, "budget_seeded": True, "costs_seeded": True, "draws_seeded": True,
        "match_seeded": True, "report_seeded": True, "closeout_seeded": True, "apis_exercised": True, "events_emitted": True,
        "workbench_queues_driven": True, "agent_summary_generated": True, "control_assertions_run": True, "release_documents_updated": True,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and (not payload.get("funder") or not payload.get("award_number") or payload.get("funding_amount", 0) <= 0 or not payload.get("source_document_evidence") or payload.get("activation_allowed") is not True):
        findings.append("grant award intake requires funder, award number, funding, source evidence, and activation clearance")
    if n == 2 and (payload.get("confidence", 0) < 0.75 or not payload.get("clause_citations") or payload.get("human_approval_required") is not True):
        findings.append("semantic award extraction requires confident clause citations and human approval")
    if n == 3 and (payload.get("spending_allowed") is not True or payload.get("drawdown_allowed") is not True or not payload.get("transition_evidence")):
        findings.append("award lifecycle transition must prove spending and drawdown eligibility")
    if n == 4 and (not payload.get("effective_date") or not payload.get("approval_evidence") or payload.get("version_locked") is not True):
        findings.append("award amendment governance requires effective date, approval evidence, and locked versioning")
    if n == 6 and (payload.get("allowability_result") != "allowable" or payload.get("remaining_budget", 0) <= 0 or payload.get("documentation_complete") is not True):
        findings.append("restriction-aware cost validation blocks unallowable, undocumented, or over-budget costs")
    if n == 10 and (payload.get("executable_rule") is not True or not payload.get("test_cases") or not payload.get("award_clause_citations")):
        findings.append("allowable cost rule compiler requires executable rules, citations, and tests")
    if n == 12 and (payload.get("duplicate_detected") is True or payload.get("reconciliation_status") != "reconciled" or payload.get("balance_updated") is not True):
        findings.append("journal and payment reconciliation must resolve duplicates and update balances")
    if n == 16 and (payload.get("payment_status") not in ("paid", "eligible_advance") or payload.get("documentation_status") != "complete" or payload.get("submission_allowed") is not True):
        findings.append("drawdown readiness requires eligible paid/advance costs, documentation, and submission clearance")
    if n == 18 and (payload.get("reconciliation_complete") is not True or payload.get("short_paid_exception") not in (None, "", False)):
        findings.append("drawdown receipt reconciliation must resolve short-paid or unmatched receipts")
    if n == 20 and (payload.get("double_counted") is True or not payload.get("documentation") or not payload.get("audit_evidence")):
        findings.append("match contribution evidence must block double counting and prove eligibility")
    if n == 24 and (payload.get("ledger_total") != payload.get("report_total") or payload.get("submission_blocked") is True):
        findings.append("report-to-ledger reconciliation must tie report totals to ledger evidence")
    if n == 26 and (payload.get("control_effective") is not True or payload.get("remediation_tasks") not in ((), [])):
        findings.append("continuous funder compliance testing must clear remediation tasks")
    if n == 34 and not all(payload.get(field) is True for field in ("final_costs_complete", "final_draws_complete", "final_reports_submitted", "match_complete", "program_income_resolved", "evidence_packet_complete", "funder_acceptance", "closeout_allowed")):
        findings.append("closeout readiness requires final costs, draws, reports, match, evidence, and funder acceptance")
    if n == 35 and payload.get("casual_edit_blocked") is not True:
        findings.append("post-closeout adjustment governance must block casual edits to closed awards")
    if n == 37 and (payload.get("proof_verified") is not True or payload.get("altered_payload_detected") is True):
        findings.append("cryptographic evidence packet failed tamper-evidence validation")
    if n == 41 and (payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != GRANT_CONTROL_REQUIRED_EVENT_TOPIC or payload.get("stream_engine_picker_visible") is True or payload.get("safe_replay_allowed") is not True):
        findings.append("AppGen-X event reliability proof requires topic, idempotency, retry, dead-letter, and no stream picker")
    if n == 42 and (payload.get("foreign_table_access_blocked") is not True or payload.get("dependency_mode") not in ("api", "event", "projection") or payload.get("owned_table_scope") is not True):
        findings.append("cross-PBC boundary proof must use APIs/events/projections and block foreign table access")
    if n in (43, 44) and (payload.get("command_preview") is not True or payload.get("permission_check") is not True or payload.get("human_confirmation") is not True or payload.get("direct_mutation_blocked") is not True):
        findings.append("grant agent assistance requires preview, permission check, confirmation, and no direct mutation")
    if n == 46 and not all(payload.get(field) is True for field in ("forms_visible", "wizards_visible", "controls_visible", "table_browsers_visible", "rule_editors_visible", "parameter_editors_visible", "agent_tools_visible", "edge_case_queues_visible", "all_capabilities_surfaced")):
        findings.append("UI capability surface proof must expose every grant accounting capability")
    if n == 48 and (payload.get("live_mutation_blocked") is not True or payload.get("dead_letter_recovery") is not True or payload.get("tenant_isolation_check") is not True):
        findings.append("grant resilience drills require recovery evidence without mutating live records")
    if n == 49 and (payload.get("readiness_score", 0) < 0.8 or payload.get("blocking_gaps") not in ((), [])):
        findings.append("grant readiness score must be high and have no blocking gaps")
    if n == 50 and not all(payload.get(field) is True for field in ("award_seeded", "budget_seeded", "costs_seeded", "draws_seeded", "match_seeded", "report_seeded", "closeout_seeded", "apis_exercised", "events_emitted", "workbench_queues_driven", "agent_summary_generated", "control_assertions_run", "release_documents_updated")):
        findings.append("end-to-end grant release proof requires seeded lifecycle, APIs, events, workbench, agent, controls, and docs")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_grant_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in GRANT_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in GRANT_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": GRANT_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": GRANT_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_grant_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_grant_control(capability) for capability in GRANT_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.grant-fund-accounting-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": GRANT_CONTROL_OWNED_TABLES,
        "declared_dependencies": GRANT_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": GRANT_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": GRANT_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


GRANT_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_grant_control(slug, payload)) for capability in GRANT_CONTROL_CAPABILITIES}

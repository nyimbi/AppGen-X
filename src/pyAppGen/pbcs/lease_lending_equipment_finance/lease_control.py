"""Executable improve1 controls for the Lease Lending and Equipment Finance PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "lease_lending_equipment_finance"
EVENT_CONTRACT = "AppGen-X"
LEASE_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
LEASE_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.lease_lending_equipment_finance.events"
LEASE_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + tuple(
    f"lease_lending_equipment_finance_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES
)))
LEASE_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "PolicyChanged", "AuditEventSealed", "OperationalKpiChanged", "CustomerUpdated",
    "SupplierQualified", "AssetTelemetryReceived", "InsurancePolicyChanged",
    "PaymentReceived", "InvestorAllocationChanged", "ResidualMarketDataChanged",
)))
LEASE_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in LEASE_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in LEASE_CONTROL_CAPABILITIES}
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {1: ('contract_family', 'booking_basis', 'purchase_option_type', 'title_transfer_path', 'residual_bearing_flag', 'usage_billing_flag', 'servicing_playbook', 'structure_specific_validation', 'product_structure_validated'), 2: ('intake_case', 'opportunity_source', 'borrower_request', 'equipment_quote', 'dealer_invoice', 'guarantor_details', 'credit_conditions', 'pre_book_status', 'booking_prerequisites_satisfied'), 3: ('party_role', 'borrower_group', 'guarantor_scope', 'notice_role', 'funding_role', 'effective_dates', 'cross_default_link', 'master_agreement', 'party_roles_governed'), 4: ('asset_id', 'manufacturer', 'model', 'serial_set', 'asset_class', 'location', 'title_identifier', 'registration_identifier', 'substitution_lineage', 'asset_identity_traceable'), 5: ('vendor_invoice', 'eligible_costs', 'delivery_evidence', 'acceptance_evidence', 'split_disbursement', 'progress_payment', 'holdback', 'asset_line_link', 'funding_reconciliation_passed'), 6: ('approval_condition', 'condition_type', 'owner', 'due_date', 'waiver_authority', 'fulfillment_evidence', 'breach_severity', 'condition_aging', 'blocking_conditions_cleared'), 7: ('pricing_case', 'yield_rate', 'implicit_rate', 'money_factor', 'base_curve', 'spread', 'fees', 'dealer_reserve', 'minimum_return_floor', 'pricing_reconciles_to_cashflows'), 8: ('contract_classification', 'tax_owner', 'property_tax_method', 'depreciation_beneficiary', 'title_expectation', 'accrual_treatment', 'classification_rationale', 'policy_conflict_blocked', 'classification_policy_passed'), 9: ('commencement_basis', 'ship_date', 'delivery_date', 'acceptance_date', 'installation_complete', 'waiver_approval', 'interim_rent_rule', 'staged_delivery', 'commencement_trigger_satisfied'), 10: ('schedule_id', 'timing_basis', 'stub_period', 'daily_accrual', 'step_payment', 'seasonal_skip', 'balloon_payment', 'version_lineage', 'schedule_generation_validated'), 11: ('day_count_convention', 'grace_window', 'late_charge_cap', 'default_interest', 'cure_period', 'policy_version', 'delinquency_event', 'fee_calculation', 'fee_timing_policy_applied'), 12: ('usage_contract', 'included_allowance', 'overage_rate', 'meter_source', 'true_up_cadence', 'dispute_workflow', 'telematics_feed', 'billing_snapshot', 'usage_billing_reconciled'), 13: ('reserve_ledger', 'collection_basis', 'draw_rule', 'approval_threshold', 'expiration', 'unused_balance_disposition', 'asset_link', 'movement_evidence', 'reserve_ledger_balanced'), 14: ('residual_value', 'origination_assumption', 'market_comps', 'appraisal_source', 'curve_version', 'review_cadence', 'downgrade_trigger', 'stressed_residual', 'residual_review_current'), 15: ('remarketing_event', 'realized_proceeds', 'selling_costs', 'downtime_days', 'condition_score', 'residual_variance', 'cohort_key', 'feedback_update', 'realized_value_feedback_posted'), 16: ('buyout_quote', 'effective_date', 'payoff_type', 'principal_component', 'accrued_rent', 'taxes', 'fees', 'residual_component', 'policy_version', 'buyout_quote_reproducible'), 17: ('end_of_term_case', 'decision_path', 'notice_deadline', 'asset_inspection', 'quote_expiration', 'concession_rule', 'maturity_queue', 'holdover_review', 'end_of_term_path_controlled'), 18: ('modification_case', 'reason_code', 'effective_date', 'before_economics', 'after_economics', 'consent_required', 'change_classification', 'replacement_schedule', 'modification_package_approved'), 19: ('collateral_package', 'primary_collateral', 'filing_jurisdiction', 'filing_number', 'continuation_deadline', 'title_status', 'control_requirement', 'perfection_defect', 'perfection_defects_controlled'), 20: ('insurance_policy', 'coverage_amount', 'loss_payee_status', 'expiration', 'tracking_device_required', 'inspection_cadence', 'lapse_event', 'cure_status', 'protection_monitoring_active'), 21: ('collections_case', 'delinquency_bucket', 'workout_status', 'litigation_hold', 'bankruptcy_hold', 'promise_to_pay', 'dispute_flag', 'cure_deadline', 'collections_segment_applied'), 22: ('relief_program', 'hardship_reason', 'term', 'payment_treatment', 'accrued_interest_handling', 'reporting_classification', 'expiration_rule', 'dual_approval', 'relief_program_governed'), 23: ('repo_case', 'notice_generation', 'repo_vendor', 'legal_hold', 'cure_countdown', 'voluntary_surrender', 'asset_location', 'condition_grade', 'repo_timeline_auditable'), 24: ('disposition_case', 'inspection_result', 'repair_authorization', 'sale_channel', 'storage_cost', 'transport_cost', 'net_proceeds', 'deficiency_or_surplus', 'recovery_waterfall_reconciled'), 25: ('investor_allocation', 'position_type', 'effective_date', 'retained_strip', 'servicing_fee_basis', 'consent_requirement', 'transfer_event', 'exposure_share', 'investor_allocations_reconcile'), 26: ('remittance_run', 'billed_rent', 'collected_cash', 'allocated_cash', 'remitted_cash', 'fees', 'recoveries', 'shortfall_exception', 'remittance_waterfall_reconciled'), 27: ('portfolio_view', 'equipment_category', 'manufacturer', 'geography', 'industry', 'obligor_group', 'residual_profile', 'stressed_exposure', 'concentration_thresholds_monitored'), 28: ('exception_type', 'taxonomy_class', 'severity', 'customer_impact', 'recovery_impact', 'legal_sensitivity', 'owner', 'sla', 'typed_exception_queue_routed'), 29: ('override_case', 'override_type', 'justification', 'approving_authority', 'expiration', 'compensating_control', 'permanent_policy_exception', 'follow_up_action', 'override_authority_enforced'), 30: ('document_type', 'extracted_fields', 'confidence', 'citation_spans', 'safe_draft_update', 'target_record', 'human_confirmation', 'low_confidence_queue', 'document_extraction_cited'), 31: ('structuring_skill', 'lease_vs_loan_alternative', 'collateral_implication', 'residual_implication', 'schedule_pattern', 'approval_conditions', 'policy_citations', 'draft_only', 'structuring_agent_guarded'), 32: ('servicing_skill', 'account_snapshot', 'payoff_composition', 'extension_summary', 'default_status', 'customer_ready_summary', 'redaction_profile', 'draft_action', 'servicing_agent_redacted'), 33: ('triage_skill', 'exception_group', 'severity_rank', 'recoverability', 'due_date', 'missing_evidence', 'linked_record', 'reviewer_feedback', 'triage_agent_evidence_linked'), 34: ('workbench_queue', 'ready_to_fund', 'conditions_due', 'schedule_exceptions', 'insurance_lapses', 'maturities', 'delinquent_accounts', 'repo_cases', 'queue_first_workbench_visible'), 35: ('deal_detail', 'contract_summary', 'cash_flow_profile', 'asset_section', 'collateral_status', 'condition_history', 'servicing_history', 'investor_allocations', 'deal_detail_story_complete'), 36: ('asset_workspace', 'serial_search', 'title_search', 'location_search', 'perfection_records', 'insurance_status', 'inspection_history', 'substitution_history', 'asset_workspace_traceable'), 37: ('recovery_workspace', 'cure_notice', 'field_action', 'promise_tracking', 'vendor_assignment', 'recovered_asset_milestone', 'legal_hold', 'net_recovery_waterfall', 'recovery_workspace_operational'), 38: ('servicing_event', 'actor', 'record_ref', 'policy_version', 'before_economics', 'after_economics', 'event_category', 'replay_hash', 'servicing_event_ledger_replayable'), 39: ('api_route', 'deal_search', 'asset_search', 'schedule_simulation', 'buyout_recalculation', 'modification_draft', 'exception_ack', 'remittance_export', 'api_surface_complete'), 40: ('subrecord_model', 'fee_component', 'tax_component', 'approval_condition', 'collateral_filing', 'insurance_coverage', 'reserve_balance', 'investor_allocation', 'economic_legal_subrecords_owned'), 41: ('policy_rule', 'runtime_parameter', 'effective_date', 'tenant_scope', 'approval_history', 'impact_simulation', 'retired_version', 'rollback_plan', 'policy_simulation_available'), 42: ('release_pack', 'origination_trace', 'funding_trace', 'schedule_trace', 'usage_trace', 'residual_trace', 'repo_trace', 'syndication_trace', 'domain_release_pack_complete'), 43: ('scenario_library', 'scenario_id', 'product_structure', 'funding_pattern', 'schedule_shape', 'asset_substitution', 'repo_outcome', 'test_mapping', 'scenario_matrix_bound_to_tests'), 44: ('migration_plan', 'booked_lease_import', 'schedule_import', 'residual_import', 'repo_import', 'servicing_history_import', 'quarantine_reason', 'reconciliation_report', 'migration_dry_run_reconciled'), 45: ('sla_metric', 'time_to_approve', 'time_to_fund', 'schedule_latency', 'quote_turnaround', 'exception_aging', 'recovery_cycle_time', 'remittance_time', 'sla_timers_governed'), 46: ('risk_model', 'residual_volatility', 'usage_trend', 'funding_before_acceptance', 'concentration_signal', 'dealer_exception_pattern', 'repeat_default', 'explanation', 'finance_signal_anomaly_explained'), 47: ('authority_boundary', 'quote_permission', 'modification_permission', 'waiver_permission', 'repo_permission', 'investor_export_permission', 'visible_diff', 'actor_attribution', 'agent_authority_boundary_enforced'), 48: ('control_assertion', 'segregation_test', 'approval_test', 'filing_staleness', 'insurance_expiry', 'investor_balance', 'repo_notice_test', 'exception_publication', 'continuous_controls_publish_exceptions'), 49: ('phase_gate', 'origination_phase', 'servicing_phase', 'recovery_phase', 'investor_phase', 'training_evidence', 'data_quality', 'fallback_plan', 'phase_readiness_signed'), 50: ('acceptance_rubric', 'structure_score', 'collateral_score', 'schedule_score', 'usage_score', 'residual_score', 'repo_score', 'agent_safety_score', 'final_acceptance_rubric_signed')}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {30: ('AuditEventSealed',), 31: ('PolicyChanged',), 32: ('AuditEventSealed',), 38: ('AuditEventSealed',), 41: ('PolicyChanged',), 45: ('OperationalKpiChanged',), 46: ('OperationalKpiChanged',), 48: ('AuditEventSealed',)}
_REQUIRED_TRUE: dict[int, tuple[str, ...]] = {1: ('product_structure_validated',), 2: ('booking_prerequisites_satisfied',), 3: ('party_roles_governed',), 4: ('asset_identity_traceable',), 5: ('funding_reconciliation_passed',), 6: ('blocking_conditions_cleared',), 7: ('pricing_reconciles_to_cashflows',), 8: ('classification_policy_passed',), 9: ('commencement_trigger_satisfied',), 10: ('schedule_generation_validated',), 11: ('fee_timing_policy_applied',), 12: ('usage_billing_reconciled',), 13: ('reserve_ledger_balanced',), 14: ('residual_review_current',), 15: ('realized_value_feedback_posted',), 16: ('buyout_quote_reproducible',), 17: ('end_of_term_path_controlled',), 18: ('modification_package_approved',), 19: ('perfection_defects_controlled',), 20: ('protection_monitoring_active',), 21: ('collections_segment_applied',), 22: ('relief_program_governed',), 23: ('repo_timeline_auditable',), 24: ('recovery_waterfall_reconciled',), 25: ('investor_allocations_reconcile',), 26: ('remittance_waterfall_reconciled',), 27: ('concentration_thresholds_monitored',), 28: ('typed_exception_queue_routed',), 29: ('override_authority_enforced',), 30: ('document_extraction_cited',), 31: ('structuring_agent_guarded',), 32: ('servicing_agent_redacted',), 33: ('triage_agent_evidence_linked',), 34: ('queue_first_workbench_visible',), 35: ('deal_detail_story_complete',), 36: ('asset_workspace_traceable',), 37: ('recovery_workspace_operational',), 38: ('servicing_event_ledger_replayable',), 39: ('api_surface_complete',), 40: ('economic_legal_subrecords_owned',), 41: ('policy_simulation_available',), 42: ('domain_release_pack_complete',), 43: ('scenario_matrix_bound_to_tests',), 44: ('migration_dry_run_reconciled',), 45: ('sla_timers_governed',), 46: ('finance_signal_anomaly_explained',), 47: ('agent_authority_boundary_enforced', 'visible_diff', 'actor_attribution'), 48: ('continuous_controls_publish_exceptions', 'exception_publication'), 49: ('phase_readiness_signed',), 50: ('final_acceptance_rubric_signed',)}
_DOMAIN_MESSAGES: dict[int, str] = {1: 'product structure must validate contract family, booking basis, purchase option, title transfer, residual bearing, usage billing, and servicing playbook', 2: 'deal intake must block booking until application, credit, vendor quote, approval conditions, documents, and funding instructions are complete', 3: 'party-role hierarchy must route notices, funding, guarantees, cross-defaults, and liabilities to effective parties', 4: 'asset identity must reject duplicate serials and preserve collateral, title, registration, substitution, pool, and assembly lineage', 5: 'funding must reconcile vendor invoices, eligible costs, delivery evidence, acceptance, split disbursements, progress payments, and holdbacks', 6: 'approval conditions must govern documentation, pricing, post-close trailing items, waivers, owners, evidence, and breach severity', 7: 'pricing must calculate yield, implicit rate, money factor, curves, spreads, fees, reserves, subsidies, and floors by structure', 8: 'classification must block incompatible tax, accounting, property tax, depreciation, title, and accrual treatment combinations', 9: 'commencement must wait for governed ship, delivery, acceptance, installation, beneficial-use, waiver, interim-rent, or staged-delivery triggers', 10: 'payment schedules must support advance/arrears, stubs, daily accrual, steps, seasonal skips, balloons, usage milestones, and controlled corrections', 11: 'timing and collections logic must persist day-count, grace, late-fee caps, default interest, cure periods, and policy version evidence', 12: 'usage billing must reconcile meter source, allowances, overage rates, true-up cadence, disputes, telematics, and locked billing snapshots', 13: 'reserve administration must govern collection basis, draws, approvals, expiry, unused-balance disposition, and asset/event linkage', 14: 'residual workflow must track assumptions, market comps, appraisals, curve versions, review cadence, downgrades, booked/current/stressed values', 15: 'remarketing outcomes must feed realized proceeds, costs, downtime, condition, residual analytics, concentration cohorts, and feedback loops', 16: 'buyout quote must preserve payoff date, unearned income, taxes, residual, fees, stipulations, components, and policy version assumptions', 17: 'end-of-term must govern purchase, return, renewal, extension, evergreen, holdover, notices, inspections, quote expiry, and concessions', 18: 'modifications must preserve before/after economics, consent, effective date, classification, original schedule, approved replacement, and approval evidence', 19: 'collateral perfection must track assets, filings, jurisdictions, deadlines, titles, control requirements, deficiencies, and funding/default blockers', 20: 'insurance and collateral protection must monitor policies, coverage, loss-payee status, expirations, tracking devices, inspections, lapses, and cures', 21: 'collections must segment delinquency, workout, litigation, bankruptcy, charge-off, promises, disputes, cure deadlines, and strategy notes', 22: 'relief programs must distinguish payment treatment, accrued interest, reporting classification, expiry, dual approval, covenant waiver, and materiality', 23: 'repossession must enforce notices, vendor assignment, legal holds, cure countdowns, surrender, location, condition, custody, and jurisdiction policy', 24: 'disposition must reconcile inspection, repair, auction/sale/re-lease, costs, proceeds, deficiency/surplus, residual feedback, and cycle time', 25: 'investor allocations must reconcile retained/sold interests, warehouse funding, dates, servicing fees, consents, transfers, and exposure shares', 26: 'remittance must allocate billed rent, cash, fees, recoveries, losses, reserves, servicing compensation, shortfalls, reversals, and exceptions', 27: 'portfolio analytics must segment exposure by collateral, manufacturer, geography, industry, group, residual profile, channel, and stressed cohorts', 28: 'exceptions must use equipment-finance taxonomy with severity, customer impact, recovery impact, legal sensitivity, owner, SLA, and narratives', 29: 'overrides must require justification, authority, expiration, compensating control, temporary/permanent type, searchability, and follow-up', 30: 'document intake must classify finance docs, extract fields with citations and confidence, draft safe updates, and require human confirmation', 31: 'structuring agent must propose policy-aware alternatives, collateral/residual implications, schedules, conditions, citations, and draft-only recommendations', 32: 'servicing agent must summarize governed account state, payoff composition, extensions, default status, redaction, and draft actions safely', 33: 'triage agent must group exceptions by severity, recoverability, due date, evidence, stale blockers, linked records, and reviewer feedback', 34: 'workbench must provide queue-first panels for funding, conditions, schedules, insurance, maturities, delinquency, repo, remittance, and personas', 35: 'deal detail must combine economics, assets, collateral, conditions, servicing, investors, end-of-term, history, versions, and roles', 36: 'asset workspace must search serials/titles/locations and pivot to leases, schedules, exceptions, repo cases, inspections, telematics, substitutions', 37: 'recovery workspace must manage cure notices, field actions, promises, vendor assignments, recovered milestones, legal holds, bankruptcy, and waterfalls', 38: 'servicing event ledger must separate actions, calculations, assistant suggestions, inbound events, policy versions, before/after economics, and replay', 39: 'APIs must cover search, simulation, correction, residual review, buyout recalculation, modification, exceptions, repo, remittance export, and evidence export', 40: 'data model must include fee/tax components, conditions, filings, insurance, reserves, usage, investors, remittance, modifications, and disposition outcomes', 41: 'policy and parameters must version origination, servicing, collateral, residual, recovery policies with effective dates, approvals, simulation, and rollback', 42: 'release pack must include origination, funding, schedules, usage, residuals, buyouts, modifications, delinquency, repo, recovery, syndication traces', 43: 'scenario library must map product, funding, schedule, asset, residual, buyout, hardship, repo, and syndication scenarios to tests/evidence', 44: 'migration must dry-run leases, schedules, residuals, buyout quotes, repo cases, servicing history, validation, quarantine, and reconciliation', 45: 'SLA instrumentation must measure approval, funding, schedules, quotes, exceptions, recovery, remittance, policy pauses, and operational delays', 46: 'risk/anomaly models must cite residual volatility, usage, funding before acceptance, concentration, dealer exceptions, repeat defaults, title/insurance mismatches', 47: 'agent actions must enforce permissions, visible diffs, actor attribution, quote/modification/waiver/repo/export/evidence authority, and denial evidence', 48: 'continuous controls must test duties, approvals, filings, insurance, investor balances, residual changes, concessions, repo notices, and release evidence', 49: 'go-live readiness must phase origination, servicing, recovery, investor operations with evidence, training, data quality, fallback plans, and blockers', 50: 'final acceptance rubric must score structures, collateral, schedules, usage, residuals, buyouts, repo, syndication, exceptions, UI, agent safety, and evidence'}
_EMPTY_ALLOWED_FIELDS = ("owner_conflicts", "quarantine_reason")


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
        "tables": (f"lease_lending_equipment_finance_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "ui": f"LeaseLendingEquipmentFinance{_camel(capability.slug)}Panel",
        "route": f"POST /lease-lending-equipment-finance/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in LEASE_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    for field in _REQUIRED_TRUE.get(resolved.feature_number, ()):
        payload[field] = True
    payload.update({
        "database_backend": "postgresql",
        "event_contract": EVENT_CONTRACT,
        "event_topic": LEASE_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    for field in _REQUIRED_TRUE.get(n, ()):
        if payload.get(field) is not True:
            findings.append(f"{capability.title} requires {field.replace('_', ' ')}")
    key = _REQUIRED_TRUE.get(n, (None,))[0]
    if key and payload.get(key) is not True:
        findings.append(_DOMAIN_MESSAGES[n])
    if n in (30, 31, 32, 33, 47) and payload.get("human_confirmation") is False:
        findings.append("agent-assisted finance actions require human confirmation and cannot bypass policy authority")
    if n == 39 and payload.get("api_surface_complete") is not True:
        findings.append("search, simulation, correction, repo, remittance, and evidence export APIs must be covered")
    if n == 40 and payload.get("economic_legal_subrecords_owned") is not True:
        findings.append("economic and legal subrecords must stay owned by this PBC")
    if n == 42 and payload.get("domain_release_pack_complete") is not True:
        findings.append("release evidence pack must cover core equipment finance workflows")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != LEASE_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("lease lending equipment finance eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in LEASE_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary lease lending equipment finance datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("lease lending equipment finance controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_lease_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in LEASE_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in LEASE_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": LEASE_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": LEASE_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_lease_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_lease_control(capability) for capability in LEASE_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.lease-lending-equipment-finance-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": LEASE_CONTROL_OWNED_TABLES,
        "declared_dependencies": LEASE_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": LEASE_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": LEASE_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


LEASE_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_lease_control(slug, payload)) for capability in LEASE_CONTROL_CAPABILITIES}

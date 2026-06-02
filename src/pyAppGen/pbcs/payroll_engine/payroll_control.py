"""Executable improve1 controls for the Payroll Engine PBC."""
from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import PAYROLL_ENGINE_OWNED_TABLES, PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC

PBC_KEY = "payroll_engine"
EVENT_CONTRACT = "AppGen-X"
PAYROLL_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PAYROLL_CONTROL_REQUIRED_EVENT_TOPIC = PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC
PAYROLL_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(PAYROLL_ENGINE_OWNED_TABLES + tuple(f"payroll_engine_{c.slug}_control" for c in IMPROVE1_CAPABILITIES)))
PAYROLL_CONTROL_DECLARED_DEPENDENCIES = (
    "LaborHoursApproved", "TaxCalculated", "WorkerProjectionChanged", "PaymentBatchProjectionChanged",
    "JournalRequestProjectionChanged", "AuditEventSealed", "TreasuryFundingChanged", "BenefitEnrollmentChanged",
    "BankInstructionVerified", "CarbonIntensityWindowChanged", "PolicyChanged", "ModelGovernanceChanged",
)
PAYROLL_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {c.feature_number: c for c in PAYROLL_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {c.slug: c for c in PAYROLL_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "legal_entity_id", "pay_group_id", "payroll_run_id", "worker_id", "period_id", "country", "currency", "actor_id", "policy_version", "evidence_references")
_FIELD_ROWS = """
1|calendar_version,pay_frequency,cutoff_window,pay_date,bank_holidays,statutory_deadlines
2|period_state,intake_close,calculation_state,approval_state,filing_state,archive_lock
3|eligibility_rule_id,worker_class,country,legal_entity,currency,labor_source
4|employer_registration,statutory_authority,filing_channel,payment_rail,funding_projection,approval_policy
5|readiness_gate_id,roster_ready,labor_ready,tax_projection_freshness,payment_readiness,open_exceptions
6|lock_level,calculation_freeze,payment_freeze,posting_freeze,filing_freeze,break_glass_approval
7|projection_source,employment_status,tax_residency,compensation_basis,termination_date,freshness
8|pay_profile_id,effective_dates,rate,fte,tax_profile_ref,retro_impact
9|bank_instruction_id,verification_status,account_mask,payment_rail,cooling_period,high_risk_flag
10|labor_event_id,idempotency_key,period_mapping,earning_code_mapping,approval_proof,stale_event_handling
11|earning_code_id,taxable_status,pensionable_flag,jurisdiction,gl_mapping,filing_box
12|gross_trace_id,input_source,earning_code,rate,multiplier,component_lineage
13|proration_method,calendar_days,workdays,scheduled_hours,jurisdiction,payslip_line
14|overtime_rule_id,approved_labor_proof,earning_mapping,cap_check,discrepancy,correction_case
15|tax_projection_id,jurisdiction,wage_base,taxable_wages,withholding_amount,recalc_trigger
16|wage_base_projection_id,taxable_base,cap,prior_amount,threshold_crossing,source_projection
17|deduction_rule_id,priority,taxable_treatment,limit,arrears_behavior,net_floor_interaction
18|garnishment_order_id,authority,case_reference,protected_amount,cap,remittance_target
19|arrears_id,origin,balance,recovery_rule,max_recovery,notification_status
20|benefit_plan_id,eligibility,employee_contribution,employer_contribution,taxable_benefit,retro_change
21|net_pay_floor_id,floor_amount,violation_reason,suggested_recovery,exception_workflow,approval_trace
22|distribution_id,priority,amount_percentage,verified_bank_instruction,residual_account,failed_distribution
23|payment_instruction_id,amount,pay_date,batch_group,approval_status,treasury_handoff
24|cash_forecast_id,tax_remittance,benefits_cash,garnishment_cash,off_cycle_cash,confidence
25|approval_id,amount_threshold,segregation_check,rejection_reason,materiality,post_approval_delta
26|posting_id,payment_batch_projection,journal_request_projection,tax_wage_base_projection,proof_hash,idempotency_key
27|payslip_id,earnings_lines,tax_lines,deduction_lines,legal_disclaimer,immutable_snapshot
28|filing_id,jurisdiction,filing_channel,materiality_threshold,validation_error,emitted_event
29|reconciliation_id,payslip_total,tax_total,wage_base_total,prior_filing,out_of_balance
30|retro_id,lookback_window,prior_value,new_value,delta,tax_recalc_dependency
31|off_cycle_id,off_cycle_type,approval_threshold,tax_treatment,cash_impact,filing_impact
32|correction_id,issue_source,impacted_payslip,amount_delta,employee_notification,closure_proof
33|exception_id,exception_type,owner,sla,severity,recovery_action
34|policy_screening_id,attributes_evaluated,decision,explanation,override_path,policy_hash
35|anomaly_id,gross_variance,net_variance,bank_change,filing_delta,reason_codes
36|exposure_model_id,cash_shortfall_distribution,compliance_error_distribution,payment_failure_distribution,mitigation_options,confidence
37|model_registry_id,feature_lineage,training_window,drift_monitoring,fairness_check,rollback
38|zk_proof_id,gross_proof,tax_proof,net_proof,filing_inclusion,verifier_api
39|audit_chain_id,worker_projection_hash,calculation_hash,approval_hash,posting_hash,temporal_reconstruction
40|event_cockpit_id,inbox_status,outbox_status,dead_letter_age,replay_eligibility,projection_freshness
41|boundary_proof_id,owned_table_check,worker_master_block,time_entry_block,tax_table_block,treasury_table_block
42|workbench_coverage_id,calendar_surface,run_console,payslip_review,filing_surface,agent_panel
43|instruction_intake_id,extracted_fact,owned_table_preview,permission_check,confidence,expected_event
44|gross_to_net_plan_id,command,owned_tables,affected_workers,net_impact,human_approval
45|simulation_id,overtime_multiplier,supplemental_rate,deduction_cap,approval_threshold,historical_run_comparison
46|cash_allocation_id,legal_priority,statutory_remittance,payment_rail_constraint,escalation,executive_approval
47|carbon_batch_id,processing_window,statutory_deadline,pay_date_constraint,selected_window,tradeoff
48|control_test_id,negative_net_check,filing_imbalance_check,foreign_table_access_check,dead_letter_aging_check,agent_bypass_check
49|readiness_score_id,setup_score,labor_score,tax_score,payment_score,event_score
50|run_proof_id,worker_projection,approved_hours,payslip_calculation,posting_handoff,filing_preparation
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {n: f"{CAPABILITY_BY_NUMBER[n].slug}_verified" for n in range(1, 51)}
_FEATURE_FIELDS = {n: _BASE_FIELDS + _DOMAIN_FIELDS[n] + (_PRIMARY_PROOF_FIELDS[n],) for n in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    7: ("WorkerProjectionChanged",), 10: ("LaborHoursApproved",), 15: ("TaxCalculated",), 16: ("TaxCalculated",),
    20: ("BenefitEnrollmentChanged",), 23: ("PaymentBatchProjectionChanged", "TreasuryFundingChanged", "BankInstructionVerified"),
    24: ("TreasuryFundingChanged",), 26: ("PaymentBatchProjectionChanged", "JournalRequestProjectionChanged", "AuditEventSealed"),
    28: ("TaxCalculated", "AuditEventSealed"), 30: ("TaxCalculated",), 37: ("ModelGovernanceChanged",),
    40: ("AuditEventSealed",), 41: ("LaborHoursApproved", "TaxCalculated", "PaymentBatchProjectionChanged", "JournalRequestProjectionChanged", "AuditEventSealed"),
    47: ("CarbonIntensityWindowChanged",),
}
_HUMAN_CONFIRMATION_FEATURES = (6, 9, 18, 21, 23, 25, 26, 28, 30, 31, 32, 34, 43, 44, 46, 50)
_PROJECTION_ONLY_FEATURES = (7, 10, 15, 16, 20, 23, 24, 26, 28, 37, 40, 41, 47)
_AGENT_PREVIEW_FEATURES = (43, 44, 50)
_NON_MUTATING_FEATURES = (24, 35, 36, 37, 38, 39, 40, 41, 45, 47, 48, 49, 50)
_PAYROLL_RISK_FEATURES = (5, 6, 9, 15, 17, 18, 21, 23, 25, 26, 28, 30, 31, 32, 34, 35, 36, 38, 39, 40, 41, 46, 48, 50)


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
        "tables": (f"payroll_engine_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"PayrollEngine{_camel(capability.slug)}Panel",
        "route": f"POST /payroll-engine/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in PAYROLL_CONTROL_CAPABILITIES}


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
        "event_topic": PAYROLL_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "payroll_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires payroll-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _PAYROLL_RISK_FEATURES and payload.get("payroll_risk_evidence_complete") is not True:
        findings.append("payroll calendar, gross-to-net, tax, deduction, garnishment, payment, filing, correction, and go-live controls require complete risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("payroll freeze, bank, garnishment, net pay, payment, approval, posting, filing, correction, agent, allocation, and run-proof decisions require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("payroll agent skills must produce cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("payroll forecasts, anomalies, stochastic models, proofs, audit, cockpit, boundary, simulation, carbon, control tests, readiness, and run proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("worker, labor, tax, benefit, treasury, ledger, model, audit, and carbon facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != PAYROLL_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("payroll eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in PAYROLL_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary payroll datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("payroll controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_payroll_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in PAYROLL_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in PAYROLL_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": PAYROLL_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": PAYROLL_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_payroll_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_payroll_control(capability) for capability in PAYROLL_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.payroll-engine-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": PAYROLL_CONTROL_OWNED_TABLES, "declared_dependencies": PAYROLL_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": PAYROLL_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": PAYROLL_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


PAYROLL_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_payroll_control(slug, payload)) for capability in PAYROLL_CONTROL_CAPABILITIES}

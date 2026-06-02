"""Executable improve1 controls for the Lending Origination and Servicing PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "lending_origination_servicing"
EVENT_CONTRACT = "AppGen-X"
LENDING_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
LENDING_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.lending_origination_servicing.events"
_BASE_OWNED_TABLES = (
    "lending_origination_servicing_loan_application",
    "lending_origination_servicing_borrower_profile",
    "lending_origination_servicing_underwriting_decision",
    "lending_origination_servicing_loan_offer",
    "lending_origination_servicing_disbursement",
    "lending_origination_servicing_repayment_schedule",
    "lending_origination_servicing_servicing_case",
    "lending_origination_servicing_lending_origination_servicing_policy_rule",
    "lending_origination_servicing_lending_origination_servicing_runtime_parameter",
    "lending_origination_servicing_lending_origination_servicing_schema_extension",
    "lending_origination_servicing_lending_origination_servicing_control_assertion",
    "lending_origination_servicing_lending_origination_servicing_governed_model",
    "lending_origination_servicing_appgen_outbox_event",
    "lending_origination_servicing_appgen_inbox_event",
    "lending_origination_servicing_appgen_dead_letter_event",
)
LENDING_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        _BASE_OWNED_TABLES
        + tuple(f"lending_origination_servicing_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES)
    )
)
LENDING_CONTROL_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        (
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
            "IdentityVerified",
            "CreditBureauSnapshotReceived",
            "DocumentClassified",
            "CollateralValuationUpdated",
            "LoanBooked",
            "FundsDisbursed",
            "PaymentAuthorized",
            "AccountingJournalPosted",
            "NoticeDelivered",
            "EscrowDisbursementPosted",
            "ComplaintReceived",
            "ChargeOffPosted",
            "PayoffCompleted",
        )
    )
)
LENDING_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in LENDING_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in LENDING_CONTROL_CAPABILITIES}

_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: "normalized_party_roles_approved",
    2: "stage_stipulations_cleared_or_waived",
    3: "repayment_capacity_components_verified",
    4: "identity_fraud_kyc_gate_passed",
    5: "bureau_snapshot_and_disputes_resolved",
    6: "collateral_lien_valuation_governed",
    7: "affordability_ratios_policy_versioned",
    8: "underwriting_policy_lineage_immutable",
    9: "adverse_action_reasons_mapped",
    10: "offer_pricing_exception_authorized",
    11: "approval_to_fund_blockers_cleared",
    12: "boarding_terms_reconciled",
    13: "executed_note_version_linked",
    14: "funding_settlement_reconciled",
    15: "amortization_method_validated",
    16: "accrual_fee_basis_aligned",
    17: "escrow_analysis_notice_ready",
    18: "payment_allocation_waterfall_applied",
    19: "reversal_lineage_preserved",
    20: "delinquency_bucket_strategy_selected",
    21: "promise_to_pay_commitment_tracked",
    22: "late_fee_waiver_authority_checked",
    23: "hardship_trial_plan_governed",
    24: "modification_accounting_approved",
    25: "payoff_quote_per_diem_reproducible",
    26: "lien_release_closure_evidence_ready",
    27: "charge_off_recovery_controls_applied",
    28: "special_status_contact_blocks_enforced",
    29: "escrow_exception_next_action_set",
    30: "complaint_regulatory_clock_active",
    31: "notice_obligation_template_versioned",
    32: "fair_lending_disparity_reviewed",
    33: "covenant_breach_workflow_governed",
    34: "fee_catalog_authority_enforced",
    35: "second_review_override_approved",
    36: "tenant_policy_scope_isolated",
    37: "event_sourced_timeline_replayable",
    38: "cross_pbc_payload_boundary_verified",
    39: "persona_queue_coverage_visible",
    40: "application_detail_evidence_complete",
    41: "servicing_detail_balances_timeline_complete",
    42: "collections_workspace_compliance_pinned",
    43: "agent_intake_confirmation_required",
    44: "underwriter_copilot_human_judgment_required",
    45: "servicing_agent_balance_action_approval_required",
    46: "audit_agent_cites_existing_evidence",
    47: "release_traceability_pack_complete",
    48: "sealed_control_test_verified",
    49: "synthetic_portfolio_dashboard_covered",
    50: "cutover_post_release_verification_complete",
}

_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    4: ("IdentityVerified",),
    5: ("CreditBureauSnapshotReceived",),
    6: ("CollateralValuationUpdated",),
    8: ("PolicyChanged", "AuditEventSealed"),
    14: ("FundsDisbursed", "AccountingJournalPosted"),
    18: ("PaymentAuthorized",),
    26: ("PayoffCompleted",),
    31: ("NoticeDelivered",),
    37: ("AuditEventSealed",),
    38: ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"),
    48: ("AuditEventSealed",),
}

_DOMAIN_MESSAGES: dict[int, str] = {
    1: "intake must normalize applicant, co-borrower, guarantor, beneficial-owner, product, purpose, consent, and channel facts before underwriting",
    2: "stipulations must distinguish pre-underwriting and pre-funding blockers, waivers, owners, due dates, and verification outcomes",
    3: "income verification must preserve gross, net, stable, excluded, seasonal, business, deposit, tax, and obligation-offset components",
    4: "identity and fraud gates must block synthetic identity, watchlist, duplicate tax identifier, device anomaly, and beneficial-owner failures",
    5: "bureau evidence must preserve pull source, tradelines, freezes, disputes, re-pull decisions, exclusions, and selected score set",
    6: "secured lending controls require collateral identity, appraisal source, valuation date, haircut, lien position, title, and insurance terms",
    7: "affordability calculations must store DTI, DSCR, residual income, global cash flow, stress assumptions, rounding, and policy version",
    8: "underwriting decisions require immutable rule package lineage, effective dates, target product, override authority, and runtime parameters",
    9: "decision explanations must map decline, conditional approval, counteroffer, pricing, and adverse-action reasons to evidence",
    10: "offers must govern term, amortization, rate basis, fees, locks, expiration, conditions, and pricing or amount exceptions",
    11: "funding readiness must hard-block unresolved documents, fraud re-check, lien prerequisites, insurance, instructions, and approval expiry",
    12: "boarding must reconcile approved offer, executed note, funded amount, due dates, payment frequency, escrow, and fee setup",
    13: "executed contract linkage must preserve signed note, disclosures, riders, modification versions, timestamps, and supersession history",
    14: "funding reconciliation must compare gross funds, net proceeds, payoffs, reserves, fee deductions, account references, and acknowledgments",
    15: "amortization must support level-pay, interest-only, balloon, step-rate, irregular first-period, and curtailment behavior",
    16: "accrual controls must align day-count, accrual start, non-business-day handling, compounding, fee accrual, and capitalization policy",
    17: "escrow must govern tax, insurance, assessment buckets, cushions, annual analysis, shortage, surplus, disbursements, and notices",
    18: "payment allocation must apply configured waterfalls for exact, partial, extra-principal, payoff, delinquent, suspense, and restricted funds",
    19: "payment reversals must preserve original posting lineage while separating policy suspense from unidentified unapplied funds",
    20: "collections must drive grace, early, late, default, workout, contact cadence, notices, approvals, and next-best action strategy",
    21: "promise-to-pay commitments must track amount, due date, channel, collector, success criteria, breach, and reopened strategy",
    22: "late charge controls must govern grace, assessment, waiver, reinstatement, cure, recurring charges, and statement presentation",
    23: "hardship workflows must capture cause, duration, relief, documents, occupancy or business status, milestones, and trial conversion",
    24: "modification accounting must approve capitalized interest, fees, deferred principal, forgiveness, re-aging, and schedule reset",
    25: "payoff quotes must reproduce principal, accrued interest, escrow, fees, prepayment charges, per-diem, good-through dates, and assumptions",
    26: "closure must block until final funds, refunds, lien satisfaction, title release, dispatch, disputes, reversals, and archive evidence clear",
    27: "charge-off servicing must separate accounting posture from legal and contact posture while governing recoveries and settlements",
    28: "bankruptcy, deceased borrower, probate, litigation hold, stay, counsel, and prohibited contact restrictions must be enforced",
    29: "insurance and tax exceptions must govern lapsed coverage, force placement, tax delinquency, escrow advances, and shortage cures",
    30: "complaints and disputes must maintain intake channel, allegation, remedy, owner, response clock, specialist routing, and final disposition",
    31: "notices must be cataloged by product, stage, borrower segment, trigger, template version, channel, suppression, and proof of delivery",
    32: "fair lending monitoring must compare approvals, counteroffers, exceptions, pricing, and modification outcomes across monitored segments",
    33: "covenants must track financial reporting, thresholds, collateral tests, receipt status, cure periods, breach workflows, and waivers",
    34: "servicing fees must flow through a catalog with trigger, cap, waiver authority, refund logic, statement presentation, and reason code",
    35: "exceptions require structured reasons, evidence, approvals, thresholds, expiry, and second review for policy-critical fields",
    36: "tenant configuration must isolate products, policies, notice packs, fee rules, approval limits, covenants, and loss-mitigation settings",
    37: "loan history must replay intake, decision, offer, funding, boarding, payments, delinquency, modification, payoff, and closure events",
    38: "cross-PBC handoffs must expose only declared APIs, events, and projections for policy, audit, KPI, funding, accounting, and payoff consumers",
    39: "workbench queues must serve underwriters, closers, servicing specialists, collectors, and compliance reviewers with SLA quick actions",
    40: "application detail must show parties, income, bureau, collateral, ratios, reasons, conditions, rule version, and risk score together",
    41: "servicing detail must show balances, transaction history, next due, escrow, delinquency, active cases, payoff readiness, and timeline",
    42: "collections UI must pin contact history, promises, hardship eligibility, and warnings for stays, cease-contact, complaints, and holds",
    43: "intake agents must draft records from documents, cite sources, propose stipulations, and require confirmation before governed writes",
    44: "underwriter copilots must summarize evidence, simulate policy outcomes, mark uncertainty, and leave credit judgment with reviewers",
    45: "servicing agents must summarize account status but gate balance, delinquency, communication, and modification actions behind approval",
    46: "audit agents must assemble policy, notices, approvals, controls, and sealed references from evidence, withholding unsupported claims",
    47: "release evidence must map every change to APIs, tables, events, notices, controls, UI, agents, tests, approvals, and lifecycle stages",
    48: "continuous controls must test approval authority, override limits, boarding, notice, payment, escrow, payoff, and sealed proof integrity",
    49: "synthetic portfolios and dashboards must cover prime, thin-file, secured, hardship, escrowed, delinquent, charge-off, and payoff scenarios",
    50: "readiness must govern migrations, policy effective dates, queues, training, notices, dashboards, rollback, and early-life sample checks",
}

_BASE_FIELDS = (
    "tenant_id",
    "application_id",
    "loan_id",
    "product_family",
    "lifecycle_stage",
    "policy_version",
    "required_evidence",
    "approval_record",
)


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
    proof_field = _PRIMARY_PROOF_FIELDS[capability.feature_number]
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"lending_origination_servicing_{capability.slug}_control",),
        "fields": _BASE_FIELDS + (proof_field,),
        "ui": f"LendingOriginationServicing{_camel(capability.slug)}Panel",
        "route": f"POST /lending-origination-servicing/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
        "primary_proof": proof_field,
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {
    capability.feature_number: _spec_for(capability) for capability in LENDING_CONTROL_CAPABILITIES
}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update(
        {
            "database_backend": "postgresql",
            "event_contract": EVENT_CONTRACT,
            "event_topic": LENDING_CONTROL_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "human_confirmation": True,
            "side_effects": (),
        }
    )
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    spec = CONTROL_SPECS[capability.feature_number]
    proof_field = spec["primary_proof"]
    if payload.get(proof_field) is not True:
        findings.append(f"{capability.title} requires {proof_field.replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[capability.feature_number])
    if capability.feature_number in (43, 44, 45, 46) and payload.get("human_confirmation") is False:
        findings.append("lending agents must propose or draft only; approval is required before governed loan mutations")
    if capability.feature_number in (32, 36, 38) and payload.get("shared_table_access"):
        findings.append("fair-lending, tenant, and cross-PBC context must use owned data plus declared APIs/events/projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != LENDING_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("lending eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in LENDING_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary lending datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("lending controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_lending_control(
    capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None
) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in LENDING_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(
        dependency for dependency in spec["dependencies"] if dependency not in LENDING_CONTROL_DECLARED_DEPENDENCIES
    )
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": LENDING_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": LENDING_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "domain_message": _DOMAIN_MESSAGES[resolved.feature_number],
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


def improve1_lending_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_lending_control(capability) for capability in LENDING_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.lending-origination-servicing-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": LENDING_CONTROL_OWNED_TABLES,
        "declared_dependencies": LENDING_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": LENDING_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": LENDING_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


LENDING_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_lending_control(slug, payload))
    for capability in LENDING_CONTROL_CAPABILITIES
}

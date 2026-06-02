"""Executable improve1 controls for the Loyalty Rewards PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS, LOYALTY_REWARDS_OWNED_TABLES, LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC, LOYALTY_REWARDS_RUNTIME_TABLES

PBC_KEY = "loyalty_rewards"
EVENT_CONTRACT = "AppGen-X"
LOYALTY_CONTROL_ALLOWED_DATABASE_BACKENDS = LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS
LOYALTY_CONTROL_REQUIRED_EVENT_TOPIC = LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC
LOYALTY_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(f"loyalty_rewards_{table}" if not str(table).startswith("loyalty_rewards_") else str(table) for table in LOYALTY_REWARDS_OWNED_TABLES) + tuple(LOYALTY_REWARDS_RUNTIME_TABLES) + tuple(f"loyalty_rewards_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES)))
LOYALTY_CONTROL_DECLARED_DEPENDENCIES = ("PaymentCaptured", "PromotionApplied", "RewardBalanceChanged", "CustomerSegmentUpdated", "ConsentStatusProjected", "PartnerAccrualProjected", "PartnerSettlementProjected", "AuditEventSealed", "PolicyChanged")
LOYALTY_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in LOYALTY_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in LOYALTY_CONTROL_CAPABILITIES}
_PRIMARY_PROOF_FIELDS = {1: 'enrollment_eligibility_evidence_recorded', 2: 'account_lifecycle_transition_allowed', 3: 'wallet_unit_liability_governed', 4: 'append_only_ledger_proof_present', 5: 'adjustment_reversal_approval_complete', 6: 'earning_rule_version_trace_bound', 7: 'earning_simulation_guardrails_ready', 8: 'promotion_stacking_conflicts_resolved', 9: 'tier_calendar_window_evaluated', 10: 'tier_benefit_entitlement_ledgered', 11: 'downgrade_fairness_review_complete', 12: 'redemption_reservation_lock_valid', 13: 'redemption_catalog_policy_valid', 14: 'redemption_recommendation_reason_recorded', 15: 'expiration_notice_grace_checked', 16: 'expiration_batch_simulation_approved', 17: 'liability_snapshot_drilldown_reconciled', 18: 'liability_control_assertion_passed', 19: 'breakage_forecast_model_governed', 20: 'partner_accrual_reconciliation_matched', 21: 'partner_settlement_evidence_approved', 22: 'referral_fraud_hold_decision_explained', 23: 'referral_lifecycle_state_valid', 24: 'offer_eligibility_trace_explainable', 25: 'offer_fatigue_fairness_checked', 26: 'churn_intervention_guardrails_recorded', 27: 'fraud_review_case_decision_ready', 28: 'account_merge_split_rollback_ready', 29: 'balance_reconciliation_proof_clean', 30: 'cryptographic_balance_proof_verified', 31: 'rewards_policy_compiler_approved', 32: 'rule_impact_analysis_reviewed', 33: 'segment_sync_projection_fresh', 34: 'payment_promotion_event_hardened', 35: 'refund_clawback_policy_applied', 36: 'negative_balance_policy_decided', 37: 'member_statement_visibility_safe', 38: 'operations_cockpit_permissioned', 39: 'anomaly_detection_review_routed', 40: 'exception_resolution_plan_approved', 41: 'reward_roi_assumptions_recorded', 42: 'experiment_holdout_randomization_valid', 43: 'service_agent_approval_preview_required', 44: 'program_design_agent_plan_side_effect_free', 45: 'privacy_consent_purpose_allowed', 46: 'tenant_isolation_proof_passed', 47: 'appgen_event_reliability_proof_passed', 48: 'ui_capability_surface_complete', 49: 'resilience_drill_recovery_evidence_recorded', 50: 'end_to_end_release_proof_passed'}
_FEATURE_DEPENDENCIES = {33: ('CustomerSegmentUpdated',), 34: ('PaymentCaptured', 'PromotionApplied'), 47: ('PaymentCaptured', 'PromotionApplied', 'RewardBalanceChanged', 'CustomerSegmentUpdated'), 45: ('ConsentStatusProjected',), 20: ('PartnerAccrualProjected',), 21: ('PartnerSettlementProjected',)}
_DOMAIN_MESSAGES = {1: 'enrollment must verify identity, consent, region, currency, duplicate wallets, fraud risk, partner eligibility, and disclosures before account creation', 2: 'account lifecycle must control pending, active, suspended, merged, closed, fraud-hold, estate, migrated, and archived transitions', 3: 'wallet units must govern points, miles, credits, stamps, cashback, partner conversions, rounding, expiration, and liability values', 4: 'points ledgers must be append-only with source event, rule version, idempotency, reversal link, balance-after proof, and liability impact', 5: 'adjustments and reversals require reason taxonomy, evidence, approvals, customer visibility, expiration effects, tier effects, and liability recalculation', 6: 'earning rules must preserve effective windows, predicates, multipliers, stacking, partner overrides, rounding, caps, and compiled hash lineage', 7: 'earning simulations must preview member impact, issued points, liability, fraud exposure, partner settlement, edge cases, and guardrails', 8: 'promotion stacking must enforce exclusion groups, precedence, caps, campaign budgets, conflicts, suppressions, and approval gates', 9: 'tier qualification must model periods, grace, soft landings, lifetime thresholds, status matches, freezes, exclusions, and next review', 10: 'tier benefits must ledger granted, consumed, expired, revoked, transferred benefits with source decision and downstream projection payloads', 11: 'downgrades must account for late accruals, disputes, goodwill, outages, protected cohorts, exceptions, and communication evidence', 12: 'redemptions must reserve, confirm, cancel, expire, reverse, partially release, lock points, and prevent duplicate spend', 13: 'redemption catalog options must govern cost, value, inventory, capacity, fulfillment, tiers, regions, blackout dates, partners, and policy proof', 14: 'redemption optimization must rank options by preference, liability, cost, capacity, margin, fairness, and deterministic rule-only mode', 15: 'point expiration must enforce notices, rescue offers, grace windows, protected statuses, jurisdiction rules, recalculation, and explanations', 16: 'expiration batches must simulate liability release, complaint risk, sentiment, support volume, reactivation, exclusions, and segments', 17: 'liability snapshots must reconcile points, value bands, reservations, partner receivables/payables, breakage assumptions, and ledger deltas', 18: 'liability controls must test immutability, reconciliation, expiration authorization, holds, partner completeness, model approval, and rule approvals', 19: 'breakage forecasts must govern cohorts, redemption history, expiry rules, activity, tier, promotions, model version, confidence, and approvals', 20: 'partner accrual reconciliation must handle contracts, source refs, conversion rates, settlement periods, duplicates, disputes, late events, and posting', 21: 'partner settlements must prove obligations, member points, finance liability, invoice payloads, exceptions, and approval workflow', 22: 'referral fraud must score identity, device, address, purchase quality, returns, velocity, geography, reward value, holds, and evidence', 23: 'referral lifecycle must track invite, click, signup, qualification, pending, approval, rejection, reversal, expiry, timing, and communications', 24: 'offer traces must explain shown, hidden, blocked, or expired decisions using segment, tier, balance, consent, region, risk, budget, and rule version', 25: 'offer fairness must manage fatigue caps, diversity, cohorts, protected restrictions, exposure history, and suppression explanations', 26: 'churn interventions must combine risk, value, tier, breakage, engagement, offer history, expected impact, cost, confidence, and ethics', 27: 'fraud cases must manage evidence, linked accounts, ledger entries, investigator notes, holds, releases, reversals, appeals, and privacy boundaries', 28: 'account merge and split must preview identity, ledger consolidation, tier recalculation, referrals, holds, consent, rollback, and approvals', 29: 'balance reconciliation must recompute balances from ledger, find mismatches, isolate entries, propose corrections, and record proof', 30: 'balance proof must produce cryptographic, redacted verifier artifacts for balances, tiers, reservations, liability snapshots, and partners', 31: 'policy compilation must convert structured and natural-language rules into validated predicates, effective dates, conflicts, tests, and approvals', 32: 'rule impact analysis must quantify members, issuance, liability, tier changes, redemption cost, breakage, settlement, and complaint risk', 33: 'segment synchronization must use declared events and projections with freshness, source, allowed usage, and member-impact evidence', 34: 'payment and promotion handling must verify schema versions, idempotency, references, reversals, stacking evidence, retries, and dead-letter reasons', 35: 'refund clawback must handle full returns, partial returns, exchanges, delays, negative balances, tier effects, expired points, and fraud triggers', 36: 'negative balance governance must decide holds, future earn offsets, forgiveness, exception review, tier policy, reason, amount, and jurisdiction', 37: 'member statements must show ledger, rules, expirations, holds, tier progress, benefits, partners, disputes, and hide internal sensitive notes', 38: 'operations cockpit must expose KPIs, liability, risk accounts, redemptions, partner exceptions, tier movement, expiration, fraud, events, and controls', 39: 'anomaly detection must route ledger velocity, balance jumps, redemption bursts, partner spikes, referral rings, expirations, and tier outliers', 40: 'exceptions must govern disputed points, missing earns, failed redemptions, partner delays, appeals, goodwill, evidence, SLA, actions, and closure', 41: 'ROI analytics must store incremental revenue, redemption lift, retention impact, tier migration, engagement, offer ROI, liability, breakage, and confidence', 42: 'experiments must define cells, holdouts, randomization, eligibility, exposure, outcomes, statistics, and rule-version linkage', 43: 'service agents must answer balances, explain ledgers, find missing earns, draft adjustments, preview redemptions, and require approval for mutations', 44: 'program-design agents must parse documents into rules, tiers, benefits, redemptions, expiration policy, tests, ambiguity, and side-effect-free plans', 45: 'privacy controls must enforce consent and purpose for offers, segments, statements, partner sharing, analytics, and blocked decisions', 46: 'tenant isolation must prove accounts, ledgers, rules, redemptions, tiers, partners, liabilities, models, events, and UI queries never bleed across tenants', 47: 'event reliability must prove schemas, idempotency, ordering, retries, dead letters, replay, recovery, duplicates, corrections, failures, and outbox replay', 48: 'UI proof must cover enrollment, accounts, ledger, rules, adjustments, redemptions, tiers, referrals, partners, offers, expiration, liability, fraud, events, controls, and agents', 49: 'resilience drills must cover event replay, promotion rollback, partner outage, bad rules, redemption failure, reconciliation mismatch, and dead-letter surge', 50: 'end-to-end release proof must exercise enrollment, earn, promotion, adjustment, redemption, tier, benefits, referral, partner, expiration, liability, fraud, breakage, offer, exception, reconciliation, proof, UI, eventing, boundary, and agent planning'}
_BASE_FIELDS = ("tenant_id", "program_id", "account_id", "member_id", "wallet_unit", "policy_version", "required_evidence", "approval_record")


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
    return {"title": capability.title, "slug": capability.slug, "tables": (f"loyalty_rewards_{capability.slug}_control",), "fields": _BASE_FIELDS + (proof_field,), "ui": f"LoyaltyRewards{_camel(capability.slug)}Panel", "route": f"POST /loyalty-rewards/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()), "primary_proof": proof_field}


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in LOYALTY_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({"database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "event_topic": LOYALTY_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "human_confirmation": True, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    spec = CONTROL_SPECS[capability.feature_number]
    proof_field = spec["primary_proof"]
    if payload.get(proof_field) is not True:
        findings.append(f"{capability.title} requires {proof_field.replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[capability.feature_number])
    if capability.feature_number in (31, 43, 44) and payload.get("human_confirmation") is False:
        findings.append("loyalty agents must generate side-effect-free plans and require approval before governed reward mutations")
    if capability.feature_number in (33, 45, 46, 47) and payload.get("shared_table_access"):
        findings.append("customer, consent, event, and tenant context must use declared projections/events/APIs only")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != LOYALTY_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("loyalty eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in LOYALTY_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary loyalty datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("loyalty controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_loyalty_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in LOYALTY_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in LOYALTY_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": LOYALTY_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": LOYALTY_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "domain_message": _DOMAIN_MESSAGES[resolved.feature_number], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_loyalty_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_loyalty_control(capability) for capability in LOYALTY_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.loyalty-rewards-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": LOYALTY_CONTROL_OWNED_TABLES, "declared_dependencies": LOYALTY_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": LOYALTY_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": LOYALTY_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


LOYALTY_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_loyalty_control(slug, payload)) for capability in LOYALTY_CONTROL_CAPABILITIES}

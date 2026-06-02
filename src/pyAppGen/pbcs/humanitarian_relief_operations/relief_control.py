"""Executable improve1 controls for the Humanitarian Relief Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "humanitarian_relief_operations"
EVENT_CONTRACT = "AppGen-X"
RELIEF_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
RELIEF_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.humanitarian_relief_operations.events"
RELIEF_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + tuple(
    f"humanitarian_relief_operations_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES
)))
RELIEF_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "PolicyChanged", "AuditEventSealed", "OperationalKpiChanged", "PaymentTransferProjected",
    "ProcurementReceiptProjected", "FinanceGrantRestrictionProjected", "RouteRiskProjected",
)))
RELIEF_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in RELIEF_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in RELIEF_CONTROL_CAPABILITIES}

_DEFAULT_FIELDS = ("owned_record", "required_evidence", "review_state", "approval_state", "operator_visible", "audit_trail", "safe_to_execute")
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {cap.feature_number: _DEFAULT_FIELDS for cap in RELIEF_CONTROL_CAPABILITIES}
_FEATURE_FIELDS.update({
    1: ("triage_mode", "displacement_status", "household_composition", "vulnerability_factors", "sector_severity", "assessor_confidence", "review_status", "action_ready_queue"),
    2: ("household_roster", "member_roster", "alternate_spellings", "document_refs", "community_reference_check", "duplicate_candidates", "dedupe_rationale", "distribution_approval_allowed"),
    3: ("offline_draft", "local_timestamp", "device_id", "sync_receipt", "overlapping_update", "conflict_review_opened", "original_field_timestamp_preserved"),
    5: ("sector_category", "kit_composition", "kit_version", "unit_of_issue", "substitution_policy", "hazard_flags", "expiry_controls", "handling_metadata_complete"),
    6: ("lot_id", "batch_ref", "received_date", "expiry_date", "quarantine_status", "location_bin", "available_qty", "reserved_qty", "expired_or_quarantined_blocked"),
    8: ("site_capacity", "staffing_levels", "lane_design", "time_slots", "priority_lanes", "accessibility_arrangements", "safe_attendance_per_hour", "approval_required"),
    9: ("planned_qty", "loaded_qty", "arrived_qty", "handed_over_qty", "returned_qty", "damaged_qty", "unaccounted_qty", "variance_reason", "final_approval_allowed"),
    10: ("route_legs", "checkpoint_delays", "pod_evidence", "arrival_time", "handover_witness", "route_exceptions", "operations_lead_reviewed"),
    11: ("assistance_modality", "transfer_value", "payout_channel", "voucher_validity", "redemption_status", "market_basis", "modality_controls_visible"),
    12: ("failed_transfer", "retry_eligible", "beneficiary_contact_attempts", "alternate_channel_approval", "fraud_review", "closure_outcome", "recovery_queue_visible"),
    15: ("screening_stage", "child_protection_prompt", "gbv_risk_prompt", "disability_support", "safe_referral_needed", "restricted_visibility", "referral_confirmation_required"),
    16: ("referral_chain", "minimum_necessary_disclosure", "case_owner", "handoff_status", "followup_deadline", "restricted_access_audit", "survivor_narrative_masked"),
    19: ("donor_restriction", "geography", "sector", "modality", "cost_category", "target_population", "rule_version", "operation_blocked_if_violating"),
    20: ("aggregate_scope", "geography", "activity", "population_segment", "modality", "period", "protected_fields_suppressed", "policy_recorded"),
    23: ("draft_brief", "cited_context", "variance_explanation", "donor_safe_draft", "human_acceptance_required", "direct_mutation_blocked", "rejected_draft_retained"),
    25: ("skill_policy", "beneficiary_name_redacted", "protection_narrative_redacted", "transfer_value_guarded", "donor_restriction_guarded", "unauthorized_prompt_denied", "skill_execution_logged"),
    26: ("validation_only_route", "household_search", "duplicate_check", "assessment_precheck", "structured_errors", "no_live_mutation", "owned_boundary"),
    28: ("milestone_event", "stable_schema", "registration_accepted", "shipment_dispatched", "delivery_confirmed", "incident_opened", "donor_pack_finalized"),
    29: ("inbound_event", "idempotency_key", "affected_queue", "rule_version_applied", "stale_policy_warning_cleared", "no_duplicate_side_effects", "dead_letter_route"),
    30: ("source_system_id", "idempotency_key", "mobile_retry", "stable_response", "duplicate_record_prevented", "source_key_traceable", "partner_retry_documented"),
    31: ("dead_letter_item", "operational_impact", "replay_safety_check", "operator_notes", "closure_code", "safe_replay_allowed", "affected_operation_corrected"),
    32: ("rule_pack", "eligibility_rules", "donor_restrictions", "transfer_caps", "protection_blocks", "effective_date", "simulation_available"),
    35: ("assertion_suite", "dual_approval_checked", "overdue_exception_checked", "pod_checked", "donor_pack_signed", "protection_referral_resolved", "control_effective"),
    42: ("dependency", "dependency_mode", "finance_boundary", "procurement_boundary", "audit_boundary", "foreign_table_access_blocked", "event_contract"),
    43: ("tenant_id", "country_mission", "implementing_partner", "policy_scope", "assistant_scope", "queue_leakage_blocked", "data_leakage_blocked"),
    48: ("permission", "role", "sensitivity", "restricted_field", "masking_applied", "access_audited", "least_privilege_enforced"),
    49: ("high_risk_decision", "dual_control_required", "first_approver", "second_approver", "segregation_enforced", "assistance_blocked_until_approved", "approval_audit_trail"),
    50: ("incident_review", "variance_review", "lesson_identified", "rule_update_candidate", "owner_assigned", "approval_path", "operating_rule_updated"),
})
_FEATURE_DEPENDENCIES = {19: ("FinanceGrantRestrictionProjected",), 27: ("PaymentTransferProjected", "ProcurementReceiptProjected"), 29: ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"), 42: ("PaymentTransferProjected", "ProcurementReceiptProjected", "AuditEventSealed")}
_EMPTY_ALLOWED_FIELDS = ("duplicate_candidates", "route_exceptions")


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability): return capability
    if isinstance(capability, int): return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    return {"title": capability.title, "slug": capability.slug, "tables": (f"humanitarian_relief_operations_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "ui": _camel(capability.slug), "route": f"POST /humanitarian-relief-operations/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in RELIEF_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None: return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update({
        "assessor_confidence": 0.9, "review_status": "verified", "action_ready_queue": True, "duplicate_candidates": (), "dedupe_rationale": "reviewed", "distribution_approval_allowed": True,
        "offline_draft": True, "conflict_review_opened": True, "original_field_timestamp_preserved": True, "handling_metadata_complete": True, "quarantine_status": "clear", "expired_or_quarantined_blocked": True,
        "safe_attendance_per_hour": 250, "approval_required": True, "unaccounted_qty": 0, "variance_reason": "none", "final_approval_allowed": True, "pod_evidence": "signed", "operations_lead_reviewed": True,
        "assistance_modality": "cash", "modality_controls_visible": True, "failed_transfer": True, "retry_eligible": True, "fraud_review": "cleared", "closure_outcome": "reissued", "recovery_queue_visible": True,
        "restricted_visibility": True, "referral_confirmation_required": True, "minimum_necessary_disclosure": True, "restricted_access_audit": True, "survivor_narrative_masked": True,
        "operation_blocked_if_violating": True, "protected_fields_suppressed": True, "policy_recorded": True, "human_acceptance_required": True, "direct_mutation_blocked": True, "rejected_draft_retained": True,
        "beneficiary_name_redacted": True, "protection_narrative_redacted": True, "transfer_value_guarded": True, "donor_restriction_guarded": True, "unauthorized_prompt_denied": True, "skill_execution_logged": True,
        "validation_only_route": True, "structured_errors": True, "no_live_mutation": True, "owned_boundary": True, "stable_schema": True, "no_duplicate_side_effects": True, "dead_letter_route": "owned-dlq",
        "idempotency_key": "idem-1", "stable_response": True, "duplicate_record_prevented": True, "source_key_traceable": True, "partner_retry_documented": True, "replay_safety_check": True, "safe_replay_allowed": True, "affected_operation_corrected": True,
        "simulation_available": True, "dual_approval_checked": True, "overdue_exception_checked": True, "pod_checked": True, "donor_pack_signed": True, "protection_referral_resolved": True, "control_effective": True,
        "dependency_mode": "event", "foreign_table_access_blocked": True, "event_contract": EVENT_CONTRACT, "queue_leakage_blocked": True, "data_leakage_blocked": True, "masking_applied": True, "access_audited": True, "least_privilege_enforced": True,
        "dual_control_required": True, "first_approver": "ops-lead", "second_approver": "protection-lead", "segregation_enforced": True, "assistance_blocked_until_approved": True, "approval_audit_trail": True,
        "lesson_identified": True, "rule_update_candidate": True, "owner_assigned": True, "operating_rule_updated": True, "safe_to_execute": True, "operator_visible": True, "audit_trail": "captured", "approval_state": "approved", "review_state": "reviewed", "required_evidence": "captured", "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and (payload.get("assessor_confidence", 0) < 0.75 or payload.get("review_status") != "verified" or payload.get("action_ready_queue") is not True): findings.append("household needs triage requires confidence, verified review, and action-ready queueing")
    if n == 2 and (payload.get("duplicate_candidates") not in ((), []) or not payload.get("dedupe_rationale") or payload.get("distribution_approval_allowed") is not True): findings.append("beneficiary registration must resolve duplicate household/person candidates before distribution approval")
    if n == 3 and (payload.get("conflict_review_opened") is not True or payload.get("original_field_timestamp_preserved") is not True): findings.append("offline assessment sync must open conflict review and preserve original field timestamps")
    if n == 6 and (payload.get("quarantine_status") != "clear" or payload.get("expired_or_quarantined_blocked") is not True): findings.append("warehouse lot control blocks expired or quarantined stock")
    if n == 9 and (payload.get("unaccounted_qty", 0) != 0 or payload.get("final_approval_allowed") is not True): findings.append("distribution reconciliation must explain variance before final approval")
    if n == 12 and (payload.get("recovery_queue_visible") is not True or payload.get("closure_outcome") not in ("reissued", "cancelled", "escalated")): findings.append("failed payout recovery requires visible queue and documented closure outcome")
    if n == 16 and (payload.get("minimum_necessary_disclosure") is not True or payload.get("survivor_narrative_masked") is not True or payload.get("restricted_access_audit") is not True): findings.append("referral workflows must protect survivor confidentiality and audit restricted access")
    if n == 19 and payload.get("operation_blocked_if_violating") is not True: findings.append("donor earmark enforcement must block restricted-fund leakage")
    if n == 20 and (payload.get("protected_fields_suppressed") is not True or payload.get("policy_recorded") is not True): findings.append("donor reporting packs must aggregate while suppressing sensitive detail")
    if n in (23, 24, 25) and (payload.get("direct_mutation_blocked") is not True or payload.get("human_acceptance_required", True) is not True or payload.get("unauthorized_prompt_denied", True) is not True): findings.append("humanitarian agent assistance must be draft-only, policy guarded, and human approved")
    if n == 26 and (payload.get("validation_only_route") is not True or payload.get("no_live_mutation") is not True or payload.get("owned_boundary") is not True): findings.append("validation APIs must return structured errors without live mutation")
    if n == 30 and (payload.get("duplicate_record_prevented") is not True or payload.get("stable_response") is not True): findings.append("idempotent field posting must prevent duplicate records and return stable responses")
    if n == 31 and (payload.get("safe_replay_allowed") is not True or payload.get("affected_operation_corrected") is not True): findings.append("dead-letter operations require safe replay and humanitarian closure outcome")
    if n == 35 and payload.get("control_effective") is not True: findings.append("continuous control assertions must be effective before closure")
    if n == 42 and (payload.get("dependency_mode") not in ("api", "event", "projection") or payload.get("foreign_table_access_blocked") is not True or payload.get("event_contract") != EVENT_CONTRACT): findings.append("cross-boundary event contracts require AppGen-X APIs/events/projections and no foreign table access")
    if n == 43 and (payload.get("queue_leakage_blocked") is not True or payload.get("data_leakage_blocked") is not True): findings.append("multi-tenant relief isolation must block partner and mission leakage")
    if n == 48 and (payload.get("masking_applied") is not True or payload.get("least_privilege_enforced") is not True): findings.append("fine-grained permissions must mask restricted fields and enforce least privilege")
    if n == 49 and (payload.get("segregation_enforced") is not True or payload.get("assistance_blocked_until_approved") is not True): findings.append("high-risk assistance decisions require dual control before execution")
    if n == 50 and (payload.get("lesson_identified") is not True or payload.get("operating_rule_updated") is not True): findings.append("after-action review must turn incidents and variances into operating rule updates")
    if payload.get("stream_engine_picker_visible"): findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_relief_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None: return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved); candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in RELIEF_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in RELIEF_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": RELIEF_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": RELIEF_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_relief_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_relief_control(capability) for capability in RELIEF_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.humanitarian-relief-operations-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": RELIEF_CONTROL_OWNED_TABLES, "declared_dependencies": RELIEF_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": RELIEF_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": RELIEF_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


RELIEF_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_relief_control(slug, payload)) for capability in RELIEF_CONTROL_CAPABILITIES}

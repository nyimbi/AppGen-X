"""Executable improve1 controls for the Lead Opportunity PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS,
    LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES,
    LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES,
    LEAD_OPPORTUNITY_OWNED_TABLES,
    LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC,
    LEAD_OPPORTUNITY_RUNTIME_TABLES,
)

PBC_KEY = "lead_opportunity"
EVENT_CONTRACT = "AppGen-X"
LEAD_CONTROL_ALLOWED_DATABASE_BACKENDS = LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS
LEAD_CONTROL_REQUIRED_EVENT_TOPIC = LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC
LEAD_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(
    tuple(LEAD_OPPORTUNITY_OWNED_TABLES) + tuple(LEAD_OPPORTUNITY_RUNTIME_TABLES) + tuple(
        f"lead_opportunity_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES
    )
))
LEAD_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(
    tuple(LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES)
    + tuple(LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES)
    + (
        "CustomerSegmentUpdated",
        "CustomerUpdated",
        "QuoteProposalRequested",
        "TerritoryProjectionUpdated",
        "BillingProjectionUpdated",
        "MarketingLeadCaptured",
        "ProductCatalogChanged",
        "FinancePolicyChanged",
        "AuditEventSealed",
    )
))
LEAD_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in LEAD_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in LEAD_CONTROL_CAPABILITIES}
_DEFAULT_FIELDS = ("owned_record", "pipeline_context", "required_evidence", "operator_visible", "audit_trail", "safe_to_execute")
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {cap.feature_number: _DEFAULT_FIELDS for cap in LEAD_CONTROL_CAPABILITIES}
_FEATURE_FIELDS.update({
    1: ("account_id", "tenant", "parent_account", "customer_projection_key", "region", "owner", "active_status", "duplicate_account_risk", "hierarchy_depth", "audit_proof", "account_readiness_gate_passed"),
    2: ("parent_account_id", "child_account_id", "effective_date", "region_compatibility", "owner_inheritance", "merge_split_lineage", "rollup_recalculated", "acyclic_parentage_enforced"),
    3: ("lead_source", "contact_email", "consent_marker", "region", "currency", "estimated_value", "account_projection", "duplicate_candidates", "assignment_policy", "lead_intake_ready"),
    4: ("lead_state", "actor", "timestamp", "transition_reason", "score_snapshot", "assignment_evidence", "qualification_decision", "invalid_transition_explained", "state_transition_valid"),
    5: ("enrichment_source", "fields_changed", "confidence", "freshness", "consent_status", "segment_fit", "account_match", "value_estimate", "enrichment_audit_hash", "rejected_enrichment_recorded"),
    6: ("dedupe_case", "candidate_leads", "matching_factors", "confidence", "owner_conflicts", "merge_decision", "reviewer", "account_impact", "score_recalculation_requested"),
    7: ("score_snapshot", "source_weight", "segment_fit", "engagement_score", "account_fit", "estimated_value", "negative_signals", "score_version", "threshold_comparison", "score_explainable"),
    8: ("assignment_rule", "territory", "segment", "account_owner", "workload", "skill", "language", "round_robin_state", "fallback_owner", "assignment_rationale_recorded"),
    9: ("qualification_threshold", "actual_score", "missing_data", "disqualifying_factors", "reviewer_override", "decision_reason", "valid_through", "lead_qualified_event_evidence"),
    10: ("limit_scope", "account_open_count", "owner_open_count", "segment_open_count", "region_open_count", "exception_workflow", "reassignment_recommendation", "open_opportunity_limit_enforced"),
    11: ("qualified_lead", "account_hierarchy", "amount", "currency", "stage", "close_date", "owner", "win_probability", "forecast_amount", "quote_proposal_eligible", "opportunity_creation_ready"),
    12: ("opportunity_state", "from_stage", "to_stage", "transition_rule", "forecast_change", "quote_handoff", "closure_reason", "audit_event", "opportunity_transition_valid"),
    13: ("stage_history", "prior_stage", "new_stage", "owner", "reason", "required_fields", "probability_change", "close_date_change", "forecast_snapshot_linked"),
    14: ("forecast_snapshot", "open_amount", "weighted_amount", "commit_view", "best_case_view", "pipeline_view", "close_date_distribution", "source_opportunities", "forecast_reproducible"),
    15: ("slippage_signal", "close_date_push", "stale_activity", "stage_stagnation", "negative_sentiment", "missing_next_step", "quote_delay", "recommended_action", "slippage_risk_detected"),
    16: ("probability_model", "stage", "activity_sentiment", "account_fit", "owner_history", "quote_status", "competitor_notes", "historical_outcomes", "win_probability_calibrated"),
    17: ("handoff_id", "opportunity_id", "requested_products", "amount", "currency", "customer_projection", "required_approvals", "deadline", "idempotency_key", "quote_proposal_event_evidence"),
    18: ("outcome_type", "reason", "competitor", "amount", "close_date", "sales_cycle", "lost_stage", "customer_feedback", "downstream_event_evidence", "outcome_complete"),
    19: ("won_stage", "amount_currency_valid", "customer_projection_fresh", "quote_status", "owner_approval", "duplicate_win_prevented", "opportunity_won_event", "customer_updated_event", "win_handoff_ready"),
    20: ("loss_category", "competitor", "price_reason", "product_reason", "fit_reason", "engagement_pattern", "stage_lost", "coaching_insight", "loss_analysis_recorded"),
    21: ("activity_type", "subject", "timestamp", "owner", "channel", "sentiment", "participants", "outcome", "next_step", "immutable_activity_proof"),
    22: ("activity_note", "sentiment", "intent", "objections", "buying_signals", "timeline", "decision_makers", "competitor_mentions", "reviewer_confidence", "intent_extraction_reviewed"),
    23: ("recommended_action", "stage", "stale_activity", "sentiment", "missing_stakeholders", "quote_delay", "close_date_risk", "buyer_objection", "rationale", "next_best_action_ranked"),
    24: ("coaching_insight", "source_activity", "recommendation", "owner", "manager_review", "accepted_or_dismissed", "follow_up_evidence", "outcome_correlation", "coaching_lifecycle_tracked"),
    25: ("segment_projection", "segment_id", "version", "freshness", "confidence", "allowed_use", "tenant", "event_id", "retry_dead_letter_evidence", "projection_only_boundary"),
    26: ("territory_projection", "freshness", "owner_mapping", "region_compatibility", "override_reason", "assignment_impact", "boundary_evidence", "territory_projection_only"),
    27: ("billing_projection", "payment_health", "balance_band", "renewal_timing", "expansion_eligibility", "projection_freshness", "scoring_explanation", "billing_projection_only"),
    28: ("revenue_policy", "qualification_policy", "assignment_policy", "opportunity_policy", "stage_policy", "quote_policy", "forecast_policy", "customer_update_policy", "policy_compiled"),
    29: ("runtime_parameter", "bounds", "impact_simulation", "approval_workflow", "effective_date", "tenant_region_override", "rollback", "parameter_release_evidence"),
    30: ("schema_extension", "target_owned_table", "field_validation", "sensitivity_classification", "migration_preview", "ui_binding_preview", "api_exposure_review", "schema_extension_governed"),
    31: ("inbox_event", "idempotency_key", "duplicate_suppression", "retry_evidence", "unsupported_event_rejected", "dead_letter_promotion", "projection_rebuild", "inbox_replay_control"),
    32: ("outbox_event", "ordering_group", "payload_hash", "retry_attempts", "next_retry", "delivery_proof", "dead_letter_linkage", "outbox_replay_control"),
    33: ("boundary_scan", "schema_descriptors", "services", "routes", "dsl", "workbench_bindings", "agent_plans", "foreign_table_access_blocked"),
    34: ("audit_chain", "lead_decisions", "assignments", "qualification", "stage_history", "forecast", "handoffs", "outcomes", "hash_chain_preserved"),
    35: ("pipeline_proof", "qualified_leads", "forecast_snapshot", "stage_history", "outcome", "quote_handoff", "customer_update", "selective_disclosure_proof"),
    36: ("anomaly_signal", "lead_velocity", "duplicate_rate", "score_jump", "assignment_skew", "stage_aging", "forecast_change", "dead_letter_spike", "anomaly_detected"),
    37: ("revenue_exposure", "opportunity", "owner", "region", "segment", "stage", "close_period", "activity_health", "mitigation_actions", "stochastic_exposure_modeled"),
    38: ("governed_model", "model_purpose", "training_window", "feature_lineage", "validation_metrics", "drift", "segment_impact", "approval_status", "model_evidence_complete"),
    39: ("counterfactual_simulation", "threshold_change", "assignment_mode", "stage_probability", "stale_activity_rule", "forecast_floor", "max_open_opportunities", "conversion_effect", "simulation_non_mutating"),
    40: ("sales_instruction", "target_record", "action", "stage", "amount", "date", "owner", "policy_checks", "command_preview", "no_mutation_until_confirmed"),
    41: ("agent_plan", "command", "permission", "owned_tables", "idempotency_key", "expected_event", "forecast_impact", "customer_impact", "human_confirmation", "agent_plan_safe"),
    42: ("lead_inbox", "source", "enrichment_gaps", "duplicate_risk", "score_factors", "assignment_status", "qualification_decision", "stale_warnings", "lead_inbox_complete"),
    43: ("pipeline_workbench", "stage_board", "stage_history", "amount", "probability", "close_date_risk", "activities", "handoffs", "pipeline_workbench_complete"),
    44: ("forecast_cockpit", "owner_view", "region_view", "segment_view", "stage_view", "close_period", "slippage_risk", "changed_since_last", "forecast_cockpit_explainable"),
    45: ("quality_console", "duplicate_queue", "enrichment_gap_queue", "stale_segment_projection", "missing_account_match", "invalid_contact", "owner_conflicts", "review_actions", "dedupe_enrichment_console_complete"),
    46: ("control_test", "opportunity_without_qualified_lead", "win_without_final_stage", "quote_without_opportunity", "stale_segment_scoring", "foreign_table_access", "dead_letter_aging", "agent_preview_bypass_blocked", "continuous_controls_pass"),
    47: ("resilience_drill", "duplicate_segment_event", "projection_delay", "assignment_fallback", "stage_update_conflict", "outbox_failure", "win_event_replay", "degraded_mode", "resilience_drill_safe"),
    48: ("customer_update_gate", "won_outcome", "projection_freshness", "amount_currency", "owner_approval", "duplicate_prevention", "payload_version", "delivery_proof", "customer_update_governed"),
    49: ("readiness_score", "account_hierarchy", "lead_capture", "enrichment", "dedupe", "forecasting", "event_reliability", "ui_coverage", "agent_safety", "readiness_score_evidence_backed"),
    50: ("pipeline_proof_scenario", "account_hierarchy", "segment_event", "lead_capture", "qualification", "opportunity", "activity", "quote_handoff", "forecast", "outcome", "end_to_end_proof_complete"),
})
_FEATURE_DEPENDENCIES = {
    17: ("QuoteProposalRequested",),
    19: ("OpportunityWon", "CustomerUpdated"),
    25: ("CustomerSegmentUpdated",),
    26: ("TerritoryProjectionUpdated",),
    27: ("BillingProjectionUpdated",),
    32: ("LeadQualified", "OpportunityWon", "OpportunityLost", "CustomerUpdated", "QuoteProposalRequested"),
    48: ("CustomerUpdated",),
}
_REQUIRED_TRUE = {
    1: ("account_readiness_gate_passed",), 2: ("rollup_recalculated", "acyclic_parentage_enforced"), 3: ("lead_intake_ready",),
    4: ("state_transition_valid",), 5: ("rejected_enrichment_recorded",), 6: ("score_recalculation_requested",),
    7: ("score_explainable",), 8: ("assignment_rationale_recorded",), 9: ("lead_qualified_event_evidence",),
    10: ("open_opportunity_limit_enforced",), 11: ("opportunity_creation_ready",), 12: ("opportunity_transition_valid",),
    13: ("forecast_snapshot_linked",), 14: ("forecast_reproducible",), 15: ("slippage_risk_detected",),
    16: ("win_probability_calibrated",), 17: ("quote_proposal_event_evidence",), 18: ("outcome_complete",),
    19: ("amount_currency_valid", "customer_projection_fresh", "owner_approval", "duplicate_win_prevented", "opportunity_won_event", "customer_updated_event", "win_handoff_ready"),
    20: ("loss_analysis_recorded",), 21: ("immutable_activity_proof",), 22: ("intent_extraction_reviewed",),
    23: ("next_best_action_ranked",), 24: ("coaching_lifecycle_tracked",), 25: ("projection_only_boundary",),
    26: ("territory_projection_only",), 27: ("billing_projection_only",), 28: ("policy_compiled",),
    29: ("impact_simulation", "approval_workflow", "parameter_release_evidence"), 30: ("schema_extension_governed",),
    31: ("duplicate_suppression", "unsupported_event_rejected", "dead_letter_promotion", "inbox_replay_control"),
    32: ("delivery_proof", "outbox_replay_control"), 33: ("foreign_table_access_blocked",), 34: ("hash_chain_preserved",),
    35: ("selective_disclosure_proof",), 36: ("anomaly_detected",), 37: ("stochastic_exposure_modeled",),
    38: ("model_evidence_complete",), 39: ("simulation_non_mutating",), 40: ("command_preview", "no_mutation_until_confirmed"),
    41: ("human_confirmation", "agent_plan_safe"), 42: ("lead_inbox_complete",), 43: ("pipeline_workbench_complete",),
    44: ("forecast_cockpit_explainable",), 45: ("dedupe_enrichment_console_complete",), 46: ("agent_preview_bypass_blocked", "continuous_controls_pass"),
    47: ("resilience_drill_safe",), 48: ("customer_update_governed",), 49: ("readiness_score_evidence_backed",),
    50: ("end_to_end_proof_complete",),
}
_EMPTY_ALLOWED_FIELDS = ("duplicate_candidates", "owner_conflicts", "missing_data", "disqualifying_factors")


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
        "tables": (f"lead_opportunity_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "ui": f"LeadOpportunity{_camel(capability.slug)}Panel",
        "route": f"POST /lead-opportunity/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in LEAD_CONTROL_CAPABILITIES}


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
        "event_topic": LEAD_CONTROL_REQUIRED_EVENT_TOPIC,
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
    if n == 1 and payload.get("account_readiness_gate_passed") is not True:
        findings.append("account hierarchy readiness gate must validate identity, owner, region, projection, duplicate risk, and audit proof")
    if n == 3 and payload.get("lead_intake_ready") is not True:
        findings.append("lead intake must validate contact, consent, region, currency, account context, duplicate risk, and assignment policy")
    if n == 9 and payload.get("lead_qualified_event_evidence") is not True:
        findings.append("qualification decisions must produce LeadQualified event evidence")
    if n == 11 and payload.get("opportunity_creation_ready") is not True:
        findings.append("opportunity creation requires qualified lead, account hierarchy, amount, currency, owner, close date, and quote eligibility")
    if n == 17 and payload.get("quote_proposal_event_evidence") is not True:
        findings.append("quote/proposal handoff must emit QuoteProposalRequested evidence without sharing quote tables")
    if n == 19 and payload.get("win_handoff_ready") is not True:
        findings.append("win handoff must gate OpportunityWon and CustomerUpdated on final stage, amount, projection freshness, approval, and duplicate prevention")
    if n in (25, 26, 27) and payload.get("shared_table_access") is True:
        findings.append("customer, territory, and billing context must remain projection-only")
    if n == 33 and payload.get("foreign_table_access_blocked") is not True:
        findings.append("cross-PBC boundary proof must block foreign customer, segment, billing, territory, quote, product, and finance table access")
    if n == 40 and payload.get("no_mutation_until_confirmed") is not True:
        findings.append("semantic sales instructions must stay as safe previews until confirmed")
    if n == 41 and (payload.get("human_confirmation") is not True or payload.get("agent_plan_safe") is not True):
        findings.append("agent-safe revenue plans require permission, owned tables, idempotency, expected event, impact preview, and human confirmation")
    if n == 46 and payload.get("continuous_controls_pass") is not True:
        findings.append("continuous revenue control testing must catch unsafe wins, stale projections, foreign access, and agent bypass")
    if n == 48 and payload.get("customer_update_governed") is not True:
        findings.append("CustomerUpdated publication must be gated by won outcome, projection freshness, approval, duplicate prevention, payload version, and delivery proof")
    if n == 50 and payload.get("end_to_end_proof_complete") is not True:
        findings.append("end-to-end proof must cover lead capture through opportunity outcome and customer update")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != LEAD_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("lead opportunity eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in LEAD_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary lead opportunity datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("lead opportunity controls must use owned tables plus declared APIs/events/projections")
    return tuple(findings)


def evaluate_lead_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in LEAD_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in LEAD_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": LEAD_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": LEAD_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_lead_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_lead_control(capability) for capability in LEAD_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.lead-opportunity-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": LEAD_CONTROL_OWNED_TABLES,
        "declared_dependencies": LEAD_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": LEAD_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": LEAD_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


LEAD_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_lead_control(slug, payload)) for capability in LEAD_CONTROL_CAPABILITIES}

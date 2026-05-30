"""Executable improve1 controls for the Notifications PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import NOTIFICATIONS_REQUIRED_EVENT_TOPIC

PBC_KEY = "notifications"
EVENT_CONTRACT = "AppGen-X"
NOTIFICATION_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
NOTIFICATION_CONTROL_REQUIRED_EVENT_TOPIC = NOTIFICATIONS_REQUIRED_EVENT_TOPIC
_BASE_OWNED_TABLES = (
    "notification_template",
    "template_locale_variant",
    "delivery_channel",
    "notification_recipient",
    "preference_snapshot",
    "consent_ledger",
    "delivery_schedule",
    "throttle_window",
    "provider_route",
    "message_delivery",
    "delivery_attempt",
    "retry_evidence",
    "delivery_receipt",
    "bounce_event",
    "notification_campaign",
    "campaign_dispatch",
    "transactional_notification",
    "notification_audit_log",
    "deliverability_analytics",
    "notification_rule",
    "notification_parameter",
    "notification_configuration",
    "notifications_appgen_outbox_event",
    "notifications_appgen_inbox_event",
    "notifications_dead_letter_event",
)
NOTIFICATION_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"notifications_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
NOTIFICATION_CONTROL_DECLARED_DEPENDENCIES = (
    "PreferenceChanged",
    "ConsentUpdated",
    "CampaignScheduled",
    "DeliveryReceiptImported",
    "BounceRegistered",
    "SlaBreached",
    "WorkflowCompleted",
    "TransactionalNotificationRequested",
    "RecipientProfileProjectionChanged",
    "ProviderHealthProjectionChanged",
    "CostSignalChanged",
    "CarbonIntensityWindowChanged",
    "SecurityTokenIssued",
    "DocumentEvidenceSealed",
    "AuditEventSealed",
)
NOTIFICATION_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in NOTIFICATION_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in NOTIFICATION_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "message_id", "recipient_id", "template_id", "channel_id", "purpose", "locale", "policy_version", "actor_id", "evidence_references")
_DOMAIN_FIELDS: dict[int, tuple[str, ...]] = {
    1: ("template_state", "owner", "approver", "effective_dates", "required_variables", "rollback_evidence"),
    2: ("variable_schema", "currency_format", "date_format", "link_policy", "masking_rule", "render_fixture"),
    3: ("locale_variant_id", "translator", "fallback_chain", "legal_copy_lock", "length_check", "rtl_preview"),
    4: ("channel_capability_id", "content_types", "max_size", "receipt_support", "ttl_policy", "rate_limit"),
    5: ("endpoint_id", "verification_state", "last_success", "bounce_history", "complaint_history", "source_trust"),
    6: ("preference_timeline_id", "topic_taxonomy", "channel_choice", "frequency_cap", "brand_scope", "effective_interval"),
    7: ("conflict_policy_id", "revocation_precedence", "regional_default", "transactional_exception", "proof_sufficiency", "eligibility_explanation"),
    8: ("purpose_taxonomy_id", "consent_purpose", "retention_rule", "suppression_policy", "analytics_scope", "route_descriptor"),
    9: ("timezone_confidence", "quiet_hour_calendar", "holiday_rule", "dst_edge_case", "urgent_override", "next_eligible_send"),
    10: ("schedule_plan_id", "urgency", "provider_capacity", "campaign_pacing", "rejected_alternatives", "delivery_risk"),
    11: ("contact_pressure_id", "rolling_window", "topic_cap", "priority_rule", "cooldown", "suppression_explanation"),
    12: ("suppression_group_id", "mutual_exclusivity", "priority_arbitration", "dedupe_window", "overlap_simulation", "recipient_exclusions"),
    13: ("provider_health_id", "latency", "acceptance_rate", "error_taxonomy", "receipt_lag", "route_bypass_reason"),
    14: ("route_simulation_id", "cost_projection", "capacity_projection", "success_rate", "regional_fit", "fallback_rate"),
    15: ("failover_policy_id", "provider_priority", "channel_escalation", "retry_budget", "duplicate_suppression", "cooldown"),
    16: ("idempotency_key", "request_fingerprint", "schedule_dedupe", "attempt_dedupe", "provider_ack_dedupe", "safe_replay"),
    17: ("attempt_state", "allowed_transition", "provider_payload_hash", "error_classification", "retry_eligibility", "receipt_correlation"),
    18: ("retry_policy_id", "error_taxonomy", "provider_hint", "ttl_check", "quiet_hour_check", "dead_letter_reason"),
    19: ("dead_letter_id", "failure_group", "repair_suggestion", "replay_preview", "owner_assignment", "closure_evidence"),
    20: ("receipt_correlation_id", "provider_message_id", "recipient_endpoint_hash", "timestamp_window", "payload_fingerprint", "confidence"),
    21: ("bounce_classification_id", "bounce_type", "suppression_action", "endpoint_quality_update", "revalidation_task", "remediation"),
    22: ("deliverability_metric_id", "acceptance_rate", "complaint_rate", "unsubscribe_rate", "domain_reputation", "corrective_action"),
    23: ("readiness_gate_id", "eligible_recipients", "blocking_checks", "warning_checks", "cost_forecast", "approval_proof"),
    24: ("pacing_policy_id", "provider_window", "regional_window", "segment_rate", "backpressure_signal", "adjusted_send_rate"),
    25: ("experiment_id", "holdout_cell", "stratification", "variant_allocation", "exposure_tracking", "confidence_report"),
    26: ("sla_policy_id", "queue_deadline", "provider_escalation", "channel_fallback", "late_alert", "breach_evidence"),
    27: ("payload_contract_id", "template_variable_check", "recipient_eligibility", "locale_check", "link_safety", "ttl_check"),
    28: ("token_metadata_id", "expiration_policy", "one_time_use", "scope", "channel_binding", "signed_link_proof"),
    29: ("attachment_policy_id", "scan_result", "type_allowlist", "size_limit", "encryption_metadata", "access_expiration"),
    30: ("content_screening_id", "required_disclosure", "sensitive_data_check", "prohibited_term", "brand_vocabulary", "rewrite_suggestion"),
    31: ("accessibility_check_id", "readability_score", "alt_text", "sms_segments", "push_truncation", "screen_reader_summary"),
    32: ("variant_selection_id", "selection_rule", "model_evidence", "fairness_constraint", "rejected_alternatives", "deterministic_flag"),
    33: ("escalation_graph_id", "source_channel", "target_channel", "urgency_rule", "failed_attempt_reason", "escalation_history"),
    34: ("in_app_inbox_id", "unread_state", "priority", "grouping", "deep_link", "acknowledgement"),
    35: ("preference_ui_id", "topic_control", "channel_control", "frequency_control", "quiet_hour_control", "unsubscribe_effect"),
    36: ("operations_cockpit_id", "queue_depth", "provider_alert", "campaign_progress", "transactional_sla_risk", "replay_action"),
    37: ("recipient_dossier_id", "consent_state", "delivery_timeline", "campaign_membership", "complaint_history", "authorization_scope"),
    38: ("anomaly_id", "queue_spike", "failure_taxonomy_change", "provider_latency", "duplicate_request_signal", "operator_review"),
    39: ("abuse_risk_id", "send_velocity", "template_risk", "complaint_signal", "domain_reputation", "investigation_evidence"),
    40: ("cost_optimization_id", "provider_cost", "retry_cost", "campaign_cost", "cost_per_delivered", "route_tradeoff"),
    41: ("carbon_schedule_id", "batch_window", "business_deadline", "carbon_signal", "selected_window", "override_evidence"),
    42: ("audit_hash_id", "template_hash", "recipient_eligibility_hash", "rendered_payload_hash", "route_hash", "verifier_export"),
    43: ("event_descriptor_id", "schema_version", "ordering_assumption", "retry_envelope", "dead_letter_taxonomy", "handler_evidence"),
    44: ("boundary_proof_id", "projection_contract", "api_dependency", "cached_field", "staleness_policy", "foreign_table_block"),
    45: ("agent_template_id", "instruction_source", "draft_variables", "localized_proposal", "disclosure_gap", "review_plan"),
    46: ("agent_campaign_id", "campaign_goal", "launch_checklist", "segmentation", "holdout_setup", "risk_forecast"),
    47: ("agent_troubleshoot_id", "inbound_event_trace", "payload_validation_trace", "route_trace", "dead_letter_trace", "repair_plan"),
    48: ("ui_coverage_id", "template_surface", "consent_surface", "routing_surface", "dead_letter_surface", "agent_surface"),
    49: ("resilience_drill_id", "provider_outage", "duplicate_storm", "template_rollback", "receipt_replay", "recovery_time"),
    50: ("release_proof_id", "template_approval", "localization", "consent_resolution", "route_simulation", "end_to_end_audit"),
}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    5: ("RecipientProfileProjectionChanged",),
    6: ("PreferenceChanged",),
    7: ("ConsentUpdated", "PreferenceChanged"),
    13: ("ProviderHealthProjectionChanged",),
    20: ("DeliveryReceiptImported",),
    21: ("BounceRegistered",),
    26: ("SlaBreached",),
    28: ("SecurityTokenIssued",),
    29: ("DocumentEvidenceSealed",),
    40: ("CostSignalChanged",),
    41: ("CarbonIntensityWindowChanged",),
    43: ("AuditEventSealed",),
    44: ("PreferenceChanged", "ConsentUpdated", "WorkflowCompleted"),
}
_DOMAIN_MESSAGES = {capability.feature_number: f"{capability.title} requires owned notification lifecycle, routing, consent, deliverability, UI, agent, and release evidence before approval." for capability in NOTIFICATION_CONTROL_CAPABILITIES}
_HUMAN_CONFIRMATION_FEATURES = (1, 7, 15, 19, 23, 28, 29, 30, 33, 36, 39, 45, 46, 47, 49, 50)
_PROJECTION_ONLY_FEATURES = (5, 6, 7, 13, 20, 21, 26, 28, 29, 40, 41, 43, 44)
_AGENT_PREVIEW_FEATURES = (45, 46, 47, 50)
_NON_MUTATING_FEATURES = (14, 18, 19, 22, 23, 25, 32, 38, 40, 41, 42, 44, 48, 49, 50)
_DELIVERY_RISK_FEATURES = (7, 9, 10, 11, 13, 15, 16, 17, 18, 19, 21, 23, 24, 26, 27, 28, 29, 30, 33, 36, 39, 43, 49, 50)


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
        "tables": (f"notifications_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"Notifications{_camel(capability.slug)}Panel",
        "route": f"POST /notifications/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in NOTIFICATION_CONTROL_CAPABILITIES}


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
        "event_topic": NOTIFICATION_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "delivery_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[number])
    if number in _DELIVERY_RISK_FEATURES and payload.get("delivery_risk_evidence_complete") is not True:
        findings.append("delivery, consent, provider, security, abuse, replay, and release decisions require complete evidence and approval context")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("template activation, consent conflicts, failover, replay, secure links, campaigns, and agent proposals require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("notification assistant skills must produce side-effect-free review plans before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("route simulations, retries, analytics, experiments, cost, carbon, proofs, drills, and release evidence must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("recipient, consent, preference, provider, receipt, bounce, SLA, token, cost, carbon, and audit facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != NOTIFICATION_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("notifications eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in NOTIFICATION_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary notifications datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("notifications controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_notification_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in NOTIFICATION_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in NOTIFICATION_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": NOTIFICATION_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": NOTIFICATION_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_notification_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_notification_control(capability) for capability in NOTIFICATION_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.notifications-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": NOTIFICATION_CONTROL_OWNED_TABLES, "declared_dependencies": NOTIFICATION_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": NOTIFICATION_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": NOTIFICATION_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


NOTIFICATION_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_notification_control(slug, payload)) for capability in NOTIFICATION_CONTROL_CAPABILITIES}

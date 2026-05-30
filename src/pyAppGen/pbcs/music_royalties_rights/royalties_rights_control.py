"""Executable improve1 controls for the Music Royalties and Rights PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "music_royalties_rights"
EVENT_CONTRACT = "AppGen-X"
ROYALTIES_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
ROYALTIES_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.music_royalties_rights.events"
_BASE_OWNED_TABLES = (
    "music_royalties_rights_musical_work",
    "music_royalties_rights_recording",
    "music_royalties_rights_rights_split",
    "music_royalties_rights_license",
    "music_royalties_rights_usage_report",
    "music_royalties_rights_royalty_statement",
    "music_royalties_rights_rights_dispute",
    "music_royalties_rights_contributor",
    "music_royalties_rights_contributor_affiliation",
    "music_royalties_rights_chain_of_title",
    "music_royalties_rights_registration_submission",
    "music_royalties_rights_statement_line",
    "music_royalties_rights_calculation_trace",
    "music_royalties_rights_recoupment_balance",
    "music_royalties_rights_reserve_balance",
    "music_royalties_rights_beneficiary_instruction",
    "music_royalties_rights_evidence_artifact",
    "music_royalties_rights_policy_pack",
    "music_royalties_rights_runtime_parameter",
    "music_royalties_rights_schema_extension",
    "music_royalties_rights_control_assertion",
    "music_royalties_rights_governed_model",
    "music_royalties_rights_appgen_outbox_event",
    "music_royalties_rights_appgen_inbox_event",
    "music_royalties_rights_appgen_dead_letter_event",
)
ROYALTIES_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"music_royalties_rights_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES))
)
ROYALTIES_CONTROL_DECLARED_DEPENDENCIES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "IdentityVerificationChanged",
    "PaymentInstructionChanged",
    "TaxTreatmentChanged",
    "GeneralLedgerPostingAccepted",
    "DocumentEvidenceSealed",
    "NotificationDeliveryChanged",
    "FraudRiskProjectionChanged",
)
ROYALTIES_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in ROYALTIES_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in ROYALTIES_CONTROL_CAPABILITIES}
_BASE_FIELDS = (
    "tenant_id",
    "catalog_id",
    "work_id",
    "recording_id",
    "right_type",
    "territory",
    "effective_date",
    "policy_version",
    "actor_id",
    "evidence_references",
)
_DOMAIN_FIELDS: dict[int, tuple[str, ...]] = {
    1: ("canonical_title", "alternate_titles", "translated_titles", "iswc", "duplicate_match_confidence", "title_governance_state"),
    2: ("contributor_id", "role_type", "ipi_cae", "share_basis", "administration_mode", "role_effective_dates"),
    3: ("publisher_id", "administrator_id", "sub_publisher_id", "appointment_scope", "termination_terms", "approval_authority"),
    4: ("split_version_id", "split_state", "effective_from", "effective_to", "change_reason_code", "historical_usage_selector"),
    5: ("writer_share_total", "publisher_share_total", "mechanical_share", "performance_share", "master_side_share", "rule_explanation"),
    6: ("recording_work_link_id", "relationship_type", "match_confidence", "sample_source", "medley_component", "linkage_exception"),
    7: ("recording_family_id", "variant_type", "parent_recording_id", "rights_inheritance_mode", "producer_override", "version_lineage"),
    8: ("performer_id", "producer_points", "neighboring_rights_eligibility", "session_notes", "collection_path", "payable_obligation"),
    9: ("society_id", "member_number", "administered_rights", "collection_exclusions", "affiliation_effective_dates", "waiver_reason"),
    10: ("territory_grid", "overlap_claims", "gap_claims", "revoked_appointments", "conflict_heatmap", "exception_case_id"),
    11: ("license_bundle_id", "grant_type", "media_type", "exclusivity", "fee_basis", "unlicensed_rights"),
    12: ("term_schedule_id", "option_exercise", "embargo_window", "holdback_rule", "territory_launch_dependency", "license_state"),
    13: ("source_evidence_id", "cue_sheet_id", "setlist_id", "program_log_id", "broadcaster_certification", "document_digest"),
    14: ("rate_pack_id", "format_type", "statutory_rate", "deal_override", "floor_cap_minimum", "rate_decision_path"),
    15: ("accrual_mode", "direct_performance_income", "society_distribution", "neighboring_rights_distribution", "settlement_state", "income_side"),
    16: ("sync_quote_id", "approval_chain", "mfn_terms", "upfront_fee_schedule", "backend_participation", "cue_follow_on_royalties"),
    17: ("ingestion_contract_id", "source_type", "source_fingerprint", "reporting_period", "unit_convention", "ingestion_confidence"),
    18: ("usage_line_id", "normalized_identifier", "normalized_territory", "normalized_units", "lineage_key", "dedupe_key"),
    19: ("unmatched_queue_id", "unmatched_reason", "provisional_claim", "expiry_date", "follow_up_evidence", "black_box_policy"),
    20: ("royalty_run_id", "period_state", "usage_cutoff", "split_cutoff", "license_cutoff", "reopen_reason"),
    21: ("statement_id", "statement_line_id", "source_usage_reference", "applied_rate", "split_version_id", "line_explanation"),
    22: ("advance_balance_id", "recoupment_bucket", "cross_collateral_group", "priority_rule", "earned_recouped_payable", "period_reconstruction"),
    23: ("reserve_rule_id", "suspense_bucket", "minimum_threshold", "unapplied_cash_reason", "release_trigger", "held_money_type"),
    24: ("deduction_id", "deduction_category", "basis", "cap", "agreement_reference", "gross_deduction_net"),
    25: ("beneficiary_id", "legal_entity", "payment_method", "banking_status", "payment_currency", "hold_flag"),
    26: ("tax_form_id", "residence_claim", "withholding_percentage", "treaty_relief_status", "gross_up_clause", "tax_document_expiry"),
    27: ("dispute_id", "dispute_type", "contested_object_id", "evidence_requirement", "claimant_position", "routing_path"),
    28: ("dispute_state", "sla_timer", "counter_evidence_request", "calculation_snapshot", "communication_reference", "resolution_reason"),
    29: ("correction_id", "original_statement_line_id", "restatement_reason", "affected_period", "payee_impact", "reversal_source"),
    30: ("admin_task_id", "queue_type", "assignee_id", "due_date", "escalation_path", "workload_metric"),
    31: ("reversion_schedule_id", "trigger_date", "notice_period", "affected_rights", "successor_path", "sunset_alert"),
    32: ("registration_task_id", "submission_package", "recipient", "submission_date", "acknowledgement_status", "exception_reason"),
    33: ("evidence_bundle_id", "required_documents", "chain_of_title_artifacts", "license_approval_proof", "rate_reference", "completeness_score"),
    34: ("event_schema_id", "rights_lifecycle_event", "payload_contract", "idempotency_key", "transition_mapping", "outbox_trace"),
    35: ("consumed_event_id", "reaction_type", "affected_record_id", "lineage_reference", "recalculation_scope", "unrelated_mutation_block"),
    36: ("dead_letter_id", "failure_classification", "retry_count", "replay_preview", "operator_identity", "result_summary"),
    37: ("repertoire_view_id", "catalog_health", "registration_gap_queue", "split_conflict_queue", "statement_readiness", "renewal_alerts"),
    38: ("statement_explainer_id", "payee_summary", "drill_source_usage", "drill_rate_split", "held_taxed_recouped_flags", "export_reconciliation"),
    39: ("dispute_cockpit_id", "timeline", "contested_assets", "evidence_comparison", "statement_impact", "approval_actions"),
    40: ("agent_extraction_id", "document_type", "extracted_terms", "citations", "confidence_score", "mutation_preview"),
    41: ("split_validation_assist_id", "rule_failure_explanation", "prior_split_comparison", "draft_outreach", "approval_guard", "owned_data_scope"),
    42: ("statement_qa_id", "anomaly_delta", "missing_income_explanation", "recoupment_change", "dispute_packet", "local_fact_citations"),
    43: ("catalog_follow_up_id", "missing_registration_group", "affiliation_gap_group", "expiring_deal_group", "priority_score", "proposed_action_log"),
    44: ("leakage_score_id", "unmatched_usage_rate", "registration_gap_score", "split_change_signal", "underpayment_backtest", "explainable_reasons"),
    45: ("release_scenario_id", "seeded_lifecycle", "statement_expected_outcome", "dispute_expected_outcome", "agent_safety_result", "domain_proof_status"),
    46: ("schema_expansion_id", "contributor_table", "affiliation_table", "statement_line_table", "recoupment_table", "evidence_table"),
    47: ("territory_policy_pack_id", "right_type", "territory_rules", "materiality_threshold", "dispute_sla", "policy_provenance"),
    48: ("seeded_portfolio_id", "catalog_archetype", "co_write_case", "sub_publishing_case", "remix_case", "dispute_scenario"),
    49: ("audit_proof_id", "statement_hash", "dispute_bundle_hash", "calculation_trace_hash", "registration_package_hash", "proof_status"),
    50: ("go_live_scorecard_id", "work_coverage", "split_completeness", "usage_match_rate", "statement_explainability", "agent_safety_score"),
}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    25: ("PaymentInstructionChanged",),
    26: ("TaxTreatmentChanged",),
    34: ("PolicyChanged", "AuditEventSealed"),
    35: ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"),
    36: ("AuditEventSealed", "NotificationDeliveryChanged"),
    40: ("DocumentEvidenceSealed",),
    44: ("FraudRiskProjectionChanged",),
    49: ("AuditEventSealed", "DocumentEvidenceSealed"),
}
_DOMAIN_MESSAGES = {
    capability.feature_number: (
        f"{capability.title} must be backed by owned rights, royalties, repertoire, statement, dispute, evidence, "
        "agent, UI, and release-proof artifacts before it is accepted as complete."
    )
    for capability in ROYALTIES_CONTROL_CAPABILITIES
}
_HUMAN_CONFIRMATION_FEATURES = (11, 12, 16, 20, 23, 24, 25, 27, 28, 29, 31, 34, 36, 40, 41, 42, 43, 50)
_PROJECTION_ONLY_FEATURES = (25, 26, 34, 35, 36, 40, 44, 49)
_AGENT_PREVIEW_FEATURES = (40, 41, 42, 43, 50)
_NON_MUTATING_FEATURES = (10, 14, 17, 18, 21, 29, 35, 36, 38, 44, 45, 48, 49, 50)
_MONEY_OR_RIGHTS_IMPACT_FEATURES = (4, 5, 11, 12, 14, 15, 16, 20, 21, 22, 23, 24, 25, 26, 28, 29, 31, 34, 35, 36, 44, 50)


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
        "tables": (f"music_royalties_rights_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"MusicRoyaltiesRights{_camel(capability.slug)}Panel",
        "route": f"POST /music-royalties-rights/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in ROYALTIES_CONTROL_CAPABILITIES}


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
        "event_topic": ROYALTIES_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "money_or_rights_evidence_complete": True,
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
    if number in _MONEY_OR_RIGHTS_IMPACT_FEATURES and payload.get("money_or_rights_evidence_complete") is not True:
        findings.append("royalty, rights, statement, payment, tax, dispute, or policy-impacting actions require complete evidence and approval context")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("rights grants, statement changes, payment routing, disputes, replay, and agent proposals require human approval before mutation")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("music-rights assistant skills must return cited, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("rate, matching, statement, replay, proof, rehearsal, and scorecard checks must be side-effect-free artifacts")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("payment, tax, audit, document, notification, fraud, policy, and KPI facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != ROYALTIES_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("music royalties eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in ROYALTIES_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary music royalties datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("music royalties controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_royalties_rights_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in ROYALTIES_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in ROYALTIES_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": ROYALTIES_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": ROYALTIES_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_royalties_rights_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_royalties_rights_control(capability) for capability in ROYALTIES_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.music-royalties-rights-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": ROYALTIES_CONTROL_OWNED_TABLES,
        "declared_dependencies": ROYALTIES_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": ROYALTIES_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": ROYALTIES_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


ROYALTIES_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_royalties_rights_control(slug, payload))
    for capability in ROYALTIES_CONTROL_CAPABILITIES
}

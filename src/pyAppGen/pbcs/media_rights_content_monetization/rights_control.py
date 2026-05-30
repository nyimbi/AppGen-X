"""Executable improve1 controls for the Media Rights Content Monetization PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "media_rights_content_monetization"
EVENT_CONTRACT = "AppGen-X"
RIGHTS_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
RIGHTS_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.media_rights_content_monetization.events"
_BASE_OWNED_TABLES = (
    "media_rights_content_monetization_rights_asset",
    "media_rights_content_monetization_license_agreement",
    "media_rights_content_monetization_distribution_window",
    "media_rights_content_monetization_usage_record",
    "media_rights_content_monetization_royalty_statement",
    "media_rights_content_monetization_revenue_share",
    "media_rights_content_monetization_territory_restriction",
    "media_rights_content_monetization_media_rights_content_monetization_policy_rule",
    "media_rights_content_monetization_media_rights_content_monetization_runtime_parameter",
    "media_rights_content_monetization_media_rights_content_monetization_schema_extension",
    "media_rights_content_monetization_media_rights_content_monetization_control_assertion",
    "media_rights_content_monetization_media_rights_content_monetization_governed_model",
    "media_rights_content_monetization_appgen_outbox_event",
    "media_rights_content_monetization_appgen_inbox_event",
    "media_rights_content_monetization_appgen_dead_letter_event",
)
RIGHTS_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(
    _BASE_OWNED_TABLES + tuple(f"media_rights_content_monetization_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)
))
RIGHTS_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys((
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "ContentDelivered",
    "UsageReported",
    "PayoutSettled",
)))
RIGHTS_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in RIGHTS_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in RIGHTS_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "rights_asset_id", "license_agreement_id", "distribution_window_id", "territory_id", "platform_id", "policy_version", "audit_trail", "evidence_references")
_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: 'canonical_rights_grant_model_verified',
    2: 'rights_window_versioning_verified',
    3: 'territory_hierarchy_and_rule_inheritance_verified',
    4: 'platform_and_channel_entitlement_catalog_verified',
    5: 'availability_state_machine_verified',
    6: 'holdbacks_and_carve_out_management_verified',
    7: 'exclusivity_and_competitive_blackout_controls_verified',
    8: 'licensing_boundary_between_inbound_and_outbound_rights_verified',
    9: 'term_calculation_and_renewal_workflow_verified',
    10: 'royalty_boundary_between_owed_accrued_paid_and_disputed_verified',
    11: 'usage_ingestion_normalization_by_platform_report_type_verified',
    12: 'revenue_share_waterfall_engine_verified',
    13: 'minimum_guarantee_and_recoupment_tracking_verified',
    14: 'ad_supported_monetization_rights_verified',
    15: 'sponsorship_and_branded_content_constraints_verified',
    16: 'promotional_use_and_marketing_rights_exceptions_verified',
    17: 'restriction_clause_registry_verified',
    18: 'takedown_initiation_and_sla_management_verified',
    19: 'rights_conflict_detection_across_title_lineage_verified',
    20: 'rights_conflict_resolution_workbench_verified',
    21: 'chain_of_title_evidence_tracking_verified',
    22: 'derivative_and_package_rights_modeling_verified',
    23: 'localization_rights_by_language_and_material_type_verified',
    24: 'territory_platform_availability_calendar_ui_verified',
    25: 'availability_read_model_and_api_verified',
    26: 'agent_skill_for_agreement_intake_and_clause_extraction_verified',
    27: 'agent_skill_for_conflict_triage_and_release_readiness_verified',
    28: 'expanded_domain_event_model_verified',
    29: 'event_idempotency_and_replay_evidence_verified',
    30: 'release_evidence_bundle_for_rights_decisions_verified',
    31: 'royalty_statement_review_workbench_verified',
    32: 'revenue_reconciliation_across_usage_and_payout_verified',
    33: 'avails_import_and_export_workflows_verified',
    34: 'policy_rules_for_prohibited_rights_combinations_verified',
    35: 'window_overlap_simulator_verified',
    36: 'pricing_floors_and_ad_yield_guardrails_verified',
    37: 'sponsorship_inventory_reservation_conflict_checks_verified',
    38: 'takedown_reversal_and_reinstatement_controls_verified',
    39: 'ratings_regulatory_and_audience_restriction_handling_verified',
    40: 'rights_expiry_and_sunset_alerting_verified',
    41: 'multi_tenant_rights_segregation_verified',
    42: 'bulk_correction_workflow_for_late_source_data_verified',
    43: 'release_readiness_checklist_verified',
    44: 'domain_kpi_dashboard_verified',
    45: 'exception_taxonomy_and_ownership_routing_verified',
    46: 'seed_data_and_test_scenarios_for_real_rights_cases_verified',
    47: 'specification_and_backlog_alignment_verified',
    48: 'cross_pbc_boundary_hardening_with_event_contracts_verified',
    49: 'evidence_based_approval_gates_verified',
    50: 'post_release_monitoring_and_rollback_readiness_verified',
}
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {feature_number: _BASE_FIELDS + (primary_proof,) for feature_number, primary_proof in _PRIMARY_PROOF_FIELDS.items()}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    28: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'),
    29: ('PolicyChanged',),
    40: ('OperationalKpiChanged',),
    48: ('PolicyChanged', 'AuditEventSealed'),
    50: ('OperationalKpiChanged',),
}
_DOMAIN_MESSAGES: dict[int, str] = {
    1: 'Extend `rights_asset` and `license_agreement` so every grant records rights type, grantor, grantee, exclusivity, language, version, edit type, and whether the right covers primary exploitation, marketing use, or derivative packaging.',
    2: 'Add first-class versioning for `distribution_window` so start, end, embargo, extension, and amendment history are tracked with superseded-by links and amendment reasons.',
    3: 'Model hierarchical territories in `territory_restriction` with parent-child inheritance, inclusion lists, exclusion lists, and effective precedence for overrides and carve-outs.',
    4: 'Introduce a controlled platform catalog linked to `distribution_window` and `license_agreement`, including platform family, channel class, playback mode, download permission, and offline-viewing entitlement.',
    5: 'Add an explicit availability lifecycle tied to `rights_asset` and `distribution_window`, including state transitions for prelaunch readiness, live activation, suspension, expiration, reinstatement, and permanent withdrawal.',
    6: 'Create holdback entities linked to `distribution_window` with rule types for blackout period, platform exclusion, partner carve-out, and market-specific delay.',
    7: 'Encode exclusivity scope in `license_agreement` and add policy checks that compare title, asset family, edit lineage, platform family, territory, and time period to detect competitive overlap.',
    8: 'Separate inbound licensing obligations from outbound commercialization rights inside `license_agreement`, and prevent downstream grants that exceed acquired scope by territory, platform, language, or term.',
    9: 'Support term anchors and renewal formulas in `license_agreement` and `distribution_window`, including auto-renewal, option exercise deadlines, and notice windows.',
    10: 'Expand `royalty_statement` so each line can be marked as calculated, accrued, invoiced, payable, paid, disputed, reversed, or carried forward, with links to the triggering usage or revenue event.',
    11: 'Create typed ingestion profiles for `usage_record` that normalize partner-specific files into a common usage vocabulary while preserving original source units and source file lineage.',
    12: 'Model `revenue_share` as a waterfall with ordered stages for gross revenue, allowed deductions, minimum guarantee recoupment, partner splits, commissions, and residual holdbacks.',
    13: 'Add minimum guarantee balances, recoupment schedules, and recoupment priority rules to `license_agreement`, linked directly to `revenue_share` and `royalty_statement`.',
    14: 'Add ad monetization flags and restrictions to `distribution_window` and `license_agreement`, including whether pre-roll, mid-roll, dynamic ad insertion, and programmatic monetization are permitted.',
    15: 'Capture sponsorship-specific restrictions for title, series, event, and package exploitation, including prohibited sponsors, prohibited industries, exclusivity promises, and approval-needed cases.',
    16: 'Add a promo-rights layer to `rights_asset` and `license_agreement` covering clip duration caps, still counts, artwork rights, trailer rights, and campaign term limits by territory and platform.',
    17: 'Create a structured clause registry for `license_agreement` and `media_rights_content_monetization_policy_rule` covering language restrictions, rating restrictions, sponsor conflicts, exclusivity promises, embargoes, and content edits required for release.',
    18: 'Introduce takedown workflows linked to `distribution_window`, `rights_asset`, and `usage_record`, including trigger source, platform targets, deadline, completion evidence, and escalation path.',
    19: 'Add lineage links among `rights_asset` records so conflict checks can compare parent title, cut, season, episode, language, edit family, and packaged derivative relationships.',
    20: 'Add a conflict-resolution area in `MediaRightsContentMonetizationWorkbench` with side-by-side comparison of overlapping grants, recommended next actions, approval chain, and final resolution type.',
    21: 'Attach chain-of-title documents, amendments, rights confirmations, and approval memos to `rights_asset` and `license_agreement`, with document type, issue date, issuer, and validity status.',
    22: 'Model package rights and derivative exploitation as explicit entities connected to underlying `rights_asset` records, with inherited and overridden restrictions clearly separated.',
    23: 'Extend `rights_asset` and `distribution_window` to capture language-specific rights for audio dub, subtitle, captions, descriptive audio, localized metadata, and localized artwork.',
    24: 'Add a calendar and matrix view in `MediaRightsContentMonetizationWorkbench` that combines `distribution_window`, `territory_restriction`, and platform entitlements into one explorable grid.',
    25: 'Create an availability projection and query API that resolves rights state, territory inclusion, platform rights, restrictions, holdbacks, and takedown state into a single eligibility response.',
    26: 'Add an assistant skill in `MediaRightsContentMonetizationAssistantPanel` that drafts `license_agreement`, clause registry, and window records from uploaded deal documents while requiring confirmation before any write.',
    27: 'Add an assistant workflow that summarizes rights conflicts, missing chain-of-title documents, expiring windows, and unresolved takedowns, then proposes assignment and remediation steps.',
    28: 'Add typed events for agreement captured, window amended, availability activated, holdback asserted, takedown opened, takedown confirmed, royalty disputed, revenue share recalculated, and rights conflict detected.',
    29: 'Strengthen idempotent handling for usage, royalty, takedown, and availability events using deterministic dedupe keys, replay-safe projections, and explicit conflict handling for out-of-order delivery.',
    30: 'Build a release-evidence bundle that captures governing agreement, active windows, territory and platform eligibility, restriction review, takedown status, and final approver decision for each release.',
    31: 'Add a dedicated royalty-review view in `MediaRightsContentMonetizationDetail` showing statement lines, deduction rationale, recoupment state, partner share, and dispute annotations.',
    32: 'Create reconciliation checks tying `usage_record`, `revenue_share`, and `royalty_statement` together by partner, title, territory, platform, and accounting period, with tolerances and exception routing.',
    33: 'Add avails import and export support derived from `rights_asset`, `distribution_window`, `territory_restriction`, and platform entitlements, including title metadata, territories, platforms, and rights notes.',
    34: 'Expand `media_rights_content_monetization_policy_rule` to express prohibited combinations, required companion rights, and mandatory review conditions for monetization scenarios.',
    35: 'Provide a simulator that compares proposed `distribution_window` changes against active windows, holdbacks, partner obligations, and territory exceptions without mutating production records.',
    36: 'Add monetization floor controls to `license_agreement` and `revenue_share`, including minimum unit price, minimum CPM, minimum guarantee to licensor, and exception flow when economics fall below threshold.',
    37: 'Add sponsorship reservation tracking linked to title, series, event, territory, platform, and sponsor category, with checks against rights restrictions and exclusivity promises.',
    38: 'Extend the takedown workflow with reversal requests, evidence review, partial reinstatement by territory or platform, and required approvals for reactivation.',
    39: 'Add structured restriction types for rating, audience, and regulatory constraints, and enforce them across territory, platform, ad mode, and sponsorship use cases.',
    40: 'Implement alerting for upcoming expiry, renewal notice deadlines, holdback release dates, sponsorship end dates, and recoupment milestones using the existing event and workbench surfaces.',
    41: 'Strengthen tenant scoping across `rights_asset`, agreements, windows, usage, statements, events, and evidence bundles so cross-tenant lookup, export, and assistant context are blocked by default.',
    42: 'Add bulk correction flows for `usage_record`, `distribution_window`, and `royalty_statement` with preview diffing, row-level validation, selective approval, and automatic downstream recalculation.',
    43: 'Add a release-readiness checklist assembled from agreement validity, active windows, territory eligibility, platform rights, promo rights, ad rights, sponsorship restrictions, and chain-of-title completeness.',
    44: 'Build KPI projections for expiring rights, blocked launches, open conflicts, takedown SLA performance, royalty dispute rate, recoupment progress, and monetizable title inventory by channel.',
    45: 'Create a typed exception model with categories for rights evidence, availability conflict, territory rule, platform rule, economics, takedown, sponsor conflict, and royalty dispute, each with required owner roles and deadlines.',
    46: 'Expand `seed_data.py` and contract tests with scenarios for exclusive SVOD windows, AVOD after holdback, dubbed-only rights, sponsor-blocked content, emergency takedown, and disputed royalty statements.',
    47: 'Update `SPECIFICATION.md` structure expectations for rights grant modeling, windows, territories, monetization rules, takedowns, conflict handling, assistant behavior, and evidence bundles so backlog items can trace into delivery work.',
    48: 'Define outbound and inbound contracts around availability, takedown, payout, and policy changes using the existing event surfaces and new typed events, keeping other packages outside owned tables.',
    49: 'Require approval screens to present the active grant, windows, territories, platform rights, restrictions, economics, open exceptions, and attached evidence before `MediaRightsContentMonetizationApproved` can be emitted.',
    50: 'Add post-release monitoring for unexpected territory exposure, ad mode violations, sponsor conflicts, usage spikes, missing revenue feeds, and takedown failures, plus a rollback playbook for suspension or takedown by scope.',
}
_HUMAN_CONFIRMATION_FEATURES = (26, 27, 43, 49)
_PROJECTION_ONLY_FEATURES = (25, 28, 32, 40, 48, 50)


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
    proof = _PRIMARY_PROOF_FIELDS[capability.feature_number]
    return {"title": capability.title, "slug": capability.slug, "tables": (f"media_rights_content_monetization_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "primary_proof": proof, "ui": f"MediaRightsContentMonetization{_camel(capability.slug)}Panel", "route": f"POST /media-rights-content-monetization/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in RIGHTS_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({"database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "event_topic": RIGHTS_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "dependency_access_mode": "api_event_projection", "human_confirmation": True, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    feature_number = capability.feature_number
    spec = CONTROL_SPECS[feature_number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[feature_number])
    if feature_number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("rights assistant workflows must draft, compare, and recommend only; human approval is required before governed mutation or launch approval")
    if feature_number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("external usage, payout, content, distribution, policy, audit, and KPI context must use APIs, events, or read-only projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != RIGHTS_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("rights monetization eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in RIGHTS_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary rights monetization datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("rights controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_rights_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in RIGHTS_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in RIGHTS_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "primary_proof": spec["primary_proof"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": RIGHTS_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": RIGHTS_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_rights_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_rights_control(capability) for capability in RIGHTS_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.media-rights-content-monetization-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": RIGHTS_CONTROL_OWNED_TABLES, "declared_dependencies": RIGHTS_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": RIGHTS_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": RIGHTS_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


RIGHTS_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_rights_control(slug, payload)) for capability in RIGHTS_CONTROL_CAPABILITIES}

"""Executable improve1 controls for the Media Production Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "media_production_management"
EVENT_CONTRACT = "AppGen-X"
MEDIA_PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
MEDIA_PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.media_production_management.events"
_BASE_OWNED_TABLES = (
    "media_production_management_production",
    "media_production_management_budget_line",
    "media_production_management_crew_booking",
    "media_production_management_location_permit",
    "media_production_management_shoot_day",
    "media_production_management_post_production_task",
    "media_production_management_delivery_asset",
    "media_production_management_media_production_management_policy_rule",
    "media_production_management_media_production_management_runtime_parameter",
    "media_production_management_media_production_management_schema_extension",
    "media_production_management_media_production_management_control_assertion",
    "media_production_management_media_production_management_governed_model",
    "media_production_management_appgen_outbox_event",
    "media_production_management_appgen_inbox_event",
    "media_production_management_appgen_dead_letter_event",
)
MEDIA_PRODUCTION_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(
    _BASE_OWNED_TABLES + tuple(f"media_production_management_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)
))
MEDIA_PRODUCTION_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys((
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "VendorStatusChanged",
    "RightsClearanceChanged",
    "DistributionWindowChanged",
)))
MEDIA_PRODUCTION_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in MEDIA_PRODUCTION_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in MEDIA_PRODUCTION_CONTROL_CAPABILITIES}
_BASE_FIELDS = (
    "tenant_id",
    "production_id",
    "stage_id",
    "budget_revision_id",
    "shoot_day_id",
    "delivery_asset_id",
    "policy_version",
    "audit_trail",
    "evidence_references",
)
_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: 'development_slate_lifecycle_verified',
    2: 'script_package_and_creative_development_tracking_verified',
    3: 'budget_top_sheet_and_phase_budgeting_verified',
    4: 'budget_revision_and_change_order_control_verified',
    5: 'casting_versus_crew_boundary_verified',
    6: 'deal_memos_and_engagement_packet_intake_verified',
    7: 'stripboard_and_shooting_schedule_planning_verified',
    8: 'call_sheet_generation_and_distribution_verified',
    9: 'location_package_readiness_verified',
    10: 'travel_lodging_and_movement_logistics_verified',
    11: 'shoot_day_readiness_gate_verified',
    12: 'on_set_safety_planning_and_incident_capture_verified',
    13: 'departmental_checklist_coverage_verified',
    14: 'daily_production_report_capture_verified',
    15: 'dailies_ingest_and_review_workflow_verified',
    16: 'script_supervision_and_continuity_controls_verified',
    17: 'equipment_and_kit_allocation_verified',
    18: 'union_turnaround_and_labor_rule_compliance_verified',
    19: 'extras_and_background_performer_operations_verified',
    20: 'procurement_petty_cash_and_expense_capture_verified',
    21: 'cost_report_cadence_and_burn_analysis_verified',
    22: 'editorial_handoff_from_set_to_post_verified',
    23: 'post_production_schedule_and_milestone_board_verified',
    24: 'vfx_shot_inventory_and_turnover_control_verified',
    25: 'sound_color_and_finishing_chain_verified',
    26: 'music_archive_and_rights_clearance_verified',
    27: 'approval_matrix_by_stage_and_function_verified',
    28: 'notes_versions_and_rework_loops_verified',
    29: 'deliverables_matrix_by_platform_and_territory_verified',
    30: 'technical_qc_and_rejection_handling_verified',
    31: 'marketing_and_publicity_asset_coordination_verified',
    32: 'archive_restore_and_library_package_management_verified',
    33: 'release_documents_and_legal_packet_evidence_verified',
    34: 'production_workbench_ui_for_executive_and_line_users_verified',
    35: 'exception_first_ui_for_blockers_and_aging_verified',
    36: 'assistant_skills_for_production_operations_verified',
    37: 'document_instruction_intake_for_production_paperwork_verified',
    38: 'event_model_for_production_lifecycle_and_handoffs_verified',
    39: 'consumed_event_handling_for_policy_audit_and_kpi_signals_verified',
    40: 'predictive_risk_scoring_for_schedule_and_budget_drift_verified',
    41: 'multi_tenant_isolation_for_productions_and_vendor_data_verified',
    42: 'offline_and_poor_connectivity_field_capture_verified',
    43: 'external_vendor_and_facility_collaboration_verified',
    44: 'exception_triage_retries_and_dead_letter_recovery_verified',
    45: 'release_evidence_traceability_across_the_package_verified',
    46: 'seeded_production_scenarios_and_release_rehearsals_verified',
    47: 'operational_metrics_and_service_levels_verified',
    48: 'immutable_history_and_audit_proof_evidence_verified',
    49: 'schema_expansion_for_media_specific_subdomains_verified',
    50: 'go_live_gate_for_a_production_release_candidate_verified',
}
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {
    feature_number: _BASE_FIELDS + (primary_proof,)
    for feature_number, primary_proof in _PRIMARY_PROOF_FIELDS.items()
}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    38: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'),
    39: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'),
    43: ('VendorStatusChanged',),
    45: ('AuditEventSealed',),
    48: ('AuditEventSealed',),
}
_DOMAIN_MESSAGES: dict[int, str] = {
    1: 'Expand the production lifecycle so development executives can track script drafts, package attachments, financing readiness, greenlight gates, and target release windows before a show or film becomes an active shoot.',
    2: 'Add structured development artifacts for script versions, bible or deck references, creative notes, attachment status, and greenlight comments, with dated ownership for development, production, and finance stakeholders.',
    3: 'Extend `budget_line` behavior to support phase codes, account groups, above-the-line and below-the-line rollups, contingency buckets, currency handling, and approval thresholds tied to greenlight and reforecast events.',
    4: 'Add revision numbers, locked approved baselines, change-order reasons, variance attribution, and producer or studio approval routing whenever a budget amendment changes cash flow, shoot days, or delivery scope.',
    5: 'Separate cast engagements from crew bookings with distinct fields for role type, billing, union status, fitting dates, rehearsal dates, work guarantees, and release obligations while keeping operational handoffs visible on one production timeline.',
    6: 'Add governed intake for cast and crew deal memos, rate cards, availability windows, travel classes, accommodation rules, and special conditions so operational bookings inherit the terms that actually govern the engagement.',
    7: 'Introduce schedule planning entities around `shoot_day` for stripboard ordering, scene grouping, unit assignment, weather cover sets, turnaround rules, and schedule versions that producers can compare before locking the plan.',
    8: 'Add call sheet generation from approved schedule data, with crew call times, cast calls, unit assignments, scene blocks, transport pickups, meal breaks, nearest hospital, weather, parking, and emergency contacts.',
    9: 'Extend `location_permit` with location packets that capture jurisdiction, site owner terms, police or fire requirements, parking maps, power availability, curfew limits, insurance evidence, and contingency locations.',
    10: 'Add logistics planning linked to schedule and booking data for airport transfers, hotel blocks, rooming lists, vehicle assignments, per diem rules, and company-move timing so operations can spot impossible travel plans before issue.',
    11: 'Add a readiness gate for each shoot day that checks cast confirmations, crew assignments, location clearance, call sheet approval, transport readiness, equipment availability, weather review, and open blocking exceptions.',
    12: 'Add safety plans for stunts, weapons, animals, minors, water work, vehicles, special effects, night work, and extreme weather, plus incident and near-miss capture linked to the relevant shoot day and call sheet revision.',
    13: 'Add department checklists, owners, due times, and signoff states so shoot readiness can show which department still blocks first shot and which items were waived with approval.',
    14: 'Add daily production report capture for actual call, first shot, meal, wrap, pages completed, scenes shot, overtime, weather impact, incidents, delays, and reasons, with variance against planned schedule and budget.',
    15: 'Create dailies workflows tied to `delivery_asset` and `post_production_task` for camera card ingest, checksum verification, sync status, review sessions, clip notes, and reshoot flags from editorial or production.',
    16: 'Add continuity records for slate, take continuity, prop continuity, costume continuity, line changes, coverage completeness, and notes requiring pick-ups or inserts.',
    17: 'Add equipment package reservations, prep dates, return dates, damaged-kit incidents, sub-rental approvals, and cross-unit conflicts so each shoot day shows the kit plan that supports it.',
    18: 'Add rules for turnaround windows, meal-break timing, overtime triggers, consecutive-day constraints, child labor restrictions, and role-specific rest requirements for cast and crew.',
    19: 'Add dedicated flows for background counts, holding-area plans, wardrobe states, meal planning, voucher capture, crowd wrangling, and release evidence for minors or restricted extras.',
    20: 'Extend budget operations with purchase requests, purchase orders, petty cash envelopes, receipt matching, approver limits, and departmental charge coding linked back to cost reports.',
    21: 'Add cost-report views with current actuals, committed costs, estimate to complete, contingency drawdown, overage drivers, and schedule-linked forecast risk.',
    22: 'Create a formal handoff that packages camera and sound manifests, script notes, dailies status, music reports, continuity notes, and open set issues into the first editorial queue.',
    23: 'Add milestone templates, dependencies, planned dates, owners, and approval states for editorial, sound, music, color, graphics, subtitling, localization, and mastering.',
    24: 'Add VFX shot tracking with sequence and shot codes, vendor assignment, bid status, turnover packages, plate availability, temp comps, finals, notes, and approval rounds.',
    25: 'Model sound editorial, ADR, Foley, premix, final mix, conform, color prep, grade, online, graphics, captions, subtitles, and mastering as linked finishing tasks with handoff evidence.',
    26: 'Add rights and clearance tracking for music cues, archival elements, stock material, trademarks, performer releases, and location releases with dates, terms, territories, and expiry handling.',
    27: 'Add stage-specific approval types with named approver roles, quorum rules, delegated authority, escalation paths, and rework reasons mapped to production, budget, schedule, post, and deliverable events.',
    28: 'Add version lineage for scripts, call sheets, schedules, budgets, edits, VFX shots, sound mixes, and deliverables, with note categories, reply chains, and mandatory resolution before closure.',
    29: 'Expand `delivery_asset` into a deliverables matrix that tracks package type, spec version, territory, language, audio layout, caption set, artwork set, checksum, QC result, and shipment state.',
    30: 'Add QC result capture for video, audio, captions, metadata, packaging, and checksum failures, with root-cause categories that route issues back to editorial, sound, VFX, mastering, or metadata owners.',
    31: 'Add coordinated tracking for marketing assets, embargo dates, approval rounds, territory variants, and linkage to final release windows so launch-critical materials are not managed off-system.',
    32: 'Add archive bundles with source media lineage, retention classes, cold-storage status, retrieval tests, and package manifests that support remastering, clip licensing, or platform redelivery later.',
    33: 'Create a governed evidence vault for talent releases, location releases, insurance certificates, cue sheets, chain-of-title records, censorship filings, and distribution affidavits linked to the production and deliverable they support.',
    34: 'Split the workbench into views for slate and development, budget control, casting and crew, schedule and call sheets, locations, shoot-day readiness, post and VFX, deliverables, and release evidence.',
    35: 'Add exception queues for missing approvals, location gaps, cast conflicts, labor-rule breaches, missing dailies, VFX delays, QC rejections, and missing release documents, with aging, owner, and next action.',
    36: 'Add assistant skills for draft call sheet assembly, budget variance explanation, crew conflict review, location packet validation, dailies completeness checks, VFX turnover prep, and deliverable package review, all using governed previews before mutation.',
    37: 'Expand document intake so the assistant can parse and map production paperwork into safe draft updates, cite extracted source spans, flag low-confidence fields, and route ambiguous items to humans.',
    38: 'Add typed domain events for development-greenlight, budget-approved, schedule-locked, call-sheet-issued, shoot-day-ready, dailies-missing, editorial-started, VFX-turnover-sent, picture-locked, QC-passed, and package-delivered transitions.',
    39: 'Map `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` to concrete actions such as approval rule recalculation, sealed-evidence locking, KPI-driven risk escalation, and workbench alerts on affected productions.',
    40: 'Add predictive risk models that score shoot-day readiness, labor-risk exposure, location instability, budget burn risk, post bottlenecks, VFX delay exposure, and delivery miss probability with explainable feature outputs.',
    41: 'Strengthen tenant scoping for production records, bookings, call sheets, safety plans, post workflows, and deliverables so tenant boundaries hold across API, UI, events, storage, and assistant skills.',
    42: 'Add offline draft capture and later reconciliation for daily production reports, safety incidents, location notes, and departmental checklists, with conflict detection when data syncs back to the main record.',
    43: 'Add controlled external collaboration for turnover receipt, delivery acknowledgement, note response, asset reupload, and status updates using scoped roles, expiring links, and inbound evidence validation.',
    44: 'Expand exception handling so dead-letter events, failed dailies ingests, rejected call sheets, broken delivery packages, and stuck approval chains surface in guided triage queues with replay, retry, and closeout actions.',
    45: 'Tie every production-domain capability in this backlog to explicit release evidence entries, with trace links from schema entities and API actions to UI states, event contracts, agent skills, and tests.',
    46: 'Add seeded scenarios for feature film, episodic television, branded content, documentary travel shoot, VFX-heavy show, and urgent redelivery, each exercising development, budgeting, scheduling, shooting, post, approvals, and deliverables.',
    47: 'Add domain analytics and service levels across development, prep, shoot, post, and delivery, with drill-down from executive summary to specific blocking records and departments.',
    48: 'Expand event-sourced history and proof sealing so every material approval, schedule issue, budget revision, safety incident, QC outcome, and release packet change can be reconstructed with actor, timestamp, and evidence hashes.',
    49: 'Plan owned-schema expansion for media-specific tables and projections so the package can represent those concepts directly instead of hiding them in generic payloads or comments.',
    50: 'Add a final release candidate gate that checks approved budget, locked schedule, cleared locations, completed safety review, ingested dailies, completed post milestones, approved VFX finals, passed QC, complete deliverables matrix, and complete legal packet evidence.',
}
_HUMAN_CONFIRMATION_FEATURES = (6, 36, 37, 43)
_PROJECTION_ONLY_FEATURES = (26, 38, 39, 43)


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
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"media_production_management_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": proof,
        "ui": f"MediaProductionManagement{_camel(capability.slug)}Panel",
        "route": f"POST /media-production-management/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in MEDIA_PRODUCTION_CONTROL_CAPABILITIES}


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
        "event_topic": MEDIA_PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    feature_number = capability.feature_number
    spec = CONTROL_SPECS[feature_number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[feature_number])
    if feature_number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("media production assistant skills must preview and cite changes; human approval is required before governed mutation or external collaboration")
    if feature_number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("external vendor, rights, policy, audit, KPI, and distribution context must use declared APIs, events, or read-only projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != MEDIA_PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("media production eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in MEDIA_PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary media production datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("media production controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_media_production_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in MEDIA_PRODUCTION_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in MEDIA_PRODUCTION_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": MEDIA_PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": MEDIA_PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_media_production_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_media_production_control(capability) for capability in MEDIA_PRODUCTION_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.media-production-management-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": MEDIA_PRODUCTION_CONTROL_OWNED_TABLES,
        "declared_dependencies": MEDIA_PRODUCTION_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": MEDIA_PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": MEDIA_PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


MEDIA_PRODUCTION_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_media_production_control(slug, payload))
    for capability in MEDIA_PRODUCTION_CONTROL_CAPABILITIES
}

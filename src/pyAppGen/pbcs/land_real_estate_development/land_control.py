"""Executable improve1 controls for the Land and Real Estate Development PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "land_real_estate_development"
EVENT_CONTRACT = "AppGen-X"
LAND_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
LAND_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.land_real_estate_development.events"
LAND_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + tuple(
    f"land_real_estate_development_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES
)))
LAND_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "PolicyChanged",
    "CustomerUpdated",
    "SupplierQualified",
    "ParcelIdentityProjected",
    "SurveyRevisionFiled",
    "TitleCommitmentChanged",
    "EnvironmentalFindingRecorded",
    "JurisdictionCalendarChanged",
    "UtilityCapacityChanged",
    "FinanceCovenantChanged",
    "SalesReleaseProjected",
    "LeaseDemandProjected",
    "AuditEventSealed",
    "CarbonIntensityProjected",
)))
LAND_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in LAND_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in LAND_CONTROL_CAPABILITIES}
_DEFAULT_FIELDS = ("owned_record", "project_context", "required_evidence", "operator_visible", "audit_trail", "safe_to_execute")
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {cap.feature_number: _DEFAULT_FIELDS for cap in LAND_CONTROL_CAPABILITIES}
_FEATURE_FIELDS.update({
    1: ("parcel_id", "assessor_parcel_number", "legal_description", "survey_revision", "source_rank", "discrepancy_badge_visible", "canonical_identity_confirmed"),
    2: ("assemblage_id", "controlled_acres", "target_acres", "seller_holdouts", "drop_dead_date", "termination_rights", "control_threshold_met", "holdout_blocked"),
    3: ("conflict_id", "survey_revision", "title_exception", "encroachment", "cure_owner", "cure_due_date", "unresolved_conflict_blocks_subdivision"),
    4: ("title_exception", "exception_type", "burdened_acres", "endorsement_dependency", "closing_condition", "lenderability_impact", "fatal_exception_blocks_acquisition"),
    5: ("environmental_stage", "recognized_condition", "remediation_plan", "agency_closure", "schedule_impact_days", "residual_value_adjusted", "unresolved_environmental_issue_blocks_go"),
    6: ("site_constraint", "soil_severity", "floodplain_status", "groundwater_risk", "mitigation_cost_range", "affected_parcels", "constraint_cost_updates_feasibility"),
    7: ("zoning_district", "overlay_district", "permitted_use", "density_limit", "height_limit", "setback_rule", "ordinance_citation", "ordinance_rule_passed"),
    8: ("approval_node", "prerequisites", "parallel_tracks", "appeal_window", "blocked_tasks", "critical_path_days", "dependency_sequence_valid"),
    9: ("jurisdiction", "submission_cutoff", "notice_lead_days", "staff_review_window", "hearing_date", "blackout_calendar", "cutoff_calendar_applied"),
    10: ("stakeholder", "issue_theme", "position", "severity", "mitigation_promise", "post_approval_obligation", "mitigation_obligation_created"),
    11: ("closing_gate", "executed_agreement", "deposit_status", "diligence_complete", "title_cures_complete", "survey_approved", "all_closing_conditions_satisfied"),
    12: ("option_id", "premium_schedule", "exercise_deadline", "extension_rights", "notice_address", "refundability", "valuation_consequence", "notice_window_monitored"),
    13: ("constraint_id", "gross_acres", "easement_acres", "dedication_acres", "setback_area", "net_buildable_acres", "net_buildable_area_recalculated"),
    14: ("scenario_id", "program_mix", "density_assumption", "parking_strategy", "phasing_strategy", "entitlement_burden", "baseline_preserved"),
    15: ("assumption_id", "source_type", "source_date", "confidence_band", "market_basis", "status", "stale_assumption_blocked"),
    16: ("waterfall_id", "revenue", "vertical_costs", "infrastructure_costs", "soft_costs", "developer_margin", "seller_price_bridge_calculated"),
    17: ("utility_provider", "available_capacity", "required_capacity", "upgrade_scope", "will_serve_status", "commitment_expiration", "will_serve_valid"),
    18: ("offsite_item", "agency_owner", "frontage_limit", "trigger_condition", "estimated_cost", "reimbursement_potential", "prerequisite_to_vertical_tracked"),
    19: ("map_type", "review_stage", "agency_signoff", "recording_status", "marketable_phase", "sale_or_permit_blocked", "recordation_required_for_release"),
    20: ("permit_packet", "drawing_set_version", "discipline_checklist", "consultant_seals", "jurisdiction_forms", "deferred_items", "completeness_score_green"),
    21: ("agency_comment", "department", "plan_sheet_ref", "response_owner", "due_date", "acceptance_status", "unresolved_comments_block_resubmittal"),
    22: ("obligation_id", "approval_condition", "agreement_clause", "trigger", "owner", "due_date", "evidence_status", "obligation_survives_handoff"),
    23: ("fee_item", "ordinance_basis", "accrued_amount", "paid_amount", "credit_amount", "reimbursement_claim", "fee_ledger_reconciled"),
    24: ("benefit_commitment", "unit_or_spend_count", "trigger_date", "monitoring_period", "handoff_team", "reporting_deadline", "commitment_monitoring_active"),
    25: ("handoff_packet", "approved_drawings", "condition_summary", "utility_commitments", "allowances", "unresolved_risks", "governed_handoff_packet_signed"),
    26: ("supplier_projection", "bid_package", "required_trade", "insurance_requirement", "qualified_bidders", "procurement_readiness", "qualified_supplier_required"),
    27: ("relocation_task", "provider_owner", "outage_window", "prerequisite_permits", "customer_notifications", "commissioning_dependency", "relocation_complete_for_mobilization"),
    28: ("draw_condition", "covenant", "lender_evidence", "inspection_report", "funding_release", "agency_vs_funding_readiness", "lender_evidence_required"),
    29: ("sales_release", "final_map_status", "disclosure_packet", "pricing_authorization", "hoa_setup", "escrow_dependency", "disclosure_packet_complete"),
    30: ("lease_handoff", "temporary_certificate", "unit_turn_sequence", "common_area_readiness", "ti_allowance", "delivery_constraint", "occupancy_clearance_verified"),
    31: ("release_baseline", "unit_mix", "pricing_band", "absorption_assumption", "concession", "drift_threshold", "deviation_review_required"),
    32: ("deadline_id", "trigger_event", "grace_logic", "escalation_ladder", "calendar_rule", "exception_opened", "deadline_engine_active"),
    33: ("risk_transfer_item", "carrier", "limit", "obligee", "expiration", "endorsement", "expired_coverage_blocks_release"),
    34: ("risk_axis", "risk_score", "kill_criterion", "stage", "executive_review", "decision_packet", "kill_criteria_escalates"),
    35: ("milestone_id", "predecessors", "float_days", "long_lead_tag", "external_owner", "slippage_band", "critical_path_recalculated"),
    36: ("counterfactual_id", "redesign_move", "baseline_case", "variance_report", "approval_tradeoff", "exploratory_status", "counterfactual_non_mutating"),
    37: ("denial_case", "denial_basis", "cure_option", "appeal_deadline", "rehearing_strategy", "financeability_review", "appeal_deadline_enforced"),
    38: ("parcel_cockpit", "stack_health", "site_control_coverage", "title_cure_progress", "diligence_findings", "acquisition_gate", "parcel_cockpit_visible"),
    39: ("entitlement_cockpit", "hearing_calendar", "open_conditions", "public_comments", "agency_comments", "role_actions", "entitlement_cockpit_visible"),
    40: ("committee_cockpit", "scenario_comparison", "residual_value_bridge", "risk_heatmap", "capital_milestones", "source_links", "committee_metrics_traceable"),
    41: ("operations_cockpit", "intake_queue", "completeness_score", "comment_aging", "scheduled_hearing", "submittal_status", "aging_queue_visible"),
    42: ("handoff_cockpit", "will_serve_status", "offsite_items", "relocation_tasks", "handoff_packets", "downstream_release", "handoff_cockpit_blocks_downstream"),
    43: ("document_intake", "document_type", "extracted_fact", "source_span", "confidence", "human_review", "citations_required"),
    44: ("agent_due_diligence_flow", "finding_source", "draft_task", "policy_check", "owner_assignment", "human_confirmation", "assignment_without_confirmation_blocked"),
    45: ("agent_negotiation_flow", "version_diff", "changed_term", "affected_obligation", "memo_draft", "human_approval", "approval_checkpoint"),
    46: ("approval_packet_flow", "plan_set", "studies", "consultant_signatures", "jurisdiction_forms", "missing_pieces", "immutable_packet_manifest"),
    47: ("cross_pbc_event", "event_type", "idempotency_key", "posture_recalculation", "lineage_record", "workbench_notification", "idempotent_event_handler"),
    48: ("evidence_pack", "approval_type", "source_documents", "decision_logs", "signoffs", "integrity_hash", "integrity_proof_verified"),
    49: ("closeout_state", "final_acceptance", "warranty_handoff", "fee_reconciliation", "stabilized_occupancy", "archive_snapshot", "open_obligations_block_archive"),
    50: ("portfolio_pattern", "completed_project_context", "recommended_buffer", "default_contingency", "playbook_reuse", "governance_review", "reviewed_default_activation_required"),
})
_FEATURE_DEPENDENCIES = {
    1: ("ParcelIdentityProjected",),
    3: ("SurveyRevisionFiled", "TitleCommitmentChanged"),
    4: ("TitleCommitmentChanged",),
    5: ("EnvironmentalFindingRecorded",),
    9: ("JurisdictionCalendarChanged",),
    17: ("UtilityCapacityChanged",),
    26: ("SupplierQualified",),
    28: ("FinanceCovenantChanged",),
    29: ("SalesReleaseProjected",),
    30: ("LeaseDemandProjected",),
    47: ("PolicyChanged", "CustomerUpdated", "SupplierQualified"),
    48: ("AuditEventSealed",),
}
_EMPTY_ALLOWED_FIELDS = ("seller_holdouts", "missing_pieces")
_REQUIRED_TRUE = {
    1: ("discrepancy_badge_visible", "canonical_identity_confirmed"),
    2: ("control_threshold_met", "holdout_blocked"),
    3: ("unresolved_conflict_blocks_subdivision",),
    4: ("fatal_exception_blocks_acquisition",),
    5: ("residual_value_adjusted", "unresolved_environmental_issue_blocks_go"),
    6: ("constraint_cost_updates_feasibility",),
    7: ("ordinance_rule_passed",),
    8: ("dependency_sequence_valid",),
    9: ("cutoff_calendar_applied",),
    10: ("mitigation_obligation_created",),
    11: ("all_closing_conditions_satisfied",),
    12: ("notice_window_monitored",),
    13: ("net_buildable_area_recalculated",),
    14: ("baseline_preserved",),
    15: ("stale_assumption_blocked",),
    16: ("seller_price_bridge_calculated",),
    17: ("will_serve_valid",),
    18: ("prerequisite_to_vertical_tracked",),
    19: ("recordation_required_for_release",),
    20: ("completeness_score_green",),
    21: ("unresolved_comments_block_resubmittal",),
    22: ("obligation_survives_handoff",),
    23: ("fee_ledger_reconciled",),
    24: ("commitment_monitoring_active",),
    25: ("governed_handoff_packet_signed",),
    26: ("qualified_supplier_required",),
    27: ("relocation_complete_for_mobilization",),
    28: ("lender_evidence_required",),
    29: ("disclosure_packet_complete",),
    30: ("occupancy_clearance_verified",),
    31: ("deviation_review_required",),
    32: ("exception_opened", "deadline_engine_active"),
    33: ("expired_coverage_blocks_release",),
    34: ("kill_criteria_escalates",),
    35: ("critical_path_recalculated",),
    36: ("counterfactual_non_mutating",),
    37: ("appeal_deadline_enforced",),
    38: ("parcel_cockpit_visible",),
    39: ("entitlement_cockpit_visible",),
    40: ("committee_metrics_traceable",),
    41: ("aging_queue_visible",),
    42: ("handoff_cockpit_blocks_downstream",),
    43: ("source_span", "human_review", "citations_required"),
    44: ("policy_check", "human_confirmation", "assignment_without_confirmation_blocked"),
    45: ("human_approval", "approval_checkpoint"),
    46: ("immutable_packet_manifest",),
    47: ("idempotent_event_handler",),
    48: ("integrity_proof_verified",),
    49: ("open_obligations_block_archive",),
    50: ("governance_review", "reviewed_default_activation_required"),
}


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
        "tables": (f"land_real_estate_development_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "ui": f"LandRealEstateDevelopment{_camel(capability.slug)}Panel",
        "route": f"POST /land-real-estate-development/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in LAND_CONTROL_CAPABILITIES}


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
        "event_topic": LAND_CONTROL_REQUIRED_EVENT_TOPIC,
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
    if n == 1 and payload.get("canonical_identity_confirmed") is not True:
        findings.append("parcel identity mastering must reconcile assessor, recorder, survey, and legal description sources")
    if n == 2 and payload.get("control_threshold_met") is not True:
        findings.append("assemblage workflow must block advancement until controlled acreage meets threshold")
    if n == 3 and payload.get("unresolved_conflict_blocks_subdivision") is not True:
        findings.append("survey, title, and boundary conflicts must block subdivision readiness")
    if n == 4 and payload.get("fatal_exception_blocks_acquisition") is not True:
        findings.append("fatal title exceptions must block acquisition approval")
    if n == 5 and payload.get("unresolved_environmental_issue_blocks_go") is not True:
        findings.append("environmental diligence must open blocking exceptions for unresolved recognized conditions")
    if n == 7 and payload.get("ordinance_citation") in (None, "", (), []):
        findings.append("zoning ordinance rules require source ordinance citations")
    if n == 8 and payload.get("dependency_sequence_valid") is not True:
        findings.append("entitlement dependency graph must reject impossible approval sequences")
    if n == 11 and payload.get("all_closing_conditions_satisfied") is not True:
        findings.append("acquisition closing gate must require agreement, deposit, diligence, title, and survey signoff")
    if n == 17 and payload.get("will_serve_valid") is not True:
        findings.append("infrastructure capacity must block readiness when will-serve commitments are absent or expired")
    if n == 20 and payload.get("completeness_score_green") is not True:
        findings.append("permit package completeness must be green before official intake")
    if n == 21 and payload.get("unresolved_comments_block_resubmittal") is not True:
        findings.append("unresolved high-severity agency comments must block resubmittal approval")
    if n == 25 and payload.get("governed_handoff_packet_signed") is not True:
        findings.append("construction handoff requires signed governed basis package")
    if n in (43, 44, 45, 46) and payload.get("human_review") is False:
        findings.append("agent-assisted land development flows require human review for governed mutations")
    if n == 44 and (payload.get("human_confirmation") is not True or payload.get("assignment_without_confirmation_blocked") is not True):
        findings.append("due-diligence task agent may draft but not silently assign or close tasks")
    if n == 47 and payload.get("idempotent_event_handler") is not True:
        findings.append("cross-PBC policy, customer, and supplier handlers must be idempotent")
    if n == 48 and payload.get("integrity_proof_verified") is not True:
        findings.append("audit-proof evidence packs require verified integrity proofs")
    if n == 49 and payload.get("open_obligations_block_archive") is not True:
        findings.append("closeout cannot archive while open obligations remain")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != LAND_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("land development eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in LAND_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary land development PBC datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("land development controls must use owned tables plus declared API/event projections")
    return tuple(findings)


def evaluate_land_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in LAND_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in LAND_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": LAND_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": LAND_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_land_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_land_control(capability) for capability in LAND_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.land-real-estate-development-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": LAND_CONTROL_OWNED_TABLES,
        "declared_dependencies": LAND_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": LAND_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": LAND_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


LAND_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_land_control(slug, payload)) for capability in LAND_CONTROL_CAPABILITIES}

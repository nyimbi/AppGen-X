"""Executable improve1 controls for the Mining Operations Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "mining_operations_management"
EVENT_CONTRACT = "AppGen-X"
MINING_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
MINING_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.mining_operations_management.events"
_BASE_OWNED_TABLES = (
    "mining_operations_management_mine_plan",
    "mining_operations_management_pit_block",
    "mining_operations_management_extraction_shift",
    "mining_operations_management_haulage_cycle",
    "mining_operations_management_fleet_asset",
    "mining_operations_management_ore_quality",
    "mining_operations_management_stockpile",
    "mining_operations_management_policy_rule",
    "mining_operations_management_runtime_parameter",
    "mining_operations_management_schema_extension",
    "mining_operations_management_control_assertion",
    "mining_operations_management_governed_model",
    "mining_operations_management_appgen_outbox_event",
    "mining_operations_management_appgen_inbox_event",
    "mining_operations_management_appgen_dead_letter_event",
)
MINING_OPERATIONS_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"mining_operations_management_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
MINING_OPERATIONS_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys((
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "SafetyPermitChanged",
    "GeotechHazardChanged",
    "WeatherConstraintChanged",
    "MaintenanceAssetAvailabilityChanged",
    "PlantFeedDemandChanged",
    "AssayResultChanged",
    "SurveyMeasurementChanged",
)))
MINING_OPERATIONS_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in MINING_OPERATIONS_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in MINING_OPERATIONS_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "mine_id", "shift_id", "area_id", "plan_version", "policy_version", "actor_id", "audit_trail", "evidence_references")
_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: 'hierarchical_mine_plan_structure_verified',
    2: 'spatial_identity_for_pits_benches_stopes_and_drawpoints_verified',
    3: 'drill_pattern_planning_verified',
    4: 'blast_execution_and_blast_clearance_control_verified',
    5: 'dig_block_and_ore_parcel_definition_verified',
    6: 'shift_target_planning_verified',
    7: 'haul_route_catalog_and_route_constraints_verified',
    8: 'dispatch_assignment_engine_verified',
    9: 'equipment_boundary_and_capability_model_verified',
    10: 'ore_control_sampling_workflow_verified',
    11: 'ore_waste_boundary_decisions_verified',
    12: 'dilution_and_ore_loss_accounting_verified',
    13: 'stockpile_genealogy_verified',
    14: 'stockpile_quality_estimation_verified',
    15: 'plant_feed_nomination_and_blend_planning_verified',
    16: 'crusher_and_rom_pad_queue_visibility_verified',
    17: 'payload_and_tonnage_adjustment_governance_verified',
    18: 'grade_reconciliation_chain_verified',
    19: 'survey_and_measured_volume_integration_verified',
    20: 'geotechnical_domain_and_hazard_tagging_verified',
    21: 'geotechnical_exclusion_zones_and_conditional_approvals_verified',
    22: 'water_dewatering_and_weather_constraints_verified',
    23: 'maintenance_and_availability_boundary_verified',
    24: 'shift_handover_and_supervisor_notes_verified',
    25: 'delay_code_taxonomy_verified',
    26: 'shift_production_reporting_verified',
    27: 'variance_explanation_workflow_verified',
    28: 'rolling_forecast_update_cycle_verified',
    29: 'underground_stope_readiness_checklist_verified',
    30: 'open_pit_phase_and_pushback_readiness_checklist_verified',
    31: 'typed_operational_event_model_verified',
    32: 'event_sourced_operational_history_views_verified',
    33: 'projection_freshness_and_dead_letter_handling_verified',
    34: 'agent_skill_for_shift_planning_verified',
    35: 'agent_skill_for_blast_readiness_review_verified',
    36: 'agent_skill_for_ore_control_and_destination_advice_verified',
    37: 'workbench_shift_console_verified',
    38: 'pit_and_stope_detail_workspace_verified',
    39: 'stockpile_and_plant_feed_board_verified',
    40: 'reconciliation_workspace_verified',
    41: 'mobile_and_low_connectivity_capture_verified',
    42: 'mine_specific_permissions_and_approvals_verified',
    43: 'scenario_simulation_for_mine_to_plant_decisions_verified',
    44: 'mining_anomaly_detection_verified',
    45: 'release_evidence_pack_for_operations_scenarios_verified',
    46: 'seed_data_for_realistic_mine_operations_verified',
    47: 'api_surface_completeness_verified',
    48: 'mining_runbooks_and_operator_guidance_verified',
    49: 'test_matrix_across_mining_flows_verified',
    50: 'operational_readiness_gate_verified',
}
_DOMAIN_FIELDS: dict[int, tuple[str, ...]] = {
    1: ('plan_version_id', 'phase_id', 'pushback_id', 'bench_id', 'stope_id', 'drawpoint_id', 'planned_tonnage', 'planned_grade', 'stripping_ratio', 'ore_destination'),
    2: ('canonical_location_id', 'mine_coordinate_reference', 'mining_method', 'active_status', 'owning_plan_period', 'boundary_polygon_ref'),
    3: ('drill_pattern_id', 'hole_count', 'hole_depth', 'burden', 'spacing', 'sub_drill', 'explosive_type', 'initiation_sequence', 'powder_factor', 'fragmentation_class'),
    4: ('blast_id', 'drill_pattern_id', 'blast_time', 'clearance_confirmed', 'exclusion_zone_checked', 'misfire_flag', 'reentry_approval', 'post_blast_inspection'),
    5: ('ore_parcel_id', 'pit_block_id', 'stope_id', 'expected_tonnes', 'expected_grade_band', 'lithology', 'destination_policy', 'dilution_risk', 'sequence_priority'),
    6: ('shift_target_id', 'shift_code', 'ore_tonnes_target', 'waste_tonnes_target', 'metres_drilled_target', 'blasts_due', 'truck_load_target', 'plant_feed_nomination', 'critical_constraints'),
    7: ('haul_route_id', 'from_point', 'to_point', 'ramp_segment', 'distance_km', 'gradient_band', 'expected_cycle_time', 'traffic_direction_rule', 'closure_state'),
    8: ('dispatch_assignment_id', 'loader_id', 'truck_id', 'operator_projection_id', 'loading_point_id', 'route_id', 'payload_class', 'reassignment_reason', 'compatibility_result'),
    9: ('fleet_asset_id', 'equipment_class', 'payload_band', 'approved_mining_areas', 'operator_certification_required', 'fuel_type', 'communication_available', 'operating_boundary'),
    10: ('sample_id', 'dig_block_id', 'blast_polygon_id', 'stope_id', 'sample_type', 'sample_interval', 'assay_status', 'provisional_grade', 'final_grade', 'sampling_confidence'),
    11: ('boundary_decision_id', 'dig_line_adjustment', 'visual_geology_observation', 'assay_reference', 'grade_threshold', 'destination_change', 'approver_id'),
    12: ('ore_loss_event_id', 'dig_block_id', 'blast_id', 'haul_cycle_id', 'loss_category', 'dilution_tonnes', 'ore_loss_tonnes', 'sampling_uncertainty'),
    13: ('stockpile_movement_id', 'source_parcel_id', 'movement_type', 'top_up_tonnes', 'reclaim_tonnes', 'moisture_adjustment', 'source_lineage'),
    14: ('stockpile_id', 'estimated_tonnes', 'estimated_grade', 'moisture', 'density_factor', 'confidence_class', 'last_survey_date', 'last_sample_date'),
    15: ('feed_nomination_id', 'shift_code', 'required_tonnes', 'target_grade_band', 'blend_components', 'stockpile_draw_plan', 'plant_destination', 'fallback_feed_options'),
    16: ('queue_state_id', 'destination_id', 'queue_length', 'wait_time_band', 'destination_available', 'diversion_rule', 'delay_attribution'),
    17: ('tonnage_adjustment_id', 'payload_tonnes', 'truck_count_tonnes', 'survey_tonnes', 'plant_receipt_tonnes', 'adjustment_method', 'effective_period', 'material_classes'),
    18: ('reconciliation_id', 'plan_grade', 'control_grade', 'mined_grade', 'stockpile_grade', 'plant_feed_grade', 'variance_reason', 'signoff_stage'),
    19: ('survey_id', 'survey_date', 'survey_source', 'survey_method', 'measured_volume', 'confidence', 'affected_production_records'),
    20: ('geotech_domain_id', 'hazard_state', 'risk_rating', 'monitoring_source', 'mitigation_requirement', 'condition_expiry'),
    21: ('exclusion_zone_id', 'allowed_activity', 'allowed_equipment', 'monitoring_checks', 'escort_requirement', 'review_interval', 'approval_expiry'),
    22: ('constraint_id', 'rainfall', 'dewatering_status', 'road_condition', 'sump_capacity', 'visibility_window', 'blocked_activity'),
    23: ('fleet_asset_id', 'availability_state', 'breakdown_class', 'maintenance_due_window', 'workshop_queue', 'return_to_service_release'),
    24: ('handover_id', 'active_headings', 'blocked_areas', 'equipment_issues', 'destination_changes', 'outstanding_blasts', 'stockpile_concerns', 'plant_feed_risks'),
    25: ('delay_code_id', 'delay_domain', 'primary_cause', 'secondary_cause', 'lost_minutes', 'availability_impact', 'utilization_impact'),
    26: ('shift_report_id', 'ore_tonnes', 'waste_tonnes', 'metres_drilled', 'blasts_fired', 'truck_loads', 'stockpile_movements', 'plant_feed_sent', 'delay_summary'),
    27: ('variance_id', 'measure_type', 'planned_value', 'actual_value', 'variance_threshold', 'causal_category', 'action_owner', 'future_commitment_impact'),
    28: ('forecast_version_id', 'forecast_horizon', 'delta_from_plan', 'confidence_band', 'dependency_assumptions', 'approval_state'),
    29: ('stope_readiness_id', 'development_complete', 'support_installed', 'ventilation_available', 'services_in_place', 'brow_condition_checked', 'drawpoint_ready', 'backfill_status'),
    30: ('pit_phase_readiness_id', 'access_established', 'dewatering_complete', 'ramp_serviceable', 'wall_monitoring_active', 'prestrip_achieved', 'first_blast_approval'),
    31: ('event_schema_id', 'event_type', 'required_mining_fields', 'generic_lifecycle_lineage', 'downstream_projection'),
    32: ('timeline_id', 'source_event_id', 'actor_id', 'reason_code', 'before_summary', 'after_summary', 'replay_checksum'),
    33: ('projection_id', 'freshness_seconds', 'dead_letter_id', 'replay_action', 'operator_explanation', 'affected_area'),
    34: ('shift_plan_skill_id', 'proposed_tonnes', 'active_areas', 'equipment_assignments', 'blast_windows', 'risk_notes', 'diff_preview'),
    35: ('blast_readiness_skill_id', 'drill_completion_summary', 'clearance_status', 'explosive_plan', 'exclusion_zone_checks', 'geotech_status', 'blockers'),
    36: ('ore_advice_skill_id', 'grade_evidence', 'reconciliation_state', 'policy_threshold', 'suggested_destination', 'confidence', 'rationale'),
    37: ('shift_console_id', 'active_areas', 'dispatch_board', 'blast_windows', 'queue_states', 'delays', 'feed_nomination', 'safety_constraints'),
    38: ('workspace_id', 'area_type', 'plan_tab', 'readiness_tab', 'blast_status_tab', 'ore_control_tab', 'active_equipment_tab', 'reconciliation_history'),
    39: ('feed_board_id', 'stockpile_tonnes', 'grade_band', 'moisture', 'reclaim_plan', 'blend_recipe', 'nomination_gap', 'feed_risk_alert'),
    40: ('reconciliation_workspace_id', 'survey_updates', 'tonnage_adjustments', 'grade_variances', 'dilution_events', 'stakeholder_signoffs', 'blockers'),
    41: ('offline_capture_id', 'capture_type', 'local_queue_id', 'conflict_resolution', 'sync_status', 'duplicate_prevention_key'),
    42: ('approval_policy_id', 'permission_scope', 'threshold', 'segregation_of_duties_rule', 'escalation_path', 'denial_reason'),
    43: ('scenario_id', 'scenario_type', 'equipment_loss', 'blast_slip', 'geotech_closure', 'stockpile_depletion', 'plant_grade_target', 'non_mutating_output'),
    44: ('anomaly_id', 'anomaly_type', 'cycle_time_check', 'material_flow_check', 'dispatch_conflict_check', 'false_positive_suppression', 'triage_outcome'),
    45: ('scenario_pack_id', 'open_pit_pack', 'underground_pack', 'blast_release_pack', 'stockpile_pack', 'plant_feed_pack', 'reconciliation_pack'),
    46: ('seed_dataset_id', 'open_pit_scenario', 'underground_scenario', 'fleet_records', 'drill_patterns', 'assay_results', 'plant_feed_targets'),
    47: ('api_surface_id', 'dispatch_api', 'blast_readiness_api', 'ore_sample_api', 'stockpile_adjustment_api', 'feed_nomination_api', 'reconciliation_api', 'validation_only_flow'),
    48: ('runbook_id', 'shift_planning_steps', 'blast_control_steps', 'dispatch_recovery_steps', 'stockpile_correction_steps', 'feed_nomination_steps', 'close_steps'),
    49: ('test_matrix_id', 'open_pit_flow', 'underground_flow', 'drill_blast_flow', 'dispatch_flow', 'ore_control_flow', 'reconciliation_flow'),
    50: ('readiness_gate_id', 'scenario_tests_passed', 'ui_snapshots_fresh', 'typed_event_samples_present', 'seed_reproducible', 'reconciliation_outputs_present', 'domain_signoff'),
}
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {feature_number: _BASE_FIELDS + _DOMAIN_FIELDS[feature_number] + (primary_proof,) for feature_number, primary_proof in _PRIMARY_PROOF_FIELDS.items()}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    20: ("GeotechHazardChanged",),
    21: ("GeotechHazardChanged", "SafetyPermitChanged"),
    22: ("WeatherConstraintChanged",),
    23: ("MaintenanceAssetAvailabilityChanged",),
    31: ("AuditEventSealed",),
    33: ("AuditEventSealed", "OperationalKpiChanged"),
    42: ("PolicyChanged",),
    49: ("PolicyChanged", "AuditEventSealed"),
    50: ("AuditEventSealed", "OperationalKpiChanged"),
}
_DOMAIN_MESSAGES: dict[int, str] = {
    1: 'Extend the planning model so one mine plan can contain period versions, pit phases, pushbacks, benches, stopes, drawpoints, and mining blocks with explicit parent-child relationships, sequencing windows, planned tonnage, planned grade, stripping ratio, and ore destination.',
    2: 'Add canonical location identifiers and boundary metadata for pit, bench, stope, drawpoint, ore drive, and loading point records, including mine coordinate reference, mining method, active status, and linkage to the owning mine plan period.',
    3: 'Introduce drill pattern entities and workflow steps for hole count, hole depth, burden, spacing, sub-drill, explosive type, initiation sequence, powder factor, target fragmentation class, and shift readiness status.',
    4: 'Add blast execution records tied to drill patterns with blast time, clearance confirmation, exclusion zone checks, misfire flags, re-entry approval, and post-blast inspection outcome.',
    5: 'Add dig block or ore parcel records beneath pit blocks and stopes with expected tonnes, expected grade bands, lithology, destination policy, dilution risk, and mining sequence priority.',
    6: 'Add shift target objects for day and night shifts with target ore tonnes, waste tonnes, metres drilled, blasts due, truck loads, plant feed nomination, and critical constraints by mining area.',
    7: 'Add haul route definitions with from-point, to-point, ramp segment, distance, gradient band, expected cycle time, traffic direction rule, and temporary closure state.',
    8: 'Add dispatch assignment capabilities that allocate trucks to loaders or stopes, track dispatch board state, capture reassignment reasons, and enforce equipment compatibility by loading point, payload class, and route condition.',
    9: 'Extend fleet asset coverage to include equipment class, payload band, approved mining areas, operator certification requirements, fuel type, communication availability, and whether the unit is cleared for pit, underground, or dual-use operation.',
    10: 'Introduce ore control sample records tied to dig blocks, blast polygons, and stopes with sample type, interval, assay status, provisional grade, final grade, and sampling confidence.',
    11: 'Add boundary decision records that capture dig-line adjustments, visual geology observations, assay references, grade thresholds, destination changes, and who approved the ore or waste call.',
    12: 'Add dilution and ore-loss events linked to dig blocks, stopes, blasts, and haul cycles, with causal categories such as overbreak, underbreak, backfill contamination, poor dig compliance, and sampling uncertainty.',
    13: 'Extend stockpile handling to track build, top-up, reclaim, depletion, moisture adjustment, and source lineage from pit block, stope, or ore parcel into every stockpile movement.',
    14: 'Add estimated tonnes, estimated grade, moisture, density factor, confidence class, last survey date, and last sample date to stockpiles with governed recalculation rules after each movement or survey adjustment.',
    15: 'Add plant feed nominations by shift and day with required tonnes, target grade band, blend components, stockpile draw plan, crusher or mill destination, and fallback feed options if a source becomes unavailable.',
    16: 'Add queue state records for crusher pockets, ROM pads, ore passes, and tipping locations with queue length, wait time band, destination availability, and diversion rules.',
    17: 'Add tonnage adjustment records that compare payload system, truck count, survey, and plant receipt measures, including approved adjustment method, effective period, and material classes affected.',
    18: 'Build reconciliation entities and projections for plan grade, control grade, mined grade, stockpile grade, and plant feed grade, including variance reasons and sign-off stages.',
    19: 'Add measured survey capture for excavation progress, stockpile volumes, stope voids, and backfill progress with survey date, source, method, confidence, and linkage to affected production records.',
    20: 'Add geotechnical domain tags and hazard states to pits, benches, stopes, and active work areas with risk rating, monitoring source, mitigation requirement, and expiry time for the current ground condition assessment.',
    21: 'Add exclusion zone rules and conditional approval workflows that specify allowed activity, allowed equipment, monitoring checks, escort requirements, and review interval.',
    22: 'Add operational constraint records for rainfall, dewatering status, road condition, sump capacity, and visibility windows, with logic that can block drilling, blasting, loading, or haulage by area.',
    23: 'Extend fleet assets with availability states, breakdown class, maintenance due windows, workshop queue, and return-to-service release checks that feed directly into dispatch eligibility.',
    24: 'Add structured shift handover records covering active headings, blocked areas, equipment issues, ore destination changes, outstanding blasts, stockpile concerns, and plant feed risks.',
    25: 'Add a mine-specific delay taxonomy for drilling, blasting, loading, haulage, ore pass, crusher, geotech, weather, survey, and maintenance interruptions with primary and secondary cause capture.',
    26: 'Add shift production reports that summarize ore tonnes, waste tonnes, metres drilled, blasts fired, truck loads, stockpile movements, plant feed sent, delays, and safety or geotech exceptions by area.',
    27: 'Add variance records for tonnes, grade, metres, blasts, cycle count, and equipment hours with causal categories, supporting evidence, action owner, and whether the variance impacts future plan commitments.',
    28: 'Add rolling forecast versions for next shift, next day, and next week with deltas from the approved plan, confidence band, and dependency assumptions for active mining areas and plant feed.',
    29: 'Add stope readiness checklists with headings for development complete, support installed, ventilation available, services in place, brow condition checked, drawpoint readiness, and backfill status.',
    30: 'Add pit-phase readiness records for access established, dewatering complete, ramp serviceability, wall monitoring active, pre-strip achieved, and first-blast approval.',
    31: 'Expand emitted events into typed mining events such as `MinePlanVersionApproved`, `BlastCleared`, `DispatchAssignmentChanged`, `OreBoundaryAdjusted`, `StockpileReconciled`, and `PlantFeedNominated` while preserving lineage to the generic package lifecycle.',
    32: 'Build event-backed timelines for plan versions, shift execution, dispatch changes, ore boundary calls, stockpile genealogy, and reconciliation adjustments with actor, reason, and before-after summaries.',
    33: 'Add freshness indicators, dead-letter queues, replay actions, and operator explanations for mining projections that power dispatch, stockpile, and reporting screens.',
    34: 'Add an agent skill that drafts a shift plan with proposed tonnes, active areas, equipment assignments, blast windows, ore destination changes, and risk notes, all as preview-only until a human confirms.',
    35: 'Add an agent skill that summarizes drill completion, clearance status, explosive plan, exclusion zone checks, geotech status, and outstanding blockers for a specific blast area.',
    36: 'Add an agent skill that proposes ore-waste boundary adjustments, stockpile destinations, or plant feed substitutions based on grade evidence, reconciliation state, and policy thresholds.',
    37: 'Create a shift console in `MiningOperationsManagementWorkbench` showing active areas, dispatch board, blast windows, queue states, delays, stockpile movements, plant feed nomination, and unresolved safety or geotech constraints.',
    38: 'Extend `MiningOperationsManagementDetail` into pit and stope workspaces with tabs for plan, readiness, blast status, ore control, active equipment, delays, and reconciliation history.',
    39: 'Add a board view for stockpiles and plant feed showing tonnes, grade bands, moisture, reclaim plan, active blend recipes, nomination gaps, and feed risk alerts.',
    40: 'Add a reconciliation workspace for monthly and weekly close that stages survey updates, tonnage adjustments, grade variances, dilution events, and sign-off tasks from mining, geology, survey, and plant stakeholders.',
    41: 'Add offline-tolerant capture flows for delay events, sample collection, shift notes, and area readiness checks with local queueing, conflict resolution, and later synchronization through governed APIs.',
    42: 'Add permission scopes and approval policies for plan approval, blast clearance, ore boundary change, stockpile adjustment, plant feed nomination, and reconciliation sign-off, with thresholds and segregation-of-duties checks.',
    43: 'Add simulation flows for what-if scenarios covering equipment loss, blast slip, geotech closure, stockpile depletion, and altered plant grade targets, with projected impact on tonnes, grade, queues, and backlog.',
    44: 'Build anomaly rules and models for improbable haul cycles, grade jumps, inconsistent tonnage flows, dispatch conflicts, unapproved area activation, and reconciliation mismatches.',
    45: 'Expand release evidence so it contains scenario packs for open-pit production, underground stope mining, blast release, stockpile management, plant feed nomination, and reconciliation close, each with input data, UI proof, events, and outcome summaries.',
    46: 'Enrich package seed data with at least one open-pit and one underground mine scenario, including active equipment, drill patterns, blasts, stockpiles, assay results, haul routes, delays, and plant feed targets.',
    47: 'Add governed APIs for dispatch assignments, blast readiness, ore-control samples, stockpile adjustments, plant feed nominations, reconciliation actions, delay capture, and forecast versions, plus read endpoints for area workspaces and boards.',
    48: 'Add domain runbooks and assistant help content for shift planning, blast control, dispatch recovery, stockpile correction, plant feed nomination, and reconciliation close, all aligned with package workflows and screens.',
    49: 'Add a test matrix that covers open-pit and underground plan setup, drill-and-blast control, dispatching, ore control updates, stockpile genealogy, plant feed nominations, geotech restrictions, and reconciliation close.',
    50: 'Add a release gate that requires passing scenario tests, fresh UI snapshots, typed event samples, seed-data reproducibility, reconciliation outputs, and sign-off that dispatch, ore control, stockpile, plant feed, and geotech surfaces all behaved as expected.',
}
_HUMAN_CONFIRMATION_FEATURES = (4, 11, 17, 21, 27, 29, 30, 34, 35, 36, 40, 42, 43, 50)
_PROJECTION_ONLY_FEATURES = (20, 21, 22, 23, 31, 33, 42, 49, 50)
_AGENT_PREVIEW_FEATURES = (34, 35, 36)
_NON_MUTATING_FEATURES = (43, 49, 50)


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
        "tables": (f"mining_operations_management_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": proof,
        "ui": f"MiningOperationsManagement{_camel(capability.slug)}Panel",
        "route": f"POST /mining-operations-management/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in MINING_OPERATIONS_CONTROL_CAPABILITIES}


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
        "event_topic": MINING_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
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
        findings.append("mining operations decisions with safety, production, grade, dispatch, or release impact require human approval before mutation")
    if feature_number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("mining assistant skills must produce preview-only drafts with source evidence and human confirmation gates")
    if feature_number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("mining simulations, release gates, and overlap checks must be side-effect-free planning artifacts")
    if feature_number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("geotech, weather, maintenance, assay, survey, safety, plant, policy, and audit context must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != MINING_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("mining operations eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in MINING_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary mining operations datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("mining operations controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_mining_operations_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in MINING_OPERATIONS_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in MINING_OPERATIONS_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": MINING_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": MINING_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_mining_operations_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_mining_operations_control(capability) for capability in MINING_OPERATIONS_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.mining-operations-management-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": MINING_OPERATIONS_CONTROL_OWNED_TABLES, "declared_dependencies": MINING_OPERATIONS_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": MINING_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": MINING_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


MINING_OPERATIONS_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_mining_operations_control(slug, payload)) for capability in MINING_OPERATIONS_CONTROL_CAPABILITIES}

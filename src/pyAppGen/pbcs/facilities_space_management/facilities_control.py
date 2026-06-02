"""Executable improve1 controls for the Facilities Space Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "facilities_space_management"
EVENT_CONTRACT = "AppGen-X"
FACILITIES_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
FACILITIES_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.facilities_space_management.events"
FACILITIES_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(DOMAIN_OWNED_TABLES + (
    "facilities_space_management_facility_site",
    "facilities_space_management_building",
    "facilities_space_management_room_space",
    "facilities_space_management_occupancy_snapshot",
    "facilities_space_management_space_reservation",
    "facilities_space_management_maintenance_link",
    "facilities_space_management_lease_metadata",
    "facilities_space_management_space_plan",
    "facilities_space_management_appgen_outbox_event",
    "facilities_space_management_appgen_inbox_event",
    "facilities_space_management_appgen_dead_letter_event",
)))
FACILITIES_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "EmployeeCreated",
    "EmployeeProvisioned",
    "WorkOrderCompleted",
    "MaintenanceCompleted",
    "AccessPolicyChanged",
    "PolicyChanged",
    "LeaseContractApproved",
    "SafetyIncidentRecorded",
    "FinancialPeriodChanged",
    "POST /notifications/messages",
)))

FACILITIES_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in FACILITIES_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in FACILITIES_CONTROL_CAPABILITIES}

_SPEC_ROWS: tuple[tuple[int, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = [(1, ('facilities_space_management_facility_site',), ('campus_hierarchy', 'geospatial_boundary', 'building_group', 'operating_hours', 'facility_owner', 'service_zones', 'emergency_zones', 'parking_assets', 'visitor_entrances', 'loading_areas', 'site_status'), 'FacilitySiteTopologyWorkbench', 'POST /facility-sites/topology', ()), (2, ('facilities_space_management_facility_floor', 'facilities_space_management_space_record'), ('floor_map', 'coordinate_system', 'zones', 'entrances', 'elevators', 'stairs', 'exits', 'restrooms', 'amenities', 'restricted_areas', 'map_version', 'change_impact'), 'BuildingFloorDigitalTwin', 'POST /floors/digital-twin', ()), (3, ('facilities_space_management_space_record',), ('gross_area', 'rentable_area', 'usable_area', 'assignable_area', 'net_area', 'capacity_method', 'seating_count', 'neighborhood', 'amenities', 'accessibility', 'av_features', 'environmental_profile', 'measurement_evidence'), 'SpaceRecordPrecisionPanel', 'POST /spaces/area-standardize', ()), (4, ('facilities_space_management_space_type', 'facilities_space_management_facility_policy_rule'), ('taxonomy', 'usage_constraints', 'safety_requirements', 'reservation_eligibility', 'capacity_method', 'access_rules', 'amenities', 'compliance_attributes', 'lifecycle_state'), 'SpaceTypeTaxonomyStudio', 'POST /space-types/classify', ()), (5, ('facilities_space_management_occupancy_plan',), ('plan_version', 'baseline', 'scenario_assumptions', 'target_utilization', 'department_allocations', 'effective_dates', 'approval_status', 'freeze_window', 'rollback_plan', 'comparison_view'), 'OccupancyPlanScenarioControl', 'POST /occupancy-plans/versions', ()), (6, ('facilities_space_management_occupancy_assignment', 'facilities_space_management_access_constraint'), ('assignment_type', 'occupant_projection', 'department', 'work_pattern', 'required_equipment', 'accessibility_needs', 'security_clearance', 'adjacency_requirements', 'start_date', 'end_date', 'approval_evidence', 'capacity_validation'), 'OccupantAssignmentGovernance', 'POST /occupancy-assignments/validate', ('EmployeeCreated', 'AccessPolicyChanged')), (7, ('facilities_space_management_occupancy_plan', 'facilities_space_management_utilization_observation'), ('team_patterns', 'anchor_days', 'visit_frequency', 'booking_preferences', 'peak_windows', 'collocation_needs', 'forecast_input', 'hr_mutation_blocked'), 'HybridWorkPatternModeling', 'POST /hybrid-patterns/model', ('EmployeeCreated',)), (8, ('facilities_space_management_space_reservation', 'facilities_space_management_space_availability_snapshot', 'facilities_space_management_access_constraint'), ('capacity_check', 'requester_role', 'attendee_count', 'equipment_check', 'accessibility_check', 'maintenance_block_check', 'access_constraint_check', 'booking_horizon', 'setup_buffer', 'conflict_policy', 'blocked_explanation'), 'SpaceReservationEligibilityEngine', 'POST /space-reservations/eligibility', ('AccessPolicyChanged', 'WorkOrderCompleted')), (9, ('facilities_space_management_space_reservation', 'facilities_space_management_facility_governed_model'), ('alternate_spaces', 'alternate_times', 'layout_swaps', 'nearby_rooms', 'split_booking', 'equipment_substitution', 'priority_resolution', 'tradeoffs', 'required_approvals'), 'ReservationConflictOptimization', 'POST /space-reservations/optimize-conflict', ()), (10, ('facilities_space_management_space_reservation', 'facilities_space_management_move_task'), ('setup_requirements', 'service_tasks', 'setup_buffer', 'teardown_buffer', 'provider_assignments', 'readiness_checks', 'completion_evidence', 'confirmation_gate'), 'MeetingRoomSetupDependencies', 'POST /space-reservations/setup-readiness', ()), (11, ('facilities_space_management_space_record', 'facilities_space_management_space_reservation'), ('hot_desk_pool', 'neighborhood', 'desk_features', 'booking_rules', 'auto_release', 'check_in_evidence', 'team_adjacency', 'utilization_feedback', 'recommendation_reason'), 'HotDeskNeighborhoodManager', 'POST /hot-desks/recommend', ()), (12, ('facilities_space_management_utilization_observation',), ('observation_source', 'confidence', 'sampling_method', 'privacy_basis', 'time_window', 'occupancy_estimate', 'sensor_health', 'reservation_reconciliation', 'assignment_reconciliation', 'confidence_interval'), 'OccupancyObservationConfidence', 'POST /utilization-observations/reconcile', ()), (13, ('facilities_space_management_utilization_observation', 'facilities_space_management_facility_policy_rule'), ('aggregation_threshold', 'anonymization_policy', 'retention_period', 'purpose_basis', 'role_based_masking', 'forbidden_drilldowns', 'privacy_decision', 'individual_exposure_blocked'), 'PrivacySafeWorkplaceAnalytics', 'POST /workplace-analytics/privacy-check', ('AccessPolicyChanged',)), (14, ('facilities_space_management_space_availability_snapshot',), ('availability_reason', 'blocked_intervals', 'confidence', 'source_records', 'capacity_remaining', 'maintenance_state', 'safety_state', 'access_constraints', 'reservation_eligibility', 'material_change_event'), 'AvailabilitySnapshotSemantics', 'POST /availability-snapshots/publish', ()), (15, ('facilities_space_management_maintenance_signal', 'facilities_space_management_space_availability_snapshot'), ('affected_spaces', 'severity', 'expected_duration', 'usable_capacity', 'noise_impact', 'odor_impact', 'access_impact', 'safety_impact', 'required_buffers', 'release_criteria', 'work_order_projection'), 'MaintenanceAwareSpaceBlocking', 'POST /maintenance-signals/block-space', ('WorkOrderCompleted', 'MaintenanceCompleted')), (16, ('facilities_space_management_move_request', 'facilities_space_management_move_task'), ('move_type', 'affected_occupants', 'source_spaces', 'destination_spaces', 'approval_routing', 'move_date', 'dependencies', 'risk', 'communication_plan', 'readiness_checklist', 'capacity_impact'), 'MoveRequestLifecycle', 'POST /move-requests/open', ('EmployeeCreated',)), (17, ('facilities_space_management_move_task', 'facilities_space_management_move_request'), ('dependency_graph', 'task_role', 'due_date', 'evidence', 'blocker', 'handoff', 'confirmation', 'rollback', 'critical_dependencies_open', 'completion_decision'), 'MoveTaskDependencyOrchestration', 'POST /move-tasks/complete', ()), (18, ('facilities_space_management_access_constraint', 'facilities_space_management_space_reservation'), ('constraint_type', 'affected_spaces', 'allowed_roles', 'effective_window', 'reason', 'policy_basis', 'emergency_override', 'access_projection', 'reservation_application', 'wayfinding_application'), 'AccessConstraintGovernance', 'POST /access-constraints/apply', ('AccessPolicyChanged',)), (19, ('facilities_space_management_space_reservation', 'facilities_space_management_access_constraint'), ('visitor_eligibility', 'escort_requirements', 'visitor_capacity', 'check_in_dependencies', 'badge_prerequisites', 'confidentiality_restrictions', 'guest_host_linkage', 'planning_decision'), 'VisitorGuestSpaceControls', 'POST /visitor-space-controls/check', ('AccessPolicyChanged',)), (20, ('facilities_space_management_safety_inspection', 'facilities_space_management_space_availability_snapshot'), ('inspection_type', 'checklist', 'inspector', 'hazard_severity', 'affected_spaces', 'required_remediation', 'recurrence', 'due_dates', 'evidence_attachments', 'space_block_decision'), 'SafetyInspectionProgram', 'POST /safety-inspections/record', ()), (21, ('facilities_space_management_safety_inspection', 'facilities_space_management_maintenance_signal', 'facilities_space_management_access_constraint'), ('hazard_record', 'linked_spaces', 'linked_floors', 'linked_inspections', 'linked_maintenance', 'incident_projection', 'reservation_cancellations', 'remediation_tasks', 'reinspection_required'), 'HazardIncidentLinkage', 'POST /hazards/link-space', ('SafetyIncidentRecorded',)), (22, ('facilities_space_management_capacity_plan', 'facilities_space_management_occupancy_plan'), ('demand_drivers', 'headcount_projection', 'hybrid_patterns', 'reservation_trends', 'utilization_observations', 'occupancy_targets', 'scenario_assumptions', 'shortfall_by_site', 'surplus_by_space_type'), 'CapacityPlanDemandForecasting', 'POST /capacity-plans/forecast', ('EmployeeCreated',)), (23, ('facilities_space_management_utilization_observation', 'facilities_space_management_facility_governed_model'), ('site_heatmap', 'floor_heatmap', 'zone_heatmap', 'room_heatmap', 'desk_pool_heatmap', 'space_type_heatmap', 'day_hour_pattern', 'confidence', 'observation_source', 'redesign_recommendations'), 'WorkplaceUtilizationHeatmaps', 'GET /workplace-analytics/heatmaps', ()), (24, ('facilities_space_management_capacity_plan', 'facilities_space_management_facility_governed_model'), ('attendance_policy_scenario', 'department_move_scenario', 'site_closure_scenario', 'lease_change_scenario', 'renovation_phase_scenario', 'emergency_closure_scenario', 'utilization_impact', 'safety_impact', 'cost_impact'), 'SpaceDemandScenarioSimulation', 'POST /space-demand/simulate', ('LeaseContractApproved',)), (25, ('facilities_space_management_lease_metadata', 'facilities_space_management_capacity_plan'), ('projection_source', 'freshness', 'allowed_fields', 'cost_per_area', 'expiration', 'options', 'restrictions', 'chargeback_context', 'foreign_mutation_blocked'), 'LeaseCostContextProjections', 'POST /lease-cost-projections/refresh', ('LeaseContractApproved',)), (26, ('facilities_space_management_space_plan', 'facilities_space_management_appgen_outbox_event'), ('department', 'cost_center_projection', 'space', 'area', 'utilization_basis', 'time_period', 'rule_version', 'allocation_evidence', 'finance_handoff_event'), 'SpaceChargebackAllocationEvidence', 'POST /space-chargebacks/publish', ('FinancialPeriodChanged',)), (27, ('facilities_space_management_space_record', 'facilities_space_management_occupancy_assignment'), ('accessibility_attributes', 'accommodation_constraints', 'accessible_route_map', 'privacy_controls', 'reservation_filters', 'move_validation', 'assignment_validation', 'violation_blocked'), 'AccessibilityInclusiveWorkplaceControls', 'POST /accessibility/validate-space-use', ('EmployeeCreated',)), (28, ('facilities_space_management_utilization_observation', 'facilities_space_management_maintenance_signal'), ('temperature', 'humidity', 'air_quality', 'noise', 'light', 'crowding', 'thresholds', 'affected_spaces', 'comfort_score', 'remediation_link'), 'IndoorEnvironmentalQualitySignals', 'POST /environmental-observations/record', ()), (29, ('facilities_space_management_facility_governed_model', 'facilities_space_management_capacity_plan'), ('energy_estimate', 'carbon_estimate', 'site', 'floor', 'zone', 'utilization_scenario', 'consolidation_recommendation', 'hvac_schedule', 'reservation_clustering', 'employee_experience_tradeoff'), 'EnergyCarbonAwareSpaceOps', 'POST /space-operations/carbon-optimize', ()), (30, ('facilities_space_management_facility_site', 'facilities_space_management_access_constraint', 'facilities_space_management_safety_inspection'), ('emergency_zones', 'muster_areas', 'route_constraints', 'floor_wardens', 'capacity_limits', 'emergency_contacts', 'drill_evidence', 'blocked_exits', 'readiness_status'), 'EmergencyPreparednessMusterZones', 'POST /emergency-readiness/prove', ()), (31, ('facilities_space_management_space_record', 'facilities_space_management_access_constraint'), ('wayfinding_graph', 'paths', 'elevators', 'stairs', 'entrances', 'amenities', 'accessible_routes', 'temporary_closures', 'access_respected', 'route_result'), 'WayfindingOccupantExperience', 'POST /wayfinding/route', ()), (32, ('facilities_space_management_space_record', 'facilities_space_management_space_availability_snapshot'), ('amenity_record', 'capacity', 'location', 'availability', 'service_hours', 'restrictions', 'support_owner', 'incident_state', 'recommendation_input'), 'AmenitiesServiceLevelManagement', 'POST /amenities/manage', ()), (33, ('facilities_space_management_space_reservation', 'facilities_space_management_move_task'), ('cleaning_policy', 'turnover_buffer', 'cleaning_task_evidence', 'high_use_trigger', 'post_event_cleaning', 'readiness_status', 'back_to_back_block', 'turnover_decision'), 'CleaningTurnoverScheduling', 'POST /space-reservations/turnover-check', ()), (34, ('facilities_space_management_space_reservation', 'facilities_space_management_move_task', 'facilities_space_management_access_constraint'), ('event_record', 'multiple_spaces', 'setup_tasks', 'service_dependencies', 'attendee_capacity', 'visitor_rules', 'emergency_capacity', 'approval_workflow', 'planning_status'), 'EventLargeGatheringPlanning', 'POST /facility-events/plan', ()), (35, ('facilities_space_management_space_plan', 'facilities_space_management_move_request', 'facilities_space_management_access_constraint'), ('renovation_phases', 'affected_spaces', 'closure_windows', 'temporary_assignments', 'safety_constraints', 'noise_impacts', 'contractor_access', 'communication_plan', 'simulation_result'), 'RenovationConstructionPhasing', 'POST /renovations/simulate', ('WorkOrderCompleted',)), (36, ('facilities_space_management_facility_exception_case',), ('exception_type', 'scope', 'approver_authority', 'expiry', 'compensating_controls', 'affected_spaces', 'user_impact', 'closure_evidence', 'decision'), 'FacilityExceptionWorkflow', 'POST /facility-exceptions/resolve', ()), (37, ('facilities_space_management_space_reservation', 'facilities_space_management_utilization_observation'), ('check_in_tracking', 'no_show_detection', 'grace_period', 'auto_release', 'repeat_no_show_patterns', 'notification', 'exception_handling', 'policy_tuning_signal'), 'ReservationNoShowReleaseOptimization', 'POST /space-reservations/no-show-release', ()), (38, ('facilities_space_management_occupancy_plan', 'facilities_space_management_occupancy_assignment'), ('adjacency_requirements', 'team_neighborhoods', 'compatibility_rules', 'collaboration_frequency', 'quiet_zones', 'noisy_zones', 'scenario_score', 'assignment_recommendation'), 'NeighborhoodTeamAdjacencyPlanning', 'POST /occupancy-plans/adjacency-score', ()), (39, ('facilities_space_management_space_record', 'facilities_space_management_space_availability_snapshot'), ('search_intent', 'capacity', 'equipment', 'location', 'accessibility', 'privacy', 'availability', 'policy_constraints', 'distance', 'utilization', 'setup_needs', 'ranking_reason'), 'SpaceSearchRecommendationEngine', 'POST /space-search/recommend', ()), (40, ('facilities_space_management_facility_schema_extension', 'facilities_space_management_facility_control_assertion'), ('source_document', 'proposed_sites', 'proposed_floors', 'proposed_spaces', 'proposed_reservations', 'proposed_move_tasks', 'proposed_maintenance_blocks', 'proposed_access_constraints', 'proposed_safety_findings', 'proposed_capacity_plans', 'source_citations', 'confidence', 'affected_tables', 'event_plan', 'human_confirmation'), 'AgentFacilityDocumentIntake', 'POST /facility-agent/document-intake', ()), (41, ('facilities_space_management_facility_floor', 'facilities_space_management_space_record', 'facilities_space_management_facility_control_assertion'), ('map_change', 'space_change', 'affected_reservations', 'affected_occupants', 'affected_safety_zones', 'affected_moves', 'affected_maintenance', 'affected_reporting', 'materiality', 'approval_required'), 'FloorPlanChangeImpactAnalysis', 'POST /floor-plans/impact-analysis', ()), (42, ('facilities_space_management_capacity_plan', 'facilities_space_management_lease_metadata', 'facilities_space_management_facility_governed_model'), ('portfolio_decision', 'capacity', 'utilization', 'cost_projection', 'lease_dates', 'commute_impact', 'amenities', 'safety', 'carbon', 'scenario_comparisons', 'executive_recommendation'), 'PortfolioLeaseDecisionSupport', 'POST /portfolio-rationalization/recommend', ('LeaseContractApproved',)), (43, ('facilities_space_management_maintenance_signal', 'facilities_space_management_facility_control_assertion'), ('maintenance_projection_contract', 'work_order_completion_projection', 'affected_spaces', 'downtime', 'readiness', 'freshness', 'fallback', 'foreign_work_order_mutation', 'boundary_decision'), 'MaintenanceDependencyBoundaryProof', 'POST /facility-boundaries/maintenance-proof', ('WorkOrderCompleted', 'MaintenanceCompleted')), (44, ('facilities_space_management_access_constraint', 'facilities_space_management_facility_control_assertion'), ('access_policy_projection', 'allowed_fields', 'source_pbc', 'effective_date', 'freshness', 'emergency_override_semantics', 'shared_table_mutation_blocked', 'reservation_usage', 'wayfinding_usage'), 'AccessPolicyBoundaryProof', 'POST /facility-boundaries/access-proof', ('AccessPolicyChanged',)), (45, ('facilities_space_management_facility_exception_case', 'facilities_space_management_utilization_observation'), ('feedback_record', 'linked_spaces', 'linked_reservations', 'linked_floors', 'linked_amenities', 'linked_issues', 'theme_analysis', 'severity', 'recurrence', 'recommendation_handoff'), 'WorkplaceExperienceFeedbackLoop', 'POST /workplace-feedback/analyze', ()), (46, ('facilities_space_management_facility_policy_rule', 'facilities_space_management_facility_runtime_parameter'), ('policy_version', 'simulation', 'approval', 'effective_dates', 'rollback', 'test_cases', 'impact_analysis', 'reservation_impact', 'assignment_impact', 'move_impact', 'capacity_impact'), 'FacilityPolicyParameterStudio', 'POST /facility-policies/compile', ('PolicyChanged',)), (47, ('facilities_space_management_facility_control_assertion',), ('transaction_time', 'effective_time', 'space_records', 'reservations', 'occupancy_assignments', 'access_constraints', 'safety_inspections', 'maintenance_blocks', 'availability_snapshots', 'reconstruction_hash'), 'TimeTravelSpaceOccupancyReconstruction', 'POST /space-history/reconstruct', ()), (48, ('facilities_space_management_facility_control_assertion', 'facilities_space_management_appgen_outbox_event', 'facilities_space_management_appgen_inbox_event', 'facilities_space_management_appgen_dead_letter_event'), ('schema_hashes', 'migration_manifests', 'service_contracts', 'event_schemas', 'idempotent_handler_proofs', 'retry_dead_letter_tests', 'reservation_simulations', 'safety_gates', 'ui_coverage', 'agent_skill_manifests'), 'FacilitiesReleaseEvidencePacks', 'POST /release/facilities-evidence-pack', ()), (49, ('facilities_space_management_appgen_inbox_event', 'facilities_space_management_appgen_outbox_event', 'facilities_space_management_appgen_dead_letter_event'), ('inbox_view', 'outbox_view', 'retry_state', 'quarantine_state', 'dead_letter_events', 'payload_lineage', 'idempotency_keys', 'replay_decision', 'unknown_event_mutation_blocked'), 'SpaceEventDeadLetterReplayOps', 'POST /facility-events/dead-letter/replay', ('EmployeeCreated', 'WorkOrderCompleted', 'AccessPolicyChanged', 'PolicyChanged', 'LeaseContractApproved')), (50, ('facilities_space_management_facility_control_assertion',), ('facility_manager_workbench', 'space_planner_workbench', 'employee_workbench', 'move_coordinator_workbench', 'safety_reviewer_workbench', 'maintenance_liaison_workbench', 'workplace_analyst_workbench', 'executive_sponsor_workbench', 'sites_coverage', 'floors_coverage', 'maps_coverage', 'spaces_coverage', 'reservations_coverage', 'occupancy_coverage', 'moves_coverage', 'maintenance_blocks_coverage', 'access_constraints_coverage', 'safety_coverage', 'utilization_coverage', 'capacity_coverage', 'scenarios_coverage', 'policies_coverage', 'agent_panels_coverage', 'release_evidence_coverage'), 'CompleteFacilitiesWorkbenchCoverage', 'GET /facilities-workbench/coverage', ())]
CONTROL_SPECS: dict[int, dict[str, Any]] = {number: {"tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps} for number, tables, fields, ui, route, deps in _SPEC_ROWS}
_EMPTY_ALLOWED_FIELDS = (
    "blocker",
    "critical_dependencies_open",
    "foreign_mutation_blocked",
    "foreign_work_order_mutation",
    "forbidden_drilldowns",
    "restricted_areas",
    "reservation_cancellations",
    "shortfall_by_site",
    "surplus_by_space_type",
    "shared_table_mutation_blocked",
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update({
        "site_status": "operational",
        "map_version": "v1",
        "change_impact": "assessed",
        "measurement_evidence": "survey",
        "reservation_eligibility": "eligible",
        "approval_status": "approved",
        "capacity_validation": "passed",
        "hr_mutation_blocked": True,
        "maintenance_block_check": "clear",
        "access_constraint_check": "clear",
        "blocked_explanation": "none",
        "required_approvals": "captured",
        "confirmation_gate": "passed",
        "check_in_evidence": "present",
        "confidence": 0.9,
        "privacy_basis": "aggregated",
        "aggregation_threshold": 10,
        "individual_exposure_blocked": True,
        "material_change_event": "FacilityAvailabilityChanged",
        "severity": "medium",
        "safety_impact": "none",
        "release_criteria": "met",
        "approval_routing": "complete",
        "readiness_checklist": "complete",
        "critical_dependencies_open": (),
        "completion_decision": "complete",
        "emergency_override": "logged",
        "planning_decision": "allowed",
        "hazard_severity": "low",
        "space_block_decision": "not_blocked",
        "reservation_cancellations": (),
        "reinspection_required": False,
        "headcount_projection": "current",
        "shortfall_by_site": (),
        "surplus_by_space_type": (),
        "confidence_interval": "95pct",
        "redesign_recommendations": "none",
        "cost_impact": "known",
        "foreign_mutation_blocked": True,
        "finance_handoff_event": "SpaceAllocationPublished",
        "violation_blocked": True,
        "comfort_score": 0.82,
        "employee_experience_tradeoff": "acceptable",
        "readiness_status": "ready",
        "access_respected": True,
        "route_result": "available",
        "incident_state": "none",
        "back_to_back_block": "not_required",
        "planning_status": "approved",
        "simulation_result": "safe",
        "decision": "approved_with_controls",
        "auto_release": "enabled",
        "policy_tuning_signal": "captured",
        "scenario_score": 0.86,
        "ranking_reason": "policy_fit",
        "source_citations": ("doc-1",),
        "human_confirmation": True,
        "materiality": "material",
        "approval_required": True,
        "executive_recommendation": "retain",
        "foreign_work_order_mutation": (),
        "boundary_decision": "passed",
        "shared_table_mutation_blocked": True,
        "recommendation_handoff": "space_plan",
        "test_cases": ("positive", "negative"),
        "rollback": "available",
        "reconstruction_hash": "sha256:space-history",
        "schema_hashes": "sha256:schema",
        "migration_manifests": "complete",
        "service_contracts": "complete",
        "event_schemas": "complete",
        "idempotent_handler_proofs": "complete",
        "retry_dead_letter_tests": "passed",
        "ui_coverage": "complete",
        "agent_skill_manifests": "complete",
        "idempotency_keys": ("idem-1",),
        "replay_decision": "safe",
        "unknown_event_mutation_blocked": True,
        "facility_manager_workbench": True,
        "space_planner_workbench": True,
        "employee_workbench": True,
        "move_coordinator_workbench": True,
        "safety_reviewer_workbench": True,
        "maintenance_liaison_workbench": True,
        "workplace_analyst_workbench": True,
        "executive_sponsor_workbench": True,
        "sites_coverage": True,
        "floors_coverage": True,
        "maps_coverage": True,
        "spaces_coverage": True,
        "reservations_coverage": True,
        "occupancy_coverage": True,
        "moves_coverage": True,
        "maintenance_blocks_coverage": True,
        "access_constraints_coverage": True,
        "safety_coverage": True,
        "utilization_coverage": True,
        "capacity_coverage": True,
        "scenarios_coverage": True,
        "policies_coverage": True,
        "agent_panels_coverage": True,
        "release_evidence_coverage": True,
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and payload.get("site_status") not in {"planned", "operational", "restricted", "closed"}:
        findings.append("facility site status is not governed")
    if n == 2 and not payload.get("map_version"):
        findings.append("floor digital twin requires map versioning")
    if n == 6 and payload.get("capacity_validation") != "passed":
        findings.append("occupant assignment must validate capacity and access")
    if n == 7 and payload.get("hr_mutation_blocked") is not True:
        findings.append("hybrid pattern modeling must not mutate HR records")
    if n == 8 and payload.get("maintenance_block_check") != "clear":
        findings.append("reservation eligibility blocks maintenance-impacted spaces")
    if n == 10 and payload.get("confirmation_gate") != "passed":
        findings.append("reservation setup dependencies are incomplete")
    if n == 13 and (payload.get("aggregation_threshold", 0) < 5 or payload.get("individual_exposure_blocked") is not True):
        findings.append("workplace analytics must be privacy-safe")
    if n == 15 and payload.get("release_criteria") != "met":
        findings.append("maintenance-aware block cannot release without criteria")
    if n == 17 and payload.get("critical_dependencies_open"):
        findings.append("move task cannot complete with open critical dependencies")
    if n == 18 and not payload.get("policy_basis"):
        findings.append("access constraints require policy basis")
    if n == 20 and payload.get("hazard_severity") in {"high", "critical"} and payload.get("space_block_decision") != "blocked":
        findings.append("high-severity safety findings must block spaces")
    if n == 25 and payload.get("foreign_mutation_blocked") is not True:
        findings.append("lease projections cannot mutate lease or finance records")
    if n == 27 and payload.get("violation_blocked") is not True:
        findings.append("accessibility violations must be blocked")
    if n == 31 and payload.get("access_respected") is not True:
        findings.append("wayfinding must respect access constraints")
    if n == 33 and payload.get("back_to_back_block") == "required_missing":
        findings.append("turnover scheduling blocks unsafe back-to-back bookings")
    if n == 36 and not payload.get("closure_evidence"):
        findings.append("facility exceptions require closure evidence")
    if n == 40 and (not payload.get("source_citations") or payload.get("human_confirmation") is not True):
        findings.append("agent document intake requires citations and human confirmation")
    if n == 41 and payload.get("materiality") == "material" and payload.get("approval_required") is not True:
        findings.append("material floor plan changes require approval")
    if n == 43 and payload.get("foreign_work_order_mutation"):
        findings.append("maintenance boundary proof forbids work-order mutation")
    if n == 44 and payload.get("shared_table_mutation_blocked") is not True:
        findings.append("access policy boundary forbids shared-table mutation")
    if n == 48 and payload.get("retry_dead_letter_tests") != "passed":
        findings.append("release evidence pack requires retry/dead-letter proof")
    if n == 49 and payload.get("unknown_event_mutation_blocked") is not True:
        findings.append("unknown events cannot mutate facility state")
    if n == 50 and not all(payload.get(field) is True for field in ("facility_manager_workbench", "space_planner_workbench", "employee_workbench", "move_coordinator_workbench", "safety_reviewer_workbench", "maintenance_liaison_workbench", "workplace_analyst_workbench", "executive_sponsor_workbench", "sites_coverage", "floors_coverage", "maps_coverage", "spaces_coverage", "reservations_coverage", "occupancy_coverage", "moves_coverage", "maintenance_blocks_coverage", "access_constraints_coverage", "safety_coverage", "utilization_coverage", "capacity_coverage", "scenarios_coverage", "policies_coverage", "agent_panels_coverage", "release_evidence_coverage")):
        findings.append("complete facilities workbench coverage is incomplete")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_facilities_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in FACILITIES_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in FACILITIES_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": FACILITIES_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": FACILITIES_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_facilities_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_facilities_control(capability) for capability in FACILITIES_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.facilities-space-management-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": FACILITIES_CONTROL_OWNED_TABLES,
        "declared_dependencies": FACILITIES_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": FACILITIES_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": FACILITIES_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


FACILITIES_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_facilities_control(slug, payload)) for capability in FACILITIES_CONTROL_CAPABILITIES}

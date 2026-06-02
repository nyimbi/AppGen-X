"""Executable improve1 controls for the Fleet Mobility Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "fleet_mobility_operations"
EVENT_CONTRACT = "AppGen-X"
FLEET_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
FLEET_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.fleet_mobility_operations.events"
FLEET_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + (
    "fleet_mobility_operations_vehicle_readiness_projection",
    "fleet_mobility_operations_driver_assignment_control",
    "fleet_mobility_operations_dispatch_board_state",
    "fleet_mobility_operations_route_stop_projection",
    "fleet_mobility_operations_telematics_quarantine",
    "fleet_mobility_operations_trip_reconstruction",
    "fleet_mobility_operations_maintenance_horizon",
    "fleet_mobility_operations_incident_command",
    "fleet_mobility_operations_fuel_anomaly_case",
    "fleet_mobility_operations_ev_charging_plan",
    "fleet_mobility_operations_utilization_heatmap",
    "fleet_mobility_operations_geofence_event",
    "fleet_mobility_operations_driver_compliance_card",
    "fleet_mobility_operations_driver_behavior_score",
    "fleet_mobility_operations_exception_sla_clock",
    "fleet_mobility_operations_control_tower_view",
    "fleet_mobility_operations_workshop_plan",
    "fleet_mobility_operations_safety_compliance_case",
    "fleet_mobility_operations_agent_action_preview",
    "fleet_mobility_operations_maintenance_triage_skill",
    "fleet_mobility_operations_assignment_command",
    "fleet_mobility_operations_route_read_model",
    "fleet_mobility_operations_readiness_event_contract",
    "fleet_mobility_operations_route_reprojection_event",
    "fleet_mobility_operations_incident_lifecycle_event",
    "fleet_mobility_operations_device_message_idempotency",
    "fleet_mobility_operations_energy_ledger",
    "fleet_mobility_operations_service_trigger_calibration",
    "fleet_mobility_operations_shift_handoff_log",
    "fleet_mobility_operations_dead_letter_operations",
    "fleet_mobility_operations_route_variance_analytics",
    "fleet_mobility_operations_downtime_forecast",
    "fleet_mobility_operations_counterfactual_dispatch_simulation",
    "fleet_mobility_operations_tenant_depot_policy_boundary",
    "fleet_mobility_operations_override_audit_proof",
    "fleet_mobility_operations_release_evidence_pack",
    "fleet_mobility_operations_configuration_workbench",
    "fleet_mobility_operations_policy_impact_preview",
    "fleet_mobility_operations_kpi_reprioritization",
    "fleet_mobility_operations_schema_extension_registry",
    "fleet_mobility_operations_driver_acknowledgement",
    "fleet_mobility_operations_idle_standby_control",
    "fleet_mobility_operations_maintenance_campaign",
    "fleet_mobility_operations_turnaround_metric",
    "fleet_mobility_operations_incident_root_cause_catalog",
    "fleet_mobility_operations_telematics_freshness",
    "fleet_mobility_operations_fuel_odometer_reconciliation",
    "fleet_mobility_operations_charger_queue_projection",
    "fleet_mobility_operations_carbon_energy_report",
    "fleet_mobility_operations_operational_release_gate",

)))
FLEET_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "FleetMobilityOperationsReadinessBlocked", "FleetMobilityOperationsReadinessRestored",
    "FleetMobilityOperationsRouteReprojected", "FleetMobilityOperationsIncidentEscalated",
    "FleetMobilityOperationsEnergyAnomalyOpened",
)))
FLEET_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in FLEET_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in FLEET_CONTROL_CAPABILITIES}
_SPEC_ROWS: tuple[tuple[int, str, str, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = [(1, 'Vehicle dispatch-readiness ledger', 'vehicle_dispatch_readiness_ledger', ('fleet_mobility_operations_vehicle_readiness_projection',), ('registration_status', 'open_maintenance_count', 'unresolved_safety_events', 'assignment_state', 'fuel_or_soc_threshold', 'telematics_freshness', 'dispatchable_verdict', 'blocked_reason', 'readiness_evidence'), 'VehicleDispatchReadinessLedger', 'POST /fleet-mobility-operations/improve1/vehicle_dispatch_readiness_ledger', ()), (2, 'Assignment overlap and rest-window enforcement', 'assignment_overlap_and_rest_window_enforcement', ('fleet_mobility_operations_driver_assignment_control',), ('driver_id', 'vehicle_id', 'route_id', 'shift_window', 'overlap_check', 'rest_window_hours', 'handoff_acknowledged', 'acceptance_reason', 'refusal_reason'), 'AssignmentOverlapAndRestWindowEnforcement', 'POST /fleet-mobility-operations/improve1/assignment_overlap_and_rest_window_enforcement', ()), (3, 'Dispatch board for live reallocation', 'dispatch_board_for_live_reallocation', ('fleet_mobility_operations_dispatch_board_state',), ('unassigned_vehicles', 'unassigned_drivers', 'route_plan_gaps', 'late_departures', 'reassignment_candidates', 'policy_check', 'operator_action', 'audit_event_id'), 'DispatchBoardForLiveReallocation', 'POST /fleet-mobility-operations/improve1/dispatch_board_for_live_reallocation', ()), (4, 'Stop-level route ETA projection', 'stop_level_route_eta_projection', ('fleet_mobility_operations_route_stop_projection',), ('route_id', 'stop_id', 'planned_arrival', 'projected_arrival', 'dwell_minutes', 'delay_minutes', 'missed_stop_risk', 'completion_confidence', 'latest_telematics_event'), 'StopLevelRouteEtaProjection', 'POST /fleet-mobility-operations/improve1/stop_level_route_eta_projection', ()), (5, 'Telematics quarantine for malformed device traffic', 'telematics_quarantine_for_malformed_device_traffic', ('fleet_mobility_operations_telematics_quarantine',), ('device_id', 'source_timestamp', 'message_hash', 'schema_valid', 'identity_verified', 'timestamp_sanity', 'idempotency_key', 'quarantine_reason', 'dead_letter_eligible'), 'TelematicsQuarantineForMalformedDeviceTraffic', 'POST /fleet-mobility-operations/improve1/telematics_quarantine_for_malformed_device_traffic', ()), (6, 'Trip reconstruction from event streams', 'trip_reconstruction_from_event_streams', ('fleet_mobility_operations_trip_reconstruction',), ('trip_id', 'vehicle_id', 'ignition_window', 'route_deviation', 'idle_segments', 'unscheduled_stops', 'ordered_event_count', 'planned_route_id', 'reconstruction_confidence'), 'TripReconstructionFromEventStreams', 'POST /fleet-mobility-operations/improve1/trip_reconstruction_from_event_streams', ()), (7, 'Maintenance readiness horizon', 'maintenance_readiness_horizon', ('fleet_mobility_operations_maintenance_horizon',), ('vehicle_id', 'due_7_days', 'due_14_days', 'due_30_days', 'odometer_projection', 'engine_hour_projection', 'wear_signal', 'route_commitments', 'withhold_from_dispatch'), 'MaintenanceReadinessHorizon', 'POST /fleet-mobility-operations/improve1/maintenance_readiness_horizon', ()), (8, 'Roadside breakdown incident command view', 'roadside_breakdown_incident_command_view', ('fleet_mobility_operations_incident_command',), ('incident_id', 'incident_location', 'driver_status', 'towing_need', 'replacement_vehicle_action', 'rerouting_action', 'service_return_criteria', 'incident_state', 'closure_evidence'), 'RoadsideBreakdownIncidentCommandView', 'POST /fleet-mobility-operations/improve1/roadside_breakdown_incident_command_view', ()), (9, 'Fuel fraud and abnormal burn detection', 'fuel_fraud_and_abnormal_burn_detection', ('fleet_mobility_operations_fuel_anomaly_case',), ('transaction_id', 'vehicle_id', 'fuel_card_id', 'odometer_delta', 'idle_time', 'route_distance', 'approved_geofence', 'duplicate_fill_check', 'anomaly_reason'), 'FuelFraudAndAbnormalBurnDetection', 'POST /fleet-mobility-operations/improve1/fuel_fraud_and_abnormal_burn_detection', ()), (10, 'EV charging readiness planner', 'ev_charging_readiness_planner', ('fleet_mobility_operations_ev_charging_plan',), ('vehicle_id', 'state_of_charge', 'charger_availability', 'charging_window_fit', 'route_energy_requirement', 'minimum_arrival_soc', 'dispatch_decision', 'charger_queue_position', 'energy_risk_reason'), 'EvChargingReadinessPlanner', 'POST /fleet-mobility-operations/improve1/ev_charging_readiness_planner', ()), (11, 'Utilization heatmap by depot, class, and shift', 'utilization_heatmap_by_depot_class_and_shift', ('fleet_mobility_operations_utilization_heatmap',), ('depot', 'vehicle_class', 'shift_window', 'active_hours', 'idle_hours', 'route_occupancy', 'assignment_gap_hours', 'maintenance_downtime', 'utilization_score'), 'UtilizationHeatmapByDepotClassAndShift', 'POST /fleet-mobility-operations/improve1/utilization_heatmap_by_depot_class_and_shift', ()), (12, 'Geofence arrival, dwell, and exit controls', 'geofence_arrival_dwell_and_exit_controls', ('fleet_mobility_operations_geofence_event',), ('geofence_id', 'geofence_type', 'arrival_time', 'dwell_minutes', 'exit_time', 'authorized_visit', 'route_deviation', 'threshold_breach', 'derived_event_id'), 'GeofenceArrivalDwellAndExitControls', 'POST /fleet-mobility-operations/improve1/geofence_arrival_dwell_and_exit_controls', ()), (13, 'Driver license, certification, and medical expiry controls', 'driver_license_certification_and_medical_expiry_controls', ('fleet_mobility_operations_driver_compliance_card',), ('driver_id', 'license_class', 'endorsements', 'medical_valid_until', 'training_complete', 'jurisdiction', 'credential_freshness', 'assignment_allowed', 'block_reason'), 'DriverLicenseCertificationAndMedicalExpiryControls', 'POST /fleet-mobility-operations/improve1/driver_license_certification_and_medical_expiry_controls', ('PolicyChanged',)), (14, 'Driver behavior scoring from telematics', 'driver_behavior_scoring_from_telematics', ('fleet_mobility_operations_driver_behavior_score',), ('driver_id', 'speeding_events', 'harsh_braking_events', 'rapid_acceleration_events', 'seat_belt_gaps', 'idle_excess_minutes', 'score', 'coaching_queue', 'explainable_weights'), 'DriverBehaviorScoringFromTelematics', 'POST /fleet-mobility-operations/improve1/driver_behavior_scoring_from_telematics', ()), (15, 'Dispatch exception SLA engine', 'dispatch_exception_sla_engine', ('fleet_mobility_operations_exception_sla_clock',), ('exception_id', 'exception_type', 'opened_at', 'sla_deadline', 'pause_reason', 'resume_time', 'aging_bucket', 'escalation_state', 'breach_reason'), 'DispatchExceptionSlaEngine', 'POST /fleet-mobility-operations/improve1/dispatch_exception_sla_engine', ()), (16, 'Fleet control tower workbench', 'fleet_control_tower_workbench', ('fleet_mobility_operations_control_tower_view',), ('dispatch_board', 'live_route_map', 'blocked_asset_queue', 'telematics_freshness', 'high_risk_exception_panel', 'permission_actions', 'route_risk_panel', 'asset_status_panel', 'operator_filter'), 'FleetControlTowerWorkbench', 'POST /fleet-mobility-operations/improve1/fleet_control_tower_workbench', ()), (17, 'Workshop planner workbench', 'workshop_planner_workbench', ('fleet_mobility_operations_workshop_plan',), ('maintenance_order_id', 'due_service', 'parts_readiness', 'bay_capacity', 'replacement_vehicle_need', 'return_to_road_decision', 'open_defects', 'workshop_queue', 'capacity_conflict'), 'WorkshopPlannerWorkbench', 'POST /fleet-mobility-operations/improve1/workshop_planner_workbench', ()), (18, 'Safety and compliance workbench', 'safety_and_compliance_workbench', ('fleet_mobility_operations_safety_compliance_case',), ('case_id', 'incident_queue', 'driver_credential_gap', 'policy_breach', 'coaching_action', 'audit_evidence_export', 'investigation_state', 'source_record_id', 'closure_reason'), 'SafetyAndComplianceWorkbench', 'POST /fleet-mobility-operations/improve1/safety_and_compliance_workbench', ()), (19, 'Dispatch replanning agent skill', 'dispatch_replanning_agent_skill', ('fleet_mobility_operations_agent_action_preview',), ('skill_name', 'breakdown_context', 'replacement_vehicle_options', 'alternative_driver_options', 'revised_route_priority', 'preview_only', 'approval_required', 'audit_trace', 'user_confirmation'), 'DispatchReplanningAgentSkill', 'POST /fleet-mobility-operations/improve1/dispatch_replanning_agent_skill', ('OperationalKpiChanged',)), (20, 'Maintenance triage agent skill', 'maintenance_triage_agent_skill', ('fleet_mobility_operations_maintenance_triage_skill',), ('fault_evidence', 'service_history', 'telematics_alerts', 'repair_sequence', 'repeat_failure_signal', 'dispatch_removal_recommendation', 'source_citations', 'approval_gate', 'triage_summary'), 'MaintenanceTriageAgentSkill', 'POST /fleet-mobility-operations/improve1/maintenance_triage_agent_skill', ('OperationalKpiChanged',)), (21, 'Assignment command boundary expansion', 'assignment_command_boundary_expansion', ('fleet_mobility_operations_assignment_command',), ('command_id', 'command_type', 'validation_only', 'driver_acknowledgement', 'reassignment_reason', 'cancellation_reason', 'closeout_state', 'idempotency_key', 'workbench_action'), 'AssignmentCommandBoundaryExpansion', 'POST /fleet-mobility-operations/improve1/assignment_command_boundary_expansion', ()), (22, 'Query boundary for route and telematics read models', 'query_boundary_for_route_and_telematics_read_models', ('fleet_mobility_operations_route_read_model',), ('read_model_type', 'route_progress', 'telematics_freshness', 'geofence_activity', 'utilization_summary', 'maintenance_readiness', 'freshness_metadata', 'projection_source', 'api_response_shape'), 'QueryBoundaryForRouteAndTelematicsReadModels', 'POST /fleet-mobility-operations/improve1/query_boundary_for_route_and_telematics_read_models', ()), (23, 'Vehicle readiness change event contract', 'vehicle_readiness_change_event_contract', ('fleet_mobility_operations_readiness_event_contract',), ('vehicle_id', 'readiness_state', 'previous_state', 'transition_reason', 'outbox_event_type', 'event_payload_version', 'subscriber_projection', 'event_topic', 'integrity_hash'), 'VehicleReadinessChangeEventContract', 'POST /fleet-mobility-operations/improve1/vehicle_readiness_change_event_contract', ('FleetMobilityOperationsUpdated',)), (24, 'Route reprojection event contract', 'route_reprojection_event_contract', ('fleet_mobility_operations_route_reprojection_event',), ('route_id', 'reprojection_reason', 'old_eta_window', 'new_eta_window', 'geofence_deviation', 'maintenance_withdrawal', 'downstream_notification', 'materiality_threshold', 'event_payload_version'), 'RouteReprojectionEventContract', 'POST /fleet-mobility-operations/improve1/route_reprojection_event_contract', ('FleetMobilityOperationsUpdated',)), (25, 'Incident lifecycle event contract', 'incident_lifecycle_event_contract', ('fleet_mobility_operations_incident_lifecycle_event',), ('incident_id', 'lifecycle_state', 'actor_id', 'asset_reference', 'route_reference', 'evidence_references', 'event_order', 'replay_sequence', 'closure_link'), 'IncidentLifecycleEventContract', 'POST /fleet-mobility-operations/improve1/incident_lifecycle_event_contract', ('AuditEventSealed',)), (26, 'Idempotent device-message handling', 'idempotent_device_message_handling', ('fleet_mobility_operations_device_message_idempotency',), ('device_id', 'source_timestamp', 'event_hash', 'receive_window', 'duplicate_detected', 'stored_effect_count', 'conflict_reason', 'dead_letter_reason', 'projection_stability'), 'IdempotentDeviceMessageHandling', 'POST /fleet-mobility-operations/improve1/idempotent_device_message_handling', ()), (27, 'Unified fuel and charging ledger', 'unified_fuel_and_charging_ledger', ('fleet_mobility_operations_energy_ledger',), ('energy_session_id', 'energy_type', 'liquid_units', 'charging_kwh', 'charger_source', 'charging_loss', 'normalized_cost', 'cost_per_kilometer', 'mixed_fleet_view'), 'UnifiedFuelAndChargingLedger', 'POST /fleet-mobility-operations/improve1/unified_fuel_and_charging_ledger', ()), (28, 'Odometer and engine-hour service trigger calibration', 'odometer_and_engine_hour_service_trigger_calibration', ('fleet_mobility_operations_service_trigger_calibration',), ('vehicle_id', 'manual_odometer', 'telematics_odometer', 'engine_hour_projection', 'drift_detected', 'trigger_source', 'adjusted_due_date', 'calibration_reason', 'service_alert'), 'OdometerAndEngineHourServiceTriggerCalibration', 'POST /fleet-mobility-operations/improve1/odometer_and_engine_hour_service_trigger_calibration', ()), (29, 'Shift handoff log for dispatch continuity', 'shift_handoff_log_for_dispatch_continuity', ('fleet_mobility_operations_shift_handoff_log',), ('shift_id', 'handoff_owner', 'blocked_assets', 'open_incidents', 'at_risk_routes', 'pending_reassignments', 'telematics_gaps', 'audit_history', 'receiver_acknowledgement'), 'ShiftHandoffLogForDispatchContinuity', 'POST /fleet-mobility-operations/improve1/shift_handoff_log_for_dispatch_continuity', ()), (30, 'Dead-letter operations for telematics and fleet events', 'dead_letter_operations_for_telematics_and_fleet_events', ('fleet_mobility_operations_dead_letter_operations',), ('message_id', 'message_type', 'root_cause_tag', 'replay_eligible', 'suppression_control', 'operator_note', 'retry_attempts', 'poison_message', 'replay_result'), 'DeadLetterOperationsForTelematicsAndFleetEvents', 'POST /fleet-mobility-operations/improve1/dead_letter_operations_for_telematics_and_fleet_events', ()), (31, 'Route-plan versus actual variance analytics', 'route_plan_versus_actual_variance_analytics', ('fleet_mobility_operations_route_variance_analytics',), ('route_id', 'late_departure_minutes', 'missed_stops', 'unscheduled_dwell', 'excess_distance', 'geofence_detours', 'completion_reliability', 'dispatcher_id', 'route_type'), 'RoutePlanVersusActualVarianceAnalytics', 'POST /fleet-mobility-operations/improve1/route_plan_versus_actual_variance_analytics', ()), (32, 'Vehicle downtime and replacement-cost forecasting', 'vehicle_downtime_and_replacement_cost_forecasting', ('fleet_mobility_operations_downtime_forecast',), ('vehicle_id', 'maintenance_risk', 'incident_frequency', 'utilization_intensity', 'telematics_stress', 'downtime_probability', 'replacement_dispatch_cost', 'explainable_factors', 'forecast_horizon'), 'VehicleDowntimeAndReplacementCostForecasting', 'POST /fleet-mobility-operations/improve1/vehicle_downtime_and_replacement_cost_forecasting', ()), (33, 'Counterfactual dispatch simulation', 'counterfactual_dispatch_simulation', ('fleet_mobility_operations_counterfactual_dispatch_simulation',), ('scenario_id', 'disruption_type', 'driver_absence', 'depot_closure', 'vehicle_breakdown', 'charger_outage', 'coverage_effect', 'utilization_effect', 'live_mutation_blocked'), 'CounterfactualDispatchSimulation', 'POST /fleet-mobility-operations/improve1/counterfactual_dispatch_simulation', ()), (34, 'Multi-tenant depot and policy isolation', 'multi_tenant_depot_and_policy_isolation', ('fleet_mobility_operations_tenant_depot_policy_boundary',), ('tenant_id', 'depot_scope', 'vehicle_pool_scope', 'driver_scope', 'device_scope', 'workbench_filter', 'policy_rule_id', 'cross_tenant_access_blocked', 'evidence_scope'), 'MultiTenantDepotAndPolicyIsolation', 'POST /fleet-mobility-operations/improve1/multi_tenant_depot_and_policy_isolation', ()), (35, 'Override reason capture with audit proofs', 'override_reason_capture_with_audit_proofs', ('fleet_mobility_operations_override_audit_proof',), ('override_id', 'blocked_object_type', 'structured_reason', 'supporting_evidence', 'approver_identity', 'cryptographic_proof_link', 'audit_event_id', 'force_through_allowed', 'proof_verified'), 'OverrideReasonCaptureWithAuditProofs', 'POST /fleet-mobility-operations/improve1/override_reason_capture_with_audit_proofs', ('AuditEventSealed',)), (36, 'Release evidence pack for fleet scenarios', 'release_evidence_pack_for_fleet_scenarios', ('fleet_mobility_operations_release_evidence_pack',), ('scenario_id', 'dispatch_readiness', 'telematics_projection', 'route_replanning', 'maintenance_blocking', 'compliance_rejection', 'fuel_anomaly_detection', 'incident_closure', 'release_candidate'), 'ReleaseEvidencePackForFleetScenarios', 'POST /fleet-mobility-operations/improve1/release_evidence_pack_for_fleet_scenarios', ()), (37, 'Configuration workbench for geofences, thresholds, and depot calendars', 'configuration_workbench_for_geofences_thresholds_and_depot_calendars', ('fleet_mobility_operations_configuration_workbench',), ('geofence_definition', 'telematics_staleness_threshold', 'fuel_anomaly_threshold', 'rest_window_rule', 'depot_calendar', 'charging_readiness_limit', 'approval_history', 'runtime_effective_at', 'validation_result'), 'ConfigurationWorkbenchForGeofencesThresholdsAndDepotCalendars', 'POST /fleet-mobility-operations/improve1/configuration_workbench_for_geofences_thresholds_and_depot_calendars', ()), (38, 'Policy-change impact preview', 'policy_change_impact_preview', ('fleet_mobility_operations_policy_impact_preview',), ('policy_event_id', 'affected_vehicles', 'affected_assignments', 'affected_routes', 'affected_maintenance_plans', 'affected_incidents', 'preview_before_enforcement', 'object_grouping', 'enforcement_decision'), 'PolicyChangeImpactPreview', 'POST /fleet-mobility-operations/improve1/policy_change_impact_preview', ('PolicyChanged',)), (39, 'Operational KPI-driven reprioritization', 'operational_kpi_driven_reprioritization', ('fleet_mobility_operations_kpi_reprioritization',), ('kpi_event_id', 'on_time_departure_trend', 'downtime_trend', 'telematics_lag_trend', 'safety_exception_trend', 'queue_before', 'queue_after', 'rationale', 'priority_change'), 'OperationalKpiDrivenReprioritization', 'POST /fleet-mobility-operations/improve1/operational_kpi_driven_reprioritization', ('OperationalKpiChanged',)), (40, 'Governed schema extension registry for fleet metadata', 'governed_schema_extension_registry_for_fleet_metadata', ('fleet_mobility_operations_schema_extension_registry',), ('extension_id', 'target_table', 'custom_field_name', 'validation_rule', 'ui_rendering_rule', 'event_compatibility_check', 'schema_version', 'approval_state', 'zero_downtime_safe'), 'GovernedSchemaExtensionRegistryForFleetMetadata', 'POST /fleet-mobility-operations/improve1/governed_schema_extension_registry_for_fleet_metadata', ()), (41, 'Driver acknowledgement and exception handback', 'driver_acknowledgement_and_exception_handback', ('fleet_mobility_operations_driver_acknowledgement',), ('assignment_id', 'ack_state', 'decline_reason', 'clarification_request', 'supervisor_queue', 'replan_trigger', 'ack_deadline', 'driver_comment', 'reassignment_opened'), 'DriverAcknowledgementAndExceptionHandback', 'POST /fleet-mobility-operations/improve1/driver_acknowledgement_and_exception_handback', ()), (42, 'Idle-time and standby utilization controls', 'idle_time_and_standby_utilization_controls', ('fleet_mobility_operations_idle_standby_control',), ('vehicle_id', 'depot', 'route_family', 'idle_minutes', 'standby_minutes', 'engine_on_dwell', 'exception_threshold', 'dispatcher_action', 'idle_ratio'), 'IdleTimeAndStandbyUtilizationControls', 'POST /fleet-mobility-operations/improve1/idle_time_and_standby_utilization_controls', ()), (43, 'Seasonal maintenance campaign planning', 'seasonal_maintenance_campaign_planning', ('fleet_mobility_operations_maintenance_campaign',), ('campaign_id', 'service_theme', 'grouped_service_window', 'reserved_bay_capacity', 'availability_impact', 'assignment_collision_check', 'vehicle_population', 'seasonal_risk', 'campaign_state'), 'SeasonalMaintenanceCampaignPlanning', 'POST /fleet-mobility-operations/improve1/seasonal_maintenance_campaign_planning', ()), (44, 'Depot arrival-to-dispatch turnaround metric', 'depot_arrival_to_dispatch_turnaround_metric', ('fleet_mobility_operations_turnaround_metric',), ('vehicle_id', 'depot_arrival_time', 'dispatch_ready_time', 'fueling_stage_minutes', 'inspection_stage_minutes', 'maintenance_stage_minutes', 'documentation_stage_minutes', 'assignment_prep_minutes', 'slowest_stage'), 'DepotArrivalToDispatchTurnaroundMetric', 'POST /fleet-mobility-operations/improve1/depot_arrival_to_dispatch_turnaround_metric', ()), (45, 'Incident root-cause catalog and repeat-failure detection', 'incident_root_cause_catalog_and_repeat_failure_detection', ('fleet_mobility_operations_incident_root_cause_catalog',), ('root_cause_id', 'incident_id', 'corrective_action', 'repeat_failure_group', 'vehicle_cluster', 'driver_cluster', 'depot_cluster', 'route_family_cluster', 'policy_feedback'), 'IncidentRootCauseCatalogAndRepeatFailureDetection', 'POST /fleet-mobility-operations/improve1/incident_root_cause_catalog_and_repeat_failure_detection', ()), (46, 'Offline telematics resilience and freshness warnings', 'offline_telematics_resilience_and_freshness_warnings', ('fleet_mobility_operations_telematics_freshness',), ('device_id', 'heartbeat_age_minutes', 'delayed_upload_window', 'last_known_position_age', 'stationary_inferred', 'disconnect_state', 'dispatch_trust_level', 'freshness_warning', 'block_dispatch'), 'OfflineTelematicsResilienceAndFreshnessWarnings', 'POST /fleet-mobility-operations/improve1/offline_telematics_resilience_and_freshness_warnings', ()), (47, 'Fuel-card versus odometer reconciliation workflow', 'fuel_card_versus_odometer_reconciliation_workflow', ('fleet_mobility_operations_fuel_odometer_reconciliation',), ('transaction_id', 'entered_odometer', 'telematics_odometer', 'route_distance', 'mismatch_amount', 'investigation_queue', 'operator_commentary', 'resolution_state', 'manipulation_suspected'), 'FuelCardVersusOdometerReconciliationWorkflow', 'POST /fleet-mobility-operations/improve1/fuel_card_versus_odometer_reconciliation_workflow', ()), (48, 'Charger occupancy and queue projection', 'charger_occupancy_and_queue_projection', ('fleet_mobility_operations_charger_queue_projection',), ('charging_site_id', 'charger_id', 'occupancy_state', 'expected_wait_minutes', 'session_duration_minutes', 'route_departure_commitment', 'asset_swap_option', 'assignment_delay_risk', 'contention_decision'), 'ChargerOccupancyAndQueueProjection', 'POST /fleet-mobility-operations/improve1/charger_occupancy_and_queue_projection', ()), (49, 'Carbon and energy intensity reporting', 'carbon_and_energy_intensity_reporting', ('fleet_mobility_operations_carbon_energy_report',), ('route_id', 'fuel_burn', 'charging_mix', 'idle_emissions', 'route_energy_intensity', 'depot_filter', 'vehicle_class_filter', 'sustainability_tradeoff', 'energy_profile_change'), 'CarbonAndEnergyIntensityReporting', 'POST /fleet-mobility-operations/improve1/carbon_and_energy_intensity_reporting', ('OperationalKpiChanged',)), (50, 'Release gate for operational proof, not only build proof', 'release_gate_for_operational_proof_not_only_build_proof', ('fleet_mobility_operations_operational_release_gate',), ('vehicle_readiness_proof', 'assignment_validation_proof', 'telematics_projection_proof', 'route_variance_proof', 'maintenance_blocking_proof', 'compliance_rejection_proof', 'incident_handling_proof', 'energy_reconciliation_proof', 'event_integrity_proof'), 'ReleaseGateForOperationalProofNotOnlyBuildProof', 'POST /fleet-mobility-operations/improve1/release_gate_for_operational_proof_not_only_build_proof', ())]
CONTROL_SPECS: dict[int, dict[str, Any]] = {number: {"title": title, "slug": slug, "tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps} for number, title, slug, tables, fields, ui, route, deps in _SPEC_ROWS}
_EMPTY_ALLOWED_FIELDS = ("blocked_reason", "refusal_reason", "quarantine_reason", "anomaly_reason", "energy_risk_reason", "block_reason", "breach_reason", "capacity_conflict", "decline_reason", "clarification_request", "operator_commentary")


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
        "registration_status": "valid", "open_maintenance_count": 0, "unresolved_safety_events": 0,
        "assignment_state": "unassigned", "fuel_or_soc_threshold": "met", "telematics_freshness": "fresh",
        "dispatchable_verdict": "ready", "overlap_check": "clear", "rest_window_hours": 12,
        "handoff_acknowledged": True, "policy_check": "passed", "audit_event_id": "audit-fleet-1",
        "projected_arrival": "on_time", "missed_stop_risk": "low", "completion_confidence": 0.93,
        "schema_valid": True, "identity_verified": True, "timestamp_sanity": "within_window",
        "quarantine_reason": "", "dead_letter_eligible": False, "ordered_event_count": 9,
        "reconstruction_confidence": 0.91, "withhold_from_dispatch": False, "incident_state": "contained",
        "closure_evidence": "captured", "approved_geofence": True, "duplicate_fill_check": "unique",
        "anomaly_reason": "", "state_of_charge": 82, "charger_availability": "available",
        "charging_window_fit": True, "minimum_arrival_soc": 20, "dispatch_decision": "allow",
        "utilization_score": 0.78, "authorized_visit": True, "threshold_breach": False,
        "medical_valid_until": "2027-12-31", "training_complete": True, "assignment_allowed": True,
        "coaching_queue": "reviewed", "explainable_weights": {"speeding": 0.35, "braking": 0.25},
        "pause_reason": "none", "escalation_state": "green", "permission_actions": "role_checked",
        "return_to_road_decision": "cleared", "investigation_state": "closed", "preview_only": True,
        "approval_required": True, "user_confirmation": True, "source_citations": ("service-history", "telematics-alert"),
        "approval_gate": True, "validation_only": True, "idempotency_key": "fleet-idem-1",
        "freshness_metadata": "included", "api_response_shape": "typed", "outbox_event_type": "FleetMobilityOperationsReadinessBlocked",
        "event_topic": FLEET_CONTROL_REQUIRED_EVENT_TOPIC, "integrity_hash": "sha256:fleet", "event_payload_version": "v1",
        "materiality_threshold": "met", "replay_sequence": 1, "stored_effect_count": 1,
        "projection_stability": "stable", "normalized_cost": 12.4, "mixed_fleet_view": "available",
        "drift_detected": False, "adjusted_due_date": "2027-01-31", "receiver_acknowledgement": True,
        "replay_eligible": True, "poison_message": False, "replay_result": "succeeded",
        "completion_reliability": 0.96, "downtime_probability": 0.18, "replacement_dispatch_cost": 250.0,
        "live_mutation_blocked": True, "cross_tenant_access_blocked": True, "proof_verified": True,
        "force_through_allowed": False, "release_candidate": "rc-fleet", "validation_result": "passed",
        "preview_before_enforcement": True, "enforcement_decision": "operator_review", "priority_change": "explained",
        "zero_downtime_safe": True, "reassignment_opened": True, "idle_ratio": 0.12,
        "assignment_collision_check": "clear", "dispatch_ready_time": "2026-05-30T09:00:00Z",
        "slowest_stage": "inspection", "corrective_action": "scheduled", "policy_feedback": "opened",
        "dispatch_trust_level": "trusted", "freshness_warning": "none", "block_dispatch": False,
        "manipulation_suspected": False, "resolution_state": "resolved", "assignment_delay_risk": "low",
        "contention_decision": "charge_now", "route_energy_intensity": 0.42,
        "sustainability_tradeoff": "documented", "energy_profile_change": "reduced_idle",
        "vehicle_readiness_proof": True, "assignment_validation_proof": True, "telematics_projection_proof": True,
        "route_variance_proof": True, "maintenance_blocking_proof": True, "compliance_rejection_proof": True,
        "incident_handling_proof": True, "energy_reconciliation_proof": True, "event_integrity_proof": True,
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and (payload.get("dispatchable_verdict") != "ready" or payload.get("open_maintenance_count", 0) or payload.get("unresolved_safety_events", 0)):
        findings.append("vehicle readiness ledger blocks dispatch until maintenance and safety are clear")
    if n == 2 and (payload.get("overlap_check") != "clear" or payload.get("rest_window_hours", 0) < 8 or payload.get("handoff_acknowledged") is not True):
        findings.append("assignment requires no overlap, minimum rest, and handoff acknowledgement")
    if n == 5 and (payload.get("schema_valid") is not True or payload.get("identity_verified") is not True or payload.get("timestamp_sanity") != "within_window"):
        findings.append("telematics ingestion must quarantine malformed, unknown, or impossible messages")
    if n == 7 and payload.get("withhold_from_dispatch") is True:
        findings.append("maintenance horizon withholds high-risk vehicle from new assignments")
    if n == 9 and (payload.get("approved_geofence") is not True or payload.get("duplicate_fill_check") != "unique"):
        findings.append("fuel transaction failed fraud and geofence reconciliation")
    if n == 10 and (payload.get("charging_window_fit") is not True or payload.get("state_of_charge", 0) < payload.get("minimum_arrival_soc", 100)):
        findings.append("EV dispatch requires sufficient charge and feasible charging window")
    if n == 13 and (payload.get("training_complete") is not True or payload.get("assignment_allowed") is not True or payload.get("medical_valid_until", "") < "2026-05-30"):
        findings.append("driver credentials are not current for dispatch")
    if n == 19 and (payload.get("preview_only") is not True or payload.get("approval_required") is not True or payload.get("user_confirmation") is not True):
        findings.append("dispatch replanning agent must stay preview-only until confirmed")
    if n == 20 and (not payload.get("source_citations") or payload.get("approval_gate") is not True):
        findings.append("maintenance triage agent requires cited evidence and approval gate")
    if n == 26 and payload.get("stored_effect_count") != 1:
        findings.append("duplicate device messages must produce exactly one stored effect")
    if n == 30 and payload.get("poison_message") is True and payload.get("replay_eligible") is True:
        findings.append("poison dead-letter messages cannot be replay eligible")
    if n == 33 and payload.get("live_mutation_blocked") is not True:
        findings.append("counterfactual dispatch simulation cannot mutate live plans")
    if n == 34 and payload.get("cross_tenant_access_blocked") is not True:
        findings.append("tenant depot and policy boundary must block cross-tenant access")
    if n == 35 and (not payload.get("structured_reason") or not payload.get("supporting_evidence") or payload.get("proof_verified") is not True):
        findings.append("manual override requires reason, evidence, approver, and verified audit proof")
    if n == 40 and payload.get("zero_downtime_safe") is not True:
        findings.append("fleet schema extension must be zero-downtime safe")
    if n == 46 and (payload.get("dispatch_trust_level") != "trusted" or payload.get("block_dispatch") is True):
        findings.append("stale telematics cannot be trusted for dispatch")
    if n == 48 and payload.get("assignment_delay_risk") == "high" and payload.get("contention_decision") not in ("swap_asset", "delay_assignment"):
        findings.append("charger queue contention requires asset swap or assignment delay")
    if n == 50 and not all(payload.get(field) is True for field in ("vehicle_readiness_proof", "assignment_validation_proof", "telematics_projection_proof", "route_variance_proof", "maintenance_blocking_proof", "compliance_rejection_proof", "incident_handling_proof", "energy_reconciliation_proof", "event_integrity_proof")):
        findings.append("operational release gate requires every fleet scenario proof")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_fleet_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in FLEET_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in FLEET_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"], "required_fields": spec["fields"],
        "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT, "required_event_topic": FLEET_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": FLEET_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"], "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_fleet_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_fleet_control(capability) for capability in FLEET_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.fleet-mobility-operations-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": FLEET_CONTROL_OWNED_TABLES, "declared_dependencies": FLEET_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": FLEET_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": FLEET_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


FLEET_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_fleet_control(slug, payload)) for capability in FLEET_CONTROL_CAPABILITIES}

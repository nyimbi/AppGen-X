"""Executable improve1 controls for the Mining Safety Permits PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "mining_safety_permits"
EVENT_CONTRACT = "AppGen-X"
MINING_SAFETY_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
MINING_SAFETY_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.mining_safety_permits.events"
_BASE_OWNED_TABLES = (
    "mining_safety_permits_mine_permit",
    "mining_safety_permits_shift_roster",
    "mining_safety_permits_blast_plan",
    "mining_safety_permits_safety_inspection",
    "mining_safety_permits_incident_report",
    "mining_safety_permits_regulatory_submission",
    "mining_safety_permits_control_action",
    "mining_safety_permits_policy_rule",
    "mining_safety_permits_runtime_parameter",
    "mining_safety_permits_schema_extension",
    "mining_safety_permits_control_assertion",
    "mining_safety_permits_governed_model",
    "mining_safety_permits_appgen_outbox_event",
    "mining_safety_permits_appgen_inbox_event",
    "mining_safety_permits_appgen_dead_letter_event",
)
MINING_SAFETY_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"mining_safety_permits_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
MINING_SAFETY_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys((
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "MineAreaStatusChanged",
    "VentilationStatusChanged",
    "GeotechHazardChanged",
    "WorkerCompetencyChanged",
    "RosterFatigueChanged",
    "AssetIsolationChanged",
    "RegulatoryRuleChanged",
)))
MINING_SAFETY_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in MINING_SAFETY_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in MINING_SAFETY_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "site_id", "permit_id", "shift_id", "area_id", "policy_version", "actor_id", "audit_trail", "evidence_references")
_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: 'canonical_permit_to_work_register_verified',
    2: 'permit_lifecycle_with_mining_specific_hold_points_verified',
    3: 'isolation_and_lockout_verification_verified',
    4: 'isolation_boundary_change_control_verified',
    5: 'confined_space_inventory_and_classification_verified',
    6: 'gas_testing_sequence_and_validity_logic_verified',
    7: 'ventilation_and_atmospheric_dependency_checks_verified',
    8: 'ground_control_pre_start_assessment_verified',
    9: 'ground_support_defect_escalation_verified',
    10: 'explosives_permit_prerequisites_verified',
    11: 'blast_clearance_and_re_entry_control_verified',
    12: 'simultaneous_operations_conflict_detection_verified',
    13: 'shift_handover_permit_continuity_verified',
    14: 'crew_competency_and_authorization_checks_verified',
    15: 'contractor_verification_for_high_risk_tasks_verified',
    16: 'fatigue_fit_for_work_and_roster_exceptions_verified',
    17: 'hazard_control_library_aligned_to_mining_work_verified',
    18: 'critical_control_verification_before_work_starts_verified',
    19: 'water_ingress_and_inundation_risk_checks_verified',
    20: 'mobile_equipment_interaction_controls_verified',
    21: 'incident_precursor_and_near_miss_capture_verified',
    22: 'incident_prevention_feedback_loop_verified',
    23: 'high_potential_event_escalation_workflow_verified',
    24: 'regulatory_evidence_pack_assembly_verified',
    25: 'jurisdiction_and_site_rule_overlay_support_verified',
    26: 'workbench_area_control_board_verified',
    27: 'permit_detail_view_optimized_for_field_decision_making_verified',
    28: 'assistant_skill_for_permit_drafting_from_site_language_verified',
    29: 'assistant_skill_for_incident_and_handover_summarization_verified',
    30: 'assistant_refusal_and_escalation_rules_for_unsafe_requests_verified',
    31: 'event_model_expanded_to_domain_milestones_verified',
    32: 'event_sourced_reconstruction_of_safety_decisions_verified',
    33: 'operational_anomaly_detection_for_permit_misuse_verified',
    34: 'continuous_control_testing_of_safety_rules_verified',
    35: 'policy_rule_workbench_for_safety_governance_verified',
    36: 'runtime_parameter_controls_for_operational_thresholds_verified',
    37: 'offline_capable_field_capture_for_inspections_and_gas_tests_verified',
    38: 'attachment_and_evidence_provenance_handling_verified',
    39: 'rescue_readiness_checks_for_confined_space_and_high_risk_work_verified',
    40: 'stop_work_authority_and_rapid_suspension_controls_verified',
    41: 'cross_shift_analytics_for_recurring_hazards_verified',
    42: 'scenario_simulation_for_permit_and_blasting_decisions_verified',
    43: 'dead_letter_and_retry_handling_for_safety_events_verified',
    44: 'multi_tenant_and_site_isolation_of_safety_data_verified',
    45: 'competency_driven_approval_routing_verified',
    46: 'formal_release_evidence_for_safety_critical_changes_verified',
    47: 'safety_focused_contract_and_integration_tests_verified',
    48: 'audit_proof_chain_for_evidence_integrity_verified',
    49: 'domain_training_sandbox_and_seeded_walkthroughs_verified',
    50: 'operational_readiness_review_before_go_live_verified',
}
_DOMAIN_FIELDS: dict[int, tuple[str, ...]] = {
    1: ('permit_id', 'permit_class', 'work_area', 'start_window', 'expiry_window', 'simops_flags', 'issuing_authority', 'performing_crew', 'affected_assets', 'mandatory_control_bundle'),
    2: ('lifecycle_state', 'transition_reason', 'actor_role', 'review_state', 'suspension_reason', 'extension_window', 'closure_verification', 'revalidation_required'),
    3: ('isolation_id', 'energy_source_type', 'isolation_point', 'lock_id', 'tag_id', 'applied_by_role', 'verified_by_role', 'zero_energy_confirmed'),
    4: ('boundary_revision_id', 'diagram_version', 'added_lock_points', 'removed_lock_points', 'change_reason', 'issuer_reaccepted', 'field_supervisor_reaccepted'),
    5: ('confined_space_id', 'space_type', 'dimensions', 'access_points', 'ventilation_arrangement', 'engulfment_hazard', 'adjacent_energy_hazards', 'rescue_method', 'standby_requirement'),
    6: ('gas_test_id', 'instrument_id', 'bump_test_status', 'tester_competency', 'reading_timestamp', 'gases_measured', 'permissible_limits', 'retest_interval', 'invalidation_trigger'),
    7: ('ventilation_circuit_id', 'working_area', 'primary_airflow', 'secondary_airflow', 'critical_fans', 'dead_zones', 'gas_monitoring_points', 'ventilation_status'),
    8: ('ground_assessment_id', 'support_type', 'last_scaling_date', 'geotechnical_inspection_status', 'seismicity_alert', 'water_ingress_observation', 'brow_condition', 'unsupported_span_risk'),
    9: ('ground_defect_id', 'defect_type', 'severity', 'barricade_status', 'corrective_owner', 'return_to_service_criteria', 'affected_permits'),
    10: ('blast_permit_id', 'shotfirer_authorization', 'magazine_reconciliation', 'blast_hole_readiness', 'exclusion_zone_design', 'firing_window', 'firing_circuit_check', 'misfire_response_plan', 'clearance_authority'),
    11: ('reentry_release_id', 'fumes_clearance', 'reentry_gas_tests', 'geotech_inspection', 'brow_crest_inspection', 'misfire_confirmation', 'crew_release_signed', 'equipment_release_signed'),
    12: ('conflict_id', 'overlapping_permits', 'conflict_type', 'conflict_area', 'resolution_guidance', 'approval_blocked', 'activation_blocked'),
    13: ('handover_id', 'active_permits', 'outstanding_isolations', 'changed_conditions', 'incomplete_controls', 'open_exceptions', 'atmospheric_status', 'pending_retests', 'dual_supervisor_signoff'),
    14: ('competency_check_id', 'worker_id', 'role_type', 'license_expiry', 'medical_restriction', 'induction_status', 'area_authorization', 'assignment_result'),
    15: ('contractor_check_id', 'contractor_id', 'insurance_status', 'scope_authorization', 'induction_status', 'supervisor_nomination', 'equipment_compliance', 'rescue_arrangements', 'method_statement'),
    16: ('fit_for_work_id', 'shift_roster_id', 'hours_worked', 'rest_hours', 'overtime_flag', 'medical_restriction', 'safety_critical_task', 'supervisor_justification'),
    17: ('control_library_id', 'hazard_family', 'work_type', 'area_type', 'mandatory_controls', 'template_binding', 'omitted_control_detection'),
    18: ('critical_control_verification_id', 'control_id', 'field_verified', 'verified_at', 'verifier_id', 'evidence_attachment', 'recheck_interval'),
    19: ('water_risk_id', 'nearby_workings', 'dewatering_status', 'sump_capacity', 'bund_integrity', 'rainfall_trigger', 'old_workings_proximity', 'extra_controls'),
    20: ('traffic_control_id', 'equipment_exclusion_zone', 'spotter_required', 'radio_channel', 'one_way_restriction', 'parking_boundary', 'immobilization_check'),
    21: ('precursor_id', 'near_miss_type', 'unsafe_condition', 'permit_breach', 'gas_exceedance', 'control_failure', 'linked_permit', 'escalation_state'),
    22: ('prevention_action_id', 'incident_classification', 'new_control_proposal', 'template_change', 'training_need', 'policy_update', 'repeat_event_metric'),
    23: ('high_potential_id', 'event_class', 'immediate_area_hold', 'senior_review', 'evidence_preservation', 'notification_deadline', 'closure_requirement'),
    24: ('evidence_pack_id', 'permit_forms', 'approvals', 'gas_tests', 'isolation_records', 'handovers', 'inspections', 'incident_links', 'event_history'),
    25: ('rule_overlay_id', 'site_id', 'country_code', 'commodity', 'operation_type', 'permit_field_overrides', 'retention_period', 'atmospheric_limits'),
    26: ('area_board_id', 'area_id', 'current_permits', 'active_isolations', 'confined_space_entries', 'blasting_windows', 'open_hazards', 'shift_owner'),
    27: ('detail_view_id', 'hazard_controls_visible', 'atmospheric_status_visible', 'isolations_visible', 'handover_notes_visible', 'competency_gaps_visible', 'why_blocked_section'),
    28: ('permit_draft_skill_id', 'source_instruction', 'proposed_permit_class', 'proposed_work_area', 'proposed_controls', 'missing_information_prompts', 'confirmation_required'),
    29: ('summary_skill_id', 'source_references', 'handover_brief', 'open_permit_digest', 'incident_summary', 'claim_support_status', 'drilldown_links'),
    30: ('assistant_refusal_id', 'unsafe_request_type', 'missing_controls', 'escalation_role', 'audit_trail_preserved', 'datastore_command_blocked'),
    31: ('domain_event_schema_id', 'event_type', 'permit_milestone', 'required_payload_fields', 'consumer_example', 'generic_lineage'),
    32: ('decision_event_id', 'actor_id', 'actor_role', 'shift_id', 'area_id', 'source_record', 'prior_state', 'new_state', 'justification'),
    33: ('anomaly_score_id', 'fast_approval_signal', 'override_pattern_signal', 'late_gas_test_signal', 'explosives_window_signal', 'area_suspension_signal', 'review_action'),
    34: ('control_assertion_id', 'assertion_family', 'expired_active_permit_check', 'gas_test_current_check', 'blast_exclusion_check', 'incident_closure_check', 'exception_opened'),
    35: ('policy_workbench_id', 'rule_id', 'approval_state', 'activation_date', 'superseded_rule', 'rollback_target', 'simulation_output'),
    36: ('runtime_parameter_id', 'parameter_name', 'validity_window', 'escalation_timer', 'retention_window', 'stale_warning_threshold', 'rollback_state'),
    37: ('offline_capture_id', 'capture_type', 'local_timestamp', 'device_identity', 'sync_status', 'conflict_resolution', 'duplicate_prevention_key'),
    38: ('attachment_id', 'device_id', 'uploader_id', 'captured_at', 'related_area', 'evidence_type', 'tamper_hash', 'linked_record'),
    39: ('rescue_plan_id', 'standby_person', 'communication_method', 'retrieval_equipment', 'casualty_route', 'response_team_available', 'refuge_location'),
    40: ('stop_work_id', 'trigger_reason', 'authorized_role', 'affected_crews', 'notification_sent', 'revalidation_required', 'restart_evidence'),
    41: ('hazard_analytics_id', 'gas_exceedance_trend', 'ground_defect_trend', 'permit_extension_trend', 'incident_concentration', 'corrective_action_aging', 'handover_breakdown'),
    42: ('scenario_id', 'blast_reschedule', 'permit_extension', 'shift_reduction', 'area_closure', 'ventilation_degradation', 'non_mutating_output'),
    43: ('dead_letter_id', 'failure_reason', 'retry_count', 'payload_summary', 'affected_record', 'safe_replay_control', 'idempotency_key'),
    44: ('tenant_site_scope_id', 'tenant_id', 'site_id', 'query_scope', 'event_scope', 'assistant_context_scope', 'export_scope', 'cross_tenant_denied'),
    45: ('approval_route_id', 'hazard_profile', 'permit_class', 'required_reviewer_role', 'geotech_required', 'shotfirer_required', 'override_justification'),
    46: ('release_evidence_id', 'rule_diff_summary', 'high_risk_workflow_results', 'event_compatibility_check', 'blocked_action_ui_evidence', 'regulatory_pack_export'),
    47: ('safety_test_matrix_id', 'permit_api_contracts', 'handover_integration', 'gas_expiry_scenario', 'confined_space_flow', 'blasting_flow', 'isolation_flow'),
    48: ('audit_proof_id', 'artifact_hash', 'decision_hash', 'chain_previous_hash', 'proof_manifest', 'tamper_verification', 'redacted_export'),
    49: ('training_sandbox_id', 'confined_space_walkthrough', 'highwall_scaling_walkthrough', 'electrical_isolation_walkthrough', 'production_blast_walkthrough', 'incident_investigation_walkthrough', 'production_isolation'),
    50: ('readiness_gate_id', 'configured_rule_sets', 'validated_site_overlays', 'trained_approvers', 'tested_event_handlers', 'reviewed_dashboards', 'approved_release_evidence', 'incident_response_owner'),
}
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {feature_number: _BASE_FIELDS + _DOMAIN_FIELDS[feature_number] + (primary_proof,) for feature_number, primary_proof in _PRIMARY_PROOF_FIELDS.items()}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    7: ("VentilationStatusChanged",),
    8: ("GeotechHazardChanged",),
    14: ("WorkerCompetencyChanged",),
    16: ("RosterFatigueChanged",),
    20: ("MineAreaStatusChanged",),
    25: ("RegulatoryRuleChanged",),
    31: ("AuditEventSealed",),
    41: ("OperationalKpiChanged",),
    44: ("PolicyChanged",),
    50: ("AuditEventSealed", "PolicyChanged"),
}
_DOMAIN_MESSAGES: dict[int, str] = {
    1: 'Expand the permit model so every permit-to-work carries permit class, work area, start and expiry windows, simultaneous operations flags, issuing authority, performing crew, affected assets, and mandatory control bundles. Include permit-type-specific rules for underground, open-pit, plant, tailings, laboratory, and workshop work.',
    2: 'Define a state machine for permit draft, supervisor review, safety review, active, suspended, extended, closed, canceled, and expired states with explicit reasons and actor attribution. Require renewed checks before returning a suspended permit to active status.',
    3: 'Add a structured isolation module capturing electrical, hydraulic, pneumatic, mechanical, gravity, pressure, and stored-energy sources; isolation points; lock and tag IDs; applied-by and verified-by roles; and zero-energy confirmation before work starts.',
    4: 'Track isolation boundary revisions with versioned diagrams, added or removed lock points, reason for change, and compulsory re-acceptance by the permit issuer and the field supervisor.',
    5: 'Maintain a classified confined-space inventory linked to permit records, including space type, dimensions, access points, ventilation arrangements, engulfment hazards, adjacent energy hazards, rescue method, and standby requirements.',
    6: 'Model gas testing as a structured sequence with instrument ID, bump-test status, tester competency, reading timestamp, gases measured, permissible limits, retest interval, and invalidation triggers such as blasting, ventilation interruption, or elapsed time.',
    7: 'Introduce ventilation dependency fields for working area, primary and secondary airflow, critical fans, known dead zones, and gas-monitoring points. Add rules that suspend permits when ventilation status is degraded or readings trend toward alarm thresholds.',
    8: 'Add ground control assessments to relevant permits, capturing support type, last scaling date, geotechnical inspection status, seismicity alerts, water ingress observations, brow condition, and unsupported span risk.',
    9: 'Create a defect workflow for missing bolts, failed mesh, damaged props, loose ground, crest cracks, berm failures, and shotcrete delamination, with severity, barricade status, corrective owner, and return-to-service criteria.',
    10: 'Expand blast-plan and explosives permit data to include shotfirer authorization, magazine issue reconciliation, blast-hole readiness, exclusion zone design, firing windows, firing circuit checks, misfire response plan, and blast clearance authority.',
    11: 'Add post-blast checks for fumes clearance, re-entry gas tests, geotechnical inspection, brow and crest inspection, misfire confirmation, and signed release for adjacent crews and mobile equipment.',
    12: 'Build a conflict engine that checks overlapping permits for blasting near confined-space work, energization during maintenance, hot work near hydrocarbons, mobile equipment near suspended loads, and work beneath unsupported ground.',
    13: 'Add structured handover records with active permits, outstanding isolations, changed conditions, incomplete controls, open exceptions, atmospheric status, pending re-tests, and supervisor signoff from both outgoing and incoming shifts.',
    14: 'Introduce competency matching for permit issuer, permit receiver, gas tester, standby person, isolator, electrician, rigger, shotfirer, and geotechnical examiner roles. Validate license dates, medical restrictions, induction status, and area-specific authorizations.',
    15: 'Add contractor readiness checks for insurance, scope authorization, inductions, supervisor nomination, equipment compliance, rescue arrangements, and approved work method statements for the specific permit type.',
    16: 'Connect shift-roster records to permit approval checks that flag excessive hours, insufficient rest, unplanned overtime, and medically restricted assignments for safety-critical tasks.',
    17: 'Build a control library for ground control, ventilation, explosives, mobile equipment interaction, energy isolation, water management, confined space, working at height, lifting, and hazardous substances. Allow permit templates to require specific controls by work type and area.',
    18: 'Require field verification for selected critical controls with timestamp, verifier identity, evidence attachment, and periodic recheck logic. Examples include barricades in place, ventilation on, scaling completed, gas readings acceptable, and lock points intact.',
    19: 'Add water-related assessments for nearby workings, dewatering status, sump capacity, bund integrity, rainfall triggers for surface operations, and known old-workings proximity before permits are approved in exposed areas.',
    20: 'Add traffic-management fields to permits for equipment exclusion zones, spotters, radio channel, one-way restrictions, parking boundaries, and immobilization checks when maintenance occurs near operating plant or haul roads.',
    21: 'Extend incident reporting so near misses, unsafe conditions, permit breaches, gas exceedances, and control failures can be logged quickly and linked to the relevant permit, shift, area, and crew.',
    22: 'Add a prevention loop that proposes new controls, template changes, training needs, and policy updates based on incident classifications such as fall of ground, energy release, explosives misfire, atmospheric hazard, vehicle interaction, or procedural breach.',
    23: 'Introduce a dedicated high-potential pathway for events with blast misfires, serious gas exceedances, ground collapse indicators, uncontrolled energy release, or major permit violations, including immediate area holds, senior review, and evidence preservation.',
    24: 'Build exportable evidence packs that gather permit forms, approvals, gas tests, isolation records, handovers, inspections, incident links, control verifications, and event history into a reproducible package.',
    25: 'Add a rule overlay model allowing site, country, commodity, and operation-type variations for permit fields, retention periods, explosives controls, atmospheric limits, and mandatory evidence.',
    26: 'Redesign the workbench with an area control board showing current permits, isolations, confined-space entries, blasting windows, open hazards, incidents, and shift ownership by mining area.',
    27: 'Rework the detail panel so hazard controls, atmospheric status, isolations, handover notes, competency gaps, and stop-work conditions appear ahead of less critical metadata. Include a clear “why blocked” section when a permit cannot proceed.',
    28: 'Add an agent skill that converts user instructions such as “pump change in decline sump after isolating panel and testing air” into a draft permit with proposed type, work area, controls, and missing-information prompts.',
    29: 'Add a governed summarization skill that composes shift handover briefs, open-permit digests, and incident summaries with explicit source citations to permits, inspections, gas readings, and control actions.',
    30: 'Define refusal logic for requests such as approving without gas tests, closing incidents without findings, ignoring competency gaps, or reactivating suspended permits without rechecks. Escalate such requests to named human roles with a preserved audit trail.',
    31: 'Emit typed domain events for permit issued, permit suspended, isolation verified, confined-space entry started, gas test failed, blast cleared, handover accepted, incident classified, and regulatory pack exported.',
    32: 'Capture immutable decision events with actor, role, shift, area, source record, prior state, new state, and justification for approvals, suspensions, overrides, and closures across permits and incidents.',
    33: 'Add anomaly scoring for patterns such as permits approved too quickly, recurrent use of the same override reason, repeated late gas tests, unusual explosives activity windows, and repeated suspensions in one area.',
    34: 'Create automated control assertions that continuously test for expired permits still marked active, confined-space entries lacking current gas tests, blasting permits without exclusion evidence, and closed incidents missing corrective-action closure.',
    35: 'Add a governance UI for rule creation, approval, activation date, supersession, and rollback of permit, gas-testing, competency, ground-control, and explosives rules.',
    36: 'Separate policy rules from runtime parameters and manage parameters for gas-test validity, handover reminder timing, incident escalation windows, evidence export retention, and stale-permit warnings with approval and rollback support.',
    37: 'Support offline entry of inspections, gas tests, control verifications, and permit acknowledgements with local timestamps, device identity, later synchronization, and conflict resolution rules.',
    38: 'Add attachment provenance fields for device, uploader, captured-at time, related area, evidence type, and tamper-evident hashing. Link each artifact to permit steps, inspections, incidents, or regulatory submissions.',
    39: 'Require rescue planning fields for standby person, communication method, retrieval equipment, route to casualty, emergency response team availability, and nearest refuge or muster location where applicable.',
    40: 'Add a stop-work action that any authorized supervisor or safety role can use to suspend active permits, capture the trigger reason, notify affected crews, and require formal revalidation before restart.',
    41: 'Add analytics for repeated gas exceedances, recurring ground defects, repeated permit extensions, incident concentration by area, unresolved corrective actions, and frequent handover breakdowns.',
    42: 'Provide simulation tools for blast rescheduling, permit extension, shift reduction, area closure, and ventilation degradation that estimate conflicts, expired gas tests, handover impact, and productivity disruption.',
    43: 'Build an operational console for failed event deliveries with reason, retry count, payload summary, affected record, and safe replay controls for safety-critical event types.',
    44: 'Enforce tenant and site scoping across records, queries, events, assistant context, analytics, and exports, with explicit policy separation for local rule overlays and release evidence.',
    45: 'Route approvals dynamically based on hazard profile so that electrical isolation may need an authorized electrician, a blast permit requires a shotfirer or blasting engineer, and a ground-control deviation requires geotechnical review.',
    46: 'Expand `RELEASE_EVIDENCE.md` expectations to include rule-diff summaries, high-risk workflow test results, event compatibility checks, UI evidence for blocked unsafe actions, and sample regulatory pack exports.',
    47: 'Add contract tests for permit APIs, integration tests for shift handover plus active permits, scenario tests for gas-test expiry, and end-to-end tests for confined-space, blasting, and isolation workflows.',
    48: 'Hash and chain critical evidence artifacts and decision events so exported proof manifests can show integrity for permit approvals, gas tests, blast clearances, and incident closures without exposing unnecessary content.',
    49: 'Provide seeded scenarios covering a confined-space pump repair, a highwall scaling job, an underground electrical isolation, a production blast, and an incident investigation, each with realistic data and guided assistant prompts.',
    50: 'Define a go-live readiness gate covering configured rule sets, validated site overlays, trained approvers, tested event handlers, reviewed dashboards, approved release evidence, and incident-response ownership for the PBC.',
}
_HUMAN_CONFIRMATION_FEATURES = (2, 3, 4, 10, 11, 12, 18, 23, 28, 30, 35, 40, 42, 45, 50)
_PROJECTION_ONLY_FEATURES = (7, 8, 14, 16, 20, 25, 31, 41, 44, 50)
_AGENT_PREVIEW_FEATURES = (28, 29, 30)
_NON_MUTATING_FEATURES = (35, 42, 46, 47, 49, 50)
SAFETY_CRITICAL_FEATURES = (3, 6, 7, 8, 10, 11, 12, 18, 23, 30, 34, 40, 45, 48, 50)


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
        "tables": (f"mining_safety_permits_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": proof,
        "ui": f"MiningSafetyPermits{_camel(capability.slug)}Panel",
        "route": f"POST /mining-safety-permits/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in MINING_SAFETY_CONTROL_CAPABILITIES}


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
        "event_topic": MINING_SAFETY_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "safety_evidence_complete": True,
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
    if feature_number in SAFETY_CRITICAL_FEATURES and payload.get("safety_evidence_complete") is not True:
        findings.append("safety-critical mining permit controls require complete field evidence before approval, re-entry, closure, or release")
    if feature_number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("mining safety permit decisions with safety, legal, blast, isolation, or go-live impact require human approval before mutation")
    if feature_number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("mining safety assistant skills must draft, summarize, refuse, or escalate only with source evidence and confirmation gates")
    if feature_number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("policy simulations, evidence checks, training sandboxes, tests, and readiness gates must be side-effect-free planning artifacts")
    if feature_number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("ventilation, geotech, competency, roster, area, regulatory, KPI, policy, and audit context must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != MINING_SAFETY_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("mining safety permit eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in MINING_SAFETY_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary mining safety permit datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("mining safety controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_mining_safety_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in MINING_SAFETY_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in MINING_SAFETY_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": MINING_SAFETY_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": MINING_SAFETY_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_mining_safety_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_mining_safety_control(capability) for capability in MINING_SAFETY_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.mining-safety-permits-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": MINING_SAFETY_CONTROL_OWNED_TABLES, "declared_dependencies": MINING_SAFETY_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": MINING_SAFETY_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": MINING_SAFETY_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


MINING_SAFETY_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_mining_safety_control(slug, payload)) for capability in MINING_SAFETY_CONTROL_CAPABILITIES}

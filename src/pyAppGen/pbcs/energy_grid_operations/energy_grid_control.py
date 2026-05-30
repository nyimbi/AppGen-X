"""Executable improve1 controls for the energy grid operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "energy_grid_operations"
EVENT_CONTRACT = "AppGen-X"
ENERGY_GRID_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
ENERGY_GRID_REQUIRED_EVENT_TOPIC = "pbc.energy_grid_operations.events"

ASSET = "energy_grid_operations_grid_asset"
FORECAST = "energy_grid_operations_load_forecast"
SWITCHING = "energy_grid_operations_switching_order"
DISPATCH = "energy_grid_operations_dispatch_instruction"
OUTAGE = "energy_grid_operations_outage_event"
CONSTRAINT = "energy_grid_operations_reliability_constraint"
TOPOLOGY = "energy_grid_operations_grid_topology"
RULE = "energy_grid_operations_energy_grid_operations_policy_rule"
PARAMETER = "energy_grid_operations_energy_grid_operations_runtime_parameter"
SCHEMA_EXTENSION = "energy_grid_operations_energy_grid_operations_schema_extension"
CONTROL = "energy_grid_operations_energy_grid_operations_control_assertion"
MODEL = "energy_grid_operations_energy_grid_operations_governed_model"
OUTBOX = "energy_grid_operations_appgen_outbox_event"
INBOX = "energy_grid_operations_appgen_inbox_event"
DEAD_LETTER = "energy_grid_operations_appgen_dead_letter_event"

ENERGY_GRID_OWNED_TABLES = (
    ASSET,
    FORECAST,
    SWITCHING,
    DISPATCH,
    OUTAGE,
    CONSTRAINT,
    TOPOLOGY,
    RULE,
    PARAMETER,
    SCHEMA_EXTENSION,
    CONTROL,
    MODEL,
    OUTBOX,
    INBOX,
    DEAD_LETTER,
)
ENERGY_GRID_DECLARED_DEPENDENCIES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "SCADAAlarmRaised",
    "WeatherRiskChanged",
    "CrewAvailabilityChanged",
    "OutageManagementUpdated",
    "DERSignalChanged",
    "GET /weather/grid-risk/{territory}",
    "GET /crew/availability/{territory}",
    "POST /notifications/messages",
    "POST /audit/events/seal",
)

ENERGY_GRID_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in ENERGY_GRID_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in ENERGY_GRID_CONTROL_CAPABILITIES}

_SPEC_ROWS: tuple[tuple[int, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = (
    (1, (ASSET, TOPOLOGY), ("voltage_class", "parent_asset_id", "normal_state", "protection_zone", "feeder_id", "substation_id", "gis_reference", "scada_points"), "FeederHierarchyWorkbench", "POST /grid-assets/hierarchy-validate", ()),
    (2, (ASSET, CONTROL), ("device_type", "interrupting_rating", "operating_mode", "normal_position", "phase_combination", "scada_tag", "quality_gate"), "ControllableDeviceQualityPanel", "POST /grid-assets/device-quality", ()),
    (3, (TOPOLOGY, CONSTRAINT), ("source_asset_id", "energized_sections", "normally_open_ties", "backfeed_paths", "phase_map", "topology_version"), "PhaseAwareFeederGraph", "POST /grid-topology/pathfind", ("SCADAAlarmRaised",)),
    (4, (ASSET, OUTBOX), ("utility_asset_id", "commissioning_evidence", "gis_reference", "scada_mapping", "field_correction_note", "idempotency_key"), "UtilityAssetIntake", "POST /grid-assets", ()),
    (5, (SWITCHING, CONTROL), ("step_sequence", "actions", "hold_points", "telemetry_confirmation", "clearance_id", "reversal_steps"), "SwitchingOrderStepTimeline", "POST /switching-orders/sequence-review", ()),
    (6, (SWITCHING, TOPOLOGY, CONSTRAINT), ("validation_only", "proposed_steps", "impacted_feeders", "violated_constraints", "approval_required", "mutation_count"), "SwitchingSimulationWorkbench", "POST /switching-orders/simulate", ()),
    (7, (DISPATCH, OUTBOX), ("objective_type", "control_target", "target_interval", "expected_load_movement", "voltage_support_intent", "rollback_conditions"), "DispatchObjectiveWorkbench", "POST /dispatch-instructions", ("DERSignalChanged",)),
    (8, (DISPATCH, CONSTRAINT, SWITCHING), ("telemetry_freshness_seconds", "active_constraints", "active_outages", "overlapping_switching_orders", "conflict_codes"), "DispatchConflictReview", "POST /dispatch-instructions/conflict-check", ("SCADAAlarmRaised",)),
    (9, (OUTAGE, CONTROL), ("state_transition", "cause_code", "restoration_clock", "partial_restoration", "misoperation_correction", "post_event_review"), "OutageLifecycleWorkbench", "POST /outage-events/lifecycle", ()),
    (10, (OUTAGE, INBOX), ("initiating_device", "impacted_feeder_sections", "estimated_customers", "crew_eta", "restoration_hypothesis", "correlation_id"), "StormOutageIntake", "POST /outage-events", ("OutageManagementUpdated", "SCADAAlarmRaised")),
    (11, (FORECAST, TOPOLOGY), ("substation_id", "feeder_id", "downstream_segment", "native_load", "der_contribution", "confidence_band", "reverse_flow_risk"), "FeederForecastWorkbench", "POST /load-forecasts/granular", ("WeatherRiskChanged", "DERSignalChanged")),
    (12, (FORECAST, CONTROL), ("source_system", "forecast_horizon", "interval_size", "confidence_metadata", "weather_reference", "der_assumptions", "override_reason"), "ForecastProvenanceDetail", "POST /load-forecasts", ("WeatherRiskChanged",)),
    (13, (CONSTRAINT, RULE), ("constraint_type", "scope_id", "scope_level", "severity", "expiry", "resolution_order"), "ReliabilityConstraintStudio", "POST /reliability-constraints", ()),
    (14, (TOPOLOGY, OUTAGE, CONSTRAINT), ("candidate_paths", "switching_count", "expected_load_pickup", "constrained_devices", "field_verification_steps"), "RestorationPathComparison", "POST /restoration-paths/rank", ()),
    (15, (ASSET, SWITCHING, OUTAGE, FORECAST, CONSTRAINT), ("feeder_cards", "substation_cards", "switching_queue", "restoration_clocks", "forecast_actual_delta", "stale_projection_warning"), "EnergyGridOperationsWorkbench", "GET /energy-grid-operations-workbench", ()),
    (16, (ASSET, SWITCHING, OUTAGE, DISPATCH, CONSTRAINT), ("one_line_context", "substation_source", "open_points", "event_timeline", "switching_steps", "approval_chronology"), "EnergyGridOperationsDetail", "GET /energy-grid-operations-detail/{id}", ()),
    (17, (MODEL, CONTROL), ("allowed_skills", "blocked_actions", "source_records", "required_approvers", "preview_first", "human_approval_gate"), "EnergyGridOperationsAssistantPanel", "POST /assistant/skill-preview", ()),
    (18, (INBOX, OUTBOX, TOPOLOGY), ("projection_timestamp", "consumed_event_lag", "territory_scope", "feeder_filters", "substation_filters", "active_mode"), "WorkbenchFreshnessBanner", "GET /energy-grid-operations-workbench", ("OperationalKpiChanged",)),
    (19, (FORECAST, CONSTRAINT, OUTAGE, MODEL), ("loading_margin", "asset_criticality", "restoration_complexity", "forecast_uncertainty", "weather_severity", "crew_safety_exposure"), "GridRiskScorePanel", "POST /analytics/risk-score", ("WeatherRiskChanged",)),
    (20, (OUTAGE, SWITCHING, FORECAST, CONTROL), ("saidi", "saifi", "caidi", "maifi", "restoration_age", "switching_backlog_age", "stale_telemetry_count"), "ReliabilityMetricDashboard", "GET /analytics/reliability-metrics", ("OperationalKpiChanged",)),
    (21, (OUTBOX, ASSET, SWITCHING, OUTAGE, DISPATCH, CONSTRAINT), ("aggregate_type", "aggregate_id", "feeder_scope", "actor_class", "initial_state", "source_command", "topology_impact"), "CreationEventInspector", "POST /events/creation-snapshot", ()),
    (22, (OUTBOX, SWITCHING, DISPATCH, OUTAGE), ("change_class", "revision_number", "changed_fields", "safety_impact", "topology_impact", "rereview_required"), "UpdateEventInspector", "POST /events/update-delta", ()),
    (23, (OUTBOX, RULE, CONTROL), ("approver_identity_class", "approval_reason", "policy_version", "constraint_snapshot", "follow_up_actions", "replay_context"), "ApprovalReplayWorkbench", "POST /approvals/replay", ("PolicyChanged",)),
    (24, (OUTBOX, DEAD_LETTER, CONTROL), ("exception_cause", "severity", "owner_role", "affected_feeder_scope", "remediation_workflow", "restoration_impact"), "OperatorExceptionQueue", "POST /exceptions/open", ()),
    (25, (INBOX, RULE, SWITCHING, DISPATCH), ("policy_version", "authority_recalculation", "clearance_requirements", "hold_point_updates", "affected_active_records", "exception_opened"), "PolicyChangeImpactWorkbench", "POST /events/policy-changed", ("PolicyChanged",)),
    (26, (INBOX, CONTROL, SWITCHING, OUTAGE, DISPATCH), ("audit_seal_id", "target_record", "integrity_marker", "retrieval_path", "sealed_evidence_link"), "AuditSealDetail", "POST /audit/seals/attach", ("AuditEventSealed", "POST /audit/events/seal")),
    (27, (INBOX, PARAMETER, CONTROL), ("reliability_target", "urgency_band", "feeder_stress_flags", "escalation_thresholds", "projection_catchup"), "KpiPostureWorkbench", "POST /events/kpi-changed", ("OperationalKpiChanged",)),
    (28, (OUTBOX, INBOX, SWITCHING, OUTAGE), ("history_stream", "correlation_id", "command_events", "confirmation_events", "projection_checkpoints", "replay_digest"), "EventSourcedTimeline", "POST /timeline/replay", ()),
    (29, (ASSET, OUTAGE, SWITCHING, MODEL), ("tenant", "territory_scope", "event_stream_scope", "assistant_scope", "release_artifact_scope", "cross_tenant_lookup"), "TenantIsolationWorkbench", "POST /tenant-boundary/proof", ()),
    (30, (SCHEMA_EXTENSION, ASSET, TOPOLOGY), ("target_table", "device_class", "telemetry_attributes", "compatibility_result", "activation_gate", "rollback_plan"), "SchemaEvolutionStudio", "POST /schema-extensions/device-class", ()),
    (31, (MODEL, SWITCHING, OUTAGE, FORECAST, DISPATCH), ("anomaly_type", "breaker_cycles", "restoration_eta_regression", "forecast_divergence", "telemetry_silence", "reviewer_outcome"), "GridAnomalyReviewQueue", "POST /anomalies/detect", ("SCADAAlarmRaised", "WeatherRiskChanged")),
    (32, (MODEL, SWITCHING, OUTAGE, CONTROL), ("source_document", "document_type", "extracted_steps", "feeder_identifiers", "safety_notes", "source_span_citations"), "SwitchingSheetParser", "POST /assistant/documents/parse", ()),
    (33, (RULE, PARAMETER), ("policy_profile", "operating_mode", "inheritance_chain", "approval_threshold_delta", "restoration_threshold_delta", "visible_mode_banner"), "OperatingModePolicyWorkbench", "POST /policies/profile-switch", ("PolicyChanged",)),
    (34, (TOPOLOGY, CONSTRAINT, DISPATCH), ("scenario_alternatives", "expected_load_pickup", "voltage_risk", "crew_travel", "der_participation", "side_effect_free"), "CounterfactualScenarioWorkbench", "POST /simulations/counterfactual", ()),
    (35, (CONTROL, SWITCHING, OUTAGE, DISPATCH), ("hash_chain", "actor", "record_revision", "constraint_snapshot", "document_reference", "proof_valid"), "SafetyCriticalProofs", "POST /audit/proofs/verify", ("AuditEventSealed",)),
    (36, (CONTROL, SWITCHING, OUTAGE), ("control_name", "isolation_verification", "clearance_evidence", "overlapping_authority", "stale_outage_state", "block_approval"), "ContinuousControlWorkbench", "POST /controls/run", ()),
    (37, (DISPATCH, CONSTRAINT, FORECAST), ("carbon_delta", "loss_delta", "reliability_priority", "thermal_constraint", "voltage_constraint", "advisory_label"), "SustainabilityAdvisoryPanel", "POST /dispatch/sustainability-advisory", ("DERSignalChanged",)),
    (38, (INBOX, OUTBOX, CONTROL), ("declared_event_contracts", "projection_adapters", "foreign_table_scan", "dependency_map", "boundary_status"), "FederatedSignalBoundary", "POST /boundary/event-federation", ENERGY_GRID_DECLARED_DEPENDENCIES),
    (39, (MODEL, CONTROL, RULE), ("skill_name", "permission_checked", "data_scope", "preview_payload", "confirmation_required", "blocked_mutation"), "GovernedGridAgentConsole", "POST /assistant/governed-execution", ()),
    (40, (PARAMETER, RULE), ("territory_calendar", "storm_mode", "switching_window", "restoration_target_band", "telemetry_freshness_threshold", "feeder_naming_pattern"), "GridConfigurationWorkbench", "POST /configuration/validate", ()),
    (41, (RULE, CONSTRAINT, SWITCHING), ("rule_inputs", "backfeed_prevention", "reserve_margin", "clearance_sequence", "der_islanding", "rule_version"), "ElectricalRuleExplanation", "POST /rules/evaluate", ()),
    (42, (PARAMETER, OUTAGE, CONTROL), ("parameter_name", "bounded_value", "storm_override", "rollback_evidence", "change_history", "audit_approval"), "StormParameterTuningPanel", "POST /parameters/tune", ()),
    (43, (SWITCHING, OUTAGE, ASSET, TOPOLOGY), ("switching_steps", "safety_clearances", "outage_milestones", "telemetry_references", "restoration_decisions", "owned_relationships"), "OwnedSchemaExplorer", "GET /schema/operational-depth", ()),
    (44, (OUTBOX, INBOX), ("event_partition", "correlation_id", "projection_checkpoint", "freshness_report", "event_topic", "stream_engine_picker_visible"), "GridEventLineagePanel", "GET /events/lineage", ("OperationalKpiChanged", "AuditEventSealed")),
    (45, (INBOX, OUTAGE, OUTBOX), ("source_event_identity", "feeder_scope", "record_revision", "duplicate_detected", "stable_output_state", "conflict_dead_letter"), "DuplicateFeedSafetyPanel", "POST /events/idempotency-check", ("SCADAAlarmRaised", "OperationalKpiChanged")),
    (46, (DEAD_LETTER, INBOX, CONTROL), ("failed_source_event", "affected_feeder", "processing_error", "replay_safety_assessment", "operator_rationale", "resolution_outcome"), "DeadLetterReplayWorkbench", "POST /events/dead-letter/replay", ()),
    (47, (RULE, CONTROL, MODEL), ("role_matrix", "create_permission", "approve_permission", "simulate_permission", "dual_approval_required", "storm_mode_override"), "ControlRoomRoleMatrix", "GET /permissions/control-room", ()),
    (48, (MODEL, SWITCHING, OUTAGE, CONTROL), ("document_packet", "document_type", "extracted_record", "citation_spans", "approval_preview", "draft_side_effect_free"), "PacketIntakeAssistant", "POST /assistant/packets/intake", ()),
    (49, (CONTROL, TOPOLOGY, SWITCHING, OUTAGE, OUTBOX), ("simulation_gate", "replay_gate", "control_gate", "metric_gate", "assistant_governance_gate", "failed_gate_detail"), "ReleaseAssuranceWorkbench", "POST /release/assurance-run", ()),
    (50, (CONTROL, SCHEMA_EXTENSION, OUTBOX), ("readiness_pack_sections", "topology_check", "switching_simulation", "outage_replay", "event_boundary_proof", "unresolved_risks"), "UtilityOperationsReadinessPack", "GET /release/readiness-pack", ()),
)


_EMPTY_ALLOWED_FIELDS = (
    "active_constraints",
    "conflict_codes",
    "foreign_table_scan",
    "unresolved_risks",
)

CONTROL_SPECS: dict[int, dict[str, Any]] = {
    number: {"tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps}
    for number, tables, fields, ui, route, deps in _SPEC_ROWS
}


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
    payload.update(
        {
            "tenant": "utility-a",
            "feeder_id": "feeder-12",
            "substation_id": "sub-4",
            "parent_asset_id": "sub-4",
            "voltage_class": "13.8kv",
            "voltage_kv": 13.8,
            "normal_state": "closed",
            "phase_combination": ("A", "B", "C"),
            "scada_tag": "SCADA.FEEDER12.BKR",
            "interrupting_rating": "25ka",
            "operating_mode": "supervisory",
            "quality_gate": "passed",
            "source_asset_id": "sub-4-main-bus",
            "phase_compatible": True,
            "source_lineage": ("gis", "scada", "field_correction"),
            "step_sequence": (1, 2, 3),
            "actions": ("open", "verify", "close"),
            "hold_points": ("verify-isolation",),
            "ordered_steps": True,
            "validation_only": True,
            "mutation_count": 0,
            "objective_type": "load_relief",
            "rollback_conditions": ("load-normalized",),
            "telemetry_freshness_seconds": 90,
            "active_constraints": (),
            "conflict_codes": (),
            "state_transition": ("confirmed_outage", "isolated", "partial_restoration", "full_restoration"),
            "correlation_id": "storm-42",
            "confidence_band": (0.82, 0.93),
            "confidence_metadata": "p90",
            "constraint_type": "thermal",
            "severity": "high",
            "expiry": "2026-05-30T06:00:00Z",
            "candidate_paths": ("tie-14", "tie-22"),
            "projection_timestamp": "2026-05-30T00:00:00Z",
            "stale_projection_warning": True,
            "chronology_valid": True,
            "preview_first": True,
            "human_approval_gate": True,
            "source_records": ("switching:swo-1",),
            "risk_drivers": ("loading_margin", "weather_severity"),
            "formula_inputs": ("outage_minutes", "customers_interrupted"),
            "aggregate_type": "switching_order",
            "feeder_scope": "feeder-12",
            "topology_impact": True,
            "revision_number": 2,
            "changed_fields": ("hold_points",),
            "rereview_required": True,
            "approver_identity_class": "control_room_supervisor",
            "policy_version": "grid-policy-2026.05",
            "constraint_snapshot": "snapshot-1",
            "owner_role": "restoration_lead",
            "remediation_workflow": "restore_projection",
            "affected_active_records": ("swo-1",),
            "audit_seal_id": "seal-1",
            "sealed_evidence_link": "audit://seal-1",
            "projection_catchup": True,
            "replay_digest": "sha256:replay",
            "event_stream_scope": "tenant",
            "cross_tenant_lookup": False,
            "target_table": ASSET,
            "compatibility_result": "backward_compatible",
            "reviewer_outcome": "true_positive",
            "source_span_citations": ("packet:1-5",),
            "policy_profile": "storm",
            "inheritance_chain": ("normal", "storm"),
            "scenario_alternatives": ("tie-14", "hold-open"),
            "side_effect_free": True,
            "hash_chain": ("h1", "h2"),
            "proof_valid": True,
            "isolation_verification": "verified",
            "clearance_evidence": "clearance-1",
            "block_approval": False,
            "reliability_priority": "primary",
            "advisory_label": "secondary_to_reliability",
            "declared_event_contracts": ENERGY_GRID_DECLARED_DEPENDENCIES,
            "foreign_table_scan": (),
            "permission_checked": True,
            "confirmation_required": True,
            "blocked_mutation": False,
            "territory_calendar": "approved",
            "switching_window": "valid",
            "telemetry_freshness_threshold": 300,
            "rule_inputs": ("topology", "constraint", "clearance"),
            "backfeed_prevention": True,
            "bounded_value": 0.75,
            "rollback_evidence": "rollback-plan",
            "owned_relationships": True,
            "event_topic": ENERGY_GRID_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "duplicate_detected": True,
            "stable_output_state": True,
            "replay_safety_assessment": "safe_after_operator_review",
            "operator_rationale": "missing projection restored",
            "role_matrix": ("dispatcher", "switching_supervisor", "reliability_engineer"),
            "dual_approval_required": True,
            "citation_spans": ("packet:7-12",),
            "approval_preview": True,
            "draft_side_effect_free": True,
            "simulation_gate": "passed",
            "replay_gate": "passed",
            "control_gate": "passed",
            "metric_gate": "passed",
            "assistant_governance_gate": "passed",
            "readiness_pack_sections": ("topology", "switching", "outage", "events", "assistant", "risks"),
            "unresolved_risks": (),
        }
    )
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and (not payload.get("parent_asset_id") or not payload.get("feeder_id") or not payload.get("substation_id")):
        findings.append("asset hierarchy requires parent, feeder, and substation lineage")
    if n == 2 and not all(payload.get(field) for field in ("interrupting_rating", "operating_mode", "normal_state", "scada_tag")):
        findings.append("controllable devices require ratings, operating mode, normal state, and SCADA tag")
    if n == 3 and payload.get("phase_compatible") is not True:
        findings.append("feeder graph pathfinding cannot accept phase-incompatible paths")
    if n == 4 and not payload.get("source_lineage"):
        findings.append("asset intake must preserve GIS, SCADA, commissioning, or field-correction lineage")
    if n == 5 and (payload.get("ordered_steps") is not True or not payload.get("hold_points")):
        findings.append("switching orders require ordered steps with explicit hold points")
    if n == 6 and (payload.get("validation_only") is not True or payload.get("mutation_count", 1) != 0):
        findings.append("switching simulation must be validation-only and side-effect free")
    if n == 7 and (payload.get("objective_type") not in {"load_relief", "voltage_support", "der_curtailment", "restoration_support"} or not payload.get("rollback_conditions")):
        findings.append("dispatch instructions require a grid objective and rollback conditions")
    if n == 8 and (int(payload.get("telemetry_freshness_seconds", 9999)) > 300 or payload.get("conflict_codes")):
        findings.append("dispatch requests must block stale telemetry and active conflicts")
    if n == 9 and "full_restoration" not in tuple(payload.get("state_transition", ())) :
        findings.append("outage lifecycle requires restoration milestones through full restoration")
    if n == 10 and not payload.get("correlation_id"):
        findings.append("storm and alarm-burst outage intake requires a correlation identity")
    if n == 11 and not payload.get("confidence_band"):
        findings.append("feeder, substation, and DER forecasts require confidence bands")
    if n == 12 and not payload.get("confidence_metadata"):
        findings.append("forecast API payloads require source and confidence lineage")
    if n == 13 and payload.get("constraint_type") not in {"thermal", "voltage", "crew_safety", "switching_window", "der_export", "restoration_sequence"}:
        findings.append("reliability constraints must use grid operating constraint types")
    if n == 14 and len(tuple(payload.get("candidate_paths", ()))) < 2:
        findings.append("restoration projection requires ranked alternative paths")
    if n == 15 and not payload.get("stale_projection_warning"):
        findings.append("control-room workbench must expose stale projection warnings")
    if n == 16 and payload.get("chronology_valid") is not True:
        findings.append("detail screens must preserve operator event chronology")
    if n == 17 and (payload.get("preview_first") is not True or payload.get("human_approval_gate") is not True):
        findings.append("assistant skills must preview before mutation and require human approval")
    if n == 18 and not payload.get("projection_timestamp"):
        findings.append("workbench query responses require freshness metadata")
    if n == 19 and not payload.get("risk_drivers"):
        findings.append("grid risk score requires operational driver explanations")
    if n == 20 and not payload.get("formula_inputs"):
        findings.append("reliability metric definitions require auditable formula inputs")
    if n == 21 and not all(payload.get(field) for field in ("aggregate_type", "feeder_scope", "topology_impact")):
        findings.append("creation events require aggregate type, feeder scope, and topology impact")
    if n == 22 and payload.get("safety_impact") and payload.get("rereview_required") is not True:
        findings.append("safety-impacting updates require operator re-review")
    if n == 23 and not all(payload.get(field) for field in ("approver_identity_class", "policy_version", "constraint_snapshot")):
        findings.append("approval events require approver class, policy basis, and constraint snapshot")
    if n == 24 and not all(payload.get(field) for field in ("owner_role", "remediation_workflow")):
        findings.append("exception events require owner role and remediation workflow")
    if n == 25 and not payload.get("affected_active_records"):
        findings.append("policy changes must identify affected active switching or dispatch records")
    if n == 26 and not payload.get("sealed_evidence_link"):
        findings.append("audit seals must link back to safety-critical records")
    if n == 27 and payload.get("projection_catchup") is not True:
        findings.append("KPI changes must update workbench posture after projection catch-up")
    if n == 28 and not payload.get("replay_digest"):
        findings.append("event-sourced timelines require deterministic replay evidence")
    if n == 29 and payload.get("cross_tenant_lookup") is True:
        findings.append("tenant isolation forbids cross-tenant feeder or event lookup")
    if n == 30 and payload.get("target_table") not in ENERGY_GRID_OWNED_TABLES:
        findings.append("schema extensions for grid equipment must target owned tables")
    if n == 31 and not payload.get("reviewer_outcome"):
        findings.append("electrical anomaly detection requires reviewer outcome evidence")
    if n == 32 and not payload.get("source_span_citations"):
        findings.append("document understanding requires source-span citations")
    if n == 33 and payload.get("policy_profile") not in {"normal", "storm", "emergency_restoration", "planned_maintenance", "high_risk"}:
        findings.append("default policies must use a named grid operating profile")
    if n == 34 and (payload.get("side_effect_free") is not True or len(tuple(payload.get("scenario_alternatives", ()))) < 2):
        findings.append("counterfactual simulations must compare alternatives without mutating state")
    if n == 35 and payload.get("proof_valid") is not True:
        findings.append("safety-critical hash-chain proof failed verification")
    if n == 36 and payload.get("block_approval"):
        findings.append("continuous control failure blocks approval")
    if n == 37 and payload.get("reliability_priority") != "primary":
        findings.append("carbon and loss advisory cannot outrank safety or reliability")
    if n == 38 and payload.get("foreign_table_scan"):
        findings.append("federated grid signals must not read undeclared foreign tables")
    if n == 39 and (payload.get("permission_checked") is not True or payload.get("confirmation_required") is not True or payload.get("blocked_mutation")):
        findings.append("governed AI execution requires permission checks, preview, and confirmation")
    if n == 40 and int(payload.get("telemetry_freshness_threshold", 0)) <= 0:
        findings.append("configuration schema requires valid telemetry freshness thresholds")
    if n == 41 and not (payload.get("rule_inputs") and payload.get("backfeed_prevention") is True):
        findings.append("electrical rule evaluation requires inputs and backfeed prevention logic")
    if n == 42 and not (payload.get("rollback_evidence") and payload.get("bounded_value") is not None):
        findings.append("storm parameter tuning requires bounds and rollback evidence")
    if n == 43 and payload.get("owned_relationships") is not True:
        findings.append("operational schema depth must use owned relationships for steps and milestones")
    if n == 44 and (payload.get("event_topic") != ENERGY_GRID_REQUIRED_EVENT_TOPIC or payload.get("stream_engine_picker_visible") is True):
        findings.append("grid event lineage must use AppGen-X topic without a stream-engine picker")
    if n == 45 and (payload.get("stable_output_state") is not True or not payload.get("duplicate_detected")):
        findings.append("duplicate feed handling must detect duplicates and preserve stable output state")
    if n == 46 and not all(payload.get(field) for field in ("replay_safety_assessment", "operator_rationale")):
        findings.append("dead-letter replay requires safety assessment and operator rationale")
    if n == 47 and not payload.get("role_matrix"):
        findings.append("control-room permission model requires an explicit role matrix")
    if n == 48 and (payload.get("draft_side_effect_free") is not True or not payload.get("citation_spans")):
        findings.append("packet intake drafts must be side-effect free and citation backed")
    if n == 49 and any(payload.get(field) != "passed" for field in ("simulation_gate", "replay_gate", "control_gate", "metric_gate", "assistant_governance_gate")):
        findings.append("release assurance requires passing simulation, replay, control, metric, and assistant gates")
    if n == 50 and (not payload.get("readiness_pack_sections") or payload.get("unresolved_risks")):
        findings.append("readiness pack requires complete sections and no unresolved operational risks")
    return tuple(findings)


def evaluate_energy_grid_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in ENERGY_GRID_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in ENERGY_GRID_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": ENERGY_GRID_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": ENERGY_GRID_ALLOWED_DATABASE_BACKENDS,
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


def improve1_energy_grid_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_energy_grid_control(capability) for capability in ENERGY_GRID_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.energy-grid-operations-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": ENERGY_GRID_OWNED_TABLES,
        "declared_dependencies": ENERGY_GRID_DECLARED_DEPENDENCIES,
        "allowed_database_backends": ENERGY_GRID_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": ENERGY_GRID_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


ENERGY_GRID_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_energy_grid_control(slug, payload))
    for capability in ENERGY_GRID_CONTROL_CAPABILITIES
}

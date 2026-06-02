"""World-class domain depth contract for the smart_city_mobility_operations PBC."""

from __future__ import annotations

import hashlib

PBC_KEY = "smart_city_mobility_operations"
DOMAIN_ENTITY = "corridor_registry"
DOMAIN_PURPOSE = (
    "City mobility command for corridors, intersections, signal timing, transit "
    "priority, curb and parking operations, micromobility, incidents, closures, "
    "permits, sensor feeds, congestion pricing, accessibility, emissions, "
    "multimodal reliability, public notifications, and governed AI previews"
)

DOMAIN_RECORD_SPECS = (
    {
        "record_type": "corridor_registry",
        "operation": "register_corridor",
        "table": f"{PBC_KEY}_corridor_registry",
        "event": "CorridorCommandUpdated",
        "permission": f"{PBC_KEY}.create",
        "id_field": "corridor_id",
        "required_fields": (
            "corridor_id",
            "tenant",
            "name",
            "functional_class",
            "operating_objective",
        ),
        "references": (),
        "wizard": "CorridorCommandWizard",
        "form": "CorridorRegistryForm",
        "path": "/app/smart-city-mobility-operations/corridors",
        "keywords": (
            "corridor",
            "arterial",
            "bus lane",
            "school zone",
            "freight",
        ),
    },
    {
        "record_type": "intersection_registry",
        "operation": "register_intersection",
        "table": f"{PBC_KEY}_intersection_registry",
        "event": "CorridorCommandUpdated",
        "permission": f"{PBC_KEY}.create",
        "id_field": "intersection_id",
        "required_fields": (
            "intersection_id",
            "tenant",
            "corridor_id",
            "name",
            "control_mode",
            "movements",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "CorridorCommandWizard",
        "form": "IntersectionRegistryForm",
        "path": "/app/smart-city-mobility-operations/intersections",
        "keywords": ("intersection", "phase", "movement", "crosswalk", "detector"),
    },
    {
        "record_type": "signal_plan",
        "operation": "author_signal_plan",
        "table": f"{PBC_KEY}_signal_plan",
        "event": "SignalPlanActivated",
        "permission": f"{PBC_KEY}.approve",
        "id_field": "signal_plan_id",
        "required_fields": (
            "signal_plan_id",
            "tenant",
            "corridor_id",
            "intersection_id",
            "plan_name",
            "cycle_length_seconds",
            "phase_splits",
            "accessibility_profile",
        ),
        "references": (
            ("corridor_id", "corridor_registry"),
            ("intersection_id", "intersection_registry"),
        ),
        "wizard": "SignalTimingReviewWizard",
        "form": "SignalPlanForm",
        "path": "/app/smart-city-mobility-operations/signal-plans",
        "keywords": (
            "signal",
            "retiming",
            "offset",
            "split",
            "pedestrian timing",
        ),
    },
    {
        "record_type": "transit_priority_rule_pack",
        "operation": "configure_transit_priority",
        "table": f"{PBC_KEY}_transit_priority_rule_pack",
        "event": "TransitPriorityRuleConfigured",
        "permission": f"{PBC_KEY}.approve",
        "id_field": "priority_rule_id",
        "required_fields": (
            "priority_rule_id",
            "tenant",
            "corridor_id",
            "eligible_routes",
            "lateness_threshold_minutes",
            "occupancy_threshold",
            "green_extension_limit_seconds",
            "red_truncation_limit_seconds",
            "blackout_conditions",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "SignalTimingReviewWizard",
        "form": "TransitPriorityRuleForm",
        "path": "/app/smart-city-mobility-operations/transit-priority-rules",
        "keywords": ("transit priority", "bus priority", "lateness", "headway"),
    },
    {
        "record_type": "emergency_preemption_policy",
        "operation": "configure_emergency_preemption",
        "table": f"{PBC_KEY}_emergency_preemption_policy",
        "event": "EmergencyPreemptionPolicyPublished",
        "permission": f"{PBC_KEY}.approve",
        "id_field": "preemption_policy_id",
        "required_fields": (
            "preemption_policy_id",
            "tenant",
            "intersection_id",
            "priority_order",
            "recovery_strategy",
        ),
        "references": (("intersection_id", "intersection_registry"),),
        "wizard": "SignalTimingReviewWizard",
        "form": "EmergencyPreemptionForm",
        "path": "/app/smart-city-mobility-operations/emergency-preemptions",
        "keywords": ("preemption", "emergency", "fire", "ambulance", "recovery"),
    },
    {
        "record_type": "curb_zone",
        "operation": "register_curb_zone",
        "table": f"{PBC_KEY}_curb_zone",
        "event": "CurbWindowChanged",
        "permission": f"{PBC_KEY}.create",
        "id_field": "curb_zone_id",
        "required_fields": (
            "curb_zone_id",
            "tenant",
            "corridor_id",
            "block_face",
            "use_type",
            "time_bands",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "CurbAndParkingWizard",
        "form": "CurbZoneForm",
        "path": "/app/smart-city-mobility-operations/curb-zones",
        "keywords": ("curb", "loading", "pickup", "dropoff", "bus stop"),
    },
    {
        "record_type": "parking_asset",
        "operation": "register_parking_asset",
        "table": f"{PBC_KEY}_parking_asset",
        "event": "ParkingAssetClosed",
        "permission": f"{PBC_KEY}.create",
        "id_field": "parking_asset_id",
        "required_fields": (
            "parking_asset_id",
            "tenant",
            "corridor_id",
            "asset_type",
            "capacity",
            "accessible_spaces",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "CurbAndParkingWizard",
        "form": "ParkingAssetForm",
        "path": "/app/smart-city-mobility-operations/parking-assets",
        "keywords": ("parking", "garage", "lot", "occupancy", "accessible parking"),
    },
    {
        "record_type": "micromobility_dock",
        "operation": "register_micromobility_dock",
        "table": f"{PBC_KEY}_micromobility_dock",
        "event": "CorridorCommandUpdated",
        "permission": f"{PBC_KEY}.create",
        "id_field": "dock_id",
        "required_fields": (
            "dock_id",
            "tenant",
            "corridor_id",
            "dock_name",
            "dock_type",
            "geofence",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "MicromobilityGovernanceWizard",
        "form": "MicromobilityDockForm",
        "path": "/app/smart-city-mobility-operations/micromobility-docks",
        "keywords": ("dock", "scooter", "bike", "geofence", "corral"),
    },
    {
        "record_type": "traffic_incident",
        "operation": "record_traffic_incident",
        "table": f"{PBC_KEY}_traffic_incident",
        "event": "TrafficIncidentLifecycleChanged",
        "permission": f"{PBC_KEY}.update",
        "id_field": "incident_id",
        "required_fields": (
            "incident_id",
            "tenant",
            "corridor_id",
            "taxonomy_code",
            "stage",
            "severity",
            "impacted_modes",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "IncidentPlaybookWizard",
        "form": "TrafficIncidentForm",
        "path": "/app/smart-city-mobility-operations/traffic-incidents",
        "keywords": ("incident", "crash", "signal dark", "hazard", "lane blockage"),
    },
    {
        "record_type": "planned_disruption",
        "operation": "plan_construction_closure",
        "table": f"{PBC_KEY}_planned_disruption",
        "event": "ConstructionClosurePlanned",
        "permission": f"{PBC_KEY}.approve",
        "id_field": "closure_id",
        "required_fields": (
            "closure_id",
            "tenant",
            "corridor_id",
            "closure_type",
            "start_at",
            "end_at",
            "detour_summary",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "PlannedDisruptionWizard",
        "form": "ConstructionClosureForm",
        "path": "/app/smart-city-mobility-operations/construction-closures",
        "keywords": ("construction", "closure", "event", "detour", "work zone"),
    },
    {
        "record_type": "street_use_permit",
        "operation": "issue_street_use_permit",
        "table": f"{PBC_KEY}_street_use_permit",
        "event": "ConstructionClosurePlanned",
        "permission": f"{PBC_KEY}.approve",
        "id_field": "permit_id",
        "required_fields": (
            "permit_id",
            "tenant",
            "corridor_id",
            "permit_type",
            "holder_name",
            "effective_window",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "PlannedDisruptionWizard",
        "form": "StreetUsePermitForm",
        "path": "/app/smart-city-mobility-operations/street-use-permits",
        "keywords": ("permit", "occupation", "street use", "festival", "utility"),
    },
    {
        "record_type": "mobility_sensor_feed",
        "operation": "register_sensor_feed",
        "table": f"{PBC_KEY}_mobility_sensor_feed",
        "event": "SensorFeedQuarantined",
        "permission": f"{PBC_KEY}.update",
        "id_field": "feed_id",
        "required_fields": (
            "feed_id",
            "tenant",
            "corridor_id",
            "feed_type",
            "owner",
            "freshness_seconds",
            "quality_score",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "FeedQualityWizard",
        "form": "SensorFeedForm",
        "path": "/app/smart-city-mobility-operations/sensor-feeds",
        "keywords": ("feed", "sensor", "gtfs", "spat", "quality", "quarantine"),
    },
    {
        "record_type": "congestion_pricing_policy",
        "operation": "configure_congestion_pricing",
        "table": f"{PBC_KEY}_congestion_pricing_policy",
        "event": "CorridorCommandUpdated",
        "permission": f"{PBC_KEY}.approve",
        "id_field": "pricing_policy_id",
        "required_fields": (
            "pricing_policy_id",
            "tenant",
            "corridor_id",
            "zone_code",
            "peak_windows",
            "price_schedule",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "CongestionPricingWizard",
        "form": "CongestionPricingForm",
        "path": "/app/smart-city-mobility-operations/congestion-pricing-policies",
        "keywords": ("pricing", "toll", "congestion", "peak window", "zone"),
    },
    {
        "record_type": "accessibility_disruption",
        "operation": "publish_accessibility_detour",
        "table": f"{PBC_KEY}_accessibility_disruption",
        "event": "AccessibilityDetourPublished",
        "permission": f"{PBC_KEY}.approve",
        "id_field": "detour_id",
        "required_fields": (
            "detour_id",
            "tenant",
            "corridor_id",
            "impact_type",
            "replacement_guidance",
            "affected_audience",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "AccessibilityProtectionWizard",
        "form": "AccessibilityDetourForm",
        "path": "/app/smart-city-mobility-operations/accessibility-detours",
        "keywords": ("accessibility", "detour", "elevator", "curb ramp", "ADA"),
    },
    {
        "record_type": "public_notification",
        "operation": "publish_public_notification",
        "table": f"{PBC_KEY}_public_notification",
        "event": "PublicNotificationIssued",
        "permission": f"{PBC_KEY}.approve",
        "id_field": "notification_id",
        "required_fields": (
            "notification_id",
            "tenant",
            "corridor_id",
            "template_key",
            "channels",
            "message",
            "languages",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "PublicNotificationWizard",
        "form": "PublicNotificationForm",
        "path": "/app/smart-city-mobility-operations/notifications",
        "keywords": ("notification", "alert", "sms", "push", "signage"),
    },
    {
        "record_type": "multimodal_trip",
        "operation": "capture_multimodal_trip",
        "table": f"{PBC_KEY}_multimodal_trip",
        "event": "CorridorCommandUpdated",
        "permission": f"{PBC_KEY}.create",
        "id_field": "trip_id",
        "required_fields": (
            "trip_id",
            "tenant",
            "corridor_id",
            "modes",
            "travel_time_minutes",
            "reliability_score",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "MultimodalReliabilityWizard",
        "form": "MultimodalTripForm",
        "path": "/app/smart-city-mobility-operations/multimodal-trips",
        "keywords": ("multimodal", "trip", "bus", "bike", "walk", "journey"),
    },
    {
        "record_type": "service_reliability_snapshot",
        "operation": "record_service_reliability",
        "table": f"{PBC_KEY}_service_reliability_snapshot",
        "event": "CorridorCommandUpdated",
        "permission": f"{PBC_KEY}.update",
        "id_field": "reliability_snapshot_id",
        "required_fields": (
            "reliability_snapshot_id",
            "tenant",
            "corridor_id",
            "on_time_percentage",
            "average_delay_minutes",
            "sla_status",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "MultimodalReliabilityWizard",
        "form": "ServiceReliabilityForm",
        "path": "/app/smart-city-mobility-operations/service-reliability",
        "keywords": ("sla", "reliability", "on time", "bunching", "headway"),
    },
    {
        "record_type": "environmental_analytics",
        "operation": "capture_environmental_analytics",
        "table": f"{PBC_KEY}_environmental_analytics",
        "event": "CorridorCommandUpdated",
        "permission": f"{PBC_KEY}.update",
        "id_field": "analytics_id",
        "required_fields": (
            "analytics_id",
            "tenant",
            "corridor_id",
            "emission_delta_kg_co2e",
            "noise_db",
            "analysis_window",
        ),
        "references": (("corridor_id", "corridor_registry"),),
        "wizard": "EnvironmentalAnalyticsWizard",
        "form": "EnvironmentalAnalyticsForm",
        "path": "/app/smart-city-mobility-operations/environmental-analytics",
        "keywords": ("emissions", "noise", "idling", "queue", "analytics"),
    },
    {
        "record_type": "governed_instruction_preview",
        "operation": "preview_governed_instruction",
        "table": f"{PBC_KEY}_governed_instruction_preview",
        "event": "GovernedInstructionPreviewPrepared",
        "permission": f"{PBC_KEY}.approve",
        "id_field": "preview_id",
        "required_fields": ("preview_id", "tenant", "document", "instruction"),
        "references": (),
        "wizard": "GovernedPreviewWizard",
        "form": "GovernedPreviewForm",
        "path": "/app/smart-city-mobility-operations/governed-previews",
        "keywords": ("document", "instruction", "preview", "assistant", "governed"),
    },
)

GOVERNANCE_TABLES = (
    f"{PBC_KEY}_smart_city_mobility_operations_policy_rule",
    f"{PBC_KEY}_smart_city_mobility_operations_runtime_parameter",
    f"{PBC_KEY}_smart_city_mobility_operations_schema_extension",
    f"{PBC_KEY}_smart_city_mobility_operations_control_assertion",
    f"{PBC_KEY}_smart_city_mobility_operations_governed_model",
)
EVENT_TABLES = (
    f"{PBC_KEY}_appgen_outbox_event",
    f"{PBC_KEY}_appgen_inbox_event",
    f"{PBC_KEY}_appgen_dead_letter_event",
)
BUSINESS_TABLES = tuple(spec["table"] for spec in DOMAIN_RECORD_SPECS)
DOMAIN_OWNED_TABLES = BUSINESS_TABLES + GOVERNANCE_TABLES + EVENT_TABLES
DOMAIN_OPERATIONS = tuple(spec["operation"] for spec in DOMAIN_RECORD_SPECS)
DOMAIN_QUERY_SPECS = (
    {
        "query": "build_workbench_view",
        "path": "/app/smart-city-mobility-operations/workbench",
        "permission": f"{PBC_KEY}.read",
        "table": f"{PBC_KEY}_corridor_registry",
        "view": "corridor command",
    },
    {
        "query": "build_corridor_snapshot",
        "path": "/app/smart-city-mobility-operations/corridor-snapshot",
        "permission": f"{PBC_KEY}.read",
        "table": f"{PBC_KEY}_corridor_registry",
        "view": "corridor detail",
    },
    {
        "query": "build_intersection_detail",
        "path": "/app/smart-city-mobility-operations/intersection-detail",
        "permission": f"{PBC_KEY}.read",
        "table": f"{PBC_KEY}_intersection_registry",
        "view": "intersection detail",
    },
    {
        "query": "build_readiness_scorecard",
        "path": "/app/smart-city-mobility-operations/readiness-scorecard",
        "permission": f"{PBC_KEY}.read",
        "table": f"{PBC_KEY}_service_reliability_snapshot",
        "view": "go-live readiness scorecard",
    },
)
DOMAIN_RULES = (
    "signal_safety_policy",
    "transit_priority_policy",
    "emergency_preemption_policy",
    "curb_allocation_policy",
    "construction_closure_policy",
    "accessibility_detour_policy",
    "public_notification_policy",
    "feed_quality_quarantine_policy",
    "congestion_pricing_policy",
    "multimodal_reliability_policy",
)
DOMAIN_PARAMETERS = (
    "corridor_command_limit",
    "incident_clearance_sla_minutes",
    "signal_plan_approval_sla_hours",
    "congestion_pricing_peak_multiplier",
    "accessibility_detour_max_minutes",
    "feed_quality_floor",
    "emissions_factor_bus",
    "noise_threshold_db",
    "public_alert_radius_km",
    "multimodal_trip_retention_days",
)
DOMAIN_EVENTS = tuple(dict.fromkeys(spec["event"] for spec in DOMAIN_RECORD_SPECS))
DOMAIN_CONSUMED_EVENTS = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")
DOMAIN_ADVANCED_CAPABILITIES = (
    "corridor_command_orchestration",
    "movement_level_intersection_intelligence",
    "signal_timing_version_control",
    "transit_priority_governance",
    "emergency_preemption_separation",
    "accessibility_safe_detours",
    "feed_quality_quarantine",
    "congestion_pricing_simulation",
    "emissions_and_noise_analytics",
    "multimodal_trip_reliability",
    "governed_document_instruction_previews",
    "release_evidence_pack_go_live_scorecard",
)
DOMAIN_WORKBENCH_VIEWS = (
    "corridor command",
    "intersection detail",
    "signal timing review",
    "curb and parking control",
    "micromobility dock health",
    "incident and closure command",
    "accessibility and emergency response",
    "emissions and reliability analytics",
    "public notification preview",
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def operation_spec(operation: str) -> dict | None:
    return next((spec for spec in DOMAIN_RECORD_SPECS if spec["operation"] == operation), None)


def record_spec(record_type: str) -> dict | None:
    return next((spec for spec in DOMAIN_RECORD_SPECS if spec["record_type"] == record_type), None)


def query_spec(name: str) -> dict | None:
    return next((spec for spec in DOMAIN_QUERY_SPECS if spec["query"] == name), None)


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "business_tables": BUSINESS_TABLES,
        "operation_count": len(DOMAIN_OPERATIONS),
        "operations": DOMAIN_OPERATIONS,
        "queries": tuple(spec["query"] for spec in DOMAIN_QUERY_SPECS),
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": DOMAIN_EVENTS,
        "consumed_events": DOMAIN_CONSUMED_EVENTS,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 20,
        "minimum_domain_operations": 15,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    spec = operation_spec(operation)
    if spec is None:
        return {
            "ok": False,
            "reason": "unknown_domain_operation",
            "operation": operation,
            "side_effects": (),
        }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": spec["table"],
        "owned_tables": (spec["table"],),
        "read_tables": tuple(record_spec(target)["table"] for _, target in spec.get("references", ())),
        "emitted_event": spec["event"],
        "event_contract": "AppGen-X",
        "idempotency_key": _digest((PBC_KEY, operation, tuple(sorted(payload.items())))),
        "rules_evaluated": tuple(
            rule for rule in DOMAIN_RULES if any(token in rule for token in spec["keywords"][:2])
        )
        or DOMAIN_RULES[:3],
        "parameters_read": DOMAIN_PARAMETERS[:4],
        "permission": spec["permission"],
        "wizard": spec["wizard"],
        "form": spec["form"],
        "route": f"POST {spec['path']}",
        "evidence_hash": _digest((operation, payload, spec["table"], spec["event"])),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(
        execute_domain_operation(operation, {"tenant": "tenant-smoke"})
        for operation in DOMAIN_OPERATIONS[:6]
    )
    return {
        "ok": contract["ok"]
        and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"]
        and contract["operation_count"] >= contract["minimum_domain_operations"]
        and all(item["ok"] for item in executions)
        and all(item["target_table"].startswith(f"{PBC_KEY}_") for item in executions),
        "contract": contract,
        "executions": executions,
        "side_effects": (),
    }


DOMAIN_EDGE_CASES = tuple(f"{operation}_edge_case" for operation in DOMAIN_OPERATIONS) + (
    "duplicate_notification",
    "missing_accessibility_guidance",
    "sensor_feed_quarantine",
    "cross_tenant_access_attempt",
    "stale_signal_plan_reference",
    "intersection_without_corridor",
    "dead_letter_recovery",
)
DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        DOMAIN_ADVANCED_CAPABILITIES
        + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)
        + tuple(f"rule_driven_{rule}" for rule in DOMAIN_RULES)
    )
)


def domain_capability_surface_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": spec["operation"],
                "surface": f"{PBC_KEY}.ui.operation.{spec['operation']}",
                "action": spec["operation"],
                "target_table": spec["table"],
                "permission": spec["permission"],
                "requires_confirmation": True,
                "agent_tool": f"{PBC_KEY}_skills.{spec['operation']}",
                "event": spec["event"],
                "route": f"POST {spec['path']}",
                "wizard": spec["wizard"],
                "form": spec["form"],
            }
            for spec in DOMAIN_RECORD_SPECS
        ),
        "query_surfaces": tuple(
            {
                "query": spec["query"],
                "surface": f"{PBC_KEY}.ui.query.{spec['query']}",
                "route": f"GET {spec['path']}",
                "permission": spec["permission"],
                "view": spec["view"],
            }
            for spec in DOMAIN_QUERY_SPECS
        ),
        "rule_surfaces": tuple(
            {
                "rule": rule,
                "surface": f"{PBC_KEY}.ui.rule.{rule}",
                "editor": True,
                "explainable": True,
            }
            for rule in DOMAIN_RULES
        ),
        "parameter_surfaces": tuple(
            {
                "parameter": parameter,
                "surface": f"{PBC_KEY}.ui.parameter.{parameter}",
                "bounded": True,
                "editable": True,
            }
            for parameter in DOMAIN_PARAMETERS
        ),
        "advanced_surfaces": tuple(
            {
                "capability": capability,
                "surface": f"{PBC_KEY}.ui.advanced.{_digest(capability)[:12]}",
                "explainable": True,
            }
            for capability in DOMAIN_ADVANCED_CAPABILITIES
        ),
        "edge_case_surfaces": tuple(
            {
                "edge_case": edge_case,
                "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}",
                "triage_queue": True,
            }
            for edge_case in DOMAIN_EDGE_CASES
        ),
        "table_surfaces": tuple(
            {
                "owned_table": table,
                "surface": f"{PBC_KEY}.ui.table.{table}",
                "read_model": True,
                "mutation_guard": True,
            }
            for table in DOMAIN_OWNED_TABLES
        ),
        "specialist_capabilities": DOMAIN_SPECIALIST_CAPABILITIES,
        "coverage": {
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
        },
        "side_effects": (),
    }

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_capability_surface_contract,
)
from .runtime import sports_venue_event_operations_build_workbench_view

PBC_KEY = "sports_venue_event_operations"


def sports_venue_event_operations_form_contracts():
    contracts = (
        {
            "key": "VenueLayoutForm",
            "operation": "upsert_venue_layout",
            "table": f"{PBC_KEY}_venue",
            "required_fields": ("venue_id", "venue_name", "venue_type", "zones"),
            "persona": "venue_ops_manager",
        },
        {
            "key": "EventCalendarForm",
            "operation": "schedule_event_calendar",
            "table": f"{PBC_KEY}_event_calendar",
            "required_fields": ("event_id", "event_name", "event_type", "event_date"),
            "persona": "booking_manager",
        },
        {
            "key": "IngressEgressPlanForm",
            "operation": "coordinate_ingress_plan",
            "table": f"{PBC_KEY}_ingress_plan",
            "required_fields": ("event_id", "gate_plan", "egress_routes"),
            "persona": "guest_experience_lead",
        },
        {
            "key": "SecurityAndCrowdForm",
            "operation": "publish_security_plan",
            "table": f"{PBC_KEY}_security_plan",
            "required_fields": ("event_id", "security_level", "screening_lanes"),
            "persona": "security_lead",
        },
        {
            "key": "RevenueAttendanceForm",
            "operation": "capture_revenue_attendance_snapshot",
            "table": f"{PBC_KEY}_revenue_attendance_snapshot",
            "required_fields": ("event_id", "attendance", "gross_revenue"),
            "persona": "finance_ops_partner",
        },
    )
    return {"ok": True, "contracts": contracts, "side_effects": ()}


def sports_venue_event_operations_wizard_contracts():
    contracts = (
        {
            "key": "EventCommandSetupWizard",
            "operation": "schedule_event_calendar",
            "keywords": ("schedule", "calendar", "event", "turnover"),
            "steps": ("calendar", "ingress", "staffing", "security", "production"),
        },
        {
            "key": "WeatherDelayResponseWizard",
            "operation": "manage_weather_delay",
            "keywords": ("weather", "delay", "lightning", "heat", "wind"),
            "steps": ("watch", "decision", "messaging", "restart"),
        },
        {
            "key": "IncidentCommandWizard",
            "operation": "open_event_incident",
            "keywords": ("incident", "emergency", "crowd", "medical"),
            "steps": ("dispatch", "command", "evidence", "closure"),
        },
        {
            "key": "AccessibilityAssistanceWizard",
            "operation": "resolve_accessibility_request",
            "keywords": ("accessibility", "ada", "relocation", "captioning"),
            "steps": ("intake", "routing", "fulfillment", "closeout"),
        },
        {
            "key": "BroadcastAndSponsorReadinessWizard",
            "operation": "confirm_production_readiness",
            "keywords": ("broadcast", "compound", "camera", "sponsor", "activation"),
            "steps": ("compound", "show", "sponsor", "approval"),
        },
    )
    return {"ok": True, "contracts": contracts, "side_effects": ()}


def sports_venue_event_operations_control_contracts():
    controls = (
        {
            "key": "GateOpenControl",
            "permission": "sports_venue_event_operations.update",
            "supports_roles": ("operator", "guest_experience_lead"),
        },
        {
            "key": "WeatherHoldControl",
            "permission": "sports_venue_event_operations.approve",
            "supports_roles": ("event_commander", "security_lead"),
        },
        {
            "key": "EmergencyActivationControl",
            "permission": "sports_venue_event_operations.admin",
            "supports_roles": ("event_commander",),
        },
        {
            "key": "SeatKillApprovalControl",
            "permission": "sports_venue_event_operations.approve",
            "supports_roles": ("operator", "guest_experience_lead"),
        },
    )
    return {"ok": True, "controls": controls, "side_effects": ()}


def sports_venue_event_operations_standalone_workbench_blueprint():
    forms = sports_venue_event_operations_form_contracts()
    wizards = sports_venue_event_operations_wizard_contracts()
    controls = sports_venue_event_operations_control_contracts()
    return {
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "forms": forms["contracts"],
        "wizards": wizards["contracts"],
        "controls": controls["controls"],
        "panels": (
            "event_calendar",
            "gate_and_queue_monitor",
            "staffing_and_credentials",
            "security_and_incidents",
            "weather_and_emergency",
            "broadcast_sponsor_and_turnover",
            "attendance_and_revenue",
        ),
        "personas": (
            "operator",
            "security_lead",
            "guest_experience_lead",
            "premium_services_lead",
            "event_commander",
        ),
        "side_effects": (),
    }


def sports_venue_event_operations_ui_contract():
    surface = domain_capability_surface_contract()
    blueprint = sports_venue_event_operations_standalone_workbench_blueprint()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "SportsVenueEventOperationsWorkbench",
            "SportsVenueEventOperationsDetail",
            "SportsVenueEventOperationsAssistantPanel",
            "SportsVenueEventOperationsSupervisorMobile",
        ),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "sports_venue_event_operations.read",
            "sports_venue_event_operations.create",
            "sports_venue_event_operations.update",
            "sports_venue_event_operations.approve",
            "sports_venue_event_operations.admin",
        ),
        "forms": blueprint["forms"],
        "wizards": blueprint["wizards"],
        "controls": blueprint["controls"],
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{operation}" for operation in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "overview",
                "operations",
                "edge_case_triage",
                "advanced_intelligence",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def sports_venue_event_operations_render_workbench():
    view = sports_venue_event_operations_build_workbench_view()
    blueprint = sports_venue_event_operations_standalone_workbench_blueprint()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": view["route"],
        "operation_actions": tuple(item["operation"] for item in blueprint["forms"]),
        "table_browsers": view["tables"],
        "side_effects": (),
    }


def sports_venue_event_operations_render_standalone_workbench(workbench):
    blueprint = sports_venue_event_operations_standalone_workbench_blueprint()
    metrics = dict(workbench.get("metrics", {}))
    summary_cards = (
        {"label": "Events", "value": metrics.get("event_count", 0)},
        {"label": "Incidents", "value": metrics.get("incident_count", 0)},
        {"label": "Delays", "value": metrics.get("weather_delay_count", 0)},
        {"label": "Revenue", "value": metrics.get("gross_revenue", 0.0)},
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "summary_cards": summary_cards,
        "queue_panels": blueprint["panels"],
        "controls": tuple(control["key"] for control in blueprint["controls"]),
        "side_effects": (),
    }


def smoke_test():
    contract = sports_venue_event_operations_ui_contract()
    rendered = sports_venue_event_operations_render_workbench()
    standalone = sports_venue_event_operations_render_standalone_workbench(
        {
            "metrics": {
                "event_count": 1,
                "incident_count": 1,
                "weather_delay_count": 0,
                "gross_revenue": 125000.0,
            }
        }
    )
    return {
        "ok": contract["ok"] and rendered["ok"] and standalone["ok"],
        "side_effects": (),
    }

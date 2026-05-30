"""UI and standalone workbench contracts for smart city mobility operations."""

from __future__ import annotations

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_PARAMETERS,
    DOMAIN_RECORD_SPECS,
    DOMAIN_RULES,
    DOMAIN_WORKBENCH_VIEWS,
    PBC_KEY,
    domain_capability_surface_contract,
)


def _control_for_field(field: str) -> str:
    if field.endswith("_id") or field.endswith("_type") or field.endswith("_name"):
        return "text"
    if field.endswith("_seconds") or field.endswith("_minutes") or field.endswith("_score") or field.endswith("_db"):
        return "number"
    if field in {"channels", "languages", "modes", "movements", "time_bands", "peak_windows"}:
        return "multiselect"
    if field in {"phase_splits", "accessibility_profile", "price_schedule", "effective_window", "geofence"}:
        return "json"
    return "textarea"


def smart_city_mobility_operations_form_contracts():
    contracts = tuple(
        {
            "key": spec["form"],
            "operation": spec["operation"],
            "table": spec["table"],
            "fields": spec["required_fields"],
            "controls": tuple(
                {"field": field, "control": _control_for_field(field)} for field in spec["required_fields"]
            ),
            "permission": spec["permission"],
        }
        for spec in DOMAIN_RECORD_SPECS
    )
    return {
        "ok": bool(contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def smart_city_mobility_operations_wizard_contracts():
    contracts = (
        {
            "key": "CorridorCommandWizard",
            "keywords": ("corridor", "intersection", "signal"),
            "steps": ("corridor_intake", "intersection_mapping", "command_review"),
            "operations": ("register_corridor", "register_intersection", "author_signal_plan"),
        },
        {
            "key": "IncidentPlaybookWizard",
            "keywords": ("incident", "closure", "detour", "alert"),
            "steps": ("triage", "mitigation", "notification"),
            "operations": ("record_traffic_incident", "plan_construction_closure", "publish_public_notification"),
        },
        {
            "key": "AccessibilityProtectionWizard",
            "keywords": ("accessibility", "detour", "elevator", "curb ramp"),
            "steps": ("impact_capture", "replacement_path", "approval"),
            "operations": ("publish_accessibility_detour", "author_signal_plan"),
        },
        {
            "key": "PublicNotificationWizard",
            "keywords": ("notification", "sms", "push", "signage"),
            "steps": ("template", "audience", "approval"),
            "operations": ("publish_public_notification",),
        },
        {
            "key": "GovernedPreviewWizard",
            "keywords": ("document", "instruction", "preview", "assistant"),
            "steps": ("extract", "preview", "human_confirmation"),
            "operations": ("preview_governed_instruction",),
        },
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def smart_city_mobility_operations_ui_contract():
    surface = domain_capability_surface_contract()
    forms = smart_city_mobility_operations_form_contracts()
    wizards = smart_city_mobility_operations_wizard_contracts()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "SmartCityMobilityOperationsWorkbench",
            "SmartCityMobilityOperationsDetail",
            "SmartCityMobilityOperationsAssistantPanel",
        ),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "smart_city_mobility_operations.read",
            "smart_city_mobility_operations.create",
            "smart_city_mobility_operations.update",
            "smart_city_mobility_operations.approve",
            "smart_city_mobility_operations.admin",
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "workbench_views": DOMAIN_WORKBENCH_VIEWS,
            "forms": tuple(item["key"] for item in forms["contracts"]),
            "wizards": tuple(item["key"] for item in wizards["contracts"]),
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "corridor_command",
                "intersection_detail",
                "controls_and_wizards",
                "advanced_intelligence",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def smart_city_mobility_operations_standalone_workbench_blueprint():
    forms = smart_city_mobility_operations_form_contracts()
    wizards = smart_city_mobility_operations_wizard_contracts()
    return {
        "format": "appgen.smart-city-mobility-operations-standalone-workbench.v1",
        "ok": forms["ok"] and wizards["ok"],
        "pbc": PBC_KEY,
        "views": DOMAIN_WORKBENCH_VIEWS,
        "cards": (
            "corridor_health",
            "intersection_failures",
            "incident_and_closure_board",
            "accessibility_detours",
            "public_notifications",
            "readiness_scorecard",
        ),
        "forms": tuple(item["key"] for item in forms["contracts"]),
        "wizards": tuple(item["key"] for item in wizards["contracts"]),
        "side_effects": (),
    }


def smart_city_mobility_operations_render_standalone_workbench(workbench: dict) -> dict:
    return {
        "ok": workbench.get("ok") is True,
        "pbc": PBC_KEY,
        "layout": ("map", "table", "time_series"),
        "corridor_count": len(workbench.get("corridor_cards", ())),
        "incident_count": workbench.get("incident_count", 0),
        "planned_disruption_count": workbench.get("planned_disruption_count", 0),
        "notification_count": workbench.get("notification_count", 0),
        "quarantined_feed_count": workbench.get("quarantined_feed_count", 0),
        "readiness_green": workbench.get("readiness", {}).get("green", False),
        "side_effects": (),
    }


def smart_city_mobility_operations_render_workbench():
    ui = smart_city_mobility_operations_ui_contract()
    blueprint = smart_city_mobility_operations_standalone_workbench_blueprint()
    full = ui["full_capability_surface"]
    return {
        "ok": ui["ok"] and blueprint["ok"],
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "operation_actions": full["operation_actions"],
        "table_browsers": tuple(item["target_table"] for item in domain_capability_surface_contract()["operation_surfaces"]),
        "workbench_views": blueprint["views"],
        "side_effects": (),
    }


def smoke_test():
    ui = smart_city_mobility_operations_ui_contract()
    rendered = smart_city_mobility_operations_render_workbench()
    return {"ok": ui["ok"] and rendered["ok"], "side_effects": ()}

"""UI contract for the Transportation Management PBC."""

from __future__ import annotations

from .runtime import TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
from .runtime import TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES
from .runtime import TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES
from .runtime import TRANSPORTATION_MANAGEMENT_OWNED_TABLES
from .runtime import TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC


TRANSPORTATION_MANAGEMENT_UI_FRAGMENT_KEYS = (
    "TransportationWorkbench",
    "ShipmentCreationConsole",
    "CarrierMasterConsole",
    "CarrierSelectionBoard",
    "TenderDispatchConsole",
    "RoutePlanningMap",
    "TrackingTimeline",
    "EtaConfidencePanel",
    "InboundArrivalBoard",
    "DeliveryProofConsole",
    "TransportExceptionBoard",
    "FreightCostAccrualPanel",
    "CrossBorderDocumentPanel",
    "TemperatureHazardControlPanel",
    "CarrierScorecardView",
    "CarbonDistanceAnalyticsView",
    "TransportationRuleStudio",
    "TransportationParameterConsole",
    "TransportationConfigurationPanel",
)


def transportation_management_ui_contract() -> dict:
    return {
        "format": "appgen.transportation-management-ui-contract.v1",
        "ok": True,
        "pbc": "transportation_management",
        "implementation_directory": "src/pyAppGen/pbcs/transportation_management",
        "fragments": TRANSPORTATION_MANAGEMENT_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/transportation_management",
            "/workbench/pbcs/transportation_management/shipments",
            "/workbench/pbcs/transportation_management/carriers",
            "/workbench/pbcs/transportation_management/selection",
            "/workbench/pbcs/transportation_management/tenders",
            "/workbench/pbcs/transportation_management/routes",
            "/workbench/pbcs/transportation_management/tracking",
            "/workbench/pbcs/transportation_management/eta",
            "/workbench/pbcs/transportation_management/arrival",
            "/workbench/pbcs/transportation_management/delivery",
            "/workbench/pbcs/transportation_management/exceptions",
            "/workbench/pbcs/transportation_management/freight-costs",
            "/workbench/pbcs/transportation_management/cross-border",
            "/workbench/pbcs/transportation_management/controls",
            "/workbench/pbcs/transportation_management/scorecards",
            "/workbench/pbcs/transportation_management/carbon",
            "/workbench/pbcs/transportation_management/rules",
            "/workbench/pbcs/transportation_management/parameters",
            "/workbench/pbcs/transportation_management/configuration",
        ),
        "panels": (
            {
                "key": "shipment_execution",
                "fragment": "ShipmentCreationConsole",
                "binds_to": ("shipment", "route", "carrier", "outbox"),
                "commands": ("create_shipment", "select_carrier", "plan_route", "dispatch_shipment"),
            },
            {
                "key": "tracking",
                "fragment": "TrackingTimeline",
                "binds_to": ("tracking_event", "eta", "exception", "delivery_proof"),
                "commands": ("record_tracking_event", "calculate_eta", "confirm_inbound_arrival", "confirm_delivery"),
            },
            {
                "key": "freight_finance",
                "fragment": "FreightCostAccrualPanel",
                "binds_to": ("route_cost", "carrier_rate", "accrual", "variance"),
                "commands": ("simulate_carrier_route", "optimize_route_carrier", "allocate_carrier_tender"),
            },
            {
                "key": "risk_control",
                "fragment": "TransportExceptionBoard",
                "binds_to": ("risk_score", "policy_screening", "control_test", "dead_letter"),
                "commands": ("recommend_exception_resolution", "screen_policy", "run_control_tests"),
            },
            {
                "key": "governance",
                "fragment": "TransportationRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": {
            "register_carrier": "transportation_management.master",
            "create_shipment": "transportation_management.plan",
            "select_carrier": "transportation_management.tender",
            "plan_route": "transportation_management.plan",
            "dispatch_shipment": "transportation_management.dispatch",
            "record_tracking_event": "transportation_management.track",
            "calculate_eta": "transportation_management.track",
            "confirm_inbound_arrival": "transportation_management.confirm",
            "confirm_delivery": "transportation_management.confirm",
            "receive_event": "transportation_management.event",
            "simulate_carrier_route": "transportation_management.audit",
            "optimize_route_carrier": "transportation_management.tender",
            "allocate_carrier_tender": "transportation_management.tender",
            "screen_policy": "transportation_management.audit",
            "run_control_tests": "transportation_management.audit",
            "register_rule": "transportation_management.configure",
            "register_schema_extension": "transportation_management.configure",
            "set_parameter": "transportation_management.configure",
            "configure_runtime": "transportation_management.configure",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "allowed_modes"),
            "allowed_database_backends": TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "fixed_event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "max_cost_per_mile",
                "on_time_weight",
                "carbon_weight",
                "service_level_weight",
                "tracking_staleness_minutes",
                "eta_confidence_threshold",
                "tender_timeout_minutes",
                "consolidation_threshold",
                "delay_risk_threshold",
                "exception_escalation_minutes",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("carrier_selection", "lane", "hazard", "temperature", "cross_border", "tender", "delivery_proof", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES,
            "consumes": TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": TRANSPORTATION_MANAGEMENT_OWNED_TABLES,
            "outbox_table": "transportation_management_appgen_outbox_event",
            "inbox_table": "transportation_management_appgen_inbox_event",
            "dead_letter_table": "transportation_management_dead_letter_event",
            "rbac_permissions": (
                "transportation_management.read",
                "transportation_management.master",
                "transportation_management.plan",
                "transportation_management.tender",
                "transportation_management.dispatch",
                "transportation_management.track",
                "transportation_management.confirm",
                "transportation_management.event",
                "transportation_management.configure",
                "transportation_management.audit",
            ),
        },
    }


def transportation_management_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = transportation_management_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    shipments = tuple(shipment for shipment in state["shipments"].values() if shipment["tenant"] == tenant)
    carriers = tuple(carrier for carrier in state["carriers"].values() if carrier["tenant"] == tenant)
    routes = tuple(route for route in state["routes"].values() if route["tenant"] == tenant)
    tracking = tuple(event for event in state["tracking_events"].values() if event["tenant"] == tenant)
    cards = (
        {"key": "shipments", "value": len(shipments), "fragment": "ShipmentCreationConsole"},
        {"key": "delivered", "value": len(tuple(shipment for shipment in shipments if shipment["status"] == "delivered")), "fragment": "DeliveryProofConsole"},
        {"key": "carriers", "value": len(carriers), "fragment": "CarrierMasterConsole"},
        {"key": "routes", "value": len(routes), "fragment": "RoutePlanningMap"},
        {"key": "tracking_events", "value": len(tracking), "fragment": "TrackingTimeline"},
        {"key": "estimated_cost", "value": round(sum(route["estimated_cost"] for route in routes), 2), "fragment": "FreightCostAccrualPanel"},
        {"key": "estimated_carbon", "value": round(sum(route["estimated_carbon"] for route in routes), 2), "fragment": "CarbonDistanceAnalyticsView"},
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "TransportationRuleStudio"},
    )
    return {
        "format": "appgen.transportation-management-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/transportation_management",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": TRANSPORTATION_MANAGEMENT_OWNED_TABLES,
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
            },
            "outbox_table": "transportation_management_appgen_outbox_event",
            "inbox_table": "transportation_management_appgen_inbox_event",
            "dead_letter_table": "transportation_management_dead_letter_event",
            "rbac_permissions": contract["binding_evidence"]["rbac_permissions"],
        },
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = transportation_management_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = transportation_management_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }


TRANSPORTATION_MANAGEMENT_FORM_KEYS = (
    "shipment_creation_form",
    "carrier_registration_form",
    "route_planning_form",
    "dispatch_tracking_form",
    "delivery_proof_form",
    "transportation_governance_form",
)
TRANSPORTATION_MANAGEMENT_WIZARD_KEYS = (
    "ship_to_deliver_wizard",
    "carrier_onboarding_wizard",
    "exception_resolution_wizard",
    "cross_border_freight_wizard",
)
TRANSPORTATION_MANAGEMENT_CONTROL_KEYS = (
    "tenant_scope_picker",
    "carrier_lane_map",
    "route_cost_carbon_meter",
    "tracking_timeline_control",
    "eta_confidence_meter",
    "event_reliability_drawer",
    "assistant_skill_panel",
)


def transportation_management_form_catalog() -> tuple[dict, ...]:
    return (
        {"key": "shipment_creation_form", "title": "Shipment Creation", "command": "create_shipment", "owned_table": "shipment", "fields": ("shipment_id", "tenant", "source_ref", "origin", "destination", "weight", "mode", "service_level", "hazmat", "temperature_controlled")},
        {"key": "carrier_registration_form", "title": "Carrier Registration", "command": "register_carrier", "owned_table": "carrier", "fields": ("carrier_id", "tenant", "mode", "service_levels", "lanes", "cost_per_mile", "on_time_rate", "carbon_per_mile", "risk", "identity")},
        {"key": "route_planning_form", "title": "Route Planning", "command": "plan_route", "owned_table": "freight_route", "fields": ("shipment_id", "distance_miles", "stops", "constraints", "carbon_target")},
        {"key": "dispatch_tracking_form", "title": "Dispatch and Tracking", "command": "record_tracking_event", "owned_table": "tracking_event", "fields": ("shipment_id", "tender_id", "event_id", "location", "distance_remaining", "delay_minutes")},
        {"key": "delivery_proof_form", "title": "Delivery Proof", "command": "confirm_delivery", "owned_table": "delivery_proof", "fields": ("shipment_id", "facility", "proof_id", "public_claims", "exception_code")},
        {"key": "transportation_governance_form", "title": "Transportation Governance", "command": "register_rule", "owned_table": "transportation_rule", "fields": ("rule_id", "tenant", "rule_type", "allowed_modes", "preferred_carriers", "restricted_carriers", "hazmat_allowed", "status")},
    )


def transportation_management_wizard_catalog() -> tuple[dict, ...]:
    return (
        {"key": "ship_to_deliver_wizard", "steps": ("shipment_creation_form", "carrier_registration_form", "route_planning_form", "dispatch_tracking_form", "delivery_proof_form"), "goal": "Create, tender, route, dispatch, track, and confirm one shipment through owned TMS tables."},
        {"key": "carrier_onboarding_wizard", "steps": ("carrier_registration_form", "transportation_governance_form"), "goal": "Validate carrier identity, lanes, service levels, risk, carbon, and contract readiness."},
        {"key": "exception_resolution_wizard", "steps": ("dispatch_tracking_form", "delivery_proof_form"), "goal": "Resolve delay, tracking silence, damage, and delivery-proof exceptions with audit evidence."},
        {"key": "cross_border_freight_wizard", "steps": ("shipment_creation_form", "route_planning_form", "delivery_proof_form"), "goal": "Coordinate cross-border freight documents, route constraints, and arrival proof."},
    )


def transportation_management_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "carrier_lane_map", "type": "map", "binds_to": "carrier_lane"},
        {"key": "route_cost_carbon_meter", "type": "meter", "binds_to": "freight_route"},
        {"key": "tracking_timeline_control", "type": "timeline", "binds_to": "tracking_event"},
        {"key": "eta_confidence_meter", "type": "meter", "binds_to": "eta_snapshot"},
        {"key": "event_reliability_drawer", "type": "drawer", "binds_to": "event_reliability"},
        {"key": "assistant_skill_panel", "type": "assistant", "binds_to": "transportation_management_skills"},
    )


def transportation_management_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": "transportation_management",
        "app_id": "transportation_management_one_pbc_app",
        "workbench_route": "/workbench/pbcs/transportation_management",
        "navigation": (
            {"key": "shipments", "route": "/workbench/pbcs/transportation_management/shipments"},
            {"key": "carriers", "route": "/workbench/pbcs/transportation_management/carriers"},
            {"key": "routes", "route": "/workbench/pbcs/transportation_management/routes"},
            {"key": "tracking", "route": "/workbench/pbcs/transportation_management/tracking"},
            {"key": "delivery", "route": "/workbench/pbcs/transportation_management/delivery"},
            {"key": "governance", "route": "/workbench/pbcs/transportation_management/configuration"},
        ),
        "forms": TRANSPORTATION_MANAGEMENT_FORM_KEYS,
        "wizards": TRANSPORTATION_MANAGEMENT_WIZARD_KEYS,
        "controls": TRANSPORTATION_MANAGEMENT_CONTROL_KEYS,
        "single_agent_namespace": "transportation_management_skills",
        "side_effects": (),
    }


def transportation_management_ui_contract() -> dict:
    shell = transportation_management_standalone_app_contract()
    return {
        "format": "appgen.transportation-management-ui-contract.v1",
        "ok": True,
        "pbc": "transportation_management",
        "implementation_directory": "src/pyAppGen/pbcs/transportation_management",
        "fragments": TRANSPORTATION_MANAGEMENT_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in shell["navigation"]) + (shell["workbench_route"],),
        "panels": (
            {"key": "shipment_execution", "fragment": "ShipmentCreationConsole", "binds_to": ("shipment", "route", "carrier", "outbox"), "commands": ("create_shipment", "select_carrier", "plan_route", "dispatch_shipment")},
            {"key": "tracking", "fragment": "TrackingTimeline", "binds_to": ("tracking_event", "eta", "exception", "delivery_proof"), "commands": ("record_tracking_event", "calculate_eta", "confirm_inbound_arrival", "confirm_delivery")},
            {"key": "freight_finance", "fragment": "FreightCostAccrualPanel", "binds_to": ("route_cost", "carrier_rate", "accrual", "variance"), "commands": ("simulate_carrier_route", "optimize_route_carrier", "allocate_carrier_tender")},
            {"key": "risk_control", "fragment": "TransportExceptionBoard", "binds_to": ("risk_score", "policy_screening", "control_test", "dead_letter"), "commands": ("recommend_exception_resolution", "screen_policy", "run_control_tests")},
            {"key": "governance", "fragment": "TransportationRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime")},
        ),
        "forms": transportation_management_form_catalog(),
        "wizards": transportation_management_wizard_catalog(),
        "controls": transportation_management_control_catalog(),
        "standalone_app": shell,
        "action_permissions": {
            "register_carrier": "transportation_management.master",
            "create_shipment": "transportation_management.plan",
            "select_carrier": "transportation_management.tender",
            "plan_route": "transportation_management.plan",
            "dispatch_shipment": "transportation_management.dispatch",
            "record_tracking_event": "transportation_management.track",
            "calculate_eta": "transportation_management.track",
            "confirm_inbound_arrival": "transportation_management.confirm",
            "confirm_delivery": "transportation_management.confirm",
            "receive_event": "transportation_management.event",
            "screen_policy": "transportation_management.audit",
            "run_control_tests": "transportation_management.audit",
            "register_rule": "transportation_management.configure",
            "register_schema_extension": "transportation_management.configure",
            "set_parameter": "transportation_management.configure",
            "configure_runtime": "transportation_management.configure",
        },
        "configuration_editor": {"required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "allowed_modes"), "allowed_database_backends": TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "fixed_event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "user_selectable_event_contract": False},
        "parameter_editor": {"numeric_parameters": ("max_cost_per_mile", "on_time_weight", "carbon_weight", "service_level_weight", "tracking_staleness_minutes", "eta_confidence_threshold", "tender_timeout_minutes", "consolidation_threshold", "delay_risk_threshold", "exception_escalation_minutes", "workbench_limit"), "bounded_supported_parameters": True},
        "rule_editor": {"rule_types": ("carrier_selection", "lane", "hazard", "temperature", "cross_border", "tender", "delivery_proof", "release_gate"), "required_fields": ("rule_id", "tenant", "scope", "status"), "compiled_evidence_required": True},
        "event_surfaces": {"emits": TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES, "consumes": TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES, "outbox_status": "visible", "inbox_status": "visible", "dead_letter_status": "visible"},
        "binding_evidence": {"owned_tables": TRANSPORTATION_MANAGEMENT_OWNED_TABLES, "outbox_table": "transportation_management_appgen_outbox_event", "inbox_table": "transportation_management_appgen_inbox_event", "dead_letter_table": "transportation_management_dead_letter_event", "shared_table_access": False, "required_event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC, "rbac_permissions": ("transportation_management.read", "transportation_management.master", "transportation_management.plan", "transportation_management.tender", "transportation_management.dispatch", "transportation_management.track", "transportation_management.confirm", "transportation_management.event", "transportation_management.configure", "transportation_management.audit")},
    }


def transportation_management_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...], repository_snapshot: dict | None = None) -> dict:
    contract = transportation_management_ui_contract()
    shell = transportation_management_standalone_app_contract()
    from .runtime import transportation_management_build_workbench_view

    snapshot = transportation_management_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    return {
        "format": "appgen.transportation-management-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "fragments": contract["fragments"],
        "navigation": shell["navigation"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cards": (
            {"key": "shipments", "value": snapshot["shipment_count"], "fragment": "ShipmentCreationConsole"},
            {"key": "delivered", "value": snapshot["delivered_count"], "fragment": "DeliveryProofConsole"},
            {"key": "carriers", "value": snapshot["carrier_count"], "fragment": "CarrierMasterConsole"},
            {"key": "routes", "value": snapshot["route_count"], "fragment": "RoutePlanningMap"},
            {"key": "tracking_events", "value": snapshot["tracking_count"], "fragment": "TrackingTimeline"},
            {"key": "estimated_cost", "value": round(sum(route.get("estimated_cost", 0) for route in state.get("routes", {}).values() if route.get("tenant") == tenant), 2), "fragment": "FreightCostAccrualPanel"},
            {"key": "estimated_carbon", "value": round(sum(route.get("estimated_carbon", 0) for route in state.get("routes", {}).values() if route.get("tenant") == tenant), 2), "fragment": "CarbonDistanceAnalyticsView"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": snapshot["configuration_bound"],
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": snapshot["inbox_count"],
        "dead_letter_count": snapshot["dead_letter_count"],
        "binding_evidence": contract["binding_evidence"],
        "repository_snapshot": repository_snapshot,
        "workbench": snapshot,
    }


def transportation_management_render_standalone_app(state: dict, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
    contract = transportation_management_ui_contract()
    permissions = principal_permissions or tuple(sorted(set(contract["action_permissions"].values())))
    rendered = transportation_management_render_workbench(state, tenant=tenant, principal_permissions=permissions)
    return {"ok": rendered["ok"], "pbc": "transportation_management", "shell": transportation_management_standalone_app_contract(), "workbench": rendered, "side_effects": ()}


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = transportation_management_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = transportation_management_render_workbench(_appgen_smoke_state(), tenant="smoke", principal_permissions=permissions)
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {"rule_types": ("configuration", "parameter", "release_gate"), "required_fields": ("rule_id", "scope", "status")}
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {"configuration_editor": configuration_editor, "parameter_editor": contract.get("parameter_editor", {}), "rule_editor": rule_editor, "event_surfaces": event_surfaces, "binding_evidence": binding_evidence}
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True and rendered.get("ok") is True and bool(contract.get("fragments")) and bool(contract.get("routes")) and bool(contract.get("forms")) and bool(contract.get("wizards")) and bool(contract.get("controls")) and bool(cards) and bool(contract.get("action_permissions")) and bool(configuration_editor) and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False and bool(contract.get("parameter_editor")) and bool(rule_editor) and bool(event_surfaces) and ("outbox_status" in event_surfaces or "contract" in event_surfaces) and binding_evidence.get("shared_table_access") is not True and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ()), "forms": tuple(item["key"] for item in contract.get("forms", ())), "wizards": tuple(item["key"] for item in contract.get("wizards", ())), "controls": tuple(item["key"] for item in contract.get("controls", ()))},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }

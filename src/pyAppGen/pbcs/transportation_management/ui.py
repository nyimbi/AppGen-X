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

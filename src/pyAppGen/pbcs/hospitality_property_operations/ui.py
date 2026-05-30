"""UI contracts and render helpers for the hospitality standalone slice."""

from __future__ import annotations

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    DOMAIN_WORKBENCH_VIEWS,
    domain_capability_surface_contract,
    workflow_catalog,
)

PBC_KEY = "hospitality_property_operations"


def hospitality_property_operations_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "HospitalityPropertyOperationsWorkbench",
            "HospitalityPropertyOperationsDetail",
            "HospitalityPropertyOperationsAssistantPanel",
        ),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "hospitality_property_operations.read",
            "hospitality_property_operations.create",
            "hospitality_property_operations.update",
            "hospitality_property_operations.approve",
            "hospitality_property_operations.admin",
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": ("overview", "arrivals", "rooms", "service_recovery", "revenue_control", "release_evidence"),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def hospitality_property_operations_assistant_panel_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "quick_prompts": (
            "Which arrivals are blocked by unsellable rooms?",
            "Show urgent guest requests that need service recovery.",
            "Summarize blocked rooms for shift handover.",
            "Explain why a rate plan should close to arrival tonight.",
        ),
        "workflow_shortcuts": tuple(item["workflow"] for item in workflow_catalog()),
        "side_effects": (),
    }


def hospitality_property_operations_standalone_workbench_blueprint() -> dict:
    from .routes import standalone_route_contracts

    routes = standalone_route_contracts()["routes"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "lanes": tuple({"view": name, "label": name.replace("_", " ").title()} for name in DOMAIN_WORKBENCH_VIEWS),
        "forms": tuple(
            {
                "name": route["form"],
                "method": route["method"],
                "path": route["path"],
                "permission": route["permission"],
            }
            for route in routes
            if route["form"]
        ),
        "wizards": (
            {
                "name": "ArrivalTurnaroundWizard",
                "steps": ("ReservationIntakeForm", "HousekeepingDispatchForm", "InspectionReleaseControl", "CheckInControl"),
            },
            {
                "name": "ServiceRecoveryWizard",
                "steps": ("GuestRequestForm", "RoomMoveForm", "GuestRequestResolutionControl"),
            },
            {
                "name": "RevenueControlWizard",
                "steps": ("OccupancySnapshotControl", "RateFenceForm"),
            },
        ),
        "controls": (
            {"name": "RoomSellableStateControl", "rule": "room_sellable_state"},
            {"name": "AccessibleAssignmentGuard", "rule": "accessible_assignment_guard"},
            {"name": "OverbookingRiskDial", "rule": "overbooking_limit"},
            {"name": "ShiftHandoverPacket", "workflow": "shift_handover"},
        ),
        "assistant_panel": hospitality_property_operations_assistant_panel_contract(),
        "side_effects": (),
    }


def hospitality_property_operations_render_workbench(view: dict | None = None) -> dict:
    blueprint = hospitality_property_operations_standalone_workbench_blueprint()
    view = dict(view or {})
    lane_summary = view.get(
        "lane_summary",
        {
            "arrivals": 0,
            "in_house": 0,
            "departures": 0,
            "room_ready_gaps": 0,
            "exceptions": 0,
            "service_recovery": 0,
        },
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "summary_cards": tuple({"metric": key, "value": value} for key, value in lane_summary.items()),
        "lanes": tuple(
            {
                "name": lane["view"],
                "label": lane["label"],
                "count": lane_summary.get(lane["view"].replace("_lane", ""), lane_summary.get(lane["view"], 0)),
            }
            for lane in blueprint["lanes"]
        ),
        "assistant_panel": blueprint["assistant_panel"],
        "side_effects": (),
    }


def hospitality_property_operations_render_room_detail(detail: dict | None = None) -> dict:
    detail = dict(detail or {})
    room = detail.get("room", {})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "header": {
            "room_id": room.get("room_id"),
            "room_number": room.get("room_number"),
            "room_class": room.get("room_class"),
            "sellable_status": room.get("sellable_status"),
        },
        "sections": (
            "room_state",
            "housekeeping_history",
            "guest_requests",
            "active_stay",
            "event_timeline",
        ),
        "side_effects": (),
    }


def smoke_test() -> dict:
    rendered = hospitality_property_operations_render_workbench({"lane_summary": {"arrivals": 2, "exceptions": 1}})
    detail = hospitality_property_operations_render_room_detail({"room": {"room_id": "rm_101", "room_number": "101"}})
    return {
        "ok": hospitality_property_operations_ui_contract()["ok"]
        and hospitality_property_operations_standalone_workbench_blueprint()["ok"]
        and hospitality_property_operations_assistant_panel_contract()["ok"]
        and rendered["ok"]
        and detail["ok"],
        "side_effects": (),
    }


# Improve1 hospitality hotel UI control extension.
from .hospitality_control import improve1_hospitality_control_contract as hospitality_property_operations_improve1_hospitality_control_contract

_HOSPITALITY_PROPERTY_OPERATIONS_BASE_UI_CONTRACT = hospitality_property_operations_ui_contract
_HOSPITALITY_PROPERTY_OPERATIONS_BASE_RENDER_WORKBENCH = hospitality_property_operations_render_workbench


def hospitality_property_operations_ui_contract() -> dict:
    base = dict(_HOSPITALITY_PROPERTY_OPERATIONS_BASE_UI_CONTRACT())
    hospitality_control = hospitality_property_operations_improve1_hospitality_control_contract()
    control_panels = tuple(item['evidence']['ui_surface'] for item in hospitality_control['capabilities'])
    service_actions = tuple(item['evidence']['service_api'] for item in hospitality_control['capabilities'])
    full_surface = dict(base.get('full_capability_surface', {}))
    full_surface.update({
        'hospitality_control_panels': control_panels,
        'hospitality_control_service_actions': service_actions,
        'hospitality_control_tables': hospitality_control['owned_tables'],
        'hospitality_control_agent_tools': tuple(f"hospitality_property_operations.agent.{item['slug']}" for item in hospitality_control['capabilities']),
    })
    return {**base, 'ok': base.get('ok') is True and hospitality_control['ok'], 'full_capability_surface': full_surface, 'hospitality_control_contract': hospitality_control, 'hospitality_control_panels': control_panels, 'hospitality_control_service_actions': service_actions, 'side_effects': ()}


def hospitality_property_operations_render_workbench(view: dict | None = None) -> dict:
    base = dict(_HOSPITALITY_PROPERTY_OPERATIONS_BASE_RENDER_WORKBENCH(view=view))
    hospitality_control = hospitality_property_operations_improve1_hospitality_control_contract()
    panels = tuple(item['evidence']['ui_surface'] for item in hospitality_control['capabilities'])
    return {**base, 'ok': base.get('ok') is True and hospitality_control['ok'], 'hospitality_control_panels': panels, 'hospitality_control_service_actions': tuple(item['evidence']['service_api'] for item in hospitality_control['capabilities']), 'agent_tools': tuple(f"hospitality_property_operations.agent.{item['slug']}" for item in hospitality_control['capabilities']), 'side_effects': ()}

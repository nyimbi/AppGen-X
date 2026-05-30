"""UI/workbench contract for hotel_revenue_management."""

from __future__ import annotations

from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import domain_capability_surface_contract
from .runtime import PBC_KEY
from .runtime import hotel_revenue_management_build_workbench_view
from .runtime import hotel_revenue_management_empty_state


FORMS = (
    {
        "id": "sellable_inventory_matrix",
        "label": "Sellable Inventory Matrix",
        "fields": (
            "hotel_id",
            "code",
            "physical_rooms",
            "maintenance_holdback",
            "complimentary_allotment",
            "capacity_adults",
            "capacity_children",
            "substitution_targets",
        ),
    },
    {
        "id": "rate_plan_fence_form",
        "label": "Rate Plan Fence Form",
        "fields": (
            "room_type_id",
            "code",
            "base_rate",
            "derived_discount_pct",
            "min_los",
            "max_los",
            "member_fence",
            "cancellation_policy",
        ),
    },
    {
        "id": "forecast_override_form",
        "label": "Forecast Override Form",
        "fields": (
            "room_type_id",
            "stay_date",
            "transient_demand",
            "corporate_demand",
            "group_demand",
            "manual_override_rooms",
            "override_reason",
            "approved_by",
        ),
    },
    {
        "id": "overbooking_guardrail_form",
        "label": "Overbooking Guardrail Form",
        "fields": (
            "room_type_id",
            "date_class",
            "overbook_limit",
            "walk_cost",
            "no_show_rate",
            "cancellation_rate",
            "arrival_protection_pct",
        ),
    },
)
WIZARDS = (
    {
        "id": "compression_night_playbook",
        "label": "Compression Night Playbook",
        "steps": (
            "review_forecast",
            "review_channel_inventory",
            "recommend_rate_move",
            "confirm_restrictions",
        ),
    },
    {
        "id": "publish_readiness",
        "label": "Publish Readiness Wizard",
        "steps": ("validate_bar_ladder", "check_channel_parity", "check_rule_assertions", "approve_release"),
    },
    {
        "id": "channel_stop_sell",
        "label": "Channel Stop-Sell Wizard",
        "steps": ("inspect_allotment", "select_channel_scope", "capture_reason", "confirm_release_back_rule"),
    },
)
CONTROLS = (
    "BarLadderValidator",
    "RateInheritanceGraph",
    "ParityExceptionQueue",
    "SellableInventoryHeatmap",
    "SnapshotLineagePanel",
)


def hotel_revenue_management_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "HotelRevenueManagementWorkbench",
            "HotelRevenueManagementDetail",
            "HotelRevenueManagementAssistantPanel",
        ),
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "hotel_revenue_management.read",
            "hotel_revenue_management.create",
            "hotel_revenue_management.update",
            "hotel_revenue_management.approve",
            "hotel_revenue_management.admin",
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "overview",
                "inventory_and_rates",
                "distribution_and_forecast",
                "yield_and_release",
                "advanced_intelligence",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def hotel_revenue_management_render_workbench(
    state: dict | None = None, tenant: str = "default"
) -> dict:
    runtime_state = hotel_revenue_management_empty_state() if state is None else state
    view = hotel_revenue_management_build_workbench_view(runtime_state, tenant)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": view["route"],
        "fragments": hotel_revenue_management_ui_contract()["fragments"],
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "metrics": view["binding_evidence"]["metrics"],
        "queues": view["binding_evidence"]["queues"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    ui = hotel_revenue_management_ui_contract()
    workbench = hotel_revenue_management_render_workbench()
    return {
        "ok": ui["ok"] and workbench["ok"] and bool(ui["forms"]) and bool(workbench["controls"]),
        "side_effects": (),
    }

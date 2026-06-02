"""Standalone one-PBC application composition for hotel_revenue_management."""

from __future__ import annotations

from . import agent
from . import events
from . import permissions
from . import routes
from . import seed_data
from . import services
from . import ui
from .manifest import PBC_MANIFEST
from .release_evidence import build_release_evidence
from .runtime import PBC_KEY
from .runtime import hotel_revenue_management_approve_demand_forecast
from .runtime import hotel_revenue_management_approve_hotel_revenue_management_runtime_parameter
from .runtime import hotel_revenue_management_build_workbench_view
from .runtime import hotel_revenue_management_configure_runtime
from .runtime import hotel_revenue_management_create_room_type
from .runtime import hotel_revenue_management_create_yield_decision
from .runtime import hotel_revenue_management_empty_state
from .runtime import hotel_revenue_management_record_hotel_revenue_management_governed_model
from .runtime import hotel_revenue_management_record_rate_plan
from .runtime import hotel_revenue_management_record_revenue_snapshot
from .runtime import hotel_revenue_management_review_channel_inventory
from .runtime import hotel_revenue_management_review_hotel_revenue_management_policy_rule
from .runtime import hotel_revenue_management_simulate_overbooking_policy


def standalone_workflow_catalog() -> tuple[dict, ...]:
    return (
        {
            "workflow_id": "hotel_revenue_management_foundation_bootstrap",
            "label": "Foundation Bootstrap",
            "steps": ("configure_runtime", "approve_hotel_revenue_management_runtime_parameter", "review_hotel_revenue_management_policy_rule", "create_room_type"),
            "outcome": "hotel_revenue_foundation_ready",
        },
        {
            "workflow_id": "hotel_revenue_management_rate_plan_governance",
            "label": "Rate Plan Governance",
            "steps": ("record_rate_plan", "review_channel_inventory", "approve_demand_forecast", "simulate_overbooking_policy"),
            "outcome": "publishable_rate_plan_candidate",
        },
        {
            "workflow_id": "hotel_revenue_management_compression_night_playbook",
            "label": "Compression Night Playbook",
            "steps": ("create_yield_decision", "record_revenue_snapshot", "operate_hotel_revenue_management_16"),
            "outcome": "compression_night_action_pack",
        },
        {
            "workflow_id": "hotel_revenue_management_release_readiness",
            "label": "Release Readiness",
            "steps": ("record_hotel_revenue_management_governed_model", "operate_hotel_revenue_management_15", "create_hotel_revenue_management_control_assertion"),
            "outcome": "release_ready_package_evidence",
        },
    )


def bootstrap_standalone_state() -> dict:
    state = hotel_revenue_management_empty_state()
    state = hotel_revenue_management_configure_runtime(state, seed_data.default_configuration())["state"]
    for key, value in seed_data.default_parameter_values().items():
        state = hotel_revenue_management_approve_hotel_revenue_management_runtime_parameter(
            state,
            {"tenant": "tenant_alpha", "parameter_key": key, "parameter_value": value},
        )["state"]
    for rule in seed_data.default_rules():
        state = hotel_revenue_management_review_hotel_revenue_management_policy_rule(
            state,
            {"tenant": "tenant_alpha", **rule},
        )["state"]
    for room_type in seed_data.default_room_types():
        state = hotel_revenue_management_create_room_type(state, room_type)["state"]
    for rate_plan in seed_data.default_rate_plans():
        state = hotel_revenue_management_record_rate_plan(state, rate_plan)["state"]
    for inventory in seed_data.default_channel_inventory_commands():
        state = hotel_revenue_management_review_channel_inventory(state, inventory)["state"]
    for forecast in seed_data.default_forecasts():
        state = hotel_revenue_management_approve_demand_forecast(state, forecast)["state"]
    for policy in seed_data.default_overbooking_policies():
        state = hotel_revenue_management_simulate_overbooking_policy(state, policy)["state"]
    state = hotel_revenue_management_create_yield_decision(
        state,
        {
            "tenant": "tenant_alpha",
            "hotel_id": "hotel_alpha",
            "room_type_id": "DLX",
            "rate_plan_id": "BAR",
            "forecast_id": "FC-0601",
            "overbooking_policy_id": "OB-PEAK",
            "stay_date": "2026-06-01",
            "code": "YD-0601",
        },
    )["state"]
    state = hotel_revenue_management_record_revenue_snapshot(
        state,
        {
            "tenant": "tenant_alpha",
            "hotel_id": "hotel_alpha",
            "code": "RS-0601",
            "stay_date": "2026-06-01",
            "rooms_sold": 12,
            "rooms_available": 16,
            "adr": 211.68,
            "channel_mix": {"direct": 6, "ota-1": 6},
            "source_decision_ids": ("YD-0601",),
        },
    )["state"]
    for model in seed_data.default_governed_models():
        state = hotel_revenue_management_record_hotel_revenue_management_governed_model(state, model)["state"]
    return state


def standalone_application_manifest() -> dict:
    state = bootstrap_standalone_state()
    workbench = hotel_revenue_management_build_workbench_view(state, tenant="tenant_alpha")
    return {
        "format": "appgen.hotel-revenue-management-standalone-app.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "mode": "standalone_one_pbc_app",
        "manifest": PBC_MANIFEST,
        "routes": routes.api_route_contracts(),
        "services": services.service_operation_manifest(),
        "permissions": permissions.permission_manifest(),
        "events": events.event_contract_manifest(),
        "ui": ui.hotel_revenue_management_ui_contract(),
        "agent": agent.composed_agent_contribution(),
        "release": build_release_evidence(),
        "seed": seed_data.seed_plan(),
        "workflows": standalone_workflow_catalog(),
        "bootstrap": {
            "state_digest": workbench["binding_evidence"]["metrics"]["yield_decisions"],
            "workbench": workbench,
            "compression_night_count": workbench["binding_evidence"]["metrics"]["compression_night_count"],
        },
        "side_effects": (),
    }


def validate_standalone_application() -> dict:
    app = standalone_application_manifest()
    workflow_ids = tuple(item["workflow_id"] for item in app["workflows"])
    missing_workflows = tuple(
        workflow
        for workflow in (
            "hotel_revenue_management_foundation_bootstrap",
            "hotel_revenue_management_rate_plan_governance",
            "hotel_revenue_management_compression_night_playbook",
            "hotel_revenue_management_release_readiness",
        )
        if workflow not in workflow_ids
    )
    missing_sections = tuple(
        section
        for section in ("routes", "services", "permissions", "events", "ui", "agent", "release", "seed")
        if not app.get(section)
    )
    return {
        "ok": app["ok"]
        and not missing_workflows
        and not missing_sections
        and app["bootstrap"]["workbench"]["configuration_bound"] is True,
        "pbc": PBC_KEY,
        "missing_workflows": missing_workflows,
        "missing_sections": missing_sections,
        "app": app,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_standalone_application()
    app = validation["app"]
    return {
        "ok": validation["ok"]
        and app["agent"]["ok"]
        and bool(app["ui"]["forms"])
        and bool(app["workflows"])
        and bool(app["bootstrap"]["workbench"]["binding_evidence"]["owned_tables"]),
        "validation": validation,
        "side_effects": (),
    }

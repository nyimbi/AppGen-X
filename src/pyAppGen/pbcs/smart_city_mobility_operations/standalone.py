"""Standalone one-PBC app composition for smart city mobility operations."""

from __future__ import annotations

from .agent import standalone_agent_workspace_contract
from .models import (
    SmartCityMobilityOperationsStandaloneStore,
    standalone_model_contract,
    standalone_store_smoke_test,
)
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import (
    SmartCityMobilityOperationsStandaloneService,
    standalone_service_operation_contracts,
)
from .ui import (
    smart_city_mobility_operations_render_standalone_workbench,
    smart_city_mobility_operations_standalone_workbench_blueprint,
)


def smart_city_mobility_operations_standalone_app_contract() -> dict:
    """Return the composed standalone-app surface for this one-PBC package."""
    models = standalone_model_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    ui = smart_city_mobility_operations_standalone_workbench_blueprint()
    agent = standalone_agent_workspace_contract()
    return {
        "format": "appgen.smart-city-mobility-operations-standalone-app.v1",
        "ok": all(item.get("ok") is True for item in (models, services, routes, ui, agent)),
        "pbc": "smart_city_mobility_operations",
        "models": models,
        "services": services,
        "routes": routes,
        "ui": ui,
        "agent": agent,
        "side_effects": (),
    }


def smart_city_mobility_operations_bootstrap_standalone_app() -> dict:
    """Create a live standalone store and service pair for local package use."""
    store = SmartCityMobilityOperationsStandaloneStore()
    service = SmartCityMobilityOperationsStandaloneService(store)
    return {
        "ok": True,
        "pbc": "smart_city_mobility_operations",
        "store": store,
        "service": service,
        "contract": smart_city_mobility_operations_standalone_app_contract(),
        "side_effects": (),
    }


def smart_city_mobility_operations_standalone_app_smoke() -> dict:
    """Exercise the standalone app through its route surface."""
    bundle = smart_city_mobility_operations_bootstrap_standalone_app()
    service = bundle["service"]
    try:
        corridor = dispatch_standalone_route(
            "POST",
            "/app/smart-city-mobility-operations/corridors",
            {
                "corridor_id": "c_standalone",
                "tenant": "tenant_standalone",
                "name": "Main Street Corridor",
                "functional_class": "arterial",
                "operating_objective": "bus reliability",
            },
            service=service,
        )
        intersection = dispatch_standalone_route(
            "POST",
            "/app/smart-city-mobility-operations/intersections",
            {
                "intersection_id": "i_standalone",
                "tenant": "tenant_standalone",
                "corridor_id": "c_standalone",
                "name": "Main & 5th",
                "control_mode": "adaptive",
                "movements": ("nb_through", "sb_through", "ped_crossing"),
            },
            service=service,
        )
        signal = dispatch_standalone_route(
            "POST",
            "/app/smart-city-mobility-operations/signal-plans",
            {
                "signal_plan_id": "sp_standalone",
                "tenant": "tenant_standalone",
                "corridor_id": "c_standalone",
                "intersection_id": "i_standalone",
                "plan_name": "Peak",
                "cycle_length_seconds": 92,
                "phase_splits": {"p2": 36, "p4": 18},
                "accessibility_profile": {
                    "walk_interval_seconds": 8,
                    "flashing_clearance_seconds": 19,
                },
            },
            service=service,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/smart-city-mobility-operations/workbench",
            {"tenant": "tenant_standalone"},
            service=service,
        )
        rendered = smart_city_mobility_operations_render_standalone_workbench(
            workbench["result"]["result"]
        )
        return {
            "ok": bundle["contract"]["ok"]
            and standalone_store_smoke_test()["ok"]
            and corridor["ok"]
            and intersection["ok"]
            and signal["ok"]
            and workbench["ok"]
            and rendered["ok"],
            "contract": bundle["contract"],
            "corridor": corridor,
            "intersection": intersection,
            "signal": signal,
            "workbench": workbench,
            "rendered": rendered,
            "side_effects": (),
        }
    finally:
        service.close()

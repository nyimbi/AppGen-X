"""Standalone one-PBC app composition for hospitality property operations."""

from __future__ import annotations

from .agent import standalone_agent_workspace_contract
from .models import HospitalityPropertyOperationsStandaloneStore, standalone_model_contract, standalone_store_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import HospitalityPropertyOperationsStandaloneService, standalone_service_operation_contracts
from .ui import (
    hospitality_property_operations_render_room_detail,
    hospitality_property_operations_render_workbench,
    hospitality_property_operations_standalone_workbench_blueprint,
)


def hospitality_property_operations_standalone_app_contract() -> dict:
    models = standalone_model_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    ui = hospitality_property_operations_standalone_workbench_blueprint()
    agent = standalone_agent_workspace_contract()
    return {
        "format": "appgen.hospitality-property-operations-standalone-app.v1",
        "ok": all(item.get("ok") is True for item in (models, services, routes, ui, agent)),
        "pbc": "hospitality_property_operations",
        "models": models,
        "services": services,
        "routes": routes,
        "ui": ui,
        "agent": agent,
        "side_effects": (),
    }


def hospitality_property_operations_bootstrap_standalone_app(database_path: str = ":memory:") -> dict:
    store = HospitalityPropertyOperationsStandaloneStore(database_path=database_path)
    service = HospitalityPropertyOperationsStandaloneService(store)
    return {
        "ok": True,
        "pbc": "hospitality_property_operations",
        "store": store,
        "service": service,
        "contract": hospitality_property_operations_standalone_app_contract(),
        "side_effects": (),
    }


def hospitality_property_operations_standalone_app_smoke() -> dict:
    bundle = hospitality_property_operations_bootstrap_standalone_app()
    service = bundle["service"]
    try:
        room = dispatch_standalone_route(
            "POST",
            "/app/hospitality-property-operations/rooms",
            {"room_id": "rm_app", "tenant": "tenant_app", "room_number": "401", "room_class": "suite"},
            service=service,
        )
        reservation = dispatch_standalone_route(
            "POST",
            "/app/hospitality-property-operations/reservations",
            {
                "reservation_id": "res_app",
                "tenant": "tenant_app",
                "reservation_code": "RSV-APP",
                "guest_name": "App Guest",
                "arrival_date": "2026-05-30",
                "departure_date": "2026-05-31",
                "room_class": "suite",
                "assigned_room_id": "rm_app",
            },
            service=service,
        )
        check_in = dispatch_standalone_route(
            "POST",
            "/app/hospitality-property-operations/stays/check-in",
            {"reservation_id": "res_app", "room_id": "rm_app"},
            service=service,
        )
        request = dispatch_standalone_route(
            "POST",
            "/app/hospitality-property-operations/guest-requests",
            {"request_id": "req_app", "tenant": "tenant_app", "room_id": "rm_app", "category": "complaint", "urgency": "urgent", "service_recovery": True},
            service=service,
        )
        request_done = dispatch_standalone_route(
            "POST",
            "/app/hospitality-property-operations/guest-requests/resolve",
            {"request_id": "req_app", "guest_confirmed": True},
            service=service,
        )
        snapshot = dispatch_standalone_route(
            "POST",
            "/app/hospitality-property-operations/occupancy-snapshots",
            {"tenant": "tenant_app", "stay_date": "2026-05-30"},
            service=service,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/hospitality-property-operations/workbench",
            {"tenant": "tenant_app"},
            service=service,
        )
        detail = dispatch_standalone_route(
            "GET",
            "/app/hospitality-property-operations/rooms/detail",
            {"room_id": "rm_app"},
            service=service,
        )
        rendered = hospitality_property_operations_render_workbench(workbench["result"])
        rendered_detail = hospitality_property_operations_render_room_detail(detail["result"])
        return {
            "ok": bundle["contract"]["ok"]
            and standalone_store_smoke_test()["ok"]
            and room["ok"]
            and reservation["ok"]
            and check_in["ok"]
            and request["ok"]
            and request_done["ok"]
            and snapshot["ok"]
            and workbench["ok"]
            and detail["ok"]
            and rendered["ok"]
            and rendered_detail["ok"],
            "contract": bundle["contract"],
            "room": room,
            "reservation": reservation,
            "check_in": check_in,
            "request": request,
            "request_done": request_done,
            "snapshot": snapshot,
            "workbench": workbench,
            "detail": detail,
            "rendered": rendered,
            "rendered_detail": rendered_detail,
            "side_effects": (),
        }
    finally:
        service.close()

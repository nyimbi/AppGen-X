"""Focused standalone one-PBC tests for hospitality_property_operations."""

from .. import agent, models, release_evidence, routes, services, standalone, ui


def test_standalone_store_executes_room_to_arrival_flow():
    store = models.HospitalityPropertyOperationsStandaloneStore()
    try:
        room = store.upsert_room_inventory(
            {
                "room_id": "rm_test_101",
                "tenant": "tenant_test",
                "room_number": "101",
                "room_class": "deluxe_king",
                "accessibility_features": ["roll_in_shower"],
            }
        )
        reservation = store.create_reservation(
            {
                "reservation_id": "res_test_101",
                "tenant": "tenant_test",
                "reservation_code": "RSV-101",
                "guest_name": "Ada Tester",
                "arrival_date": "2026-05-30",
                "departure_date": "2026-05-31",
                "room_class": "deluxe_king",
                "assigned_room_id": "rm_test_101",
                "accessible_required": True,
            }
        )
        stay = store.check_in_guest({"reservation_id": "res_test_101", "room_id": "rm_test_101"})
        checkout = store.check_out_guest({"stay_id": stay["stay"]["stay_id"]})
        task = store.schedule_housekeeping_task({"task_id": "hk_test_101", "tenant": "tenant_test", "room_id": "rm_test_101", "arrival_dependency": True})
        released = store.complete_housekeeping_task({"task_id": "hk_test_101", "inspector": "qa"})
        snapshot = store.capture_occupancy_snapshot({"tenant": "tenant_test", "stay_date": "2026-05-30"})
        detail = store.get_room_detail("rm_test_101")
        assert all(item["ok"] is True for item in (room, reservation, stay, checkout, task, released, snapshot, detail))
        assert detail["sellable_assessment"]["sellable"] is True
        assert snapshot["snapshot"]["same_day_turns"] >= 0
    finally:
        store.close()


def test_standalone_service_routes_ui_agent_and_release_surface():
    service = services.HospitalityPropertyOperationsStandaloneService()
    try:
        room = routes.dispatch_standalone_route(
            "POST",
            "/app/hospitality-property-operations/rooms",
            {"room_id": "rm_route_201", "tenant": "tenant_route", "room_number": "201", "room_class": "suite"},
            service=service,
        )
        reservation = routes.dispatch_standalone_route(
            "POST",
            "/app/hospitality-property-operations/reservations",
            {
                "reservation_id": "res_route_201",
                "tenant": "tenant_route",
                "reservation_code": "RSV-201",
                "guest_name": "Route Guest",
                "arrival_date": "2026-05-30",
                "departure_date": "2026-05-31",
                "room_class": "suite",
                "assigned_room_id": "rm_route_201",
            },
            service=service,
        )
        workbench = routes.dispatch_standalone_route(
            "GET",
            "/app/hospitality-property-operations/workbench",
            {"tenant": "tenant_route"},
            service=service,
        )
        rendered = ui.hospitality_property_operations_render_workbench(workbench["result"])
        document_plan = agent.document_instruction_plan(
            "arrival report",
            "prepare shift handover and fix urgent guest request for room 201",
        )
        crud_plan = agent.datastore_crud_plan(
            "create",
            "hospitality_property_operations_room_inventory",
            {"room_id": "rm_route_201"},
        )
        app_contract = standalone.hospitality_property_operations_standalone_app_contract()
        smoke = standalone.hospitality_property_operations_standalone_app_smoke()
        evidence = release_evidence.build_release_evidence()
        assert room["ok"] is True
        assert reservation["ok"] is True
        assert workbench["ok"] is True
        assert rendered["ok"] is True
        assert app_contract["ok"] is True
        assert smoke["ok"] is True
        assert document_plan["wizard_candidates"]
        assert crud_plan["route_candidates"]
        assert evidence["documentation"]["ok"] is True
        assert evidence["standalone_app"]["ok"] is True
    finally:
        service.close()


def test_workflow_helpers_cover_arrival_and_recovery_paths():
    service = services.HospitalityPropertyOperationsStandaloneService()
    try:
        arrival = service.run_arrival_turnaround_workflow(
            {
                "room": {"room_id": "rm_flow_301", "tenant": "tenant_flow", "room_number": "301", "room_class": "deluxe_king"},
                "reservation": {
                    "reservation_id": "res_flow_301",
                    "tenant": "tenant_flow",
                    "reservation_code": "RSV-301",
                    "guest_name": "Flow Guest",
                    "arrival_date": "2026-05-30",
                    "departure_date": "2026-05-31",
                    "room_class": "deluxe_king",
                    "assigned_room_id": "rm_flow_301",
                },
                "housekeeping_task": {"task_id": "hk_flow_301", "tenant": "tenant_flow", "room_id": "rm_flow_301", "arrival_dependency": True},
            }
        )
        recovery = service.run_service_recovery_workflow(
            {
                "guest_request": {"request_id": "req_flow_301", "tenant": "tenant_flow", "room_id": "rm_flow_301", "category": "complaint", "urgency": "urgent", "service_recovery": True},
                "guest_confirmed": True,
            }
        )
        revenue = service.run_revenue_control_workflow(
            {
                "tenant": "tenant_flow",
                "snapshot": {"tenant": "tenant_flow", "stay_date": "2026-05-30"},
                "rate_plan": {"rate_plan_id": "rate_flow_301", "tenant": "tenant_flow", "plan_code": "BAR", "room_class": "deluxe_king", "effective_from": "2026-05-30", "effective_to": "2026-05-31"},
            }
        )
        assert arrival["ok"] is True
        assert recovery["ok"] is True
        assert revenue["ok"] is True
    finally:
        service.close()

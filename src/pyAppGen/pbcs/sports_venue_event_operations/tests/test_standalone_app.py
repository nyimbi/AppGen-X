"""Focused standalone application tests for sports_venue_event_operations."""

from pathlib import Path

from .. import agent, audit, routes, services, standalone, ui


def _service():
    service = services.SportsVenueEventOperationsStandaloneService(tenant="tenant_alpha")
    service.configure({"database_backend": "postgresql"})
    service.register_defaults()
    service.upsert_venue_layout(
        {
            "venue_id": "venue_alpha",
            "venue_name": "Alpha Arena",
            "zones": ({"zone_id": "north", "name": "North Plaza", "gate_count": 6, "capacity": 12000},),
            "seats": ({"seat_id": "A1", "zone_id": "north", "accessible": True},),
        }
    )
    service.schedule_event(
        {
            "event_id": "event_alpha",
            "venue_id": "venue_alpha",
            "event_name": "Alpha Derby",
            "event_type": "soccer",
            "event_date": "2026-08-12",
        }
    )
    return service


def test_standalone_event_day_flow_runs_end_to_end():
    service = _service()
    ingress = service.plan_ingress_egress(
        {
            "event_id": "event_alpha",
            "gate_plan": ({"gate": "N1", "population": "general"},),
            "egress_routes": ({"route": "north_plaza"},),
            "queue_capacity": 16000,
        }
    )
    staffing = service.assign_staffing(
        {
            "event_id": "event_alpha",
            "roles": ("ushers", "security"),
            "shifts": (
                {"role": "ushers", "planned": 100, "assigned": 99},
                {"role": "security", "planned": 70, "assigned": 70},
            ),
        }
    )
    concessions = service.plan_concessions(
        {"event_id": "event_alpha", "stand_count": 20, "menu_focus": ("beer", "burgers")}
    )
    ticketing = service.coordinate_ticketing(
        {"event_id": "event_alpha", "hold_groups": ({"reason": "camera", "seats": 24},)}
    )
    credential = service.issue_credential(
        {"event_id": "event_alpha", "holder_name": "Network A", "credential_type": "broadcast", "zone_access": ("compound",)}
    )
    security = service.update_security_posture(
        {"event_id": "event_alpha", "security_level": "high", "screening_lanes": ("N1", "VIP"), "magnetometers": 8}
    )
    crowd = service.record_crowd_snapshot(
        {"event_id": "event_alpha", "zone_id": "north", "density": 0.88, "queue_minutes": 18}
    )
    incident = service.open_incident(
        {"event_id": "event_alpha", "category": "medical", "severity": "high", "location": "Section 109"}
    )
    weather = service.manage_weather_delay(
        {"event_id": "event_alpha", "hazard": "lightning", "state": "delay", "public_message": "Shelter now"}
    )
    production = service.confirm_production_ready(
        {"event_id": "event_alpha", "run_of_show": ({"segment": "anthem", "duration": 4},)}
    )
    sponsor = service.activate_sponsor(
        {"event_id": "event_alpha", "sponsor_name": "NorthBank", "activation_type": "plaza"}
    )
    turnover = service.complete_turnover(
        {"event_id": "event_alpha", "phase": "post_event_clean", "crew_status": "complete"}
    )
    accessibility = service.log_accessibility_request(
        {"event_id": "event_alpha", "request_type": "relocation", "location": "Section 102", "resolution": "resolved"}
    )
    lost_found = service.register_lost_and_found(
        {"event_id": "event_alpha", "description": "wallet", "found_location": "guest_services"}
    )
    emergency = service.start_emergency_operation(
        {"event_id": "event_alpha", "playbook": "weather_shelter", "incident_level": "level_2"}
    )
    revenue = service.record_attendance_and_revenue(
        {"event_id": "event_alpha", "attendance": 18250, "paid_attendance": 17910, "gross_revenue": 985000.0, "net_revenue": 812300.0}
    )
    snapshot = service.get_event_snapshot({"event_id": "event_alpha"})
    workbench = service.build_workbench({"event_id": "event_alpha", "role": "event_commander"})

    assert all(
        item["ok"] is True
        for item in (
            ingress,
            staffing,
            concessions,
            ticketing,
            credential,
            security,
            crowd,
            incident,
            weather,
            production,
            sponsor,
            turnover,
            accessibility,
            lost_found,
            emergency,
            revenue,
            snapshot,
            workbench,
        )
    )
    assert workbench["metrics"]["incident_count"] >= 1
    assert workbench["metrics"]["gross_revenue"] == 985000.0
    assert snapshot["snapshot"]["event"]["weather_state"] == "delay"
    service.close()


def test_routes_ui_agent_and_audit_expose_standalone_surface():
    service = _service()
    create = routes.dispatch_standalone_route(
        "POST",
        "/app/sports-venue-event-operations/weather-delays",
        {"event_id": "event_alpha", "hazard": "heat", "state": "watch"},
        service=service,
    )
    workbench = routes.dispatch_standalone_route(
        "GET",
        "/app/sports-venue-event-operations/workbench",
        {"event_id": "event_alpha", "role": "event_commander"},
        service=service,
    )
    rendered = ui.sports_venue_event_operations_render_standalone_workbench(workbench["result"])
    intake = agent.document_instruction_plan(
        "Broadcast compound note and weather deck",
        "update the weather delay workflow and prepare the broadcast readiness plan",
    )
    crud = agent.datastore_crud_plan(
        "update",
        "sports_venue_event_operations_weather_delay",
        {"state": "delay"},
    )
    package_audit = audit.run_sports_venue_event_operations_pbc_audit()

    assert create["ok"] is True
    assert workbench["ok"] is True
    assert rendered["ok"] is True
    assert intake["crud_preview"]["action"] == "update"
    assert crud["ok"] is True
    assert package_audit["ok"] is True
    service.close()


def test_standalone_smoke_and_docs_presence():
    smoke = standalone.standalone_smoke_test()
    docs = standalone.documentation_presence()

    assert smoke["ok"] is True
    assert docs["ok"] is True


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"):
        assert (base / name).exists() is True

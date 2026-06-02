"""Focused standalone one-PBC tests for smart_city_mobility_operations."""

from .. import agent, release_evidence, routes, services, standalone, ui
from ..models import SmartCityMobilityOperationsStandaloneStore


def test_standalone_store_persists_mobility_command_flows():
    store = SmartCityMobilityOperationsStandaloneStore()
    try:
        corridor = store.record_domain_item(
            "corridor_registry",
            {
                "corridor_id": "c_test",
                "tenant": "tenant_test",
                "name": "Harbor Corridor",
                "functional_class": "freight_arterial",
                "operating_objective": "balanced freight and bus flow",
            },
        )
        intersection = store.record_domain_item(
            "intersection_registry",
            {
                "intersection_id": "i_test",
                "tenant": "tenant_test",
                "corridor_id": "c_test",
                "name": "Harbor & 8th",
                "control_mode": "adaptive",
                "movements": ("eb_through", "wb_left", "ped_crossing"),
            },
        )
        signal = store.record_domain_item(
            "signal_plan",
            {
                "signal_plan_id": "sp_test",
                "tenant": "tenant_test",
                "corridor_id": "c_test",
                "intersection_id": "i_test",
                "plan_name": "Freight Peak",
                "cycle_length_seconds": 110,
                "phase_splits": {"p2": 40, "p6": 18},
                "accessibility_profile": {
                    "walk_interval_seconds": 8,
                    "flashing_clearance_seconds": 20,
                },
            },
        )
        transit_priority = store.record_domain_item(
            "transit_priority_rule_pack",
            {
                "priority_rule_id": "tp_test",
                "tenant": "tenant_test",
                "corridor_id": "c_test",
                "eligible_routes": ("BRT-1",),
                "lateness_threshold_minutes": 4,
                "occupancy_threshold": 30,
                "green_extension_limit_seconds": 12,
                "red_truncation_limit_seconds": 8,
                "blackout_conditions": ("school_crossing",),
            },
        )
        feed = store.record_domain_item(
            "mobility_sensor_feed",
            {
                "feed_id": "feed_test",
                "tenant": "tenant_test",
                "corridor_id": "c_test",
                "feed_type": "spat",
                "owner": "traffic_ops",
                "freshness_seconds": 300,
                "quality_score": 0.72,
            },
        )
        incident = store.record_domain_item(
            "traffic_incident",
            {
                "incident_id": "inc_test",
                "tenant": "tenant_test",
                "corridor_id": "c_test",
                "taxonomy_code": "signal_dark",
                "stage": "verified",
                "severity": "high",
                "impacted_modes": ("bus", "walk", "bike"),
            },
        )
        detour = store.record_domain_item(
            "accessibility_disruption",
            {
                "detour_id": "detour_test",
                "tenant": "tenant_test",
                "corridor_id": "c_test",
                "impact_type": "elevator_outage",
                "replacement_guidance": "Use south ramp via 8th Street",
                "affected_audience": ("wheelchair", "stroller"),
            },
        )
        notification = store.record_domain_item(
            "public_notification",
            {
                "notification_id": "note_test",
                "tenant": "tenant_test",
                "corridor_id": "c_test",
                "template_key": "signal_dark",
                "channels": ("web", "push", "sms"),
                "message": "Signal outage at Harbor & 8th; detour active.",
                "languages": ("en", "sw"),
            },
        )
        reliability = store.record_domain_item(
            "service_reliability_snapshot",
            {
                "reliability_snapshot_id": "rel_test",
                "tenant": "tenant_test",
                "corridor_id": "c_test",
                "on_time_percentage": 0.83,
                "average_delay_minutes": 6,
                "sla_status": "warning",
            },
        )
        preview = store.preview_governed_instruction(
            "special event closure memo",
            "prepare a governed closure, alert, and accessibility preview",
            tenant="tenant_test",
        )
        corridor_snapshot = store.build_corridor_snapshot("c_test")
        intersection_detail = store.build_intersection_detail("i_test")
        workbench = store.build_workbench("tenant_test")
        scorecard = store.build_readiness_scorecard("tenant_test")
        assert all(
            item["ok"] is True
            for item in (
                corridor,
                intersection,
                signal,
                transit_priority,
                feed,
                incident,
                detour,
                notification,
                reliability,
                preview,
                corridor_snapshot,
                intersection_detail,
                workbench,
                scorecard,
            )
        )
        assert feed["record"]["quality_state"] == "quarantined"
        assert workbench["quarantined_feed_count"] == 1
        assert corridor_snapshot["incident_count"] == 1
        assert intersection_detail["degraded"] is True
        assert scorecard["green"] is True
    finally:
        store.close()


def test_standalone_service_routes_ui_agent_and_release_surface():
    service = services.SmartCityMobilityOperationsStandaloneService()
    try:
        corridor = routes.dispatch_standalone_route(
            "POST",
            "/app/smart-city-mobility-operations/corridors",
            {
                "corridor_id": "c_route_test",
                "tenant": "tenant_route_test",
                "name": "Airport Link",
                "functional_class": "arterial",
                "operating_objective": "airport access",
            },
            service=service,
        )
        intersection = routes.dispatch_standalone_route(
            "POST",
            "/app/smart-city-mobility-operations/intersections",
            {
                "intersection_id": "i_route_test",
                "tenant": "tenant_route_test",
                "corridor_id": "c_route_test",
                "name": "Airport & Cargo",
                "control_mode": "adaptive",
                "movements": ("nb_through", "sb_right", "ped_crossing"),
            },
            service=service,
        )
        workbench = routes.dispatch_standalone_route(
            "GET",
            "/app/smart-city-mobility-operations/workbench",
            {"tenant": "tenant_route_test"},
            service=service,
        )
        rendered = ui.smart_city_mobility_operations_render_standalone_workbench(
            workbench["result"]["result"]
        )
        document_plan = agent.document_instruction_plan(
            "closure permit with multilingual alert request",
            "prepare governed preview for accessibility and notifications",
        )
        crud_plan = agent.datastore_crud_plan(
            "create",
            "smart_city_mobility_operations_public_notification",
            {"notification_id": "note_route_test"},
        )
        app_contract = standalone.smart_city_mobility_operations_standalone_app_contract()
        smoke = standalone.smart_city_mobility_operations_standalone_app_smoke()
        evidence = release_evidence.build_release_evidence()
        assert corridor["ok"] is True
        assert intersection["ok"] is True
        assert workbench["ok"] is True
        assert rendered["ok"] is True
        assert app_contract["ok"] is True
        assert smoke["ok"] is True
        assert "PublicNotificationWizard" in document_plan["wizard_candidates"] or "GovernedPreviewWizard" in document_plan["wizard_candidates"]
        assert crud_plan["route_candidates"]
        assert evidence["documentation"]["ok"] is True
        assert evidence["generated_artifacts"]["standalone_app"]["ok"] is True
    finally:
        service.close()

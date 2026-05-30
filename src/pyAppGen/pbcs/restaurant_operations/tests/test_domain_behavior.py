"""Domain behavior checks for restaurant operations improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..restaurant_operations_control import (
    CONTROL_SPECS,
    RESTAURANT_ALLOWED_DATABASE_BACKENDS,
    RESTAURANT_DECLARED_DEPENDENCIES,
    RESTAURANT_OWNED_TABLES,
    RESTAURANT_REQUIRED_EVENT_TOPIC,
    evaluate_restaurant_operations_control,
    improve1_restaurant_operations_control_contract,
    sample_payload_for,
)
from ..runtime import restaurant_operations_runtime_capabilities
from ..ui import restaurant_operations_render_workbench, restaurant_operations_ui_contract


def test_all_50_restaurant_controls_are_executable_and_owned():
    contract = improve1_restaurant_operations_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == RESTAURANT_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /restaurant-operations/improve1/")
        assert item["evidence"]["ui_surface"].startswith("RestaurantOperations")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == RESTAURANT_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in RESTAURANT_OWNED_TABLES
            assert table.startswith("restaurant_operations_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in RESTAURANT_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_restaurant_control_contract():
    runtime = restaurant_operations_runtime_capabilities()
    ui = restaurant_operations_ui_contract()
    workbench = restaurant_operations_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["restaurant_operations_control"]["capability_count"] == 50
    assert "evaluate_restaurant_operations_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["restaurant_operations_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["restaurant_operations_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["restaurant_operations_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["restaurant_operations_control"]["ok"] is True


def test_food_safety_service_and_commercial_controls_fail_closed_without_evidence():
    for feature in (4, 8, 9, 12, 21, 22, 23, 24, 32, 36, 37, 43, 44, 46, 50):
        result = evaluate_restaurant_operations_control(feature, {"food_safety_evidence_complete": False})
        assert result["ok"] is False
        assert any("food safety evidence" in finding for finding in result["findings"])

    for feature in (10, 11, 12, 13, 14, 15, 16, 17, 26, 33, 34, 35, 36, 37, 40, 47, 49, 50):
        result = evaluate_restaurant_operations_control(feature, {"service_evidence_complete": False})
        assert result["ok"] is False
        assert any("service evidence" in finding for finding in result["findings"])

    for feature in (1, 2, 5, 6, 7, 18, 20, 24, 25, 26, 27, 28, 29, 31, 38, 39, 46, 49, 50):
        result = evaluate_restaurant_operations_control(feature, {"commercial_evidence_complete": False})
        assert result["ok"] is False
        assert any("commercial evidence" in finding for finding in result["findings"])


def test_menu_safety_agent_and_approval_controls_are_gated():
    for feature in (1, 2, 4, 8, 9, 12, 18, 21, 22, 23, 26, 28, 29, 33, 38, 39, 40, 43, 44, 45, 46, 50):
        result = evaluate_restaurant_operations_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (1, 2, 4, 9, 12, 18, 21, 22, 23, 26, 27, 33, 38, 43, 45, 46, 50):
        result = evaluate_restaurant_operations_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (7, 18, 25, 31, 33, 37, 38, 39, 40, 46, 49, 50):
        result = evaluate_restaurant_operations_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("preview-only" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_restaurant_operations_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_restaurant_operations_control(41, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_restaurant_operations_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_restaurant_operations_control(48, {"shared_table_access": True})["ok"] is False
    assert evaluate_restaurant_operations_control(19, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    menu = sample_payload_for(1)
    assert menu["menu_lifecycle_id"].startswith("menu_lifecycle_by_store_and_daypart")
    assert menu["menu_lifecycle_by_store_and_daypart_verified"] is True
    assert menu["side_effects"] == ()

    kds = evaluate_restaurant_operations_control("kitchen_display_ticket_state_machine")
    assert kds["ok"] is True
    assert "ticket_state" in kds["evidence"]["required_fields"]
    assert "transition_actor" in kds["evidence"]["required_fields"]

    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/release_gate_traceability_to_every_operational_surface")
    assert "ui_agent_evidence" in release_gate["fields"]

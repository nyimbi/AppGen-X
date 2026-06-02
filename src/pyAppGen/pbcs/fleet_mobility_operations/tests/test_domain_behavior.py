"""Fleet-domain behavior checks for the improve1 executable control surface."""

from ..fleet_control import (
    EVENT_CONTRACT,
    FLEET_CONTROL_ALLOWED_DATABASE_BACKENDS,
    FLEET_CONTROL_OWNED_TABLES,
    FLEET_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_fleet_control,
    improve1_fleet_control_contract,
)
from ..release_evidence import release_readiness_manifest, validate_release_evidence
from ..runtime import fleet_mobility_operations_build_release_evidence, fleet_mobility_operations_runtime_capabilities
from ..ui import fleet_mobility_operations_render_workbench, fleet_mobility_operations_ui_contract


def test_all_improve1_features_have_executable_fleet_control_evidence():
    contract = improve1_fleet_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == FLEET_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == FLEET_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in FLEET_CONTROL_OWNED_TABLES
            assert table.startswith("fleet_mobility_operations_")


def test_runtime_release_and_ui_expose_fleet_control_contract():
    runtime = fleet_mobility_operations_runtime_capabilities()
    release = fleet_mobility_operations_build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = fleet_mobility_operations_ui_contract()
    workbench = fleet_mobility_operations_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_fleet_control_contract" in runtime["operations"]
    assert runtime["fleet_control"]["capability_count"] == 50
    assert release["ok"] is True and release["fleet_control"]["ok"] is True
    assert manifest["ok"] is True and "operational_release_gate" in manifest["sections"]
    assert validation["ok"] is True and validation["fleet_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["full_capability_surface"]["fleet_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["fleet_control_service_actions"]) == 50


def test_vehicle_readiness_blocks_open_maintenance_and_safety_events():
    result = evaluate_fleet_control(1, {"open_maintenance_count": 1, "unresolved_safety_events": 1, "dispatchable_verdict": "ready"})
    assert result["ok"] is False
    assert "vehicle readiness ledger blocks dispatch" in result["findings"][0]


def test_driver_assignment_enforces_overlap_rest_and_handoff():
    result = evaluate_fleet_control(2, {"overlap_check": "conflict", "rest_window_hours": 4, "handoff_acknowledged": False})
    assert result["ok"] is False
    assert "minimum rest" in result["findings"][0]


def test_telematics_ingestion_quarantines_bad_device_traffic():
    result = evaluate_fleet_control(5, {"schema_valid": False, "identity_verified": False, "timestamp_sanity": "future_dated"})
    assert result["ok"] is False
    assert "telematics ingestion must quarantine" in result["findings"][0]


def test_ev_dispatch_requires_feasible_charging_plan():
    result = evaluate_fleet_control(10, {"state_of_charge": 12, "minimum_arrival_soc": 25, "charging_window_fit": False})
    assert result["ok"] is False
    assert "EV dispatch requires sufficient charge" in result["findings"][0]


def test_agent_replanning_stays_preview_only_until_confirmed():
    result = evaluate_fleet_control(19, {"preview_only": False, "approval_required": False, "user_confirmation": False})
    assert result["ok"] is False
    assert "preview-only" in result["findings"][0]


def test_multi_tenant_boundary_blocks_cross_tenant_fleet_access():
    result = evaluate_fleet_control(34, {"cross_tenant_access_blocked": False})
    assert result["ok"] is False
    assert "cross-tenant access" in result["findings"][0]


def test_operational_release_gate_requires_all_scenario_proofs():
    result = evaluate_fleet_control(50, {"event_integrity_proof": False})
    assert result["ok"] is False
    assert "operational release gate" in result["findings"][0]

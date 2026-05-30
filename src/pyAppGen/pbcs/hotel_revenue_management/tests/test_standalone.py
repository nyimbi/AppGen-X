from pyAppGen.pbcs.hotel_revenue_management.release_evidence import build_release_evidence
from pyAppGen.pbcs.hotel_revenue_management.seed_data import seed_plan
from pyAppGen.pbcs.hotel_revenue_management.standalone import bootstrap_standalone_state
from pyAppGen.pbcs.hotel_revenue_management.standalone import smoke_test
from pyAppGen.pbcs.hotel_revenue_management.standalone import standalone_application_manifest
from pyAppGen.pbcs.hotel_revenue_management.standalone import standalone_workflow_catalog
from pyAppGen.pbcs.hotel_revenue_management.standalone import validate_standalone_application
from pyAppGen.pbcs.hotel_revenue_management.ui import hotel_revenue_management_render_workbench


def test_standalone_bootstrap_builds_operational_state():
    state = bootstrap_standalone_state()
    assert state["configuration"]["database_backend"] == "postgresql"
    assert len(state["records"]["hotel_revenue_management_room_type"]) >= 2
    assert len(state["records"]["hotel_revenue_management_rate_plan"]) >= 2
    assert len(state["records"]["hotel_revenue_management_yield_decision"]) >= 1


def test_standalone_manifest_and_validation_are_complete():
    app = standalone_application_manifest()
    validation = validate_standalone_application()
    assert app["ok"] is True
    assert validation["ok"] is True
    assert len(standalone_workflow_catalog()) == 4
    assert app["bootstrap"]["workbench"]["configuration_bound"] is True


def test_rendered_workbench_exposes_controls_and_queues():
    state = bootstrap_standalone_state()
    workbench = hotel_revenue_management_render_workbench(state, tenant="tenant_alpha")
    assert workbench["ok"] is True
    assert workbench["metrics"]["compression_night_count"] >= 1
    assert workbench["queues"]["channel_parity_exceptions"]
    assert "BarLadderValidator" in workbench["controls"]


def test_seed_bundle_and_release_evidence_match_standalone_surface():
    assert seed_plan()["ok"] is True
    evidence = build_release_evidence()
    assert evidence["ok"] is True
    assert evidence["documentation"]["present"]
    assert evidence["tests"]["present"]


def test_standalone_smoke_is_green():
    assert smoke_test()["ok"] is True

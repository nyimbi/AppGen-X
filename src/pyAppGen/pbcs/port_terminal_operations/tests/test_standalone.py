"""Focused standalone one-PBC tests for port_terminal_operations."""

from pathlib import Path

from pyAppGen.pbcs.port_terminal_operations import agent
from pyAppGen.pbcs.port_terminal_operations import release_evidence
from pyAppGen.pbcs.port_terminal_operations import standalone
from pyAppGen.pbcs.port_terminal_operations import ui


def test_standalone_app_contract_and_bootstrap_are_executable():
    contract = standalone.port_terminal_operations_standalone_app_contract()
    bundle = standalone.port_terminal_operations_bootstrap_standalone_app(tenant="tenant_test")
    try:
        app = bundle["app"]
        create = app.create_vessel_call(
            {
                "record_id": "vessel_test",
                "vessel_code": "MV-TEST",
                "service_lane": "EA1",
                "eta": "2026-06-02T08:00:00Z",
                "confidence_band": "firm",
            }
        )
        berth = app.record_berth_plan(
            {
                "record_id": "berth_test",
                "vessel_code": "MV-TEST",
                "berth_id": "B-03",
                "window_start": "2026-06-02T10:00:00Z",
                "window_end": "2026-06-02T18:00:00Z",
            }
        )
        move = app.review_container_move(
            {
                "record_id": "move_test",
                "container_id": "MSCU7654321",
                "move_kind": "load",
                "source_location": "YARD-B2",
                "target_location": "BAY-18",
            }
        )
        gate = app.simulate_gate_transaction(
            {
                "record_id": "gate_test",
                "transaction_id": "GT-TEST",
                "appointment_window": "2026-06-02T20:00:00Z/2026-06-02T21:00:00Z",
                "direction": "in",
            }
        )
        workbench = app.workbench({"tenant": "tenant_test"})
        rendered = ui.port_terminal_operations_render_standalone_workbench(workbench["result"])
        assert contract["ok"] is True
        assert create["ok"] is True
        assert berth["ok"] is True
        assert move["ok"] is True
        assert gate["ok"] is True
        assert workbench["ok"] is True
        assert workbench["result"]["record_count"] >= 4
        assert rendered["ok"] is True
        assert rendered["forms"]
        assert rendered["wizards"]
        assert rendered["controls"]
    finally:
        bundle["app"]


def test_standalone_routes_agent_and_release_surface_are_wired():
    bundle = standalone.port_terminal_operations_bootstrap_standalone_app(tenant="tenant_route")
    app = bundle["app"]
    create = standalone.dispatch_standalone_route(
        "POST",
        "/app/port-terminal-operations/vessel-calls",
        {
            "record_id": "route_vessel",
            "vessel_code": "MV-ROUTE",
            "service_lane": "EA2",
            "eta": "2026-06-03T06:00:00Z",
            "confidence_band": "provisional",
        },
        app=app,
    )
    customs = standalone.dispatch_standalone_route(
        "POST",
        "/app/port-terminal-operations/customs-handoffs",
        {
            "record_id": "route_customs",
            "container_id": "TGHU1234560",
            "release_state": "held",
            "inspection_requirement": "scan",
            "scan_result": "pending",
        },
        app=app,
    )
    workbench = standalone.dispatch_standalone_route(
        "GET",
        "/app/port-terminal-operations/workbench",
        {"tenant": "tenant_route"},
        app=app,
    )
    doc_plan = agent.document_instruction_plan(
        "Carrier message advising berth revision.",
        "Review berth nomination, customs release, and release evidence.",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        "port_terminal_operations_vessel_call",
        {"record_id": "route_vessel"},
    )
    evidence = release_evidence.build_release_evidence()
    assert create["ok"] is True
    assert customs["ok"] is True
    assert workbench["ok"] is True
    assert doc_plan["wizard_candidates"]
    assert doc_plan["route_candidates"]
    assert crud_plan["ok"] is True
    assert crud_plan["route_candidates"]
    assert evidence["ok"] is True
    assert evidence["standalone_app"]["ok"] is True
    assert evidence["documentation"]["ok"] is True


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in (
        "README.md",
        "SPECIFICATION.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
    ):
        assert (base / name).exists() is True

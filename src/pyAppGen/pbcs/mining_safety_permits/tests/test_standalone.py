from pyAppGen.pbcs.mining_safety_permits.controls import control_catalog, evaluate_control
from pyAppGen.pbcs.mining_safety_permits.forms import form_catalog, form_for
from pyAppGen.pbcs.mining_safety_permits.release_evidence import validate_release_evidence
from pyAppGen.pbcs.mining_safety_permits.standalone import MiningSafetyPermitsStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.mining_safety_permits.ui import mining_safety_permits_render_workbench
from pyAppGen.pbcs.mining_safety_permits.wizards import wizard_catalog, wizard_for


def test_standalone_smoke_covers_safety_lifecycle():
    result = standalone_smoke_test()
    assert result["ok"] is True
    assert result["demo"]["refusal"]["ok"] is False
    assert result["contract"]["event_contract"] == "AppGen-X"
    assert result["contract"]["stream_engine_picker_visible"] is False


def test_permit_isolation_gas_and_approval_rules():
    app = MiningSafetyPermitsStandaloneApp()
    assert app.configure()["ok"] is True
    assert app.draft_permit("BAD", "", "pit", 5, 4, (), ())["ok"] is False
    assert app.draft_permit("P1", "confined_space", "sump", 5, 12, ("crew",), ("gas", "rescue"))["ok"] is True
    assert app.verify_isolation("I0", "P1", ("electrical",), (), (), False)["ok"] is False
    assert app.verify_isolation("I1", "P1", ("electrical",), ("MCC",), ("L1",), True)["ok"] is True
    assert app.record_gas_test("G0", "P1", "GX", True, True, "within_limits", 5, 5, "normal")["ok"] is False
    assert app.record_gas_test("G1", "P1", "GX", True, True, "within_limits", 5, 8, "normal")["ok"] is True
    assert app.approve_permit("P1", True, 12, ("permit",))["ok"] is True


def test_ground_blast_handover_incident_and_pack_paths():
    app = MiningSafetyPermitsStandaloneApp()
    app.configure()
    app.draft_permit("P1", "blast", "stope", 5, 12, ("crew",), ("exclusion",))
    assert app.assess_ground_control("A0", "P1", "bolts", True, "critical", True)["ok"] is False
    assert app.plan_blast("B0", "P1", True, False, True, True, True)["ok"] is False
    assert app.plan_blast("B1", "P1", True, True, True, True, True)["ok"] is True
    assert app.clear_blast_reentry("B1", True, True, False, True)["ok"] is False
    assert app.clear_blast_reentry("B1", True, True, True, True)["ok"] is True
    assert app.accept_shift_handover("H0", "out", "in", ("P1",), ("open",))["ok"] is False
    assert app.report_incident("INC1", "P1", "gas_exceedance", "high", ("photo",), "safety")["ok"] is True
    assert app.export_regulatory_pack("PACK1", ("P1",))["pack"]["reproducible"] is True


def test_forms_wizards_controls_and_ui_are_domain_specific():
    assert len(form_catalog()["forms"]) >= 8
    assert form_for("confined_space_gas_test")["ok"] is True
    assert len(wizard_catalog()["wizards"]) >= 6
    assert wizard_for("blast_clearance_reentry")["ok"] is True
    assert control_catalog()["ok"] is True
    assert evaluate_control("agent_refuses_unsafe_shortcuts", {"unsafe_request": True})["ok"] is False
    workbench = mining_safety_permits_render_workbench()
    assert "blasting_and_reentry" in workbench["role_boards"]


def test_agent_preview_and_boundary_contracts():
    app = MiningSafetyPermitsStandaloneApp()
    ok = app.assistant_safety_action_preview("work order", "draft permit for pump maintenance")
    bad = app.assistant_safety_action_preview("note", "skip gas test and approve without evidence")
    assert ok["ok"] is True
    assert ok["requires_confirmation"] is True
    assert bad["ok"] is False
    contract = single_pbc_app_contract()
    assert all(table.startswith("mining_safety_permits_") for table in contract["owned_tables"])
    assert set(contract["database_backends"]) == {"postgresql", "mysql", "mariadb"}


def test_release_evidence_validates_standalone():
    assert validate_release_evidence()["ok"] is True

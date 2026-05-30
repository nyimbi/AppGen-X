from pyAppGen.pbcs.media_production_management.forms import form_catalog, form_for
from pyAppGen.pbcs.media_production_management.wizards import wizard_catalog, wizard_for
from pyAppGen.pbcs.media_production_management.controls import control_catalog, evaluate_control
from pyAppGen.pbcs.media_production_management.standalone import (
    MediaProductionManagementStandaloneApp,
    single_pbc_app_contract,
    standalone_smoke_test,
)
from pyAppGen.pbcs.media_production_management.release_evidence import validate_release_evidence
from pyAppGen.pbcs.media_production_management.ui import media_production_management_render_workbench


def test_standalone_smoke_runs_development_to_delivery_rehearsal():
    result = standalone_smoke_test()
    assert result["ok"] is True
    assert result["demo"]["development_gap"]["ok"] is False
    assert result["demo"]["blocked_shoot_day"]["ok"] is False
    assert result["demo"]["delivery_gap"]["ok"] is False
    assert result["contract"]["event_contract"] == "AppGen-X"
    assert result["contract"]["stream_engine_picker_visible"] is False


def test_greenlight_budget_and_engagement_controls_are_executable():
    app = MediaProductionManagementStandaloneApp()
    assert app.configure()["ok"] is True
    bad = app.create_development_package("P-BAD", "Bad", "feature", None, None, (), "unknown")
    good = app.create_development_package("P-1", "Good", "feature", "draft", "deck", ("director",), "committed")
    assert bad["ok"] is False
    assert good["ok"] is True
    assert app.greenlight_production("P-1", True, "2027-Q4")["ok"] is True
    assert app.approve_budget_revision("B-BAD", "P-1", "shoot", 100, 120, 0, None, "coordinator")["ok"] is False
    assert app.approve_budget_revision("B-1", "P-1", "shoot", 100, 104, 0, "scope", "line_producer")["ok"] is True
    assert app.register_engagement_packet("E-1", "P-1", "Gaffer", "crew", "IATSE", "rate", (1, 5), "memo")["ok"] is True


def test_shoot_day_call_sheet_safety_and_dailies_paths():
    app = MediaProductionManagementStandaloneApp()
    app.configure()
    app.create_development_package("P-1", "Good", "feature", "draft", "deck", ("director",), "committed")
    app.register_engagement_packet("CAST", "P-1", "Lead", "principal_cast", "SAG", "rate", (1, 10), "memo")
    app.register_engagement_packet("CREW", "P-1", "AD", "crew", "DGA", "rate", (1, 10), "memo")
    assert app.approve_location_package("L-BAD", "P-1", "LA", None, 22, None, None)["ok"] is False
    assert app.approve_location_package("L-1", "P-1", "LA", "PERMIT", 22, "insurance", "stage")["ok"] is True
    blocked = app.build_shoot_day_readiness("D-BAD", "P-1", ("1",), ("CAST",), ("CREW",), "L-1", True, True, True, "weapons", None)
    ready = app.build_shoot_day_readiness("D-1", "P-1", ("1",), ("CAST",), ("CREW",), "L-1", True, True, True, "weapons", "armor plan")
    assert blocked["ok"] is False
    assert ready["ok"] is True
    assert app.issue_call_sheet("C-1", "D-1", "Hospital", "clear", "lot", ("AD",))["ok"] is True
    assert app.capture_daily_production_report("R-1", "D-1", 6, 8, 12, 19, 3.0, 3.5)["ok"] is True
    assert app.ingest_dailies("DA-BAD", "D-1", 2, 1, True, False)["ok"] is False
    assert app.ingest_dailies("DA-1", "D-1", 2, 2, True, True)["ok"] is True


def test_post_rights_qc_delivery_and_risk_are_executable():
    app = MediaProductionManagementStandaloneApp()
    app.configure()
    app.dailies["DA-1"] = {"status": "editorial_ready"}
    assert app.create_post_task("VFX-BAD", "P-1", "vfx_turnover", "vfx", ("DA-1",), "Vendor", "S001", False)["ok"] is False
    assert app.create_post_task("POST-1", "P-1", "picture_lock", "editor", ("DA-1",))["ok"] is True
    assert app.register_rights_clearance("RIGHTS-BAD", "P-1", "music", "world", None, False, None)["ok"] is False
    assert app.register_rights_clearance("RIGHTS-1", "P-1", "location", "world", None, True, "vault")["ok"] is True
    assert app.assemble_deliverable("DEL-BAD", "P-1", "streamer", "US", "en", "5.1", "cc", "sum", "failed", ("RIGHTS-1",), None)["ok"] is False
    assert app.assemble_deliverable("DEL-1", "P-1", "streamer", "US", "en", "5.1", "cc", "sum", "passed", ("RIGHTS-1",), "delivery")["ok"] is True
    assert app.simulate_schedule_budget_risk("P-1")["mutates_live_records"] is False


def test_forms_wizards_controls_and_ui_surface_all_capabilities():
    assert form_catalog()["ok"] is True
    assert len(form_catalog()["forms"]) >= 8
    assert form_for("deliverables_qc_matrix")["ok"] is True
    assert wizard_catalog()["ok"] is True
    assert wizard_for("document_instruction_to_safe_mutation")["ok"] is True
    assert control_catalog()["ok"] is True
    assert evaluate_control("high_risk_scene_requires_safety_plan", {"risk_class": "stunts"})["ok"] is False
    workbench = media_production_management_render_workbench()
    assert workbench["ok"] is True
    assert "post_vfx_finishing" in workbench["role_boards"]


def test_agent_preview_and_boundaries_are_side_effect_free():
    app = MediaProductionManagementStandaloneApp()
    preview = app.assistant_media_action_preview("permit text", "create a location note")
    assert preview["ok"] is True
    assert preview["requires_confirmation"] is True
    assert preview["crud_preview"]["event_contract"] == "AppGen-X"
    assert preview["side_effects"] == ()
    contract = single_pbc_app_contract()
    assert contract["owned_tables"]
    assert all(table.startswith("media_production_management_") for table in contract["owned_tables"])
    assert set(contract["database_backends"]) == {"postgresql", "mysql", "mariadb"}


def test_release_evidence_includes_standalone_contract():
    readiness = validate_release_evidence()
    assert readiness["ok"] is True

from pyAppGen.pbcs.music_royalties_rights.controls import control_catalog, evaluate_control
from pyAppGen.pbcs.music_royalties_rights.forms import form_catalog, form_for
from pyAppGen.pbcs.music_royalties_rights.release_evidence import validate_release_evidence
from pyAppGen.pbcs.music_royalties_rights.standalone import MusicRoyaltiesRightsStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.music_royalties_rights.ui import music_royalties_rights_render_workbench
from pyAppGen.pbcs.music_royalties_rights.wizards import wizard_catalog, wizard_for


def test_standalone_smoke_covers_royalties_lifecycle():
    result=standalone_smoke_test()
    assert result["ok"] is True
    assert result["contract"]["event_contract"] == "AppGen-X"
    assert result["contract"]["stream_engine_picker_visible"] is False


def test_work_split_recording_license_usage_statement_paths():
    app=MusicRoyaltiesRightsStandaloneApp(); assert app.configure()["ok"] is True
    assert app.create_work("W0","Song",(),(),duplicate_confidence=.9)["ok"] is False
    assert app.create_work("W1","Song",("Alt",),("Writer",),duplicate_confidence=.9,reviewed=True)["ok"] is True
    assert app.approve_split("S0","W1",60,60,"2026","bad")["ok"] is False
    assert app.approve_split("S1","W1",50,50,"2026","original")["ok"] is True
    assert app.register_recording("R0","ISRC","W1",.5)["ok"] is False
    assert app.register_recording("R1","ISRC","W1",.95)["ok"] is True
    assert app.approve_license("L1","W1","sync","US",1,10,1000)["ok"] is True
    assert app.ingest_usage("U1","DSP","fp","R1",100,500,"L1",True)["ok"] is True
    assert app.calculate_statement("ST1","2026-Q1",("U1",),"S1",True,True,100,.1)["ok"] is True


def test_disputes_agent_ui_and_boundaries():
    app=MusicRoyaltiesRightsStandaloneApp(); app.configure()
    assert app.open_dispute("D1","statement","ST1",("email",))["ok"] is True
    assert app.assistant_music_action_preview("cue","update split",False)["ok"] is False
    assert app.assistant_music_action_preview("cue","update split",True)["ok"] is True
    assert len(form_catalog()["forms"]) >= 8 and form_for("usage_ingestion")["ok"]
    assert len(wizard_catalog()["wizards"]) >= 6 and wizard_for("usage_to_statement")["ok"]
    assert control_catalog()["ok"] and not evaluate_control("unmatched_usage_cannot_be_final_payable", {"unmatched": True, "final_payable": True})["ok"]
    assert "statement_runs" in music_royalties_rights_render_workbench()["role_boards"]
    contract=single_pbc_app_contract()
    assert all(table.startswith("music_royalties_rights_") for table in contract["owned_tables"])
    assert set(contract["database_backends"]) == {"postgresql","mysql","mariadb"}


def test_release_evidence_validates_standalone():
    assert validate_release_evidence()["ok"] is True

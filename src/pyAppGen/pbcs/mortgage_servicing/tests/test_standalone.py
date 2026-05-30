from pyAppGen.pbcs.mortgage_servicing.controls import control_catalog, evaluate_control
from pyAppGen.pbcs.mortgage_servicing.forms import form_catalog, form_for
from pyAppGen.pbcs.mortgage_servicing.release_evidence import validate_release_evidence
from pyAppGen.pbcs.mortgage_servicing.standalone import MortgageServicingStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.mortgage_servicing.ui import mortgage_servicing_render_workbench
from pyAppGen.pbcs.mortgage_servicing.wizards import wizard_catalog, wizard_for


def test_standalone_smoke_covers_servicing_lifecycle():
    result=standalone_smoke_test()
    assert result["ok"] is True
    assert result["contract"]["event_contract"] == "AppGen-X"
    assert result["contract"]["stream_engine_picker_visible"] is False


def test_boarding_transfer_payment_and_statement_paths():
    app=MortgageServicingStandaloneApp(); assert app.configure()["ok"] is True
    assert app.board_loan("BAD",{},None,None,False,None,None,None)["ok"] is False
    assert app.board_loan("L1",{"principal":100000},"2026-06-01","30/360",True,"INV","B","P")["ok"] is True
    assert app.reconcile_transfer("L1",100000,99000,500,0,())["ok"] is False
    assert app.reconcile_transfer("L1",100000,99500,500,0,())["ok"] is True
    assert app.apply_payment("P0","L1",500,1800)["payment"]["status"] == "suspense"
    assert app.apply_payment("P1","L1",1900,1800)["ok"] is True
    assert app.generate_statement("S1","L1","2026-06",1800)["ok"] is True


def test_escrow_loss_mitigation_foreclosure_and_investor_reporting():
    app=MortgageServicingStandaloneApp(); app.configure(); app.board_loan("L1",{"principal":100000},"2026-06-01","30/360",True,"INV","B","P")
    assert app.run_escrow_analysis("E1","L1",3000,1200,400)["ok"] is True
    assert app.open_loss_mitigation("LM0","L1","hardship",("paystub","bank"),("paystub",))["ok"] is False
    assert app.open_loss_mitigation("LM1","L1","hardship",("paystub",),("paystub",))["ok"] is True
    assert app.evaluate_foreclosure_referral("F0","L1",130,True,active_loss_mitigation=True,investor_approval=True)["ok"] is False
    assert app.evaluate_foreclosure_referral("F1","L1",130,True,investor_approval=True)["ok"] is True
    assert app.build_investor_report("R0","POOL",("L1",),100,90,10)["ok"] is False
    assert app.build_investor_report("R1","POOL",("L1",),100,100,10)["ok"] is True


def test_forms_wizards_controls_and_ui_are_domain_specific():
    assert len(form_catalog()["forms"]) >= 8
    assert form_for("loss_mitigation_package")["ok"] is True
    assert len(wizard_catalog()["wizards"]) >= 6
    assert wizard_for("foreclosure_readiness_review")["ok"] is True
    assert control_catalog()["ok"] is True
    assert evaluate_control("foreclosure_referral_blocks_on_protections", {"bankruptcy": True})["ok"] is False
    assert "loss_mitigation" in mortgage_servicing_render_workbench()["role_boards"]


def test_agent_preview_and_boundaries():
    app=MortgageServicingStandaloneApp()
    assert app.assistant_mortgage_action_preview("doc","update borrower hardship",False)["ok"] is False
    assert app.assistant_mortgage_action_preview("doc","update borrower hardship",True)["ok"] is True
    contract=single_pbc_app_contract()
    assert all(table.startswith("mortgage_servicing_") for table in contract["owned_tables"])
    assert set(contract["database_backends"]) == {"postgresql","mysql","mariadb"}


def test_release_evidence_validates_standalone():
    assert validate_release_evidence()["ok"] is True

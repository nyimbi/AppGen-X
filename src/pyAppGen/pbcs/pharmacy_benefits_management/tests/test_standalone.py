from pyAppGen.pbcs.pharmacy_benefits_management.controls import control_catalog, evaluate_control
from pyAppGen.pbcs.pharmacy_benefits_management.forms import form_catalog, form_for
from pyAppGen.pbcs.pharmacy_benefits_management.release_evidence import validate_release_evidence
from pyAppGen.pbcs.pharmacy_benefits_management.standalone import PharmacyBenefitsManagementStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.pharmacy_benefits_management.ui import pharmacy_benefits_management_render_workbench
from pyAppGen.pbcs.pharmacy_benefits_management.wizards import wizard_catalog, wizard_for


def test_standalone_smoke_covers_pbm_lifecycle():
    r=standalone_smoke_test(); assert r["ok"] is True; assert r["contract"]["event_contract"] == "AppGen-X"; assert r["contract"]["stream_engine_picker_visible"] is False

def test_formulary_pa_claim_rebate_paths():
    app=PharmacyBenefitsManagementStandaloneApp(); assert app.configure()["ok"]
    assert app.publish_formulary("F0","plan","US",10,1)["ok"] is False
    assert app.publish_formulary("F1","plan","US",1,10)["ok"]
    assert app.add_coverage_rule("R1","F1","drug",4,80,30,True)["ok"]
    assert app.decide_prior_authorization("PA0","drug",("dx",))["ok"] is False
    assert app.decide_prior_authorization("PA1","drug",(),True,2,True)["ok"]
    app.contract_network("N0","retail",True,False)
    assert app.adjudicate_claim("C0","R1","N0",40,30)["ok"] is False
    app.contract_network("N1","specialty",True,True)
    assert app.adjudicate_claim("C1","R1","N1",40,30,True)["ok"]
    assert app.accrue_rebate("RB1","mfg","R1",("C1",),10)["ok"]

def test_utilization_affordability_agent_and_ui():
    app=PharmacyBenefitsManagementStandaloneApp(); app.configure()
    assert app.open_utilization_review("U0","safety","opioid","high",("claim",))["ok"] is False
    assert app.open_utilization_review("U1","safety","opioid","high",("claim",),"approve")["ok"]
    assert app.affordability_assistance("drug",(("generic",20),("brand",80)),300)["outreach_needed"]
    assert app.assistant_pbm_action_preview("policy","update criteria",False)["ok"] is False
    assert app.assistant_pbm_action_preview("policy","update criteria",True)["ok"]
    assert len(form_catalog()["forms"]) >= 8 and form_for("claim_edit")["ok"]
    assert len(wizard_catalog()["wizards"]) >= 6 and wizard_for("rebate_accrual_trueup")["ok"]
    assert control_catalog()["ok"] and not evaluate_control("specialty_drug_requires_network", {"specialty": True})["ok"]
    assert "claim_edits" in pharmacy_benefits_management_render_workbench()["role_boards"]

def test_boundary_and_release_evidence():
    c=single_pbc_app_contract(); assert all(t.startswith("pharmacy_benefits_management_") for t in c["owned_tables"]); assert set(c["database_backends"]) == {"postgresql","mysql","mariadb"}; assert validate_release_evidence()["ok"]

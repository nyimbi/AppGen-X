from pyAppGen.pbcs.pharma_manufacturing_quality.controls import control_catalog, evaluate_control
from pyAppGen.pbcs.pharma_manufacturing_quality.forms import form_catalog, form_for
from pyAppGen.pbcs.pharma_manufacturing_quality.release_evidence import validate_release_evidence
from pyAppGen.pbcs.pharma_manufacturing_quality.standalone import PharmaManufacturingQualityStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.pharma_manufacturing_quality.ui import pharma_manufacturing_quality_render_workbench
from pyAppGen.pbcs.pharma_manufacturing_quality.wizards import wizard_catalog, wizard_for


def test_standalone_smoke_covers_gmp_lifecycle():
    r=standalone_smoke_test(); assert r["ok"] is True; assert r["contract"]["event_contract"] == "AppGen-X"; assert r["contract"]["stream_engine_picker_visible"] is False

def test_mbr_batch_step_deviation_capa_release_paths():
    app=PharmaManufacturingQualityStandaloneApp(); assert app.configure()["ok"]
    assert app.approve_mbr("M1","Tablet","10mg","v1",True,{"temp":(20,30)})["ok"]
    assert app.start_batch("B0","NO",("LOT",),{"qualified":True})["ok"] is False
    assert app.start_batch("B1","M1",("LOT",),{"qualified":True})["ok"]
    assert app.execute_step("B1","mix","25",40,20,30,"op","qa")["ok"] is False
    assert app.open_deviation("D1","B1","process","major","hold","root")["ok"]
    assert app.create_capa("C0","D1","fix","prevent",None)["ok"] is False
    assert app.create_capa("C1","D1","fix","prevent","effective")["ok"]
    app.deviations["D1"]["status"]="closed"
    for _dev in app.deviations.values():
        if _dev["batch_id"] == "B1":
            _dev["status"] = "closed"
    assert app.record_serialization("S1","B1","SER1","commission",1)["ok"]
    assert app.release_batch("R1","B1",True,True,True)["ok"]

def test_validation_serialization_recall_agent_and_ui():
    app=PharmaManufacturingQualityStandaloneApp(); app.configure(); app.approve_mbr("M1","Tablet","10mg","v1",True,{"temp":(20,30)}); app.start_batch("B1","M1",("LOT",),{"qualified":True})
    assert app.execute_validation("V0","process",False)["ok"] is False
    assert app.execute_validation("V1","process",True)["ok"]
    assert app.record_serialization("S1","B1","SER1","commission",1)["ok"]
    assert app.record_serialization("S2","B1","SER1","commission",2)["ok"] is False
    assert app.trace_recall_impact("LOT")["affected_batches"] == ("B1",)
    assert app.assistant_pharma_action_preview("ebr","update batch",False)["ok"] is False
    assert app.assistant_pharma_action_preview("ebr","update batch",True)["ok"]
    assert len(form_catalog()["forms"]) >= 8 and form_for("batch_release")["ok"]
    assert len(wizard_catalog()["wizards"]) >= 6 and wizard_for("deviation_to_capa")["ok"]
    assert control_catalog()["ok"] and not evaluate_control("duplicate_serial_rejected", {"duplicate_active_serial": True})["ok"]
    assert "batch_execution" in pharma_manufacturing_quality_render_workbench()["role_boards"]

def test_boundary_and_release_evidence():
    c=single_pbc_app_contract(); assert all(t.startswith("pharma_manufacturing_quality_") for t in c["owned_tables"]); assert set(c["database_backends"]) == {"postgresql","mysql","mariadb"}; assert validate_release_evidence()["ok"]

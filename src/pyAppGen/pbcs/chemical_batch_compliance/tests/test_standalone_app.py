from pyAppGen.pbcs.chemical_batch_compliance.standalone import ChemicalBatchComplianceStandaloneApp
from pyAppGen.pbcs.chemical_batch_compliance.standalone import single_pbc_app_contract
from pyAppGen.pbcs.chemical_batch_compliance.standalone import standalone_route_contracts
from pyAppGen.pbcs.chemical_batch_compliance.standalone import standalone_smoke_test
from pyAppGen.pbcs.chemical_batch_compliance.standalone import workbench_smoke_test
from pyAppGen.pbcs.chemical_batch_compliance.ui import chemical_batch_compliance_standalone_app_contract


def test_single_pbc_app_has_forms_wizards_controls_and_agent_surface():
    contract = single_pbc_app_contract()
    assert contract["ok"] is True
    assert len(contract["forms"]) >= 4
    assert len(contract["wizards"]) >= 3
    assert len(contract["controls"]) >= 5
    assert contract["dsl_exposure"]["agent_skill_namespace"] == "chemical_batch_compliance_skills"
    assert contract["stream_engine_picker_visible"] is False


def test_standalone_demo_executes_domain_workflow_with_owned_state():
    app = ChemicalBatchComplianceStandaloneApp()
    loaded = app.load_demo_workspace(tenant="tenant-standalone")
    assert loaded["ok"] is True
    assert loaded["quality"]["result"]["hold"] is not None
    assert loaded["workbench"]["summary"]["open_holds"] >= 1
    assert all(table.startswith("chemical_batch_compliance_") for table in app.state["tables"])


def test_standalone_contracts_and_smokes_are_release_ready():
    assert standalone_route_contracts()["ok"] is True
    assert chemical_batch_compliance_standalone_app_contract()["ok"] is True
    assert standalone_smoke_test()["ok"] is True
    assert workbench_smoke_test()["ok"] is True

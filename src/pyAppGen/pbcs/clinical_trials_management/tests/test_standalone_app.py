from pyAppGen.pbcs.clinical_trials_management.standalone import ClinicalTrialsManagementStandaloneApp
from pyAppGen.pbcs.clinical_trials_management.standalone import single_pbc_app_contract
from pyAppGen.pbcs.clinical_trials_management.standalone import standalone_smoke_test
from pyAppGen.pbcs.clinical_trials_management.ui import clinical_trials_management_standalone_app_contract


def test_standalone_app_runs_trial_to_lock_ready_flow():
    app = ClinicalTrialsManagementStandaloneApp()
    loaded = app.load_demo_workspace(tenant="tenant-standalone")
    assert loaded["ok"] is True
    assert loaded["lock"]["ready"] is True
    assert loaded["workbench"]["metrics"]["lock_ready"] == 1
    assert loaded["assistant"]["requires_confirmation"] is True


def test_single_pbc_contract_surfaces_forms_wizards_controls_and_agent_namespace():
    ui = clinical_trials_management_standalone_app_contract()
    contract = single_pbc_app_contract()
    assert ui["ok"] is True
    assert len(contract["forms"]) >= 10
    assert len(contract["wizards"]) >= 4
    assert len(contract["controls"]) >= 5
    assert contract["dsl_exposure"]["agent_skill_namespace"] == "clinical_trials_management_skills"
    assert contract["stream_engine_picker_visible"] is False


def test_standalone_smoke_is_release_ready():
    assert standalone_smoke_test()["ok"] is True

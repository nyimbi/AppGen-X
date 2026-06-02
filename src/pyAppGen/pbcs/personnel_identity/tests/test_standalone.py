"""Standalone and repository smoke tests for personnel_identity."""

from __future__ import annotations

from ..repository import PersonnelIdentityRepository
from ..repository import personnel_identity_repository_contract
from ..standalone import PersonnelIdentityStandaloneApp
from ..standalone import smoke_test
from ..ui import personnel_identity_standalone_app_contract


def test_standalone_manifest_repository_and_smoke():
    contract = personnel_identity_standalone_app_contract()
    repository_contract = personnel_identity_repository_contract()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert repository_contract["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]
    assert repository_contract["form_bindings"]


def test_standalone_app_can_execute_department_to_identity_flow():
    app = PersonnelIdentityStandaloneApp()
    loaded = app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(tenant="tenant_standalone")
    repository = PersonnelIdentityRepository(app.state).read_model("tenant_standalone")
    binding = PersonnelIdentityRepository(app.state).form_binding_plan("role_assignment_form")

    assert loaded["ok"] is True
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][1]["value"] == 2
    assert rendered["shell"]["app_id"] == "personnel_identity_one_pbc_app"
    assert repository["organization"]["department_count"] == 1
    assert repository["employee"]["employee_count"] == 2
    assert repository["employee"]["active_count"] == 2
    assert repository["access"]["active_role_count"] == 1
    assert repository["identity"]["attribute_count"] == 2
    assert repository["identity"]["assurance_floor"] >= 0.9
    assert binding["ok"] is True
    assert loaded["provisioning_route"]["route"] == "appgen_outbox"
    assert loaded["eligibility_proof"]["proof"].startswith("zk_people_")

from pyAppGen.pbcs.contract_lifecycle import implementation_contract, smoke_test
from pyAppGen.pbcs.contract_lifecycle.agent import composed_agent_contribution, document_instruction_plan
from pyAppGen.pbcs.contract_lifecycle.app_surface import (
    app_surface_smoke_test,
    contract_lifecycle_controls_contract,
    contract_lifecycle_forms_contract,
    contract_lifecycle_wizards_contract,
    single_pbc_contract_lifecycle_app_contract,
    standalone_route_contracts,
)
from pyAppGen.pbcs.contract_lifecycle.release_evidence import build_release_evidence, validate_release_evidence
from pyAppGen.pbcs.contract_lifecycle.routes import api_route_contracts
from pyAppGen.pbcs.contract_lifecycle.ui import contract_lifecycle_ui_contract


def test_single_pbc_contract_lifecycle_app_is_functional():
    app = single_pbc_contract_lifecycle_app_contract()

    assert app["ok"] is True
    assert app["application_mode"] == "single_pbc_standalone"
    assert len(app["owned_tables"]) >= 20
    assert len(app["forms"]["forms"]) >= 5
    assert len(app["wizards"]["wizards"]) >= 3
    assert len(app["controls"]["controls"]) >= 4
    assert app["dependency_boundary"]["writes_foreign_tables"] is False
    assert app["dependency_boundary"]["event_contract"] == "AppGen-X"


def test_forms_wizards_controls_cover_real_contract_work():
    forms = contract_lifecycle_forms_contract()
    wizards = contract_lifecycle_wizards_contract()
    controls = contract_lifecycle_controls_contract()

    assert "intake_contract" in forms["covered_operations"]
    assert "capture_signature" in wizards["terminal_operations"]
    assert wizards["supports_renewals_and_amendments"] is True
    assert "approval_matrix" in controls["control_ids"]
    assert controls["stream_engine_picker_visible"] is False


def test_document_instruction_agent_only_targets_owned_tables():
    plan = document_instruction_plan(
        "Update the renewal obligation, clause fallback, and signature packet for the supplier contract.",
        "create governed CRUD previews but require legal approval before writing",
    )

    assert plan["ok"] is True
    assert plan["requires_human_confirmation"] is True
    assert plan["single_pbc_ready"] is True
    assert all(table.startswith("contract_lifecycle_") for table in plan["candidate_tables"])
    assert all(item["requires_confirmation"] for item in plan["crud_preview"])


def test_routes_ui_agent_and_release_include_standalone_surface():
    route_paths = tuple(route["path"] for route in standalone_route_contracts())
    api = api_route_contracts()
    ui = contract_lifecycle_ui_contract()
    agent = composed_agent_contribution()
    release = build_release_evidence()

    assert "/contract-lifecycle/app" in route_paths
    assert any(route["path"] == "/contract-lifecycle/app" for route in api["standalone_routes"])
    assert ui["single_pbc_app"]["ok"] is True
    assert agent["standalone_app"]["ok"] is True
    assert release["standalone_app_smoke"]["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_package_smoke_and_implementation_expose_app_surface():
    app_surface = app_surface_smoke_test()
    implementation = implementation_contract()
    package_smoke = smoke_test()

    assert app_surface["ok"] is True
    assert implementation["single_pbc_app"]["ok"] is True
    assert implementation["app_surface_smoke"]["ok"] is True
    assert package_smoke["ok"] is True

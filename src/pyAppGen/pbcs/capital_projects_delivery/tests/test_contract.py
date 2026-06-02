from pyAppGen.pbcs.capital_projects_delivery import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.capital_projects_delivery.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.capital_projects_delivery.capability_assurance import (
    table_stakes_capability_manifest,
    validate_table_stakes_capability_coverage,
)
from pyAppGen.pbcs.capital_projects_delivery.config import governance_smoke_test
from pyAppGen.pbcs.capital_projects_delivery.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.capital_projects_delivery.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.capital_projects_delivery.models import database_backed_model_manifest
from pyAppGen.pbcs.capital_projects_delivery.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.capital_projects_delivery.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.capital_projects_delivery.schema_contract import build_schema_contract
from pyAppGen.pbcs.capital_projects_delivery.service_contract import build_service_contract
from pyAppGen.pbcs.capital_projects_delivery.services import service_operation_contracts
from pyAppGen.pbcs.capital_projects_delivery.standalone import standalone_app_manifest
from pyAppGen.pbcs.capital_projects_delivery.ui import (
    capital_projects_delivery_standalone_app_contract,
    capital_projects_delivery_ui_contract,
)
from pyAppGen.pbcs.capital_projects_delivery.runtime import (
    capital_projects_delivery_build_controls_contract,
    capital_projects_delivery_build_forms_contract,
    capital_projects_delivery_build_single_pbc_app_contract,
    capital_projects_delivery_build_workflow_contracts,
    capital_projects_delivery_build_wizards_contract,
)


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_runtime_and_event_contract():
    contract = implementation_contract()
    assert contract["pbc"] == "capital_projects_delivery"
    assert contract["single_pbc_app_contract"]["ok"] is True
    assert contract["workflow_contract"]["ok"] is True
    assert contract["standalone_app_manifest"]["ok"] is True
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    plan = document_instruction_plan(
        "project_id=PRJ-200 tenant=tenant_smoke permit_code=PERMIT-1",
        "approve gate after checklist and review permit blocker",
    )
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert composed_agent_contribution()["ok"] is True
    assert plan["ok"] is True
    assert plan["mutation_preview"]
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "capital_projects_delivery"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_route_workflow_and_ui_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert capital_projects_delivery_build_workflow_contracts()["ok"] is True
    assert len(capital_projects_delivery_build_workflow_contracts()["workflows"]) >= 4
    ui_contract = capital_projects_delivery_ui_contract()
    assert ui_contract["ok"] is True
    assert ui_contract["standalone_app"]["app_id"] == "capital_projects_delivery_one_pbc_app"
    assert capital_projects_delivery_standalone_app_contract()["ok"] is True


def test_single_pbc_app_surface_is_database_backed_and_form_driven():
    app = capital_projects_delivery_build_single_pbc_app_contract()
    assert app["ok"] is True
    assert app["database_backed"] is True
    assert len(app["forms"]) >= 3
    assert len(app["wizards"]) >= 2
    assert len(app["controls"]) >= 4
    assert len(app["workflows"]) >= 4
    assert app["standalone_entrypoint"].endswith("CapitalProjectsDeliveryStandaloneApp")
    assert database_backed_model_manifest()["database_backed"] is True
    assert capital_projects_delivery_build_forms_contract()["ok"] is True
    assert capital_projects_delivery_build_wizards_contract()["ok"] is True
    assert capital_projects_delivery_build_controls_contract()["ok"] is True


def test_configuration_permissions_seed_and_assurance_are_executable():
    manifest = table_stakes_capability_manifest()
    validation = validate_table_stakes_capability_coverage()
    assert governance_smoke_test()["ok"] is True
    assert manifest["ok"] is True
    assert validation["ok"] is True
    assert not validation["invalid_tables"]


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-capital_projects_delivery"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-capital_projects_delivery"})["dead_letter_table"].endswith("dead_letter_event")


def test_standalone_manifest_is_exposed_from_contracts():
    manifest = standalone_app_manifest()
    assert manifest["ok"] is True
    assert manifest["routes"]
    assert manifest["workflows"]


def test_manifest_and_event_contract():
    test_manifest_runtime_and_event_contract()


def test_service_and_route_surface_are_executable():
    test_service_route_workflow_and_ui_surface_are_executable()


def test_configuration_permissions_and_seed_hooks_are_executable():
    test_configuration_permissions_seed_and_assurance_are_executable()

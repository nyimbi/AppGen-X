from pyAppGen.pbcs.advertising_campaign_operations import implementation_contract
from pyAppGen.pbcs.advertising_campaign_operations import package_discovery_plan
from pyAppGen.pbcs.advertising_campaign_operations import package_metadata_manifest
from pyAppGen.pbcs.advertising_campaign_operations import validate_package_metadata
from pyAppGen.pbcs.advertising_campaign_operations.agent import agent_skill_manifest
from pyAppGen.pbcs.advertising_campaign_operations.agent import chatbot_interface_contract
from pyAppGen.pbcs.advertising_campaign_operations.agent import datastore_crud_plan
from pyAppGen.pbcs.advertising_campaign_operations.agent import document_instruction_plan
from pyAppGen.pbcs.advertising_campaign_operations.config import governance_smoke_test
from pyAppGen.pbcs.advertising_campaign_operations.events import event_contract_manifest
from pyAppGen.pbcs.advertising_campaign_operations.events import validate_event_contract
from pyAppGen.pbcs.advertising_campaign_operations.handlers import dispatch_event
from pyAppGen.pbcs.advertising_campaign_operations.handlers import handler_manifest
from pyAppGen.pbcs.advertising_campaign_operations.models import model_contracts
from pyAppGen.pbcs.advertising_campaign_operations.release_evidence import build_release_evidence
from pyAppGen.pbcs.advertising_campaign_operations.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.advertising_campaign_operations.release_evidence import validate_release_evidence
from pyAppGen.pbcs.advertising_campaign_operations.routes import api_route_contracts
from pyAppGen.pbcs.advertising_campaign_operations.routes import validate_api_route_contracts
from pyAppGen.pbcs.advertising_campaign_operations.schema_contract import build_schema_contract
from pyAppGen.pbcs.advertising_campaign_operations.service_contract import build_service_contract
from pyAppGen.pbcs.advertising_campaign_operations.ui import advertising_campaign_operations_standalone_app_contract
from pyAppGen.pbcs.advertising_campaign_operations.ui import advertising_campaign_operations_ui_contract
from pyAppGen.pbcs.advertising_campaign_operations.workflows import workflow_catalog


def test_schema_service_and_release_evidence_are_executable():
    service_contract = build_service_contract()
    assert build_schema_contract()["ok"] is True
    assert service_contract["ok"] is True
    assert service_contract["command_methods"]
    assert service_contract["query_methods"]
    assert service_contract["shared_table_access"] is False
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_metadata_and_models_are_package_local():
    contract = implementation_contract()
    assert contract["pbc"] == "advertising_campaign_operations"
    assert package_metadata_manifest()["pbc"] == "advertising_campaign_operations"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert model_contracts()["ok"] is True
    assert contract["standalone_app"]["ok"] is True


def test_ui_and_workflow_contracts_expose_standalone_surface():
    ui_contract = advertising_campaign_operations_ui_contract()
    standalone = advertising_campaign_operations_standalone_app_contract()
    workflows = workflow_catalog()
    assert ui_contract["ok"] is True
    assert standalone["ok"] is True
    assert workflows["ok"] is True
    assert ui_contract["forms"]
    assert ui_contract["wizards"]
    assert ui_contract["controls"]


def test_agent_chatbot_and_document_planning_are_governed():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    plan = document_instruction_plan("Campaign launch brief", "Create campaign plan")
    assert plan["ok"] is True
    assert plan["crud_preview"]["action"] == "create"
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_routes_services_and_events_stay_on_appgen_contracts():
    route_contracts = api_route_contracts()
    assert route_contracts["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert build_service_contract()["contracts"]
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_configuration_permissions_and_handlers_have_smoke_coverage():
    assert governance_smoke_test()["ok"] is True
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": ("PolicyChanged", "CustomerUpdated", "SupplierQualified")[0], "idempotency_key": "idem-advertising_campaign_operations"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-advertising_campaign_operations"})["dead_letter_table"].endswith("dead_letter_event")

# AppGen-X canonical source-audit contract tests for advertising_campaign_operations.
def test_service_and_route_surface_are_executable():
    import importlib

    services = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.services")
    routes = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.routes")
    service_contracts = services.service_operation_contracts()
    route_contracts = routes.api_route_contracts()
    route_validation = routes.validate_api_route_contracts()
    operation_contract = service_contracts.get("operation_contract") or service_contracts.get("contracts", ({},))[0]
    assert service_contracts["ok"] is True
    assert route_contracts["ok"] is True
    assert route_validation["ok"] is True
    assert operation_contract


def test_configuration_permissions_and_seed_hooks_are_executable():
    import importlib

    config = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.config")
    permissions = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.permissions")
    seed_data = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.seed_data")
    assert config.governance_smoke_test()["ok"] is True
    assert permissions.smoke_test()["ok"] is True
    assert seed_data.smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    import importlib

    events = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.events")
    handlers = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.handlers")
    event_contract_manifest = events.event_contract_manifest
    validate_event_contract = events.validate_event_contract
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    handler_smoke = handlers.smoke_test()
    assert handler_smoke["ok"] is True


def test_release_registration_and_package_metadata_are_executable():
    import importlib

    package = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations")
    release_evidence = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.release_evidence")
    assert package.package_metadata_manifest()["ok"] is True
    assert package.validate_package_metadata()["ok"] is True
    assert package.package_discovery_plan()["ok"] is True
    assert release_evidence.release_readiness_manifest()["ok"] is True
    assert release_evidence.validate_release_evidence()["ok"] is True


def test_generated_schema_service_and_release_evidence():
    import importlib

    schema_contract = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.schema_contract")
    service_contract = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.service_contract")
    release_evidence = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.release_evidence")
    assert schema_contract.build_schema_contract()["ok"] is True
    assert service_contract.build_service_contract()["ok"] is True
    assert release_evidence.build_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    import importlib

    manifest = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.manifest")
    events = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations.events")
    assert manifest.PBC_MANIFEST["pbc"] == "advertising_campaign_operations"
    assert events.event_contract_manifest()["ok"] is True
    assert events.validate_event_contract()["ok"] is True


def test_registration_plan_is_side_effect_free():
    import importlib

    package = importlib.import_module("pyAppGen.pbcs.advertising_campaign_operations")
    plan = package.registration_plan()
    assert plan["ok"] is True
    assert package.package_metadata_manifest()["ok"] is True
    assert package.validate_package_metadata()["ok"] is True
    assert package.package_discovery_plan()["ok"] is True

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
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
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

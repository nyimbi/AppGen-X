from pyAppGen.pbcs.insurance_claims_policy import implementation_contract
from pyAppGen.pbcs.insurance_claims_policy import package_discovery_plan
from pyAppGen.pbcs.insurance_claims_policy import package_metadata_manifest
from pyAppGen.pbcs.insurance_claims_policy import validate_package_metadata
from pyAppGen.pbcs.insurance_claims_policy.agent import agent_skill_manifest
from pyAppGen.pbcs.insurance_claims_policy.agent import chatbot_interface_contract
from pyAppGen.pbcs.insurance_claims_policy.agent import datastore_crud_plan
from pyAppGen.pbcs.insurance_claims_policy.agent import document_instruction_plan
from pyAppGen.pbcs.insurance_claims_policy.config import governance_smoke_test
from pyAppGen.pbcs.insurance_claims_policy.events import event_contract_manifest
from pyAppGen.pbcs.insurance_claims_policy.events import validate_event_contract
from pyAppGen.pbcs.insurance_claims_policy.handlers import dispatch_event
from pyAppGen.pbcs.insurance_claims_policy.handlers import handler_manifest
from pyAppGen.pbcs.insurance_claims_policy.release_evidence import build_release_evidence
from pyAppGen.pbcs.insurance_claims_policy.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.insurance_claims_policy.release_evidence import validate_release_evidence
from pyAppGen.pbcs.insurance_claims_policy.routes import api_route_contracts
from pyAppGen.pbcs.insurance_claims_policy.routes import validate_api_route_contracts
from pyAppGen.pbcs.insurance_claims_policy.schema_contract import build_schema_contract
from pyAppGen.pbcs.insurance_claims_policy.service_contract import build_service_contract
from pyAppGen.pbcs.insurance_claims_policy.services import service_operation_contracts
from pyAppGen.pbcs.insurance_claims_policy.ui import insurance_claims_policy_standalone_app_contract
from pyAppGen.pbcs.insurance_claims_policy.ui import insurance_claims_policy_ui_contract


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_event_and_ui_contracts_are_executable():
    contract = implementation_contract()
    assert contract["pbc"] == "insurance_claims_policy"
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    assert insurance_claims_policy_ui_contract()["ok"] is True
    assert insurance_claims_policy_standalone_app_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    plan = document_instruction_plan("Fire loss with reserve request.", "prepare coverage and reserve review")
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert plan["ok"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "insurance_claims_policy"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_route_surface_and_handlers_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert handler_manifest()["ok"] is True
    assert dispatch_event({"event_type": "CustomerUpdated", "event_id": "evt-1"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "event_id": "evt-2"})["dead_letter_table"].endswith("dead_letter_event")


def test_configuration_and_governance_are_executable():
    assert governance_smoke_test()["ok"] is True

# AppGen-X canonical source-audit contract tests for insurance_claims_policy.
def test_service_and_route_surface_are_executable():
    import importlib

    services = importlib.import_module("pyAppGen.pbcs.insurance_claims_policy.services")
    routes = importlib.import_module("pyAppGen.pbcs.insurance_claims_policy.routes")
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

    config = importlib.import_module("pyAppGen.pbcs.insurance_claims_policy.config")
    permissions = importlib.import_module("pyAppGen.pbcs.insurance_claims_policy.permissions")
    seed_data = importlib.import_module("pyAppGen.pbcs.insurance_claims_policy.seed_data")
    assert config.governance_smoke_test()["ok"] is True
    assert permissions.smoke_test()["ok"] is True
    assert seed_data.smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    import importlib

    events = importlib.import_module("pyAppGen.pbcs.insurance_claims_policy.events")
    handlers = importlib.import_module("pyAppGen.pbcs.insurance_claims_policy.handlers")
    event_contract_manifest = events.event_contract_manifest
    validate_event_contract = events.validate_event_contract
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    handler_smoke = handlers.smoke_test()
    assert handler_smoke["ok"] is True


def test_release_registration_and_package_metadata_are_executable():
    import importlib

    package = importlib.import_module("pyAppGen.pbcs.insurance_claims_policy")
    release_evidence = importlib.import_module("pyAppGen.pbcs.insurance_claims_policy.release_evidence")
    assert package.package_metadata_manifest()["ok"] is True
    assert package.validate_package_metadata()["ok"] is True
    assert package.package_discovery_plan()["ok"] is True
    assert release_evidence.release_readiness_manifest()["ok"] is True
    assert release_evidence.validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    import importlib

    manifest = importlib.import_module("pyAppGen.pbcs.insurance_claims_policy.manifest")
    events = importlib.import_module("pyAppGen.pbcs.insurance_claims_policy.events")
    assert manifest.PBC_MANIFEST["pbc"] == "insurance_claims_policy"
    assert events.event_contract_manifest()["ok"] is True
    assert events.validate_event_contract()["ok"] is True

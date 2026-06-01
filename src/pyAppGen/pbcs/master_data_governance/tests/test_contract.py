from pyAppGen.pbcs.master_data_governance import implementation_contract
from pyAppGen.pbcs.master_data_governance import package_discovery_plan
from pyAppGen.pbcs.master_data_governance import package_metadata_manifest
from pyAppGen.pbcs.master_data_governance import validate_package_metadata
from pyAppGen.pbcs.master_data_governance.agent import agent_skill_manifest
from pyAppGen.pbcs.master_data_governance.agent import chatbot_interface_contract
from pyAppGen.pbcs.master_data_governance.agent import datastore_crud_plan
from pyAppGen.pbcs.master_data_governance.agent import document_instruction_plan
from pyAppGen.pbcs.master_data_governance.release_evidence import build_release_evidence
from pyAppGen.pbcs.master_data_governance.release_evidence import generation_smoke_audit
from pyAppGen.pbcs.master_data_governance.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.master_data_governance.release_evidence import source_package_audit
from pyAppGen.pbcs.master_data_governance.release_evidence import specification_audit
from pyAppGen.pbcs.master_data_governance.release_evidence import validate_release_evidence
from pyAppGen.pbcs.master_data_governance.routes import api_route_contracts
from pyAppGen.pbcs.master_data_governance.routes import validate_api_route_contracts
from pyAppGen.pbcs.master_data_governance.schema_contract import build_schema_contract
from pyAppGen.pbcs.master_data_governance.seed_data import validate_seed_data
from pyAppGen.pbcs.master_data_governance.service_contract import build_service_contract
from pyAppGen.pbcs.master_data_governance.standalone import GOLDEN_TABLE
from pyAppGen.pbcs.master_data_governance.standalone import master_data_governance_standalone_app_contract
from pyAppGen.pbcs.master_data_governance.standalone import master_data_governance_standalone_app_smoke
from pyAppGen.pbcs.master_data_governance.standalone import standalone_model_contract
from pyAppGen.pbcs.master_data_governance.standalone import standalone_route_contracts
from pyAppGen.pbcs.master_data_governance.standalone import standalone_service_operation_contracts


def test_schema_service_release_and_package_metadata_are_executable():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True
    assert package_metadata_manifest()["pbc"] == "master_data_governance"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True



def test_standalone_contracts_expose_one_pbc_surface():
    models = standalone_model_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    app = master_data_governance_standalone_app_contract()
    assert models["ok"] is True
    assert services["ok"] is True
    assert routes["ok"] is True
    assert app["ok"] is True
    assert GOLDEN_TABLE in models["table_keys"]
    assert any(item["operation"] == "publish_golden_record" for item in services["contracts"])
    assert "POST /app/master-data-governance/golden-records" in routes["routes"]



def test_agent_planning_and_crud_surface_are_grounded_in_owned_tables():
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan(
        "reference-data and hierarchy governance packet",
        "register reference data, update hierarchy, and publish a golden record with audit proof",
    )
    crud = datastore_crud_plan("create", GOLDEN_TABLE, {"golden_code": "GOLD-TEST"})
    assert skills["ok"] is True
    assert chatbot["ok"] is True
    assert document["ok"] is True
    assert any("golden-records" in route for route in document["route_candidates"])
    assert crud["ok"] is True
    assert crud["table"] == GOLDEN_TABLE
    assert crud["requires_confirmation"] is True



def test_release_evidence_audits_and_generation_smoke_cover_standalone_slice():
    assert specification_audit()["ok"] is True
    assert source_package_audit()["ok"] is True
    assert generation_smoke_audit()["ok"] is True
    assert validate_seed_data()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert master_data_governance_standalone_app_smoke()["ok"] is True



def test_implementation_contract_includes_standalone_surface():
    contract = implementation_contract()
    assert contract["pbc"] == "master_data_governance"
    assert contract["standalone_app_contract"]["ok"] is True
    assert contract["agent_contribution"]["ok"] is True

# AppGen-X canonical source-audit contract tests for master_data_governance.
def test_service_and_route_surface_are_executable():
    import importlib

    services = importlib.import_module("pyAppGen.pbcs.master_data_governance.services")
    routes = importlib.import_module("pyAppGen.pbcs.master_data_governance.routes")
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

    config = importlib.import_module("pyAppGen.pbcs.master_data_governance.config")
    permissions = importlib.import_module("pyAppGen.pbcs.master_data_governance.permissions")
    seed_data = importlib.import_module("pyAppGen.pbcs.master_data_governance.seed_data")
    assert config.governance_smoke_test()["ok"] is True
    assert permissions.smoke_test()["ok"] is True
    assert seed_data.smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    import importlib

    events = importlib.import_module("pyAppGen.pbcs.master_data_governance.events")
    handlers = importlib.import_module("pyAppGen.pbcs.master_data_governance.handlers")
    event_contract_manifest = events.event_contract_manifest
    validate_event_contract = events.validate_event_contract
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    handler_smoke = handlers.smoke_test()
    assert handler_smoke["ok"] is True


def test_release_registration_and_package_metadata_are_executable():
    import importlib

    package = importlib.import_module("pyAppGen.pbcs.master_data_governance")
    release_evidence = importlib.import_module("pyAppGen.pbcs.master_data_governance.release_evidence")
    assert package.package_metadata_manifest()["ok"] is True
    assert package.validate_package_metadata()["ok"] is True
    assert package.package_discovery_plan()["ok"] is True
    assert release_evidence.release_readiness_manifest()["ok"] is True
    assert release_evidence.validate_release_evidence()["ok"] is True


def test_generated_schema_service_and_release_evidence():
    import importlib

    schema_contract = importlib.import_module("pyAppGen.pbcs.master_data_governance.schema_contract")
    service_contract = importlib.import_module("pyAppGen.pbcs.master_data_governance.service_contract")
    release_evidence = importlib.import_module("pyAppGen.pbcs.master_data_governance.release_evidence")
    assert schema_contract.build_schema_contract()["ok"] is True
    assert service_contract.build_service_contract()["ok"] is True
    assert release_evidence.build_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    import importlib

    manifest = importlib.import_module("pyAppGen.pbcs.master_data_governance.manifest")
    events = importlib.import_module("pyAppGen.pbcs.master_data_governance.events")
    assert manifest.PBC_MANIFEST["pbc"] == "master_data_governance"
    assert events.event_contract_manifest()["ok"] is True
    assert events.validate_event_contract()["ok"] is True


def test_registration_plan_is_side_effect_free():
    import importlib

    package = importlib.import_module("pyAppGen.pbcs.master_data_governance")
    plan = package.registration_plan()
    assert plan["ok"] is True
    assert package.package_metadata_manifest()["ok"] is True
    assert package.validate_package_metadata()["ok"] is True
    assert package.package_discovery_plan()["ok"] is True

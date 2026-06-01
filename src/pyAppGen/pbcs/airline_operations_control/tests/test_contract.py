from pyAppGen.pbcs.airline_operations_control import implementation_contract
from pyAppGen.pbcs.airline_operations_control import package_discovery_plan
from pyAppGen.pbcs.airline_operations_control import package_metadata_manifest
from pyAppGen.pbcs.airline_operations_control import validate_package_metadata
from pyAppGen.pbcs.airline_operations_control.agent import agent_skill_manifest
from pyAppGen.pbcs.airline_operations_control.agent import chatbot_interface_contract
from pyAppGen.pbcs.airline_operations_control.agent import datastore_crud_plan
from pyAppGen.pbcs.airline_operations_control.agent import document_instruction_plan
from pyAppGen.pbcs.airline_operations_control.config import governance_smoke_test
from pyAppGen.pbcs.airline_operations_control.events import event_contract_manifest
from pyAppGen.pbcs.airline_operations_control.events import validate_event_contract
from pyAppGen.pbcs.airline_operations_control.handlers import dispatch_event
from pyAppGen.pbcs.airline_operations_control.handlers import handler_manifest
from pyAppGen.pbcs.airline_operations_control.permissions import permission_manifest
from pyAppGen.pbcs.airline_operations_control.release_evidence import build_release_evidence
from pyAppGen.pbcs.airline_operations_control.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.airline_operations_control.release_evidence import validate_release_evidence
from pyAppGen.pbcs.airline_operations_control.routes import api_route_contracts
from pyAppGen.pbcs.airline_operations_control.routes import validate_api_route_contracts
from pyAppGen.pbcs.airline_operations_control.schema_contract import build_schema_contract
from pyAppGen.pbcs.airline_operations_control.service_contract import build_service_contract
from pyAppGen.pbcs.airline_operations_control.services import service_operation_contracts
from pyAppGen.pbcs.airline_operations_control.standalone import standalone_app_manifest
from pyAppGen.pbcs.airline_operations_control.ui import airline_operations_control_standalone_app_contract


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    assert implementation_contract()["pbc"] == "airline_operations_control"
    assert implementation_contract()["standalone_app"]["ok"] is True
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert document_instruction_plan("doc", "create") ["ok"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "airline_operations_control"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_route_permissions_and_ui_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert permission_manifest()["ok"] is True
    assert airline_operations_control_standalone_app_contract()["ok"] is True
    assert standalone_app_manifest()["ok"] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0], "idempotency_key": "idem-airline_operations_control"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-airline_operations_control"})["dead_letter_table"].endswith("dead_letter_event")

# AppGen-X canonical source-audit contract tests for airline_operations_control.
def test_service_and_route_surface_are_executable():
    import importlib

    services = importlib.import_module("pyAppGen.pbcs.airline_operations_control.services")
    routes = importlib.import_module("pyAppGen.pbcs.airline_operations_control.routes")
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

    config = importlib.import_module("pyAppGen.pbcs.airline_operations_control.config")
    permissions = importlib.import_module("pyAppGen.pbcs.airline_operations_control.permissions")
    seed_data = importlib.import_module("pyAppGen.pbcs.airline_operations_control.seed_data")
    assert config.governance_smoke_test()["ok"] is True
    assert permissions.smoke_test()["ok"] is True
    assert seed_data.smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    import importlib

    events = importlib.import_module("pyAppGen.pbcs.airline_operations_control.events")
    handlers = importlib.import_module("pyAppGen.pbcs.airline_operations_control.handlers")
    event_contract_manifest = events.event_contract_manifest
    validate_event_contract = events.validate_event_contract
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    handler_smoke = handlers.smoke_test()
    assert handler_smoke["ok"] is True


def test_release_registration_and_package_metadata_are_executable():
    import importlib

    package = importlib.import_module("pyAppGen.pbcs.airline_operations_control")
    release_evidence = importlib.import_module("pyAppGen.pbcs.airline_operations_control.release_evidence")
    assert package.package_metadata_manifest()["ok"] is True
    assert package.validate_package_metadata()["ok"] is True
    assert package.package_discovery_plan()["ok"] is True
    assert release_evidence.release_readiness_manifest()["ok"] is True
    assert release_evidence.validate_release_evidence()["ok"] is True

from pyAppGen.pbcs.defense_readiness_logistics import implementation_contract, package_discovery_plan, package_metadata_manifest, validate_package_metadata
from pyAppGen.pbcs.defense_readiness_logistics.agent import agent_skill_manifest, chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from pyAppGen.pbcs.defense_readiness_logistics.config import governance_smoke_test
from pyAppGen.pbcs.defense_readiness_logistics.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.defense_readiness_logistics.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.defense_readiness_logistics.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.defense_readiness_logistics.routes import ROUTES, api_route_contracts, dispatch_route, validate_api_route_contracts
from pyAppGen.pbcs.defense_readiness_logistics.schema_contract import build_schema_contract
from pyAppGen.pbcs.defense_readiness_logistics.seed_data import seed_plan, validate_seed_data
from pyAppGen.pbcs.defense_readiness_logistics.service_contract import build_service_contract
from pyAppGen.pbcs.defense_readiness_logistics.services import service_operation_contracts


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    assert implementation_contract()["pbc"] == "defense_readiness_logistics"
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert composed_agent_contribution()["ok"] is True
    assert document_instruction_plan("doc", "create") ["ok"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "defense_readiness_logistics"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    route_result = dispatch_route(
        ROUTES[0],
        {
            "tenant_id": "tenant-a",
            "unit_id": "route-unit-a",
            "unit_code": "route-alpha",
            "personnel": {"available": 12, "required": 10, "certified_roles": 4, "required_certified_roles": 3},
            "serviceable_assets": 3,
            "required_assets": 2,
            "supply": {"critical_fill_rate": 0.95},
            "ammo_fill_rate": 0.9,
            "fuel_days": 2,
            "inspection_evidence": ("route-pack",),
            "commander_approved": True,
        },
    )
    assert route_result["ok"] is True


def test_configuration_permissions_seed_and_governance_are_executable():
    assert governance_smoke_test()["ok"] is True
    assert seed_plan()["ok"] is True
    assert validate_seed_data()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0], "idempotency_key": "idem-defense_readiness_logistics"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-defense_readiness_logistics"})["dead_letter_table"].endswith("dead_letter_event")

# AppGen-X canonical source-audit contract tests for defense_readiness_logistics.
def test_service_and_route_surface_are_executable():
    import importlib

    services = importlib.import_module("pyAppGen.pbcs.defense_readiness_logistics.services")
    routes = importlib.import_module("pyAppGen.pbcs.defense_readiness_logistics.routes")
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

    config = importlib.import_module("pyAppGen.pbcs.defense_readiness_logistics.config")
    permissions = importlib.import_module("pyAppGen.pbcs.defense_readiness_logistics.permissions")
    seed_data = importlib.import_module("pyAppGen.pbcs.defense_readiness_logistics.seed_data")
    assert config.governance_smoke_test()["ok"] is True
    assert permissions.smoke_test()["ok"] is True
    assert seed_data.smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    import importlib

    events = importlib.import_module("pyAppGen.pbcs.defense_readiness_logistics.events")
    handlers = importlib.import_module("pyAppGen.pbcs.defense_readiness_logistics.handlers")
    event_contract_manifest = events.event_contract_manifest
    validate_event_contract = events.validate_event_contract
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    handler_smoke = handlers.smoke_test()
    assert handler_smoke["ok"] is True


def test_release_registration_and_package_metadata_are_executable():
    import importlib

    package = importlib.import_module("pyAppGen.pbcs.defense_readiness_logistics")
    release_evidence = importlib.import_module("pyAppGen.pbcs.defense_readiness_logistics.release_evidence")
    assert package.package_metadata_manifest()["ok"] is True
    assert package.validate_package_metadata()["ok"] is True
    assert package.package_discovery_plan()["ok"] is True
    assert release_evidence.release_readiness_manifest()["ok"] is True
    assert release_evidence.validate_release_evidence()["ok"] is True

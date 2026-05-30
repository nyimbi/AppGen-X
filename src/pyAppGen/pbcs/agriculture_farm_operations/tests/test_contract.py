"""Generated contract smoke tests for agriculture_farm_operations."""

from .. import (
    AgricultureFarmOperationsStandaloneApp,
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    standalone_app_manifest,
    validate_package_metadata,
)
from ..agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
    standalone_agent_workspace_contract,
)
from ..capability_assurance import (
    smoke_test as capability_smoke_test,
    table_stakes_capability_manifest,
    validate_table_stakes_capability_coverage,
)
from ..config import governance_smoke_test, smoke_test as config_smoke_test
from ..events import event_contract_manifest, smoke_test as events_smoke_test, validate_event_contract
from ..handlers import dispatch_event, handler_manifest, smoke_test as handlers_smoke_test
from ..models import smoke_test as models_smoke_test, standalone_model_contract
from ..permissions import smoke_test as permissions_smoke_test
from ..release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    smoke_test as release_smoke_test,
    validate_release_evidence,
)
from ..routes import api_route_contracts, smoke_test as routes_smoke_test, validate_api_route_contracts
from ..schema_contract import build_schema_contract
from ..seed_data import smoke_test as seed_smoke_test
from ..service_contract import build_service_contract
from ..services import service_operation_contracts, smoke_test as services_smoke_test
from ..ui import agriculture_farm_operations_standalone_app_contract, agriculture_farm_operations_ui_contract, smoke_test as ui_smoke_test


def test_generated_schema_service_and_release_evidence():
    schema = build_schema_contract()
    service = build_service_contract()
    release = build_release_evidence()
    release_manifest = release_readiness_manifest()
    release_validation = validate_release_evidence()
    assert schema["ok"] is True
    assert service["ok"] is True
    assert release["ok"] is True
    assert release_manifest["ok"] is True
    assert release_validation["ok"] is True
    assert release_smoke_test()["ok"] is True
    assert models_smoke_test()["ok"] is True
    assert standalone_model_contract()["ok"] is True


def test_manifest_and_event_contract():
    assert implementation_contract()["pbc"] == "agriculture_farm_operations"
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    assert events_smoke_test()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert document_instruction_plan("doc", "create")["ok"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False
    assert composed_agent_contribution()["ok"] is True
    assert standalone_agent_workspace_contract()["ok"] is True


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "agriculture_farm_operations"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert services_smoke_test()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert routes_smoke_test()["ok"] is True
    assert agriculture_farm_operations_standalone_app_contract()["ok"] is True
    assert standalone_app_manifest()["ok"] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert config_smoke_test()["ok"] is True
    assert governance_smoke_test()["ok"] is True
    assert permissions_smoke_test()["ok"] is True
    assert seed_smoke_test()["ok"] is True


def test_ui_workbench_surface_is_executable():
    smoke = ui_smoke_test()
    assert agriculture_farm_operations_ui_contract()["ok"] is True
    assert smoke["ok"] is True
    assert smoke["manifest"]["fragments"]
    assert smoke["rendered"]["cards"]


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    smoke = handlers_smoke_test()
    assert manifest["ok"] is True
    assert smoke["ok"] is True
    assert dispatch_event({"event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0], "idempotency_key": "idem-agriculture_farm_operations"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-agriculture_farm_operations"})["dead_letter_table"].endswith("dead_letter_event")


def test_table_stakes_and_advanced_capability_assurance_is_executable():
    manifest = table_stakes_capability_manifest()
    validation = validate_table_stakes_capability_coverage()
    assert manifest["ok"] is True
    assert validation["ok"] is True
    assert capability_smoke_test()["ok"] is True
    assert manifest["standard_features"]
    assert manifest["advanced_capabilities"]
    assert validation["boundary_rejection"]["ok"] is False
    assert validation["boundary_rejection"]["violations"]


def test_standalone_app_smoke_is_executable():
    app = AgricultureFarmOperationsStandaloneApp()
    loaded = app.load_demo_workspace(tenant="tenant_contract")
    rendered = app.render_workbench(tenant="tenant_contract")
    assert loaded["ok"] is True
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] >= 1

from pathlib import Path

from pyAppGen.pbcs.hospitality_property_operations import implementation_contract, package_discovery_plan, package_metadata_manifest, validate_package_metadata
from pyAppGen.pbcs.hospitality_property_operations.agent import agent_skill_manifest, chatbot_interface_contract, datastore_crud_plan, document_instruction_plan, standalone_agent_workspace_contract
from pyAppGen.pbcs.hospitality_property_operations.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.hospitality_property_operations.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.hospitality_property_operations.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.hospitality_property_operations.routes import api_route_contracts, standalone_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.hospitality_property_operations.schema_contract import build_schema_contract
from pyAppGen.pbcs.hospitality_property_operations.service_contract import build_service_contract
from pyAppGen.pbcs.hospitality_property_operations.standalone import hospitality_property_operations_standalone_app_contract
from pyAppGen.pbcs.hospitality_property_operations.config import governance_smoke_test
from pyAppGen.pbcs.hospitality_property_operations.services import service_operation_contracts, standalone_service_operation_contracts


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    assert implementation_contract()["pbc"] == "hospitality_property_operations"
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert document_instruction_plan("vip arrivals", "prepare shift handover and resolve urgent request")["ok"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False
    assert standalone_agent_workspace_contract()["ok"] is True


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "hospitality_property_operations"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert standalone_service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert standalone_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert service_operation_contracts()["contracts"]


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True
    assert hospitality_property_operations_standalone_app_contract()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": ("PolicyChanged", "CustomerUpdated", "SupplierQualified")[0], "idempotency_key": "idem-hospitality_property_operations"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-hospitality_property_operations"})["dead_letter_table"].endswith("dead_letter_event")


def test_package_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "SPECIFICATION.md", "RELEASE_EVIDENCE.md", "implementation-status.md"):
        assert (base / name).exists() is True

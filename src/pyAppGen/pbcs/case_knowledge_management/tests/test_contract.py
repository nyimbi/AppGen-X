from pyAppGen.pbcs.case_knowledge_management import implementation_contract
from pyAppGen.pbcs.case_knowledge_management import package_discovery_plan
from pyAppGen.pbcs.case_knowledge_management import package_metadata_manifest
from pyAppGen.pbcs.case_knowledge_management import validate_package_metadata
from pyAppGen.pbcs.case_knowledge_management.agent import agent_skill_manifest
from pyAppGen.pbcs.case_knowledge_management.agent import chatbot_interface_contract
from pyAppGen.pbcs.case_knowledge_management.agent import datastore_crud_plan
from pyAppGen.pbcs.case_knowledge_management.agent import document_instruction_plan
from pyAppGen.pbcs.case_knowledge_management.config import governance_smoke_test
from pyAppGen.pbcs.case_knowledge_management.events import event_contract_manifest
from pyAppGen.pbcs.case_knowledge_management.events import validate_event_contract
from pyAppGen.pbcs.case_knowledge_management.handlers import dispatch_event
from pyAppGen.pbcs.case_knowledge_management.handlers import handler_manifest
from pyAppGen.pbcs.case_knowledge_management.release_evidence import build_release_evidence
from pyAppGen.pbcs.case_knowledge_management.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.case_knowledge_management.release_evidence import validate_release_evidence
from pyAppGen.pbcs.case_knowledge_management.routes import api_route_contracts
from pyAppGen.pbcs.case_knowledge_management.routes import validate_api_route_contracts
from pyAppGen.pbcs.case_knowledge_management.schema_contract import build_schema_contract
from pyAppGen.pbcs.case_knowledge_management.service_contract import build_service_contract
from pyAppGen.pbcs.case_knowledge_management.services import service_operation_contracts


def test_generated_schema_service_and_release_evidence():
    schema = build_schema_contract()
    assert schema["ok"] is True
    assert len(schema["tables"]) >= 24
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    assert contract["pbc"] == "case_knowledge_management"
    assert "create_support_case" in contract["advanced_runtime"]["operations"]
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert document_instruction_plan("Please create a case for API failures.", "create")["ok"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "case_knowledge_management"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    route_contracts = api_route_contracts()
    assert route_contracts["ok"] is True
    assert any(route["path"] == "/knowledge-workbench" for route in route_contracts["routes"])
    assert validate_api_route_contracts()["ok"] is True
    assert service_operation_contracts()["operation_contract"]


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    accepted = dispatch_event({"event_type": "ServiceTicketOpened", "event_id": "idem", "payload": {"tenant": "tenant-smoke"}})
    assert accepted["ok"] is True
    duplicate = dispatch_event({"event_type": "ServiceTicketOpened", "event_id": "idem", "payload": {"tenant": "tenant-smoke"}}, accepted["state"])
    assert duplicate["status"] == "duplicate"
    rejected = dispatch_event({"event_type": "Unexpected", "event_id": "other", "payload": {"tenant": "tenant-smoke"}}, duplicate["state"])
    assert rejected["dead_letter_table"].endswith("dead_letter_event")

from pyAppGen.pbcs.chemical_batch_compliance import implementation_contract
from pyAppGen.pbcs.chemical_batch_compliance import package_discovery_plan
from pyAppGen.pbcs.chemical_batch_compliance import package_metadata_manifest
from pyAppGen.pbcs.chemical_batch_compliance import validate_package_metadata
from pyAppGen.pbcs.chemical_batch_compliance.agent import agent_skill_manifest
from pyAppGen.pbcs.chemical_batch_compliance.agent import chatbot_interface_contract
from pyAppGen.pbcs.chemical_batch_compliance.agent import datastore_crud_plan
from pyAppGen.pbcs.chemical_batch_compliance.agent import document_instruction_plan
from pyAppGen.pbcs.chemical_batch_compliance.config import governance_smoke_test
from pyAppGen.pbcs.chemical_batch_compliance.events import event_contract_manifest
from pyAppGen.pbcs.chemical_batch_compliance.events import validate_event_contract
from pyAppGen.pbcs.chemical_batch_compliance.handlers import dispatch_event
from pyAppGen.pbcs.chemical_batch_compliance.handlers import handler_manifest
from pyAppGen.pbcs.chemical_batch_compliance.release_evidence import build_release_evidence
from pyAppGen.pbcs.chemical_batch_compliance.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.chemical_batch_compliance.release_evidence import validate_release_evidence
from pyAppGen.pbcs.chemical_batch_compliance.routes import api_route_contracts
from pyAppGen.pbcs.chemical_batch_compliance.routes import validate_api_route_contracts
from pyAppGen.pbcs.chemical_batch_compliance.schema_contract import build_schema_contract
from pyAppGen.pbcs.chemical_batch_compliance.service_contract import build_service_contract
from pyAppGen.pbcs.chemical_batch_compliance.services import service_operation_contracts
from pyAppGen.pbcs.chemical_batch_compliance.ui import chemical_batch_compliance_ui_contract


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    assert contract["pbc"] == "chemical_batch_compliance"
    assert contract["schema_contract"]["ok"] is True
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    plan = document_instruction_plan("Formula Code: CBR-77", "update the formula release note")
    assert plan["ok"] is True
    assert plan["requires_human_confirmation"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "chemical_batch_compliance"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    contracts = service_operation_contracts()
    assert contracts["ok"] is True
    assert any(item["operation"] == "record_batch" for item in contracts["contracts"])
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert service_operation_contracts()["operation_contract"]


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True
    ui_contract = chemical_batch_compliance_ui_contract()
    assert ui_contract["ok"] is True
    assert len(ui_contract["full_capability_surface"]["forms"]) == 4
    assert len(ui_contract["full_capability_surface"]["wizards"]) == 3


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0], "idempotency_key": "idem-chemical_batch_compliance"})["ok"] is True
    failure = dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-chemical_batch_compliance"})
    assert failure["dead_letter_table"].endswith("dead_letter_event")

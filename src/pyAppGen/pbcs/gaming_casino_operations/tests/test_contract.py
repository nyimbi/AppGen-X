from pathlib import Path

from pyAppGen.pbcs.gaming_casino_operations import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.gaming_casino_operations.agent import agent_skill_manifest, chatbot_interface_contract, document_instruction_plan, datastore_crud_plan
from pyAppGen.pbcs.gaming_casino_operations.config import governance_smoke_test
from pyAppGen.pbcs.gaming_casino_operations.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.gaming_casino_operations.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.gaming_casino_operations.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.gaming_casino_operations.routes import api_route_contracts, standalone_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.gaming_casino_operations.schema_contract import build_schema_contract
from pyAppGen.pbcs.gaming_casino_operations.service_contract import build_service_contract
from pyAppGen.pbcs.gaming_casino_operations.services import service_operation_contracts
from pyAppGen.pbcs.gaming_casino_operations.standalone import gaming_casino_operations_standalone_app_contract


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    evidence = build_release_evidence()
    assert evidence["ok"] is True
    assert evidence["standalone_app"]["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    assert contract["pbc"] == "gaming_casino_operations"
    assert contract["standalone_app_contract"]["ok"] is True
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert document_instruction_plan("jackpot report", "approve payout")["wizard_candidates"]
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "gaming_casino_operations"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    service_contracts = service_operation_contracts()
    assert service_contracts["ok"] is True
    assert service_contracts["operation_contract"]
    assert api_route_contracts()["ok"] is True
    assert standalone_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert gaming_casino_operations_standalone_app_contract()["ok"] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": ("PolicyChanged", "CustomerUpdated", "SupplierQualified")[0], "idempotency_key": "idem-gaming_casino_operations"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-gaming_casino_operations"})["dead_letter_table"].endswith("dead_letter_event")


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md", "standalone.py"):
        assert (base / name).exists() is True

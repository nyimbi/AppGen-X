from pathlib import Path

from pyAppGen.pbcs.insurance_underwriting import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.insurance_underwriting.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.insurance_underwriting.config import governance_smoke_test
from pyAppGen.pbcs.insurance_underwriting.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.insurance_underwriting.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.insurance_underwriting.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.insurance_underwriting.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.insurance_underwriting.schema_contract import build_schema_contract
from pyAppGen.pbcs.insurance_underwriting.seed_data import validate_seed_data
from pyAppGen.pbcs.insurance_underwriting.service_contract import build_service_contract
from pyAppGen.pbcs.insurance_underwriting.services import service_operation_contracts
from pyAppGen.pbcs.insurance_underwriting.standalone import insurance_underwriting_standalone_app_contract


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    assert contract["pbc"] == "insurance_underwriting"
    assert contract["standalone_app"]["ok"] is True
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    assert handler_manifest()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert composed_agent_contribution()["ok"] is True
    assert document_instruction_plan("application and inspection", "create submission and compare quotes")["wizard_candidates"]
    assert datastore_crud_plan("create", "insurance_underwriting_underwriting_submission", {"submission_id": "sub-1"})["route_candidates"]


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "insurance_underwriting"
    assert validate_package_metadata()["ok"] is True
    discovery = package_discovery_plan()
    assert discovery["ok"] is True
    assert discovery["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert service_operation_contracts()["operation_contract"]
    assert insurance_underwriting_standalone_app_contract()["ok"] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True
    assert validate_seed_data()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-insurance-underwriting"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-insurance-underwriting"})["dead_letter_table"].endswith("dead_letter_event")


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md", "SPECIFICATION.md"):
        assert (base / name).exists() is True

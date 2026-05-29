from pyAppGen.pbcs.electronic_health_records_core import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.electronic_health_records_core.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.electronic_health_records_core.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.electronic_health_records_core.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.electronic_health_records_core.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.electronic_health_records_core.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.electronic_health_records_core.schema_contract import build_schema_contract
from pyAppGen.pbcs.electronic_health_records_core.service_contract import build_service_contract
from pyAppGen.pbcs.electronic_health_records_core.services import service_operation_contracts
from pyAppGen.pbcs.electronic_health_records_core.config import governance_smoke_test


def test_generated_schema_service_and_release_evidence():
    schema = build_schema_contract()
    release = build_release_evidence()
    assert schema["ok"] is True
    assert build_service_contract()["ok"] is True
    assert release["ok"] is True
    assert any(check["id"] == "single_pbc_app" for check in release["checks"])
    assert release_readiness_manifest()["single_pbc_app"]["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    assert contract["pbc"] == "electronic_health_records_core"
    assert contract["ui_contract"]["single_pbc_app"]["ok"] is True
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    instruction = document_instruction_plan("critical lab", "acknowledge the result and update the note")
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert instruction["ok"] is True
    assert instruction["crud_preview"]["operation"] in {"create", "update", "query"}
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "electronic_health_records_core"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    routes = api_route_contracts()
    assert service_operation_contracts()["ok"] is True
    assert routes["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert any(contract["path"] == "/allergies" for contract in routes["contracts"])


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": ("PolicyChanged", "CustomerUpdated", "SupplierQualified")[0], "idempotency_key": "idem-electronic_health_records_core"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-electronic_health_records_core"})["dead_letter_table"].endswith("dead_letter_event")

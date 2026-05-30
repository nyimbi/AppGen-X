from pyAppGen.pbcs.public_safety_dispatch import implementation_contract, package_discovery_plan, package_metadata_manifest, validate_package_metadata
from pyAppGen.pbcs.public_safety_dispatch.agent import agent_skill_manifest, chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from pyAppGen.pbcs.public_safety_dispatch.config import governance_smoke_test
from pyAppGen.pbcs.public_safety_dispatch.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.public_safety_dispatch.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.public_safety_dispatch.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.public_safety_dispatch.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.public_safety_dispatch.schema_contract import build_schema_contract
from pyAppGen.pbcs.public_safety_dispatch.service_contract import build_service_contract
from pyAppGen.pbcs.public_safety_dispatch.services import service_operation_contracts
from pyAppGen.pbcs.public_safety_dispatch.standalone import pbc_generation_smoke_audit, standalone_application_manifest, standalone_smoke_test, validate_standalone_application


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    evidence = build_release_evidence()
    assert evidence["ok"] is True
    assert any(check["id"] == "dead_letter_retry_evidence" and check["ok"] for check in evidence["checks"])
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    assert implementation_contract()["pbc"] == "public_safety_dispatch"
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    assert "CallIntakeAccepted" in event_contract_manifest()["emitted"]


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert composed_agent_contribution()["ok"] is True
    assert document_instruction_plan("dispatch notes", "summarize")["ok"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "public_safety_dispatch"
    assert validate_package_metadata()["ok"] is True
    discovery = package_discovery_plan()
    assert discovery["ok"] is True
    assert discovery["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    routes = api_route_contracts()
    assert routes["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert any(item["route"] == "POST /response-milestones" for item in routes["contracts"])


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    accepted = dispatch_event({"event_type": ("PolicyChanged", "CustomerUpdated", "SupplierQualified")[0], "idempotency_key": "idem-public-safety-dispatch"})
    rejected = dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-public-safety-dispatch"})
    assert accepted["ok"] is True
    assert rejected["dead_letter_table"].endswith("dead_letter_event")


def test_standalone_surface_is_executable():
    manifest = standalone_application_manifest()
    validation = validate_standalone_application()
    smoke = standalone_smoke_test()
    generation = pbc_generation_smoke_audit()
    assert manifest["ok"] is True
    assert validation["ok"] is True
    assert smoke["ok"] is True
    assert generation["ok"] is True
    assert manifest["mode"] == "standalone_one_pbc_app"
    assert manifest["bootstrap"]["query_result_count"] >= 1
    assert manifest["ui"]["forms"]
    assert manifest["ui"]["wizards"]

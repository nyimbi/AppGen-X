from pyAppGen.pbcs.environment_health_safety import implementation_contract, package_discovery_plan, package_metadata_manifest, validate_package_metadata
from pyAppGen.pbcs.environment_health_safety.schema_contract import build_schema_contract
from pyAppGen.pbcs.environment_health_safety.service_contract import build_service_contract
from pyAppGen.pbcs.environment_health_safety.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.environment_health_safety.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.environment_health_safety.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.environment_health_safety.services import service_operation_contracts
from pyAppGen.pbcs.environment_health_safety.routes import api_route_contracts, validate_api_route_contracts, dispatch_route
from pyAppGen.pbcs.environment_health_safety.config import governance_smoke_test
from pyAppGen.pbcs.environment_health_safety.agent import agent_skill_manifest, chatbot_interface_contract, document_instruction_plan, datastore_crud_plan
from pyAppGen.pbcs.environment_health_safety.seed_data import seed_plan, validate_seed_data


def test_generated_schema_service_and_release_evidence():
    schema = build_schema_contract()
    service = build_service_contract()
    release = build_release_evidence()
    assert schema["ok"] is True
    assert service["ok"] is True
    assert release["ok"] is True
    assert any(table["table"] == "environment_health_safety_ehs_incident" for table in schema["tables"])
    assert "create_ehs_incident" in service["command_methods"]
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    events = event_contract_manifest()
    assert contract["pbc"] == "environment_health_safety"
    assert contract["schema_contract"]["ok"] is True
    assert events["ok"] is True
    assert "EnvironmentHealthSafetyPermitIssued" in events["emitted"]
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert document_instruction_plan("permit package", "check permit conflict")["workflow"].endswith("permit_conflict_workflow")
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "environment_health_safety"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    route_result = dispatch_route(
        "POST /ehs-incidents",
        {"tenant": "tenant-smoke", "code": "INC-ROUTE", "site": "Plant", "area": "Area", "task": "Task", "severity": "near_miss"},
    )
    assert route_result["ok"] is True
    assert route_result["operation_contract"]["operation"] == "create_ehs_incident"


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True
    assert seed_plan()["ok"] is True
    assert validate_seed_data()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    first = dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-environment_health_safety", "payload": {"policy_version": "ehs-policy-2026.2"}})
    second = dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-environment_health_safety", "payload": {"policy_version": "ehs-policy-2026.2"}})
    bad = dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-environment_health_safety"})
    assert first["ok"] is True
    assert second["duplicate"] is True
    assert bad["dead_letter_table"].endswith("dead_letter_event")

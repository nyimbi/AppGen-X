from pyAppGen.pbcs.donor_grant_fundraising import implementation_contract, package_discovery_plan, package_metadata_manifest, smoke_test, validate_package_metadata
from pyAppGen.pbcs.donor_grant_fundraising.agent import agent_skill_manifest, chatbot_interface_contract, datastore_crud_plan, document_instruction_plan
from pyAppGen.pbcs.donor_grant_fundraising.config import governance_smoke_test
from pyAppGen.pbcs.donor_grant_fundraising.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.donor_grant_fundraising.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.donor_grant_fundraising.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.donor_grant_fundraising.routes import ROUTES, api_route_contracts, dispatch_route, validate_api_route_contracts
from pyAppGen.pbcs.donor_grant_fundraising.schema_contract import build_schema_contract
from pyAppGen.pbcs.donor_grant_fundraising.service_contract import build_service_contract
from pyAppGen.pbcs.donor_grant_fundraising.services import service_operation_contracts
from pyAppGen.pbcs.donor_grant_fundraising.standalone import standalone_manifest


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    assert contract["pbc"] == "donor_grant_fundraising"
    assert contract["standalone"]["ok"] is True
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    briefing = document_instruction_plan("board briefing", "assemble leadership packet")
    assert briefing["ok"] is True
    assert briefing["domain_plan"]["target_table"] == "donor_grant_fundraising_briefing_packet"
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "donor_grant_fundraising"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert "POST /grant-applications" in ROUTES
    assert dispatch_route(
        "POST /donors",
        {"donor_id": "route-donor", "donor_type": "individual", "recognition_preference": "public"},
    )["ok"] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True
    assert standalone_manifest()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": ("PolicyChanged", "CustomerUpdated", "SupplierQualified")[0], "idempotency_key": "idem-donor_grant_fundraising"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-donor_grant_fundraising"})["dead_letter_table"].endswith("dead_letter_event")


def test_package_smoke_includes_runtime_and_standalone():
    result = smoke_test()
    assert result["ok"] is True
    assert result["runtime"]["ok"] is True
    assert result["standalone"]["ok"] is True

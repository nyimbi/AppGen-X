from pyAppGen.pbcs.smart_city_mobility_operations import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    smart_city_mobility_operations_standalone_app_contract,
    validate_package_metadata,
)
from pyAppGen.pbcs.smart_city_mobility_operations.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.smart_city_mobility_operations.config import governance_smoke_test
from pyAppGen.pbcs.smart_city_mobility_operations.events import (
    event_contract_manifest,
    validate_event_contract,
)
from pyAppGen.pbcs.smart_city_mobility_operations.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.smart_city_mobility_operations.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.smart_city_mobility_operations.routes import (
    api_route_contracts,
    standalone_route_contracts,
    validate_api_route_contracts,
)
from pyAppGen.pbcs.smart_city_mobility_operations.schema_contract import build_schema_contract
from pyAppGen.pbcs.smart_city_mobility_operations.service_contract import build_service_contract
from pyAppGen.pbcs.smart_city_mobility_operations.services import (
    service_operation_contracts,
    standalone_service_operation_contracts,
)


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True
    assert build_release_evidence()["generated_artifacts"]["standalone_app"]["ok"] is True


def test_manifest_and_event_contract():
    assert implementation_contract()["pbc"] == "smart_city_mobility_operations"
    assert implementation_contract()["standalone_app_contract"]["ok"] is True
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    plan = document_instruction_plan(
        "planned closure permit and rider detour bulletin",
        "prepare governed preview and public alert",
    )
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert plan["ok"] is True
    assert "GovernedPreviewWizard" in plan["wizard_candidates"]
    assert datastore_crud_plan(
        "create",
        table="smart_city_mobility_operations_signal_plan",
        payload={"signal_plan_id": "sp_contract"},
    )["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "smart_city_mobility_operations"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert standalone_service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert standalone_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert service_operation_contracts()["operation_contract"]


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert (
        dispatch_event(
            {"event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0], "idempotency_key": "idem-smart_city_mobility_operations"}
        )["ok"]
        is True
    )
    assert (
        dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-smart_city_mobility_operations"})[
            "dead_letter_table"
        ].endswith("dead_letter_event")
    )


def test_standalone_contract_is_exported():
    contract = smart_city_mobility_operations_standalone_app_contract()
    assert contract["ok"] is True

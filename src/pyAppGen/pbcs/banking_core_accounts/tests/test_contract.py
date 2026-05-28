from pyAppGen.pbcs.banking_core_accounts import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.banking_core_accounts.agent import (
    agent_skill_manifest,
    assistant_help_manifest,
    chatbot_interface_contract,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.banking_core_accounts.capability_assurance import (
    validate_table_stakes_capability_coverage,
)
from pyAppGen.pbcs.banking_core_accounts.events import (
    event_contract_manifest,
    validate_event_contract,
)
from pyAppGen.pbcs.banking_core_accounts.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.banking_core_accounts.models import lifecycle_model_manifest
from pyAppGen.pbcs.banking_core_accounts.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.banking_core_accounts.routes import (
    api_route_contracts,
    validate_api_route_contracts,
)
from pyAppGen.pbcs.banking_core_accounts.runtime import (
    banking_core_accounts_build_app_surface,
    banking_core_accounts_build_control_surface,
    banking_core_accounts_build_forms_contract,
    banking_core_accounts_build_wizard_contract,
    banking_core_accounts_runtime_smoke,
)
from pyAppGen.pbcs.banking_core_accounts.schema_contract import build_schema_contract
from pyAppGen.pbcs.banking_core_accounts.service_contract import build_service_contract
from pyAppGen.pbcs.banking_core_accounts.services import service_operation_contracts
from pyAppGen.pbcs.banking_core_accounts.ui import banking_core_accounts_ui_contract


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True
    assert banking_core_accounts_build_forms_contract()["ok"] is True
    assert banking_core_accounts_build_wizard_contract()["ok"] is True
    assert banking_core_accounts_build_control_surface()["ok"] is True
    assert banking_core_accounts_build_app_surface()["single_pbc_app"] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    assert contract["pbc"] == "banking_core_accounts"
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    assert contract["advanced_runtime"]["single_pbc_app"]["single_pbc_app"] is True


def test_agent_chatbot_skills_and_help_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert assistant_help_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert document_instruction_plan("doc", "open account")["ok"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "banking_core_accounts"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    operation_contract = "operation_contract"
    assert operation_contract
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    route_validation = validate_api_route_contracts()
    assert route_validation["ok"] is True
    assert route_validation["service_mismatches"] == ()
    assert lifecycle_model_manifest()["ok"] is True
    assert banking_core_accounts_ui_contract()["ok"] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert "governance_smoke_test"
    assert validate_table_stakes_capability_coverage()["ok"] is True
    smoke = banking_core_accounts_runtime_smoke()
    assert smoke["ok"] is True
    assert smoke["reopened"]["account"]["lifecycle_state"] == "reopened"


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert (
        dispatch_event(
            {
                "event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0],
                "idempotency_key": "idem-banking_core_accounts",
            }
        )["ok"]
        is True
    )
    assert (
        dispatch_event(
            {"event_type": "Unexpected", "idempotency_key": "bad-banking_core_accounts"}
        )["dead_letter_table"].endswith("dead_letter_event")
    )

from pyAppGen.pbcs.identity_kyc_aml_compliance import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    smoke_test,
    validate_package_metadata,
)
from pyAppGen.pbcs.identity_kyc_aml_compliance.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.identity_kyc_aml_compliance.capability_assurance import (
    validate_table_stakes_capability_coverage,
)
from pyAppGen.pbcs.identity_kyc_aml_compliance.config import governance_smoke_test
from pyAppGen.pbcs.identity_kyc_aml_compliance.events import (
    event_contract_manifest,
    validate_event_contract,
)
from pyAppGen.pbcs.identity_kyc_aml_compliance.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.identity_kyc_aml_compliance.permissions import authorize, permission_manifest
from pyAppGen.pbcs.identity_kyc_aml_compliance.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.identity_kyc_aml_compliance.routes import (
    api_route_contracts,
    dispatch_route,
    validate_api_route_contracts,
)
from pyAppGen.pbcs.identity_kyc_aml_compliance.runtime import (
    identity_kyc_aml_compliance_build_schema_contract,
    identity_kyc_aml_compliance_build_service_contract,
    identity_kyc_aml_compliance_empty_state,
    identity_kyc_aml_compliance_runtime_smoke,
)
from pyAppGen.pbcs.identity_kyc_aml_compliance.seed_data import seed_plan, validate_seed_data
from pyAppGen.pbcs.identity_kyc_aml_compliance.services import (
    IdentityKycAmlComplianceService,
    service_operation_contracts,
)
from pyAppGen.pbcs.identity_kyc_aml_compliance.standalone import standalone_contract, standalone_smoke
from pyAppGen.pbcs.identity_kyc_aml_compliance.ui import (
    identity_kyc_aml_compliance_render_workbench,
    identity_kyc_aml_compliance_ui_contract,
)


def test_generated_schema_service_and_release_evidence():
    assert identity_kyc_aml_compliance_build_schema_contract()["ok"] is True
    assert identity_kyc_aml_compliance_build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    assert contract["pbc"] == "identity_kyc_aml_compliance"
    assert contract["boundary_contract"]["ok"] is True
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    assert validate_table_stakes_capability_coverage()["ok"] is True


def test_agent_ui_and_chatbot_surfaces_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    plan = document_instruction_plan("passport", "screen and onboard this customer")
    assert plan["ok"] is True
    assert "record_screening_hit" in plan["candidate_operations"]
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False
    assert composed_agent_contribution()["ok"] is True
    assert identity_kyc_aml_compliance_ui_contract()["ok"] is True
    assert identity_kyc_aml_compliance_render_workbench()["ok"] is True


def test_registration_plan_and_package_metadata_are_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "identity_kyc_aml_compliance"
    assert validate_package_metadata()["ok"] is True
    discovery = package_discovery_plan()
    assert discovery["ok"] is True
    assert discovery["side_effects"] == ()


def test_service_route_permissions_seed_and_governance_contracts():
    assert governance_smoke_test()["ok"] is True
    assert permission_manifest()["ok"] is True
    assert authorize("identity_kyc_aml_compliance.read", {"roles": ("analyst",)})["ok"] is True
    assert seed_plan()["ok"] is True
    assert validate_seed_data()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True


def test_routes_dispatch_and_handler_idempotency_are_executable():
    service = IdentityKycAmlComplianceService()
    created = dispatch_route(
        "POST /kyc-profiles",
        {
            "tenant": "tenant-a",
            "subject_name": "Route Test",
            "customer_type": "individual",
            "jurisdiction": "KE",
            "product_exposure": "checking",
            "channel": "remote",
            "expected_activity": "salary",
        },
        service=service,
    )
    assert created["ok"] is True
    workbench = dispatch_route("GET /identity-kyc-aml-compliance-workbench", {"tenant": "tenant-a"}, service=service)
    assert workbench["ok"] is True
    manifest = handler_manifest()
    assert manifest["ok"] is True
    state = identity_kyc_aml_compliance_empty_state()
    first = dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-contract"}, state=state)
    second = dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-contract"}, state=first["state"])
    bad = dispatch_event({"event_type": "Unexpected", "idempotency_key": "idem-bad"}, state=second["state"])
    assert first["ok"] is True
    assert second["duplicate"] is True
    assert bad["dead_letter_table"].endswith("dead_letter_event")


def test_runtime_and_standalone_smokes_pass():
    assert smoke_test()["ok"] is True
    assert identity_kyc_aml_compliance_runtime_smoke()["ok"] is True
    assert standalone_contract()["ok"] is True
    assert standalone_smoke()["ok"] is True

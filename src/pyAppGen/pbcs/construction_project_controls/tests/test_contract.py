from pyAppGen.pbcs.construction_project_controls import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.construction_project_controls.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.construction_project_controls.config import governance_smoke_test
from pyAppGen.pbcs.construction_project_controls.events import (
    event_contract_manifest,
    validate_event_contract,
)
from pyAppGen.pbcs.construction_project_controls.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.construction_project_controls.models import (
    instantiate_model,
    model_catalog,
    model_manifest,
    smoke_test as model_smoke_test,
)
from pyAppGen.pbcs.construction_project_controls.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.construction_project_controls.routes import (
    api_route_contracts,
    validate_api_route_contracts,
)
from pyAppGen.pbcs.construction_project_controls.runtime import (
    construction_project_controls_build_controls_contract,
    construction_project_controls_build_forms_contract,
    construction_project_controls_build_schema_contract,
    construction_project_controls_build_single_pbc_app_contract,
    construction_project_controls_build_wizards_contract,
)
from pyAppGen.pbcs.construction_project_controls.seed_data import seed_plan, validate_seed_data
from pyAppGen.pbcs.construction_project_controls.services import service_operation_contracts


def test_generated_schema_service_and_release_evidence():
    assert construction_project_controls_build_schema_contract()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    assert contract["pbc"] == "construction_project_controls"
    assert contract["single_pbc_app_contract"]["ok"] is True
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_agent_chatbot_skills_are_executable():
    plan = document_instruction_plan(
        "Daily progress report for WBS 1.1 installed 12 m3",
        "Create progress draft",
    )
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert plan["ok"] is True
    assert plan["domain_plan"]["target_entity"] == "site_progress"
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False
    assert composed_agent_contribution()["ok"] is True


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "construction_project_controls"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert service_operation_contracts()["operation_contract"]


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True
    assert seed_plan()["ok"] is True
    assert validate_seed_data()["ok"] is True
    assert construction_project_controls_build_forms_contract()["ok"] is True
    assert construction_project_controls_build_wizards_contract()["ok"] is True
    assert construction_project_controls_build_controls_contract()["ok"] is True
    assert construction_project_controls_build_single_pbc_app_contract()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    first = dispatch_event(
        {
            "event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0],
            "idempotency_key": "idem-construction_project_controls-1",
        }
    )
    duplicate = dispatch_event(
        {
            "event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0],
            "idempotency_key": "idem-construction_project_controls-1",
        }
    )
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-construction_project_controls-1"})
    assert first["ok"] is True
    assert duplicate["duplicate"] is True
    assert failed["dead_letter_table"].endswith("dead_letter_event")


def test_model_manifest_aligns_owned_tables_and_supports_instantiation():
    manifest = model_manifest()
    catalog = model_catalog()
    instance = instantiate_model(
        "construction_project_controls_construction_project",
        {
            "id": "CP-001",
            "tenant": "tenant-smoke",
            "code": "CP-001",
            "name": "Smoke Tower",
        },
    )
    assert manifest["ok"] is True
    assert not manifest["missing_models"]
    assert not manifest["external_models"]
    assert catalog["ok"] is True
    assert len(catalog["models"]) == len(manifest["model_tables"])
    assert instance["ok"] is True
    assert instance["instance"]["code"] == "CP-001"
    assert model_smoke_test()["ok"] is True

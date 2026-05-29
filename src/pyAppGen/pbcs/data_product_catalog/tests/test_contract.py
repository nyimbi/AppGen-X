from pyAppGen.pbcs.data_product_catalog import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    pbc_generation_smoke_audit,
    pbc_implementation_release_audit,
    pbc_source_artifact_contract,
    registration_plan,
    smoke_test,
    validate_package_metadata,
)
from pyAppGen.pbcs.data_product_catalog.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.data_product_catalog.capability_assurance import (
    validate_table_stakes_capability_coverage,
)
from pyAppGen.pbcs.data_product_catalog.config import governance_smoke_test
from pyAppGen.pbcs.data_product_catalog.domain_depth import (
    domain_capability_surface_contract,
    domain_depth_contract,
    domain_depth_smoke_test,
    ui_capability_surface_contract,
)
from pyAppGen.pbcs.data_product_catalog.events import (
    event_contract_manifest,
    validate_event_contract,
)
from pyAppGen.pbcs.data_product_catalog.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.data_product_catalog.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.data_product_catalog.routes import (
    api_route_contracts,
    validate_api_route_contracts,
)
from pyAppGen.pbcs.data_product_catalog.runtime import (
    DataProductCatalogApp,
    data_product_catalog_runtime_capabilities,
    data_product_catalog_runtime_smoke,
)
from pyAppGen.pbcs.data_product_catalog.schema_contract import (
    build_schema_contract,
    validate_schema_contract,
)
from pyAppGen.pbcs.data_product_catalog.service_contract import (
    build_service_contract,
    validate_service_contract,
)
from pyAppGen.pbcs.data_product_catalog.services import (
    DataProductCatalogService,
    service_operation_contracts,
)
from pyAppGen.pbcs.data_product_catalog.ui import (
    data_product_catalog_render_workbench,
    data_product_catalog_ui_contract,
)


def test_schema_service_and_release_evidence_are_deep_and_consistent():
    schema = build_schema_contract()
    service = build_service_contract()
    evidence = build_release_evidence()
    assert schema["ok"] is True
    assert validate_schema_contract()["ok"] is True
    assert len(schema["tables"]) >= 20
    assert service["ok"] is True
    assert validate_service_contract()["ok"] is True
    assert len(service["command_methods"]) >= 15
    assert evidence["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_generated_schema_service_and_release_evidence():
    schema = build_schema_contract()
    service = build_service_contract()
    evidence = build_release_evidence()
    assert schema["pbc"] == "data_product_catalog"
    assert service["ok"] is True
    assert evidence["ok"] is True
    assert release_readiness_manifest()["ok"] is True


def test_domain_depth_and_ui_surface_cover_operations_rules_parameters():
    domain = domain_depth_contract()
    coverage = domain_capability_surface_contract()
    ui = ui_capability_surface_contract()
    assert domain["ok"] is True
    assert domain_depth_smoke_test()["ok"] is True
    assert domain["operation_count"] >= 15
    assert len(domain["owned_tables"]) >= 20
    assert coverage["coverage_counts"]["operations"] == len(domain["operations"])
    assert coverage["coverage_counts"]["rules"] == len(domain["rules"])
    assert coverage["coverage_counts"]["parameters"] == len(domain["parameters"])
    assert ui["ok"] is True
    assert len(ui["forms"]) >= len(domain["operations"])
    assert len(ui["wizards"]) >= 6
    assert len(ui["controls"]) >= 6


def test_agent_chatbot_skills_and_governed_crud_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert composed_agent_contribution()["ok"] is True
    assert document_instruction_plan("publish the contract", "publish contract")["ok"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False


def test_service_routes_and_runtime_support_standalone_pbc_execution():
    service = DataProductCatalogService()
    command = service.create_data_product(
        {
            "tenant": "tenant-smoke",
            "code": "CUSTOMER360",
            "product_type": "analytical",
            "value_proposition": "Trusted customer profile",
        }
    )
    query = service.query_workbench({"tenant": "tenant-smoke"})
    app = DataProductCatalogApp()
    app.configure_runtime({"database_backend": "postgresql", "event_topic": "pbc.data_product_catalog.events"})
    result = app.execute(
        "publish_data_contract",
        {
            "tenant": "tenant-smoke",
            "code": "CUSTOMER360-V1",
            "data_product_id": "CUSTOMER360",
            "compatibility_level": "backward",
        },
    )
    runtime = data_product_catalog_runtime_capabilities()
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert command["ok"] is True
    assert query["ok"] is True
    assert result["ok"] is True
    assert app.query_workbench({"tenant": "tenant-smoke"})["ok"] is True
    assert data_product_catalog_runtime_smoke()["ok"] is True
    assert runtime["ok"] is True
    assert "create_data_product" in runtime["operations"]
    assert data_product_catalog_ui_contract()["ok"] is True
    assert data_product_catalog_render_workbench(runtime["smoke"]["state"])["ok"] is True


def test_manifest_events_handlers_and_governance_surfaces_are_valid():
    assert implementation_contract()["pbc"] == "data_product_catalog"
    assert package_metadata_manifest()["pbc"] == "data_product_catalog"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    assert handler_manifest()["ok"] is True
    assert dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "idem"})["ok"] is False
    assert governance_smoke_test()["ok"] is True
    assert validate_table_stakes_capability_coverage()["ok"] is True
    assert smoke_test()["ok"] is True


def test_manifest_and_event_contract():
    manifest = event_contract_manifest()
    assert manifest["ok"] is True
    assert validate_event_contract()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert package_metadata_manifest()["pbc"] == "data_product_catalog"
    assert validate_package_metadata()["ok"] is True


def test_registration_plan_is_side_effect_free():
    plan = registration_plan()
    assert plan["ok"] is True
    assert plan["registration_steps"]
    assert plan.get("side_effects", ()) == ()


def test_configuration_permissions_and_seed_hooks_are_executable():
    from pyAppGen.pbcs.data_product_catalog import permissions, seed_data

    assert governance_smoke_test()["ok"] is True
    assert permissions.permission_manifest()["ok"] is True
    assert seed_data.validate_seed_data()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    first = dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-contract"})
    second = dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-contract"})
    rejected = dispatch_event({"event_type": "Unexpected", "idempotency_key": "idem-contract-bad"})
    assert manifest["ok"] is True
    assert manifest["handlers"][0]["retry_policy"]["max_attempts"] >= 3
    assert manifest["handlers"][0]["dead_letter_table"].startswith("data_product_catalog_")
    assert first["ok"] is True
    assert second["ok"] is True
    assert second["idempotency_key"] == first["idempotency_key"]
    assert rejected["ok"] is False


def test_named_release_gates_pass_for_data_product_catalog():
    source_gate = pbc_source_artifact_contract()
    release_gate = pbc_implementation_release_audit()
    smoke_gate = pbc_generation_smoke_audit()
    assert source_gate["ok"] is True
    assert release_gate["ok"] is True
    assert smoke_gate["ok"] is True


def test_route_operations_expose_operation_contracts():
    routes = api_route_contracts()
    contracts = service_operation_contracts()
    operation_contract = contracts["contracts"][0]
    assert routes["ok"] is True
    assert contracts["ok"] is True
    assert contracts["operation_contract"]["transaction_boundary"] == "owned_datastore_plus_outbox"
    assert operation_contract["transaction_boundary"] == "owned_datastore_plus_outbox"


def test_service_and_route_surface_are_executable():
    service = DataProductCatalogService()
    route_contract = api_route_contracts()
    validation = validate_api_route_contracts()
    command = service.create_data_product(
        {
            "tenant": "tenant-route",
            "code": "ROUTE_PRODUCT",
            "product_type": "analytical",
            "value_proposition": "Route-backed trust evidence",
        }
    )
    operation_contract = service_operation_contracts()["operation_contract"]
    assert service_operation_contracts()["ok"] is True
    assert route_contract["ok"] is True
    assert validation["ok"] is True
    assert command["ok"] is True
    assert operation_contract["transaction_boundary"] == "owned_datastore_plus_outbox"

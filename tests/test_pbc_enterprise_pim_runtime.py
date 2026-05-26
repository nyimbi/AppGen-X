import pytest

from pyAppGen.pbcs.enterprise_pim import ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.enterprise_pim import ENTERPRISE_PIM_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.enterprise_pim import ENTERPRISE_PIM_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.enterprise_pim import ENTERPRISE_PIM_OWNED_TABLES
from pyAppGen.pbcs.enterprise_pim import ENTERPRISE_PIM_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_accept_dependency_schema
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_approve_validation_workflow
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_build_api_contract
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_build_workbench_view
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_configure_runtime
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_create_taxonomy
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_define_attribute
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_empty_state
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_permissions_contract
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_receive_event
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_register_rule
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_register_schema_extension
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_render_workbench
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_runtime_capabilities
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_runtime_smoke
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_set_parameter
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_start_validation_workflow
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_ui_contract
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_upsert_localized_content
from pyAppGen.pbcs.enterprise_pim import enterprise_pim_verify_owned_table_boundary
from pyAppGen.pbcs.enterprise_pim import implementation_contract


def _configured_state() -> dict:
    state = enterprise_pim_empty_state()
    state = enterprise_pim_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.enterprise-pim.events",
            "retry_limit": 2,
            "default_locale": "en-US",
            "allowed_locales": ("en-US", "fr-FR"),
            "allowed_channels": ("commerce", "search"),
            "dependency_sources": ("dam_core", "price_promotion_engine", "tax_localization", "inventory_positioning"),
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("minimum_completeness", 0.8),
        ("minimum_translation_quality", 0.7),
        ("validation_sla_hours", 24),
        ("max_inheritance_depth", 4),
        ("dead_letter_retry_limit", 2),
        ("dependency_schema_version_floor", 1),
    ):
        state = enterprise_pim_set_parameter(state, name, value)["state"]
    state = enterprise_pim_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "master_data_readiness",
            "status": "active",
            "required_locales": ("en-US", "fr-FR"),
            "required_attributes": ("material", "hazard_class"),
            "validation_policy": {"required_approvers": ("data_steward", "compliance")},
        },
    )["state"]
    return state


def test_enterprise_pim_runtime_executes_package_local_smoke() -> None:
    runtime = enterprise_pim_runtime_capabilities()
    smoke = enterprise_pim_runtime_smoke()
    contract = implementation_contract()

    assert runtime["format"] == "appgen.enterprise-pim-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/enterprise_pim"
    assert runtime["owned_tables"] == ENTERPRISE_PIM_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 20
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(ENTERPRISE_PIM_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]
    assert contract["pbc"] == "enterprise_pim"
    assert contract["side_effect_free"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["owned_tables"] == ENTERPRISE_PIM_OWNED_TABLES
    assert contract["allowed_database_backends"] == ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS
    assert contract["ui_contract"]["ok"] is True
    assert contract["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["permissions_contract"]["action_permissions"]["register_schema_extension"] == "enterprise_pim.configure"

    api = enterprise_pim_build_api_contract()
    permissions = enterprise_pim_permissions_contract()
    assert api["format"] == "appgen.enterprise-pim-api-contract.v1"
    assert api["owned_tables"] == ENTERPRISE_PIM_OWNED_TABLES
    assert api["database_backends"] == ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == ENTERPRISE_PIM_EMITTED_EVENT_TYPES
    assert api["consumes"] == ENTERPRISE_PIM_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["route"] for route in api["routes"]} >= {
        "POST /product-taxonomies",
        "POST /product-attributes",
        "POST /localized-content",
        "POST /validation-workflows",
        "POST /pim-events",
        "GET /pim-workbench",
    }
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert permissions["action_permissions"]["approve_validation_workflow"] == "enterprise_pim.approve"


def test_enterprise_pim_applies_taxonomy_attributes_localization_workflows_dependencies_and_ui() -> None:
    state = _configured_state()
    extension = enterprise_pim_register_schema_extension(
        state,
        "product_attribute",
        {"semantic_vector": "jsonb", "classification_features": "jsonb"},
    )
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["product_attribute"]["semantic_vector"] == "jsonb"

    dependency = enterprise_pim_accept_dependency_schema(
        state,
        "dam_core",
        {"schema_version": 1, "events": ("MediaAssetApproved",), "fields": ("asset_ref", "rights_status")},
    )
    state = dependency["state"]
    assert dependency["schema"]["accepted"] is True
    assert dependency["schema"]["compiled_hash"]

    state = enterprise_pim_create_taxonomy(
        state,
        {
            "taxonomy_id": "tax_ops",
            "tenant": "tenant_ops",
            "code": "industrial/valves",
            "name": "Industrial Valves",
            "parent_id": None,
            "localized_names": {"en-US": "Industrial Valves", "fr-FR": "Vannes industrielles"},
        },
    )["state"]
    state = enterprise_pim_define_attribute(
        state,
        {
            "attribute_id": "attr_material_ops",
            "tenant": "tenant_ops",
            "taxonomy_id": "tax_ops",
            "name": "material",
            "data_type": "string",
            "required": True,
            "inherited_from": None,
            "localized_labels": {"en-US": "Material", "fr-FR": "Materiau"},
            "value": "steel",
        },
    )["state"]
    hazard = enterprise_pim_define_attribute(
        state,
        {
            "attribute_id": "attr_hazard_ops",
            "tenant": "tenant_ops",
            "taxonomy_id": "tax_ops",
            "name": "hazard_class",
            "data_type": "string",
            "required": True,
            "inherited_from": "attr_material_ops",
            "localized_labels": {"en-US": "Hazard class", "fr-FR": "Classe de risque"},
            "value": "none",
        },
    )
    state = hazard["state"]
    assert hazard["attribute"]["inheritance_path"] == ("attr_material_ops", "attr_hazard_ops")

    for content in (
        {
            "content_id": "loc_ops_en",
            "tenant": "tenant_ops",
            "entity_id": "tax_ops",
            "entity_type": "product_taxonomy",
            "locale": "en-US",
            "title": "Industrial Valves",
            "description": "Enterprise governed valve taxonomy for controlled product catalogs",
            "overrides": {"short_name": "Valves"},
        },
        {
            "content_id": "loc_ops_fr",
            "tenant": "tenant_ops",
            "entity_id": "tax_ops",
            "entity_type": "product_taxonomy",
            "locale": "fr-FR",
            "title": "Vannes industrielles",
            "description": "Taxonomie gouvernee pour catalogues de produits controles",
            "overrides": {"short_name": "Vannes"},
        },
    ):
        state = enterprise_pim_upsert_localized_content(state, content)["state"]

    state = enterprise_pim_start_validation_workflow(
        state,
        {
            "workflow_id": "wf_ops",
            "tenant": "tenant_ops",
            "entity_id": "tax_ops",
            "entity_type": "product_taxonomy",
            "requested_by": "pim_steward",
            "steps": ("data_steward", "compliance"),
        },
    )["state"]
    assert enterprise_pim_approve_validation_workflow(state, "wf_ops", approver="data_steward")["ok"] is False
    state = enterprise_pim_approve_validation_workflow(state, "wf_ops", approver="data_steward")["state"]
    approval = enterprise_pim_approve_validation_workflow(state, "wf_ops", approver="compliance")
    state = approval["state"]
    assert approval["ok"] is True

    state = enterprise_pim_receive_event(
        state,
        {
            "event_id": "evt_media_ops",
            "event_type": "MediaAssetApproved",
            "idempotency_key": "media:ops:v1",
            "payload": {"tenant": "tenant_ops", "entity_id": "tax_ops", "asset_ref": "dam://ops", "rights_status": "approved"},
        },
    )["state"]
    duplicate = enterprise_pim_receive_event(
        state,
        {
            "event_id": "evt_media_ops",
            "event_type": "MediaAssetApproved",
            "idempotency_key": "media:ops:v1",
            "payload": {"tenant": "tenant_ops", "entity_id": "tax_ops", "asset_ref": "dam://ops", "rights_status": "approved"},
        },
    )
    assert duplicate["handler"]["status"] == "duplicate"

    workbench = enterprise_pim_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["taxonomy_count"] == 1
    assert workbench["attribute_count"] == 2
    assert workbench["localized_content_count"] == 2
    assert workbench["approved_workflow_count"] == 1
    assert workbench["dependency_projection_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 6
    assert workbench["binding_evidence"]["owned_tables"] == ENTERPRISE_PIM_OWNED_TABLES

    ui_contract = enterprise_pim_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == ENTERPRISE_PIM_OWNED_TABLES
    rendered = enterprise_pim_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "enterprise_pim.taxonomy",
            "enterprise_pim.attribute",
            "enterprise_pim.localization",
            "enterprise_pim.workflow",
            "enterprise_pim.approve",
            "enterprise_pim.integrate",
            "enterprise_pim.configure",
            "enterprise_pim.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == ENTERPRISE_PIM_OWNED_TABLES

    boundary = enterprise_pim_verify_owned_table_boundary(
        (
            "product_taxonomy",
            "localized_content",
            "MediaAssetApproved",
            "media_projection",
            "GET /prices",
            "enterprise_pim_appgen_outbox_event",
        )
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()

    violation = enterprise_pim_verify_owned_table_boundary(("asset",))
    assert violation["ok"] is False
    assert violation["violations"] == ("asset",)


def test_enterprise_pim_rejects_invalid_inputs_and_records_dead_letters() -> None:
    state = enterprise_pim_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        enterprise_pim_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.enterprise-pim.events",
                "retry_limit": 2,
                "default_locale": "en-US",
                "allowed_locales": ("en-US",),
                "allowed_channels": ("commerce",),
                "dependency_sources": ("dam_core",),
            },
        )
    with pytest.raises(ValueError, match="AppGen-X event contract"):
        enterprise_pim_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.enterprise-pim.events",
                "retry_limit": 2,
                "default_locale": "en-US",
                "allowed_locales": ("en-US",),
                "allowed_channels": ("commerce",),
                "dependency_sources": ("dam_core",),
                "stream_engine": "picker",
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Enterprise PIM parameter"):
        enterprise_pim_set_parameter(state, "stream_engine", 1)
    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        enterprise_pim_register_schema_extension(state, "asset", {"rights_profile": "jsonb"})
    with pytest.raises(ValueError, match="Unsupported Enterprise PIM dependency events"):
        enterprise_pim_accept_dependency_schema(state, "dam_core", {"schema_version": 1, "events": ("UnknownEvent",)})

    failed = enterprise_pim_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "UnknownDependency", "idempotency_key": "unknown:ops", "attempts": 2, "payload": {"tenant": "tenant_ops"}},
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

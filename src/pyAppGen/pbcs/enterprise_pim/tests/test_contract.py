"""Generated contract smoke tests for enterprise_pim."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    from .. import models, release_evidence, schema_contract

    assert SCHEMA_CONTRACT['pbc'] == 'enterprise_pim'
    assert SCHEMA_CONTRACT['ok'] is True
    assert SCHEMA_CONTRACT['owned_tables']
    schema_smoke = schema_contract.smoke_test()
    model_smoke = models.smoke_test()
    assert schema_smoke['ok'] is True
    assert model_smoke['ok'] is True
    assert not schema_smoke['side_effects']
    assert not model_smoke['side_effects']
    assert SERVICE_CONTRACT['pbc'] == 'enterprise_pim'
    assert SERVICE_CONTRACT['ok'] is True
    assert SERVICE_CONTRACT.get('shared_table_access') is False
    assert RELEASE_EVIDENCE['pbc'] == 'enterprise_pim'
    assert RELEASE_EVIDENCE['ok'] is True


    release_manifest = release_evidence.release_readiness_manifest()
    release_validation = release_evidence.validate_release_evidence()
    release_smoke = release_evidence.smoke_test()
    assert release_manifest['ok'] is True
    assert release_validation['ok'] is True
    assert release_smoke['ok'] is True
    assert not release_manifest['blocking_gaps']
    assert not release_validation['missing_sections']
    assert not release_validation['failed_checks']
    assert not release_validation['boundary_gaps']
    assert not release_manifest['side_effects']
    assert not release_validation['side_effects']
    assert not release_smoke['side_effects']


def test_manifest_and_event_contract():
    from .. import events

    assert PBC_MANIFEST['pbc'] == 'enterprise_pim'
    assert PBC_MANIFEST['standard_features']
    assert PBC_MANIFEST['advanced_capabilities']
    assert EVENT_CONTRACT['contract'] == 'appgen_event_contract'
    assert EVENT_CONTRACT['outbox_table'].startswith('enterprise_pim_')
    assert EVENT_CONTRACT['inbox_table'].startswith('enterprise_pim_')
    manifest = events.event_contract_manifest()
    validation = events.validate_event_contract()
    smoke = events.smoke_test()
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert manifest['stream_engine_picker_visible'] is False
    assert not validation['invalid_tables']
    assert not validation['invalid_emitted']
    assert not validation['invalid_consumed']
    assert smoke['emitted']['table'] == EVENT_CONTRACT['outbox_table']
    assert smoke['consumed']['table'] == EVENT_CONTRACT['inbox_table']
    assert smoke['emitted']['retry_policy']['max_attempts'] >= 3
    assert smoke['consumed']['dead_letter_table'].startswith(PBC_MANIFEST['pbc'] + '_')
    assert not manifest['side_effects']
    assert not validation['side_effects']
    assert not smoke['side_effects']


def test_registration_plan_is_side_effect_free():
    from .. import package_discovery_plan, package_metadata_manifest, register_pbc, registration_plan, validate_package_metadata

    assert register_pbc()['pbc'] == 'enterprise_pim'
    plan = registration_plan()
    assert plan['ok'] is True
    assert plan['catalog_patch']
    metadata = package_metadata_manifest()
    metadata_validation = validate_package_metadata()
    discovery = package_discovery_plan()
    assert metadata['ok'] is True
    assert metadata_validation['ok'] is True
    assert discovery['ok'] is True
    assert metadata['stream_engine_picker_visible'] is False
    assert metadata['event_contract'] == 'AppGen-X'
    assert not metadata_validation['missing_entrypoints']
    assert not metadata_validation['missing_publish_artifacts']
    assert not metadata_validation['missing_capability_evidence']
    assert not metadata_validation['invalid']
    assert not discovery['side_effects']


def test_service_and_route_surface_are_executable():
    from .. import routes, services

    service_smoke = services.smoke_test()
    operation_contracts = services.service_operation_contracts()
    route_contracts = routes.api_route_contracts()
    route_validation = routes.validate_api_route_contracts()
    route_smoke = routes.smoke_test()
    assert service_smoke['ok'] is True
    assert operation_contracts['ok'] is True
    assert route_contracts['ok'] is True
    assert route_validation['ok'] is True
    assert route_contracts['contracts']
    assert all(item['permission'] for item in route_contracts['contracts'])
    assert all(item['event_contract'] == 'AppGen-X' for item in route_contracts['contracts'])
    assert all(item['stream_engine_picker_visible'] is False for item in route_contracts['contracts'])
    assert all(item['shared_table_access'] is False for item in route_contracts['contracts'])
    assert not route_validation['service_mismatches']
    assert not route_validation['missing_idempotency']
    assert not route_validation['invalid_table_scope']
    assert service_smoke['result']['operation_contract']['route']['path']
    assert service_smoke['result']['operation_contract']['permission']
    assert service_smoke['result']['operation_contract']['event_contract'] == 'AppGen-X'
    assert service_smoke['result']['operation_contract']['owned_tables'] or service_smoke['result']['operation_contract']['read_tables']
    assert route_smoke['ok'] is True
    assert not service_smoke['side_effects']
    assert not operation_contracts['side_effects']
    assert not route_contracts['side_effects']
    assert not route_validation['side_effects']
    assert not route_smoke['side_effects']


def test_configuration_permissions_and_seed_hooks_are_executable():
    from .. import config, permissions, seed_data

    config_smoke = config.smoke_test()
    governance_smoke = config.governance_smoke_test()
    permission_smoke = permissions.smoke_test()
    seed_smoke = seed_data.smoke_test()
    assert config_smoke['ok'] is True
    assert governance_smoke['ok'] is True
    assert governance_smoke['parameter']['accepted'] is True
    assert governance_smoke['compiled_rule']['compiled'] is True
    assert governance_smoke['rule_decision']['allowed'] is True
    assert permission_smoke['ok'] is True
    assert seed_smoke['ok'] is True
    assert not config_smoke['side_effects']
    assert not governance_smoke['side_effects']
    assert not permission_smoke['side_effects']
    assert not seed_smoke['side_effects']


def test_ui_workbench_surface_is_executable():
    from .. import ui

    if hasattr(ui, 'smoke_test'):
        smoke = ui.smoke_test()
    else:
        contract = getattr(ui, f"{PBC_MANIFEST['pbc']}_ui_contract")()
        rendered = {
            'ok': contract['ok'],
            'cards': contract.get('panels') or contract.get('fragments'),
            'route': (contract.get('routes') or (None,))[0],
        }
        smoke = {
            'ok': contract['ok'] and bool(contract.get('fragments')) and bool(rendered['cards']),
            'manifest': {'fragments': contract.get('fragments', ())},
            'rendered': rendered,
            'side_effects': (),
        }
    assert smoke['ok'] is True
    assert smoke['manifest']['fragments']
    assert smoke['rendered']['cards']
    assert not smoke['side_effects']


def test_event_handlers_are_idempotent_and_retryable():
    from .. import handlers

    smoke = handlers.smoke_test()
    assert smoke['ok'] is True
    assert smoke['manifest']['handlers']
    assert smoke['first_result']['retry_policy']
    assert smoke['first_result']['dead_letter_table'].startswith('enterprise_pim_')
    assert smoke['duplicate_result']['duplicate'] is True
    assert smoke['unknown_result']['handled'] is False
    assert not smoke['side_effects']

def test_table_stakes_and_advanced_capability_assurance_is_executable():
    from .. import capability_assurance

    manifest = capability_assurance.table_stakes_capability_manifest()
    validation = capability_assurance.validate_table_stakes_capability_coverage()
    smoke = capability_assurance.smoke_test()
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert manifest['standard_features']
    assert manifest['advanced_capabilities']
    assert not validation['missing_standard']
    assert not validation['missing_advanced']
    assert not validation['missing_operations']
    assert not validation['uncovered_features']
    assert not validation['invalid_tables']
    assert not validation['invalid_backends']
    assert validation['stream_picker_visible'] is False
    assert validation['event_contract'] == 'AppGen-X'
    assert validation['owned_boundary_rejection']['ok'] is False
    assert validation['owned_boundary_rejection']['violations']
    assert not smoke['side_effects']


def test_executable_pim_lifecycle_covers_attributes_localization_relationships_and_exceptions():
    from .. import runtime

    state = runtime.enterprise_pim_empty_state()
    state = runtime.enterprise_pim_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": runtime.ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_locale": "en-US",
            "allowed_locales": ("en-US", "fr-FR"),
            "allowed_channels": ("commerce",),
            "dependency_sources": ("dam_core",),
        },
    )["state"]
    for name, value in (
        ("minimum_completeness", 0.8),
        ("minimum_translation_quality", 0.75),
        ("validation_sla_hours", 24),
        ("max_inheritance_depth", 4),
        ("dead_letter_retry_limit", 2),
        ("dependency_schema_version_floor", 1),
        ("anomaly_zscore_threshold", 2.5),
    ):
        state = runtime.enterprise_pim_set_parameter(state, name, value)["state"]
    state = runtime.enterprise_pim_register_rule(
        state,
        {
            "rule_id": "rule_pim_test",
            "tenant": "tenant_test",
            "scope": "master_data_readiness",
            "status": "active",
            "required_locales": ("en-US",),
            "required_attributes": ("material",),
            "validation_policy": {"required_approvers": ("data_steward",)},
        },
    )["state"]
    state = runtime.enterprise_pim_create_taxonomy(
        state,
        {
            "taxonomy_id": "tax_test",
            "tenant": "tenant_test",
            "code": "tools/pumps",
            "name": "Pumps",
            "parent_id": None,
            "localized_names": {"en-US": "Pumps"},
        },
    )["state"]
    state = runtime.enterprise_pim_define_attribute(
        state,
        {
            "attribute_id": "attr_material_test",
            "tenant": "tenant_test",
            "taxonomy_id": "tax_test",
            "name": "material",
            "data_type": "string",
            "required": True,
            "localized_labels": {"en-US": "Material"},
            "value": "steel",
        },
    )["state"]
    state = runtime.enterprise_pim_create_attribute_group(
        state,
        {
            "group_id": "grp_test",
            "tenant": "tenant_test",
            "taxonomy_id": "tax_test",
            "name": "Core",
            "sequence": 1,
            "attributes": ("attr_material_test",),
        },
    )["state"]
    state = runtime.enterprise_pim_register_attribute_value_option(
        state,
        {
            "option_id": "opt_steel",
            "tenant": "tenant_test",
            "attribute_id": "attr_material_test",
            "value": "steel",
            "label": "Steel",
        },
    )["state"]
    state = runtime.enterprise_pim_register_attribute_validation_rule(
        state,
        {
            "validation_rule_id": "avr_material",
            "tenant": "tenant_test",
            "attribute_id": "attr_material_test",
            "data_type": "string",
            "required": True,
            "pattern": "^(steel|plastic)$",
        },
    )["state"]
    state = runtime.enterprise_pim_upsert_localized_content(
        state,
        {
            "content_id": "loc_test",
            "tenant": "tenant_test",
            "entity_id": "tax_test",
            "entity_type": "product_taxonomy",
            "locale": "en-US",
            "title": "Pumps",
            "description": "Complete product taxonomy content for governed pump catalogs",
            "overrides": {},
        },
    )["state"]
    state = runtime.enterprise_pim_upsert_translation_memory(
        state,
        {
            "translation_id": "tm_test",
            "tenant": "tenant_test",
            "source_locale": "en-US",
            "target_locale": "fr-FR",
            "source_text": "Pumps",
            "target_text": "Pompes",
            "quality_score": 0.9,
        },
    )["state"]
    state = runtime.enterprise_pim_register_locale_fallback_rule(
        state,
        {
            "fallback_rule_id": "lfr_test",
            "tenant": "tenant_test",
            "locale": "fr-FR",
            "fallback_locale": "en-US",
            "priority": 1,
        },
    )["state"]
    state = runtime.enterprise_pim_create_product_relationship(
        state,
        {
            "relationship_id": "rel_test",
            "tenant": "tenant_test",
            "from_entity_id": "tax_test",
            "to_entity_id": "tax_test",
            "relationship_type": "accessory",
        },
    )["state"]
    state = runtime.enterprise_pim_define_product_bundle(
        state,
        {
            "bundle_id": "bundle_test",
            "tenant": "tenant_test",
            "taxonomy_id": "tax_test",
            "component_refs": ("pump_head", "pump_motor"),
            "bundle_policy": "kit",
        },
    )["state"]
    state = runtime.enterprise_pim_define_variant_family(
        state,
        {
            "family_id": "vf_test",
            "tenant": "tenant_test",
            "taxonomy_id": "tax_test",
            "variant_axes": ("material",),
        },
    )["state"]
    state = runtime.enterprise_pim_add_variant_member(
        state,
        {
            "member_id": "vm_test",
            "tenant": "tenant_test",
            "family_id": "vf_test",
            "sku_ref": "sku_steel",
            "axis_values": {"material": "steel"},
        },
    )["state"]
    state = runtime.enterprise_pim_assign_assortment(
        state,
        {
            "assignment_id": "assort_test",
            "tenant": "tenant_test",
            "entity_id": "tax_test",
            "channel": "commerce",
            "market": "NA",
        },
    )["state"]
    state = runtime.enterprise_pim_assign_data_steward(
        state,
        {
            "assignment_id": "steward_test",
            "tenant": "tenant_test",
            "entity_id": "tax_test",
            "steward": "owner",
            "responsibility": "taxonomy",
        },
    )["state"]
    state = runtime.enterprise_pim_open_pim_exception(
        state,
        {
            "exception_id": "exc_test",
            "tenant": "tenant_test",
            "entity_id": "tax_test",
            "exception_type": "quality_review",
            "severity": "medium",
        },
    )["state"]
    resolved = runtime.enterprise_pim_resolve_pim_exception(
        state,
        {
            "exception_id": "exc_test",
            "tenant": "tenant_test",
            "resolution": "content_approved",
            "resolved_by": "owner",
        },
    )

    state = resolved["state"]
    assert state["attribute_group"]["grp_test"]["status"] == "active"
    assert state["attribute_value_option"]["opt_steel"]["status"] == "active"
    assert state["attribute_validation_rule"]["avr_material"]["status"] == "active"
    assert state["translation_memory_entry"]["tm_test"]["status"] == "approved"
    assert state["locale_fallback_rule"]["lfr_test"]["fallback_locale"] == "en-US"
    assert state["product_relationship"]["rel_test"]["status"] == "active"
    assert state["product_bundle_definition"]["bundle_test"]["component_count"] == 2
    assert state["product_variant_member"]["vm_test"]["status"] == "active"
    assert state["assortment_assignment"]["assort_test"]["status"] == "active"
    assert state["data_steward_assignment"]["steward_test"]["status"] == "active"
    assert state["pim_exception"]["exc_test"]["status"] == "resolved"
    assert all(event["topic"] == runtime.ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC for event in state["outbox"])
    assert runtime.enterprise_pim_verify_owned_table_boundary(runtime.ENTERPRISE_PIM_OWNED_TABLES)["ok"] is True

from .. import package_discovery_plan, package_metadata_manifest, registration_plan, validate_package_metadata
from .. import events, handlers, release_evidence, routes, services, config, permissions, seed_data, agent, models
from ..schema_contract import build_schema_contract
from ..service_contract import build_service_contract


def test_generated_schema_service_and_release_evidence():
    schema = build_schema_contract(); service = build_service_contract(); release = release_evidence.build_release_evidence(); manifest = release_evidence.release_readiness_manifest(); validation = release_evidence.validate_release_evidence()
    assert schema['ok'] is True
    assert len(schema['tables']) >= 20
    assert all(table['owned_table'].startswith('multi_sided_market_') for table in schema['tables'])
    assert all(len(table['fields']) >= 10 for table in schema['tables'])
    assert any(field['name'] == 'exchange_modes' for table in schema['tables'] for field in table['fields'])
    assert any(field['name'] == 'collateral_amount' for table in schema['tables'] for field in table['fields'])
    assert any(field['name'] == 'valuation_delta' for table in schema['tables'] for field in table['fields'])
    assert any(field['name'] == 'release_policy_hash' for table in schema['tables'] for field in table['fields'])
    assert service['ok'] is True
    assert release['ok'] is True
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert not release['blocking_gaps']


def test_owned_models_are_domain_rich_and_boundary_scoped():
    manifest = models.model_manifest()
    sample = models.instantiate_model(
        'multi_sided_market_marketplace_listing',
        {'tenant': 'default', 'listing_id': 'listing_1', 'status': 'published'},
    )
    assert manifest['ok'] is True
    assert not manifest['external_models']
    assert not manifest['thin_models']
    assert sample['ok'] is True
    assert 'exchange_modes' in sample['fields']
    assert all(table.startswith('multi_sided_market_') for table in manifest['model_tables'])


def test_manifest_and_event_contract():
    manifest = events.event_contract_manifest(); validation = events.validate_event_contract(); smoke = events.smoke_test()
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert manifest['event_contract'] == 'AppGen-X'
    assert manifest['stream_engine_picker_visible'] is False


def test_registration_plan_is_side_effect_free():
    assert registration_plan()['ok'] is True
    assert package_metadata_manifest()['stream_engine_picker_visible'] is False
    assert validate_package_metadata()['ok'] is True
    assert package_discovery_plan()['side_effects'] == ()


def test_service_and_route_surface_are_executable():
    service = services.service_operation_contracts(); route = routes.api_route_contracts(); validation = routes.validate_api_route_contracts(); smoke = routes.smoke_test()
    assert service['ok'] is True
    assert route['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert all(item['event_contract'] == 'AppGen-X' for item in service['contracts'])
    assert all('idempotency_key' in item for item in route['contracts'])


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handlers.handler_manifest(); smoke = handlers.smoke_test()
    assert manifest['ok'] is True
    assert smoke['ok'] is True
    assert smoke['second']['duplicate'] is True
    assert manifest['dead_letter_table'].startswith('multi_sided_market_')


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert config.governance_smoke_test()['ok'] is True
    assert permissions.smoke_test()['ok'] is True
    assert seed_data.smoke_test()['ok'] is True


def test_agent_chatbot_skills_are_executable():
    skills = agent.agent_skill_manifest(); chatbot = agent.chatbot_interface_contract(); document = agent.document_instruction_plan('listing document', 'create rental'); read_plan = agent.datastore_crud_plan('read'); create_plan = agent.datastore_crud_plan('create', payload={'status': 'draft'}); rejected = agent.datastore_crud_plan('update', table='foreign_table')
    assert skills['ok'] is True
    assert chatbot['ok'] is True
    assert document['ok'] is True
    assert read_plan['ok'] is True
    assert create_plan['ok'] is True
    assert rejected['ok'] is False
    assert agent.composed_agent_contribution()['single_agent_skill_namespace'] == 'multi_sided_market_skills'

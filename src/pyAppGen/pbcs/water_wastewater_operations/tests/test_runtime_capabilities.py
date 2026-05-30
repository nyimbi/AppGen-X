import pytest

from pyAppGen.pbcs.water_wastewater_operations import (
    WATER_WASTEWATER_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    WATER_WASTEWATER_OPERATIONS_CONSUMED_EVENT_TYPES,
    WATER_WASTEWATER_OPERATIONS_EMITTED_EVENT_TYPES,
    WATER_WASTEWATER_OPERATIONS_OWNED_TABLES,
    WATER_WASTEWATER_OPERATIONS_REQUIRED_EVENT_TOPIC,
    implementation_contract,
    water_wastewater_operations_build_api_contract,
    water_wastewater_operations_build_release_evidence,
    water_wastewater_operations_build_schema_contract,
    water_wastewater_operations_build_service_contract,
    water_wastewater_operations_build_workbench_view,
    water_wastewater_operations_configure_runtime,
    water_wastewater_operations_empty_state,
    water_wastewater_operations_parse_document_instruction,
    water_wastewater_operations_permissions_contract,
    water_wastewater_operations_receive_event,
    water_wastewater_operations_register_rule,
    water_wastewater_operations_register_schema_extension,
    water_wastewater_operations_run_advanced_assessment,
    water_wastewater_operations_runtime_capabilities,
    water_wastewater_operations_runtime_smoke,
    water_wastewater_operations_set_parameter,
    water_wastewater_operations_ui_contract,
)


def test_runtime_capabilities_expose_advanced_schema_service_release_and_smoke():
    runtime = water_wastewater_operations_runtime_capabilities()
    smoke = water_wastewater_operations_runtime_smoke()
    contract = implementation_contract()

    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['implementation_directory'] == 'src/pyAppGen/pbcs/water_wastewater_operations'
    assert runtime['owned_tables'] == WATER_WASTEWATER_OPERATIONS_OWNED_TABLES
    assert runtime['required_event_topic'] == WATER_WASTEWATER_OPERATIONS_REQUIRED_EVENT_TOPIC
    assert runtime['allowed_database_backends'] == WATER_WASTEWATER_OPERATIONS_ALLOWED_DATABASE_BACKENDS
    assert 'build_schema_contract' in runtime['operations']
    assert 'build_service_contract' in runtime['operations']
    assert 'build_release_evidence' in runtime['operations']
    assert set(runtime['capabilities']) == {check['id'] for check in smoke['checks'] if check['id'].startswith('water_wastewater_operations_')}
    assert contract['schema_contract']['ok'] is True
    assert contract['service_contract']['ok'] is True
    assert contract['release_evidence_contract']['ok'] is True
    assert contract['ui_binding_contract']['ok'] is True
    assert contract['api_contract']['event_contract'] == 'AppGen-X'
    assert contract['boundary_contract']['ok'] is True


def test_runtime_contracts_keep_appgen_x_only_backend_allowlist_and_ui_wiring():
    schema = water_wastewater_operations_build_schema_contract()
    service = water_wastewater_operations_build_service_contract()
    api = water_wastewater_operations_build_api_contract()
    release = water_wastewater_operations_build_release_evidence()
    permissions = water_wastewater_operations_permissions_contract()
    ui = water_wastewater_operations_ui_contract()

    assert schema['ok'] is True
    assert schema['datastore_backends'] == WATER_WASTEWATER_OPERATIONS_ALLOWED_DATABASE_BACKENDS
    assert schema['shared_table_access'] is False
    assert service['ok'] is True
    assert service['eventing']['contract'] == 'AppGen-X'
    assert service['eventing']['stream_engine_picker_visible'] is False
    assert service['retry_dead_letter_evidence']['dead_letter_table'].endswith('dead_letter_event')
    assert api['ok'] is True
    assert api['required_event_topic'] == WATER_WASTEWATER_OPERATIONS_REQUIRED_EVENT_TOPIC
    assert api['emits'] == WATER_WASTEWATER_OPERATIONS_EMITTED_EVENT_TYPES
    assert api['consumes'] == WATER_WASTEWATER_OPERATIONS_CONSUMED_EVENT_TYPES
    assert api['shared_table_access'] is False
    assert all(route.get('command') or route.get('query') for route in api['routes'])
    assert release['ok'] is True
    assert not release['blocking_gaps']
    assert release['ui_binding']['binding_evidence']['forms']
    assert release['agent']['confirmation_gated'] is True
    assert permissions['action_permissions']['receive_event'] == 'water_wastewater_operations.event'
    assert permissions['action_permissions']['build_release_evidence'] == 'water_wastewater_operations.audit'
    assert ui['ok'] is True
    assert ui['forms']
    assert ui['wizards']
    assert ui['controls']


def test_runtime_configuration_rules_parameters_events_and_assessment_are_executable():
    state = water_wastewater_operations_empty_state()
    state = water_wastewater_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': WATER_WASTEWATER_OPERATIONS_REQUIRED_EVENT_TOPIC, 'retry_limit': 5})['state']
    assert state['configuration']['event_contract'] == 'AppGen-X'
    assert state['configuration']['stream_engine_picker_visible'] is False
    state = water_wastewater_operations_set_parameter(state, 'workbench_limit', 40)['state']
    state = water_wastewater_operations_set_parameter(state, 'min_distribution_pressure_psi', 32)['state']
    state = water_wastewater_operations_register_rule(state, {'rule_id': 'smoke', 'policy_area': 'sampling'})['state']
    extension = water_wastewater_operations_register_schema_extension(state, 'pressure_quality_sample', {'lab_batch_ref': 'text'})
    assert extension['fields']['lab_batch_ref'] == 'text'
    consumed = water_wastewater_operations_receive_event(state, {'event_type': 'PolicyChanged', 'idempotency_key': 'evt-1'})
    duplicate = water_wastewater_operations_receive_event(consumed['state'], {'event_type': 'PolicyChanged', 'idempotency_key': 'evt-1'})
    dead = water_wastewater_operations_receive_event(duplicate['state'], {'event_type': 'Unexpected', 'idempotency_key': 'evt-2'})
    workbench = water_wastewater_operations_build_workbench_view(dead['state'])
    assessment = water_wastewater_operations_run_advanced_assessment(dead['state'], {'tenant': 'default'})
    plan = water_wastewater_operations_parse_document_instruction('hydrant flushing memo', 'prepare governed_datastore_crud flush packet')

    assert consumed['ok'] is True
    assert duplicate['duplicate'] is True
    assert dead['ok'] is False
    assert workbench['ok'] is True
    assert assessment['ok'] is True
    assert 0.0 <= assessment['score'] <= 1.0
    assert plan['ok'] is True
    assert plan['requires_human_confirmation'] is True


@pytest.mark.parametrize('bad_config, message', [
    ({'database_backend': 'sqlite', 'event_topic': WATER_WASTEWATER_OPERATIONS_REQUIRED_EVENT_TOPIC}, 'supports only PostgreSQL, MySQL, or MariaDB'),
    ({'database_backend': 'postgresql', 'event_topic': WATER_WASTEWATER_OPERATIONS_REQUIRED_EVENT_TOPIC, 'stream_engine': 'kafka'}, 'does not allow stream-engine or user-selectable eventing fields'),
    ({'database_backend': 'postgresql', 'event_topic': 'custom.topic'}, 'event topic is fixed to AppGen-X'),
])
def test_runtime_rejects_invalid_backends_and_stream_engine_fields(bad_config, message):
    with pytest.raises(ValueError, match=message):
        water_wastewater_operations_configure_runtime(water_wastewater_operations_empty_state(), bad_config)

    with pytest.raises(ValueError, match='Unsupported Water/Wastewater Operations parameter'):
        water_wastewater_operations_set_parameter(water_wastewater_operations_empty_state(), 'unexpected_parameter', 1)

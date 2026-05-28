from pyAppGen.pbcs.media_production_management import implementation_contract, media_production_management_runtime_capabilities, media_production_management_runtime_smoke, media_production_management_build_schema_contract, media_production_management_build_service_contract, media_production_management_build_release_evidence, media_production_management_receive_event, media_production_management_verify_owned_table_boundary, media_production_management_configure_runtime, media_production_management_set_parameter, media_production_management_register_rule, media_production_management_empty_state
from pyAppGen.pbcs.media_production_management.ui import media_production_management_ui_contract, media_production_management_render_workbench


def test_media_production_management_runtime_capabilities_and_contracts():
    runtime = media_production_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/media_production_management'
    assert media_production_management_build_schema_contract()['ok'] is True
    assert media_production_management_build_service_contract()['ok'] is True
    assert media_production_management_build_release_evidence()['ok'] is True
    assert media_production_management_runtime_smoke()['ok'] is True


def test_media_production_management_events_ui_boundary_and_configuration():
    state = media_production_management_empty_state()
    assert media_production_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.media_production_management.events'})['ok'] is True
    assert media_production_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert media_production_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert media_production_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert media_production_management_ui_contract()['ok'] is True
    assert media_production_management_render_workbench()['ok'] is True
    assert media_production_management_verify_owned_table_boundary((f'media_production_management_owned_table', 'foreign_table'))['ok'] is False

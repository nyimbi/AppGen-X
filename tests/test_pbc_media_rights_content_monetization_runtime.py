from pyAppGen.pbcs.media_rights_content_monetization import implementation_contract, media_rights_content_monetization_runtime_capabilities, media_rights_content_monetization_runtime_smoke, media_rights_content_monetization_build_schema_contract, media_rights_content_monetization_build_service_contract, media_rights_content_monetization_build_release_evidence, media_rights_content_monetization_receive_event, media_rights_content_monetization_verify_owned_table_boundary, media_rights_content_monetization_configure_runtime, media_rights_content_monetization_set_parameter, media_rights_content_monetization_register_rule, media_rights_content_monetization_empty_state
from pyAppGen.pbcs.media_rights_content_monetization.ui import media_rights_content_monetization_ui_contract, media_rights_content_monetization_render_workbench


def test_media_rights_content_monetization_runtime_capabilities_and_contracts():
    runtime = media_rights_content_monetization_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/media_rights_content_monetization'
    assert media_rights_content_monetization_build_schema_contract()['ok'] is True
    assert media_rights_content_monetization_build_service_contract()['ok'] is True
    assert media_rights_content_monetization_build_release_evidence()['ok'] is True
    assert media_rights_content_monetization_runtime_smoke()['ok'] is True


def test_media_rights_content_monetization_events_ui_boundary_and_configuration():
    state = media_rights_content_monetization_empty_state()
    assert media_rights_content_monetization_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.media_rights_content_monetization.events'})['ok'] is True
    assert media_rights_content_monetization_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert media_rights_content_monetization_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert media_rights_content_monetization_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert media_rights_content_monetization_ui_contract()['ok'] is True
    assert media_rights_content_monetization_render_workbench()['ok'] is True
    assert media_rights_content_monetization_verify_owned_table_boundary((f'media_rights_content_monetization_owned_table', 'foreign_table'))['ok'] is False

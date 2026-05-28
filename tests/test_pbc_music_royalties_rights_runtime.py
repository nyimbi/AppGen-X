from pyAppGen.pbcs.music_royalties_rights import implementation_contract, music_royalties_rights_runtime_capabilities, music_royalties_rights_runtime_smoke, music_royalties_rights_build_schema_contract, music_royalties_rights_build_service_contract, music_royalties_rights_build_release_evidence, music_royalties_rights_receive_event, music_royalties_rights_verify_owned_table_boundary, music_royalties_rights_configure_runtime, music_royalties_rights_set_parameter, music_royalties_rights_register_rule, music_royalties_rights_empty_state
from pyAppGen.pbcs.music_royalties_rights.ui import music_royalties_rights_ui_contract, music_royalties_rights_render_workbench


def test_music_royalties_rights_runtime_capabilities_and_contracts():
    runtime = music_royalties_rights_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/music_royalties_rights'
    assert music_royalties_rights_build_schema_contract()['ok'] is True
    assert music_royalties_rights_build_service_contract()['ok'] is True
    assert music_royalties_rights_build_release_evidence()['ok'] is True
    assert music_royalties_rights_runtime_smoke()['ok'] is True


def test_music_royalties_rights_events_ui_boundary_and_configuration():
    state = music_royalties_rights_empty_state()
    assert music_royalties_rights_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.music_royalties_rights.events'})['ok'] is True
    assert music_royalties_rights_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert music_royalties_rights_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert music_royalties_rights_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert music_royalties_rights_ui_contract()['ok'] is True
    assert music_royalties_rights_render_workbench()['ok'] is True
    assert music_royalties_rights_verify_owned_table_boundary((f'music_royalties_rights_owned_table', 'foreign_table'))['ok'] is False

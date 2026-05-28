from pyAppGen.pbcs.tax_administration_public_sector import implementation_contract, tax_administration_public_sector_runtime_capabilities, tax_administration_public_sector_runtime_smoke, tax_administration_public_sector_build_schema_contract, tax_administration_public_sector_build_service_contract, tax_administration_public_sector_build_release_evidence, tax_administration_public_sector_receive_event, tax_administration_public_sector_verify_owned_table_boundary, tax_administration_public_sector_configure_runtime, tax_administration_public_sector_set_parameter, tax_administration_public_sector_register_rule, tax_administration_public_sector_empty_state
from pyAppGen.pbcs.tax_administration_public_sector.ui import tax_administration_public_sector_ui_contract, tax_administration_public_sector_render_workbench


def test_tax_administration_public_sector_runtime_capabilities_and_contracts():
    runtime = tax_administration_public_sector_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/tax_administration_public_sector'
    assert tax_administration_public_sector_build_schema_contract()['ok'] is True
    assert tax_administration_public_sector_build_service_contract()['ok'] is True
    assert tax_administration_public_sector_build_release_evidence()['ok'] is True
    assert tax_administration_public_sector_runtime_smoke()['ok'] is True


def test_tax_administration_public_sector_events_ui_boundary_and_configuration():
    state = tax_administration_public_sector_empty_state()
    assert tax_administration_public_sector_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.tax_administration_public_sector.events'})['ok'] is True
    assert tax_administration_public_sector_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert tax_administration_public_sector_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert tax_administration_public_sector_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert tax_administration_public_sector_ui_contract()['ok'] is True
    assert tax_administration_public_sector_render_workbench()['ok'] is True
    assert tax_administration_public_sector_verify_owned_table_boundary((f'tax_administration_public_sector_owned_table', 'foreign_table'))['ok'] is False

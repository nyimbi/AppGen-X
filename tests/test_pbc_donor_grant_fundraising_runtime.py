from pyAppGen.pbcs.donor_grant_fundraising import implementation_contract, donor_grant_fundraising_runtime_capabilities, donor_grant_fundraising_runtime_smoke, donor_grant_fundraising_build_schema_contract, donor_grant_fundraising_build_service_contract, donor_grant_fundraising_build_release_evidence, donor_grant_fundraising_receive_event, donor_grant_fundraising_verify_owned_table_boundary, donor_grant_fundraising_configure_runtime, donor_grant_fundraising_set_parameter, donor_grant_fundraising_register_rule, donor_grant_fundraising_empty_state
from pyAppGen.pbcs.donor_grant_fundraising.ui import donor_grant_fundraising_ui_contract, donor_grant_fundraising_render_workbench


def test_donor_grant_fundraising_runtime_capabilities_and_contracts():
    runtime = donor_grant_fundraising_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/donor_grant_fundraising'
    assert donor_grant_fundraising_build_schema_contract()['ok'] is True
    assert donor_grant_fundraising_build_service_contract()['ok'] is True
    assert donor_grant_fundraising_build_release_evidence()['ok'] is True
    assert donor_grant_fundraising_runtime_smoke()['ok'] is True


def test_donor_grant_fundraising_events_ui_boundary_and_configuration():
    state = donor_grant_fundraising_empty_state()
    assert donor_grant_fundraising_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.donor_grant_fundraising.events'})['ok'] is True
    assert donor_grant_fundraising_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert donor_grant_fundraising_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert donor_grant_fundraising_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert donor_grant_fundraising_ui_contract()['ok'] is True
    assert donor_grant_fundraising_render_workbench()['ok'] is True
    assert donor_grant_fundraising_verify_owned_table_boundary((f'donor_grant_fundraising_owned_table', 'foreign_table'))['ok'] is False

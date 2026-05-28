from pyAppGen.pbcs.public_safety_dispatch import implementation_contract, public_safety_dispatch_runtime_capabilities, public_safety_dispatch_runtime_smoke, public_safety_dispatch_build_schema_contract, public_safety_dispatch_build_service_contract, public_safety_dispatch_build_release_evidence, public_safety_dispatch_receive_event, public_safety_dispatch_verify_owned_table_boundary, public_safety_dispatch_configure_runtime, public_safety_dispatch_set_parameter, public_safety_dispatch_register_rule, public_safety_dispatch_empty_state
from pyAppGen.pbcs.public_safety_dispatch.ui import public_safety_dispatch_ui_contract, public_safety_dispatch_render_workbench


def test_public_safety_dispatch_runtime_capabilities_and_contracts():
    runtime = public_safety_dispatch_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/public_safety_dispatch'
    assert public_safety_dispatch_build_schema_contract()['ok'] is True
    assert public_safety_dispatch_build_service_contract()['ok'] is True
    assert public_safety_dispatch_build_release_evidence()['ok'] is True
    assert public_safety_dispatch_runtime_smoke()['ok'] is True


def test_public_safety_dispatch_events_ui_boundary_and_configuration():
    state = public_safety_dispatch_empty_state()
    assert public_safety_dispatch_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.public_safety_dispatch.events'})['ok'] is True
    assert public_safety_dispatch_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert public_safety_dispatch_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert public_safety_dispatch_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert public_safety_dispatch_ui_contract()['ok'] is True
    assert public_safety_dispatch_render_workbench()['ok'] is True
    assert public_safety_dispatch_verify_owned_table_boundary((f'public_safety_dispatch_owned_table', 'foreign_table'))['ok'] is False

from pyAppGen.pbcs.maritime_shipping_operations.controls import evaluate_control
from pyAppGen.pbcs.maritime_shipping_operations.forms import form_catalog
from pyAppGen.pbcs.maritime_shipping_operations.release_evidence import validate_release_evidence
from pyAppGen.pbcs.maritime_shipping_operations.standalone import MaritimeShippingOperationsStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.maritime_shipping_operations.ui import maritime_shipping_operations_standalone_ui_contract
from pyAppGen.pbcs.maritime_shipping_operations.wizards import wizard_catalog


def test_standalone_app_runs_voyage_to_claim_flow():
    smoke = standalone_smoke_test()
    assert smoke['ok'] is True
    demo = smoke['demo']
    assert demo['vessel_bad']['ok'] is False
    assert demo['dg_bad']['ok'] is False
    assert demo['call_bad']['ok'] is False
    assert demo['bunker_bad']['ok'] is False
    assert demo['obligation_bad']['ok'] is False
    assert demo['claim']['claim']['demurrage_amount'] > 0
    assert demo['simulation']['mutates_live_records'] is False


def test_forms_wizards_controls_surface_maritime_domain():
    assert len(form_catalog()['forms']) >= 9
    assert len(wizard_catalog()['wizards']) >= 7
    assert maritime_shipping_operations_standalone_ui_contract()['ok'] is True
    blocked = evaluate_control('booking_acceptance_control', {'capacity_check': True})
    assert blocked['ok'] is False
    assert 'accept_booking' in blocked['blocked_actions']


def test_schedule_recovery_and_boundary_are_executable():
    app = MaritimeShippingOperationsStandaloneApp()
    assert app.configure()['ok'] is True
    app.register_vessel('VES-X', 'IMO-X', True, True, True)
    app.create_voyage('VOY-X', 'VES-X', 'STRING', 'LANE', ({'seq': 1, 'from': 'A', 'to': 'B', 'eta_hour': 10},))
    sim = app.simulate_recovery('VOY-X', 'speed_up', 2.0)
    assert sim['ok'] is True
    assert sim['mutates_live_records'] is False
    preview = app.assistant_maritime_action_preview('port delay email', 'revise ETA')
    assert preview['ok'] is True
    assert preview['requires_confirmation'] is True


def test_agent_preview_is_owned_and_confirmation_gated():
    app = MaritimeShippingOperationsStandaloneApp()
    preview = app.assistant_maritime_action_preview('shipping instruction', 'draft booking update')
    assert preview['ok'] is True
    assert preview['crud_preview']['table'] == 'maritime_shipping_operations_voyage'
    assert preview['requires_confirmation'] is True
    contract = single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['stream_engine_picker_visible'] is False
    assert all(table.startswith('maritime_shipping_operations_') for table in contract['owned_tables'])


def test_release_evidence_includes_standalone_sections():
    evidence = validate_release_evidence()
    assert evidence['ok'] is True
    assert evidence['failed_checks'] == ()

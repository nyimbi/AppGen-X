from pyAppGen.pbcs.lease_lending_equipment_finance.controls import evaluate_control
from pyAppGen.pbcs.lease_lending_equipment_finance.forms import form_catalog
from pyAppGen.pbcs.lease_lending_equipment_finance.release_evidence import validate_release_evidence
from pyAppGen.pbcs.lease_lending_equipment_finance.standalone import LeaseLendingEquipmentFinanceStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.lease_lending_equipment_finance.ui import lease_lending_equipment_finance_standalone_ui_contract
from pyAppGen.pbcs.lease_lending_equipment_finance.wizards import wizard_catalog


def test_standalone_app_runs_application_to_recovery_flow():
    smoke = standalone_smoke_test()
    assert smoke['ok'] is True
    demo = smoke['demo']
    assert demo['booked']['lease']['booked'] is True
    assert demo['duplicate_asset']['ok'] is False
    assert demo['blocked_repo']['ok'] is False
    assert demo['investor_bad']['ok'] is False
    assert demo['usage']['usage']['disputed_component_paused'] is True
    assert demo['quote']['quote']['quote_type'] == 'fmv'


def test_forms_wizards_controls_surface_equipment_finance_domain():
    assert len(form_catalog()['forms']) >= 9
    assert len(wizard_catalog()['wizards']) >= 7
    assert lease_lending_equipment_finance_standalone_ui_contract()['ok'] is True
    blocked = evaluate_control('funding_disbursement_control', {'invoice_reconciled': True})
    assert blocked['ok'] is False
    assert 'release_funds' in blocked['blocked_actions']


def test_booking_requires_conditions_assets_schedule_and_funding():
    app = LeaseLendingEquipmentFinanceStandaloneApp()
    assert app.configure()['ok'] is True
    app.create_application('LEASE-X', 'loan', 'borrower', 'dealer', 100000, ('insurance',))
    blocked = app.book_lease('LEASE-X')
    assert blocked['ok'] is False
    app.clear_condition('LEASE-X', 'insurance', 'binder')
    app.register_asset('AST-X', 'LEASE-X', ('SN-X',), 'medical_device', 'clinic', 'clear')
    app.approve_structure('LEASE-X', 'loan', 'loan', 'none', False, False, 'borrower_tax_owner')
    low_yield = app.generate_schedule('LEASE-X', 100000, 24, 0.04)
    assert low_yield['ok'] is False
    assert app.book_lease('LEASE-X')['ok'] is False


def test_agent_finance_pack_preview_is_owned_and_confirmation_gated():
    app = LeaseLendingEquipmentFinanceStandaloneApp()
    preview = app.assistant_finance_pack_preview('invoice and title pack', 'draft asset update')
    assert preview['ok'] is True
    assert preview['crud_preview']['table'] == 'lease_lending_equipment_finance_equipment_lease'
    assert preview['requires_confirmation'] is True
    assert preview['extraction']['requires_citation_spans'] is True
    contract = single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['stream_engine_picker_visible'] is False
    assert all(table.startswith('lease_lending_equipment_finance_') for table in contract['owned_tables'])


def test_release_evidence_includes_standalone_sections():
    evidence = validate_release_evidence()
    assert evidence['ok'] is True
    assert evidence['failed_checks'] == ()

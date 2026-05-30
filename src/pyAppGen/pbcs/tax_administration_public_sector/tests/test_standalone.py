from pyAppGen.pbcs.tax_administration_public_sector.controls import evaluate_control
from pyAppGen.pbcs.tax_administration_public_sector.forms import form_catalog, form_for
from pyAppGen.pbcs.tax_administration_public_sector.standalone import TaxAdministrationPublicSectorStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.tax_administration_public_sector.wizards import wizard_catalog, wizard_for


def test_single_pbc_app_contract_exposes_tax_administration_surface():
    contract=single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['database_backends'] == ('postgresql','mysql','mariadb')
    assert contract['event_contract'] == 'AppGen-X'
    assert contract['stream_engine_picker_visible'] is False
    assert contract['dsl']['skills_namespace'] == 'tax_administration_public_sector_skills'
    assert len(contract['forms']['forms']) >= 12
    assert len(contract['wizards']['wizards']) >= 9
    assert len(contract['controls']['controls']) >= 12


def test_forms_wizards_and_controls_cover_revenue_administration():
    assert form_catalog()['ok'] is True
    assert form_for('taxpayer_identity')['form']['owned_table'] == 'tax_administration_public_sector_taxpayer_account'
    assert form_for('refund_claim')['ok'] is True
    assert wizard_catalog()['ok'] is True
    assert wizard_for('return_to_assessment')['ok'] is True
    assert wizard_for('assistant_intake_preview')['ok'] is True
    assert evaluate_control('identity_has_legal_basis', {'legal_name':'A'})['ok'] is False
    assert evaluate_control('refund_screening_complete', {'bank_verified': True})['ok'] is False
    assert evaluate_control('agent_mutations_require_confirmation', {'confirmed': False})['ok'] is False


def test_standalone_tax_administration_workflow_is_executable_and_guarded():
    app=TaxAdministrationPublicSectorStandaloneApp()
    assert app.configure()['ok'] is True
    assert app.register_taxpayer_identity('T0','Acme',None,'KE')['ok'] is False
    assert app.register_taxpayer_identity('T1','Acme Ltd','company','KE',tin='TIN-1')['ok'] is True
    assert app.approve_registration_roles('R0','T1',())['ok'] is False
    assert app.approve_registration_roles('R1','T1',('income_tax','vat'))['ok'] is True
    assert app.derive_filing_obligation('O0','T1','VAT','2026-01','monthly')['ok'] is False
    assert app.derive_filing_obligation('O1','T1','VAT','2026-01','monthly','2026-02-20')['ok'] is True
    assert app.intake_return('F0','T1','2026-01',duplicate=True)['ok'] is False
    assert app.intake_return('F1','T1','2026-01',amount=1000)['ok'] is True
    assert app.raise_assessment('A0','T1','self',1000,'2026-01')['ok'] is False
    assert app.raise_assessment('A1','T1','self',1000,'2026-01','VAT Act')['ok'] is True
    assert app.allocate_payment('P0','T1','PAY',1000)['ok'] is False
    assert app.allocate_payment('P1','T1','PAY',1000,'oldest_debt_first')['ok'] is True
    assert app.review_refund('RF0','T1',100)['ok'] is False
    assert app.review_refund('RF1','T1',100,True,True,True,('maker','checker'))['ok'] is True
    assert app.serve_notice('N0','T1','v1','VAT Act','portal')['ok'] is False
    assert app.serve_notice('N1','T1','v1','VAT Act','portal','2026-03-01')['ok'] is True
    assert app.open_audit_case('AU0','T1','risk',(),50)['ok'] is False
    assert app.open_audit_case('AU1','T1','risk',('underpayment',),50)['ok'] is True
    assert app.lodge_appeal('AP0','T1','A1','2026-03-01','2026-03-10','grounds')['ok'] is False
    assert app.lodge_appeal('AP1','T1','A1','2026-03-01','2026-03-10','grounds','complete')['ok'] is True
    assert app.issue_collection_action('C0','T1','A1',True,False,True)['ok'] is False
    assert app.issue_collection_action('C1','T1','A1',True,True,True)['ok'] is True
    assert app.simulate_debt_treatment('T1',150,20000)['mutates_live_records'] is False
    assert app.assistant_tax_action_preview('return','create',False)['ok'] is False
    assert app.assistant_tax_action_preview('return','create',True)['ok'] is True


def test_standalone_smoke_proves_single_pbc_readiness():
    smoke=standalone_smoke_test()
    assert smoke['ok'] is True
    assert smoke['contract']['routes']['stream_engine_picker_visible'] is False

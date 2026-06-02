from pyAppGen.pbcs.humanitarian_relief_operations.controls import evaluate_control
from pyAppGen.pbcs.humanitarian_relief_operations.forms import form_catalog
from pyAppGen.pbcs.humanitarian_relief_operations.release_evidence import validate_release_evidence
from pyAppGen.pbcs.humanitarian_relief_operations.standalone import HumanitarianReliefOperationsStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.humanitarian_relief_operations.ui import humanitarian_relief_operations_standalone_ui_contract
from pyAppGen.pbcs.humanitarian_relief_operations.wizards import wizard_catalog


def test_standalone_app_runs_assessment_to_donor_pack_flow():
    smoke = standalone_smoke_test()
    assert smoke['ok'] is True
    assert smoke['demo']['duplicate']['ok'] is False
    assert smoke['demo']['blocked_shipment']['ok'] is False
    assert smoke['demo']['variance']['ok'] is False
    assert smoke['demo']['donor']['donor_pack']['signoff_status'] == 'ready'


def test_forms_wizards_controls_surface_humanitarian_domain():
    assert len(form_catalog()['forms']) >= 8
    assert len(wizard_catalog()['wizards']) >= 6
    assert humanitarian_relief_operations_standalone_ui_contract()['ok'] is True
    blocked = evaluate_control('protection_confidentiality_control', {'failures': ('donor_export',)})
    assert blocked['ok'] is False
    assert 'donor_export' in blocked['blocked_actions']


def test_agent_brief_preview_stays_redacted_and_owned():
    app = HumanitarianReliefOperationsStandaloneApp()
    preview = app.assistant_brief_preview('field note with household names', 'draft donor-safe summary')
    assert preview['ok'] is True
    assert preview['crud_preview']['table'] == 'humanitarian_relief_operations_distribution_event'
    assert preview['requires_confirmation'] is True
    assert preview['redaction_policy'] == 'beneficiary_and_protection_safe'
    contract = single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['stream_engine_picker_visible'] is False
    assert all(table.startswith('humanitarian_relief_operations_') for table in contract['owned_tables'])


def test_release_evidence_includes_standalone_sections():
    assert validate_release_evidence()['ok'] is True

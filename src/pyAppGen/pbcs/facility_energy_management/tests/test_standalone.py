from pyAppGen.pbcs.facility_energy_management.controls import evaluate_control
from pyAppGen.pbcs.facility_energy_management.forms import form_catalog
from pyAppGen.pbcs.facility_energy_management.release_evidence import validate_release_evidence
from pyAppGen.pbcs.facility_energy_management.standalone import FacilityEnergyManagementStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.facility_energy_management.ui import facility_energy_management_standalone_ui_contract
from pyAppGen.pbcs.facility_energy_management.wizards import wizard_catalog


def test_standalone_app_runs_meter_to_settlement_flow():
    smoke = standalone_smoke_test()
    assert smoke['ok'] is True
    assert smoke['demo']['blocked_critical_load_dispatch']['ok'] is False
    assert smoke['demo']['dispatch']['event']['state'] == 'settled'
    assert smoke['demo']['optimization']['optimization']['command_boundary'] == 'approval_gated_handoff'


def test_facility_energy_forms_wizards_and_controls_are_domain_specific():
    assert form_catalog()['ok'] is True
    assert len(form_catalog()['forms']) >= 7
    assert wizard_catalog()['ok'] is True
    assert len(wizard_catalog()['wizards']) >= 6
    assert facility_energy_management_standalone_ui_contract()['ok'] is True
    blocked = evaluate_control('critical_load_guardrail', {'failures': ('shed_action',)})
    assert blocked['ok'] is False
    assert 'shed_action' in blocked['blocked_actions']


def test_agent_preview_and_contract_stay_inside_owned_boundary():
    app = FacilityEnergyManagementStandaloneApp()
    preview = app.assistant_preview('utility bill and tenant comfort memo', 'create tariff scenario')
    assert preview['ok'] is True
    assert preview['crud_preview']['table'] == 'facility_energy_management_energy_optimization'
    assert preview['requires_confirmation'] is True
    contract = single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['stream_engine_picker_visible'] is False
    assert all(table.startswith('facility_energy_management_') for table in contract['owned_tables'])


def test_release_evidence_includes_standalone_sections():
    evidence = validate_release_evidence()
    assert evidence['ok'] is True

from pyAppGen.pbcs.telecom_network_operations.controls import evaluate_control
from pyAppGen.pbcs.telecom_network_operations.forms import form_catalog, form_for
from pyAppGen.pbcs.telecom_network_operations.standalone import TelecomNetworkOperationsStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.telecom_network_operations.wizards import wizard_catalog, wizard_for


def test_single_pbc_app_contract_exposes_telecom_surface():
    contract=single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['database_backends'] == ('postgresql','mysql','mariadb')
    assert contract['event_contract'] == 'AppGen-X'
    assert contract['stream_engine_picker_visible'] is False
    assert contract['dsl']['skills_namespace'] == 'telecom_network_operations_skills'
    assert len(contract['forms']['forms']) >= 11
    assert len(contract['wizards']['wizards']) >= 7
    assert len(contract['controls']['controls']) >= 11


def test_forms_wizards_controls_cover_noc_domain():
    assert form_catalog()['ok'] is True
    assert form_for('site_hierarchy')['form']['owned_table'] == 'telecom_network_operations_network_element'
    assert form_for('outage_war_room')['ok'] is True
    assert wizard_catalog()['ok'] is True
    assert wizard_for('alarm_to_outage')['ok'] is True
    assert wizard_for('assistant_alarm_triage')['ok'] is True
    assert evaluate_control('site_has_geospatial_identity', {'site_code':'S'})['ok'] is False
    assert evaluate_control('capacity_headroom_positive', {'installed':100,'reserved':80,'used':40})['ok'] is False
    assert evaluate_control('agent_mutations_require_confirmation', {'confirmed':False})['ok'] is False


def test_standalone_telecom_workflow_is_executable_and_guarded():
    app=TelecomNetworkOperationsStandaloneApp()
    assert app.configure()['ok'] is True
    assert app.register_site('S0','SITE',None,36.8,'macro')['ok'] is False
    assert app.register_site('S1','SITE-1',-1.2,36.8,'macro')['ok'] is True
    assert app.model_radio_cell('C0','missing','5G','A')['ok'] is False
    assert app.model_radio_cell('C1','S1','5G','A')['ok'] is True
    assert app.register_circuit_path('CK0','A',None,())['ok'] is False
    assert app.register_circuit_path('CK1','S1','POP1',('fiber-1','agg-1'),True)['ok'] is True
    assert app.normalize_alarm('AL0','RAW',None,'critical','loss','cell')['ok'] is False
    assert app.normalize_alarm('AL1','RAW','transport_loss','critical','fiber_cut','circuit','CK1')['ok'] is True
    assert app.correlate_root_cause('COR0',None,('AL1',))['ok'] is False
    assert app.correlate_root_cause('COR1','AL1',('AL2','AL3'))['ok'] is True
    assert app.declare_outage('I0','declared',None,('svc',))['ok'] is False
    assert app.declare_outage('I1','declared','noc-chief',('enterprise-vpn',),'30m')['ok'] is True
    assert app.approve_maintenance_window('MW0','MOP1',None,('S1',))['ok'] is False
    assert app.approve_maintenance_window('MW1','MOP1','rollback',('S1',))['ok'] is True
    assert app.calculate_sla_impact('SLA0','CASE1',True,False)['ok'] is False
    assert app.calculate_sla_impact('SLA1','CASE1',True,True,'planned')['ok'] is True
    assert app.record_capacity_snapshot('CAP0',100,80,40)['ok'] is False
    assert app.record_capacity_snapshot('CAP1',100,20,40)['ok'] is True
    assert app.open_assurance_case('CASE1','I1','P1','500 circuits')['ok'] is True
    assert app.capture_field_evidence('FE0','CASE1')['ok'] is False
    assert app.capture_field_evidence('FE1','CASE1','photo','done')['ok'] is True
    assert app.simulate_reroute_playbook('CK1',('alt-1',))['mutates_live_records'] is False
    assert app.assistant_alarm_triage_preview('alarms','create outage',False)['ok'] is False
    assert app.assistant_alarm_triage_preview('alarms','create outage',True)['ok'] is True


def test_standalone_smoke_proves_single_pbc_readiness():
    smoke=standalone_smoke_test()
    assert smoke['ok'] is True
    assert smoke['contract']['routes']['stream_engine_picker_visible'] is False

from pyAppGen.pbcs.waste_recycling_operations.controls import evaluate_control
from pyAppGen.pbcs.waste_recycling_operations.forms import form_catalog, form_for
from pyAppGen.pbcs.waste_recycling_operations.standalone import WasteRecyclingOperationsStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.waste_recycling_operations.wizards import wizard_catalog, wizard_for


def test_single_pbc_contract_exposes_waste_operations_surface():
    contract = single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['database_backends'] == ('postgresql', 'mysql', 'mariadb')
    assert contract['event_contract'] == 'AppGen-X'
    assert contract['stream_engine_picker_visible'] is False
    assert contract['dsl']['skills_namespace'] == 'waste_recycling_operations_skills'
    assert len(contract['forms']['forms']) >= 10
    assert len(contract['wizards']['wizards']) >= 7
    assert len(contract['controls']['controls']) >= 9


def test_forms_wizards_and_controls_are_domain_specific():
    assert form_catalog()['ok'] is True
    assert form_for('RouteReleaseForm')['form']['owned_table'] == 'waste_recycling_operations_waste_route'
    assert form_for('HazardousExceptionForm')['ok'] is True
    assert wizard_catalog()['ok'] is True
    assert wizard_for('MissedPickupResolutionWizard')['ok'] is True
    assert wizard_for('DiversionReportingWizard')['ok'] is True
    assert evaluate_control('route_has_crew_vehicle_and_facility_window', {'crew_projection': 'c'})['ok'] is False
    assert evaluate_control('disposal_ticket_weights_reconcile', {'gross_weight': 100, 'tare_weight': 20, 'net_weight': 70})['ok'] is False
    assert evaluate_control('agent_mutations_require_confirmation', {'confirmed': False})['ok'] is False


def test_standalone_waste_recycling_workflow_is_executable_and_guarded():
    app = WasteRecyclingOperationsStandaloneApp()
    assert app.configure()['ok'] is True
    assert app.release_route('R0', '2026-05-30', 'recycling', 'north', ('S1',))['ok'] is False
    assert app.release_route('R1', '2026-05-30', 'recycling', 'north', ('S1',), 'crew-a', 'truck-9', '06:00-14:00')['ok'] is True
    assert app.register_bin('B1', 'SER1', 'RF1', 'recycling', '12 River Rd')['ok'] is True
    assert app.define_material_stream('MS1', ('paper', 'cardboard'), ('battery', 'food'), .08, 'MRF-1')['ok'] is True
    assert app.record_pickup('P0', 'R1', 'B1', 'missed')['ok'] is False
    assert app.record_pickup('P1', 'R1', 'B1', 'completed', gps='-1,36', weight_estimate=14, photo_digest='photo')['ok'] is True
    assert app.classify_missed_pickup('MP1', 'P1', 'resident', 'operator_miss', True)['ok'] is True
    assert app.record_contamination('C1', 'B1', 'R1', 'plastic_bag', 'medium', 'photo', 2)['ok'] is True
    assert app.open_hazardous_exception('H1', 'R1', 'B1', 'battery', 'isolate bin')['ok'] is True
    assert app.reconcile_disposal_ticket('T0', 'R1', 'MRF-1', 100, 20, 70, 'recycling')['ok'] is False
    assert app.reconcile_disposal_ticket('T1', 'R1', 'MRF-1', 100, 20, 80, 'recycling')['ok'] is True
    assert app.calculate_recycling_yield('Y1', 'MRF-1', 'recycling', 80, 8, 64)['yield']['diversion_rate'] == 0.8
    assert app.assistant_preview('missed pickup memo', 'create recovery task', False)['ok'] is False
    assert app.assistant_preview('missed pickup memo', 'create recovery task', True)['ok'] is True


def test_standalone_smoke_proves_single_pbc_readiness():
    smoke = standalone_smoke_test()
    assert smoke['ok'] is True
    assert smoke['contract']['routes']['stream_engine_picker_visible'] is False

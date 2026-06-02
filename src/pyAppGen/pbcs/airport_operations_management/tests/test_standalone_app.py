from pyAppGen.pbcs.airport_operations_management import implementation_contract, smoke_test
from pyAppGen.pbcs.airport_operations_management.agent import composed_agent_contribution, document_instruction_plan
from pyAppGen.pbcs.airport_operations_management.release_evidence import build_release_evidence
from pyAppGen.pbcs.airport_operations_management.routes import api_route_contracts
from pyAppGen.pbcs.airport_operations_management.standalone import (
    airport_controls_contract,
    airport_forms_contract,
    airport_wizards_contract,
    assistant_document_plan,
    baggage_contingency_plan,
    build_turnaround_milestone_graph,
    full_airport_operations_drill,
    gate_change_impact_preview,
    go_live_drill_scorecard,
    overlap_guardrail,
    passenger_flow_forecast,
    plan_deicing_queue,
    plan_remote_bussing,
    reconcile_acdm_slot,
    seeded_airport_scenario_library,
    single_pbc_app_contract,
    standalone_route_contracts,
    standalone_smoke_test,
)


def test_single_pbc_app_covers_airport_backlog_surface():
    app = single_pbc_app_contract()
    assert app['ok'] is True
    assert app['database_backends'] == ('postgresql', 'mysql', 'mariadb')
    assert app['event_contract'] == 'AppGen-X'
    assert app['stream_engine_picker_visible'] is False
    assert app['forms']['covered_improve1_items'] == tuple(range(1, 51))
    assert app['wizards']['covered_improve1_items'] == tuple(range(1, 51))
    assert app['controls']['covered_improve1_items'] == tuple(range(1, 51))
    assert app['dsl_exposure']['agent_skill_namespace'] == 'airport_operations_management_skills'


def test_forms_wizards_controls_are_owned_and_no_stream_picker():
    forms = airport_forms_contract()
    wizards = airport_wizards_contract()
    controls = airport_controls_contract()
    assert forms['ok'] is True
    assert wizards['ok'] is True
    assert controls['ok'] is True
    assert all(form['owned_table'].startswith('airport_operations_management_') for form in forms['forms'])
    assert forms['foreign_table_writes'] == ()
    assert controls['event_contract'] == 'AppGen-X'
    assert controls['stream_engine_picker_visible'] is False


def test_airport_operating_primitives_execute():
    graph = build_turnaround_milestone_graph({'on_block': {'planned': '09:00'}, 'doors_closed': {'planned': '10:00', 'depends_on': ('fuel_complete',), 'predicted_delay_minutes': 7}})
    assert graph['ok'] is True
    assert graph['critical_path']
    assert plan_remote_bussing(passengers=180, buses_available=2, bus_capacity=90, lead_time_minutes=15)['ok'] is True
    assert plan_deicing_queue(({'flight_number': 'A1'},), pads=1, type_i_liters=1500, type_iv_liters=500)['ok'] is True
    assert reconcile_acdm_slot('10:00', '09:55', '10:10', '10:20')['resync_required'] is True


def test_baggage_passenger_flow_gate_impact_and_drill_controls():
    assert baggage_contingency_plan('R1', ({'belt': 'R2', 'available': True, 'capacity_bags': 100},))['ok'] is True
    flow = passenger_flow_forecast({'security': 300}, {'security': 250})
    assert flow['ok'] is False
    assert flow['capacity_breaches'][0]['segment'] == 'security'
    impact = gate_change_impact_preview({'passengers': 210, 'prm_travelers': 1})
    assert impact['requires_approval'] is True
    assert go_live_drill_scorecard({'stand_allocation': True})['ok'] is False


def test_agent_document_plans_are_cited_confirmed_and_permissioned():
    plan = assistant_document_plan('Gate change with deicing and baggage belt issue', 'preview stand change')
    assert plan['ok'] is True
    assert plan['citations_required'] is True
    assert plan['requires_human_confirmation'] is True
    assert plan['escalation_required'] is True
    assert plan['crud_preview']['foreign_table_writes'] == ()
    delegated = document_instruction_plan('Runway closure brief', 'generate disruption brief')
    assert delegated['ok'] is True
    assert delegated['requires_human_confirmation'] is True


def test_overlap_guard_rejects_external_source_tables():
    assert overlap_guardrail(('aodb_flight_projection', 'weather_projection'))['ok'] is True
    assert overlap_guardrail(('aodb_flight',))['ok'] is False


def test_release_drill_routes_implementation_and_package_smoke():
    assert seeded_airport_scenario_library()['ok'] is True
    drill = full_airport_operations_drill()
    assert drill['ok'] is True
    assert drill['blocking_gaps'] == ()
    routes = api_route_contracts()
    assert routes['ok'] is True
    assert 'GET /airport-operations-management/app' in routes['routes']
    assert standalone_route_contracts()['ok'] is True
    evidence = build_release_evidence()
    assert evidence['ok'] is True
    assert evidence['single_pbc_app']['ok'] is True
    contract = implementation_contract()
    assert contract['single_pbc_app']['ok'] is True
    assert standalone_smoke_test()['ok'] is True
    assert smoke_test()['ok'] is True
    assert composed_agent_contribution()['standalone_app']['pbc'] == 'airport_operations_management'

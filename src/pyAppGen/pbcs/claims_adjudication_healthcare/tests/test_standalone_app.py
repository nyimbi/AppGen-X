from pyAppGen.pbcs.claims_adjudication_healthcare import implementation_contract, smoke_test
from pyAppGen.pbcs.claims_adjudication_healthcare.agent import composed_agent_contribution
from pyAppGen.pbcs.claims_adjudication_healthcare.release_evidence import build_release_evidence
from pyAppGen.pbcs.claims_adjudication_healthcare.routes import api_route_contracts
from pyAppGen.pbcs.claims_adjudication_healthcare.standalone import (
    adjudicate_mixed_claim_lines,
    canonicalize_claim,
    controls_contract,
    duplicate_claim_score,
    forms_contract,
    full_claims_adjudication_simulation,
    overlap_guardrail,
    release_scenario_library,
    single_pbc_app_contract,
    standalone_route_contracts,
    standalone_smoke_test,
    wizards_contract,
)


def test_single_pbc_app_covers_improve1_surface():
    app = single_pbc_app_contract()
    assert app['ok'] is True
    assert app['database_backends'] == ('postgresql', 'mysql', 'mariadb')
    assert app['event_contract'] == 'AppGen-X'
    assert app['stream_engine_picker_visible'] is False
    assert app['forms']['covered_improve1_items'] == tuple(range(1, 51))
    assert app['wizards']['covered_improve1_items'] == tuple(range(1, 51))
    assert app['controls']['covered_improve1_items'] == tuple(range(1, 51))


def test_forms_wizards_controls_are_owned_and_guarded():
    forms = forms_contract()
    wizards = wizards_contract()
    controls = controls_contract()
    assert forms['ok'] is True
    assert wizards['ok'] is True
    assert controls['ok'] is True
    assert all(form['owned_table'].startswith('claims_adjudication_healthcare_') for form in forms['forms'])
    assert forms['foreign_table_writes'] == ()
    assert controls['event_contract'] == 'AppGen-X'


def test_claim_table_stakes_execute():
    assert canonicalize_claim({'claim_number': 'C1', 'member_id': 'M1', 'provider_id': 'P1', 'plan_id': 'PPO'})['ok'] is True
    mixed = adjudicate_mixed_claim_lines(({'line_number': 1, 'charge_amount': 100}, {'line_number': 2, 'charge_amount': 50, 'deny': True}, {'line_number': 3, 'requires_review': True}))
    assert mixed['ok'] is True
    assert mixed['has_mixed_outcomes'] is True
    duplicate = duplicate_claim_score({'member_id': 'M1', 'provider_id': 'P1', 'service_date': '2026-01-01', 'procedure_code': '99213', 'units': 1, 'charge_amount': 100}, ({'claim_id': 'old', 'member_id': 'M1', 'provider_id': 'P1', 'service_date': '2026-01-01', 'procedure_code': '99213', 'units': 1, 'charge_amount': 100},))
    assert duplicate['matches'][0]['score'] == 1.0


def test_boundary_guard_rejects_external_tables():
    assert overlap_guardrail(('member_eligibility_projection', 'provider_network_projection'))['ok'] is True
    assert overlap_guardrail(('member_enrollment',))['ok'] is False


def test_release_simulation_routes_agent_and_package_smoke():
    assert release_scenario_library()['ok'] is True
    simulation = full_claims_adjudication_simulation()
    assert simulation['ok'] is True
    assert simulation['blocking_gaps'] == ()
    routes = api_route_contracts()
    assert routes['ok'] is True
    assert 'GET /claims-adjudication-healthcare/app' in routes['routes']
    assert standalone_route_contracts()['ok'] is True
    evidence = build_release_evidence()
    assert evidence['ok'] is True
    assert evidence['single_pbc_app']['ok'] is True
    assert implementation_contract()['single_pbc_app']['ok'] is True
    assert standalone_smoke_test()['ok'] is True
    assert smoke_test()['ok'] is True
    assert composed_agent_contribution()['standalone_app']['pbc'] == 'claims_adjudication_healthcare'

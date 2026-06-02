from pyAppGen.pbcs.actuarial_pricing_reserving import implementation_contract, smoke_test
from pyAppGen.pbcs.actuarial_pricing_reserving.agent import composed_agent_contribution, document_instruction_plan
from pyAppGen.pbcs.actuarial_pricing_reserving.release_evidence import build_release_evidence
from pyAppGen.pbcs.actuarial_pricing_reserving.routes import api_route_contracts
from pyAppGen.pbcs.actuarial_pricing_reserving.standalone import (
    actuarial_controls_contract,
    actuarial_forms_contract,
    actuarial_wizards_contract,
    agent_document_instruction_plan,
    assemble_actuarial_memo,
    credibility_blend,
    dependency_freshness_gate,
    finance_handoff_event,
    full_actuarial_release_simulation,
    model_validation_gate,
    monitor_model_drift,
    overlap_guardrail,
    rate_dislocation_analysis,
    replay_dead_letter_event,
    reserve_uncertainty_distribution,
    seeded_actuarial_scenario_library,
    single_pbc_app_contract,
    standalone_route_contracts,
    standalone_smoke_test,
    verify_evidence_chain,
)


def test_single_pbc_app_surfaces_full_improve1_backlog():
    app = single_pbc_app_contract()
    assert app['ok'] is True
    assert app['database_backends'] == ('postgresql', 'mysql', 'mariadb')
    assert app['event_contract'] == 'AppGen-X'
    assert app['stream_engine_picker_visible'] is False
    assert app['forms']['covered_improve1_items'] == tuple(range(1, 51))
    assert app['wizards']['covered_improve1_items'] == tuple(range(1, 51))
    assert app['controls']['covered_improve1_items'] == tuple(range(1, 51))
    assert app['dsl_exposure']['agent_skill_namespace'] == 'actuarial_pricing_reserving_skills'


def test_forms_wizards_controls_are_owned_and_actionable():
    forms = actuarial_forms_contract()
    wizards = actuarial_wizards_contract()
    controls = actuarial_controls_contract()
    assert forms['ok'] is True
    assert wizards['ok'] is True
    assert controls['ok'] is True
    assert all(form['owned_table'].startswith('actuarial_pricing_reserving_') for form in forms['forms'])
    assert forms['foreign_table_writes'] == ()
    assert controls['event_contract'] == 'AppGen-X'


def test_actuarial_table_stakes_and_advanced_functions_execute():
    assert credibility_blend('1.20', '1.05', '0.40')['blended_indication'] == '1.1100'
    assert rate_dislocation_analysis(('100',), ('140',), cap='0.15')['cohorts'][0]['capped'] is True
    assert reserve_uncertainty_distribution('1000')['percentiles'][2]['percentile'] == 'P95'
    assert dependency_freshness_gate({'claims': {'freshness_score': '0.80', 'stale_policy': 'block'}})['ok'] is False
    assert monitor_model_drift({'calibration_error': '0.07'}, {'calibration_error': '0.05'})['open_review_task'] is True


def test_agent_document_crud_requires_citations_confirmation_and_authority():
    plan = agent_document_instruction_plan('Reserve close memo with trend assumption', 'create reserve estimate')
    assert plan['ok'] is True
    assert plan['citations_required'] is True
    assert plan['requires_human_confirmation'] is True
    assert plan['missing_permissions']
    assert plan['crud_preview']['foreign_table_writes'] == ()
    delegated = document_instruction_plan('Capital stress instruction', 'run capital scenario')
    assert delegated['ok'] is True
    assert delegated['requires_human_confirmation'] is True


def test_boundary_handoff_and_dead_letter_are_safe():
    assert overlap_guardrail(('policy_exposure_projection', 'claims_projection'))['ok'] is True
    assert overlap_guardrail(('gl_entry',))['ok'] is False
    handoff = finance_handoff_event({'close_package_id': 'CLOSE-1', 'reserve_estimate_id': 'RES-1'})
    assert handoff['ok'] is True
    assert 'gl_entry' in handoff['forbidden_writes']
    replay = replay_dead_letter_event({'idempotency_keys': {'idem-1'}}, {'idempotency_key': 'idem-1'})
    assert replay['duplicate'] is True


def test_release_simulation_run_package_and_evidence_chain():
    seeds = seeded_actuarial_scenario_library()
    assert seeds['ok'] is True
    simulation = full_actuarial_release_simulation()
    assert simulation['ok'] is True
    assert simulation['blocking_gaps'] == ()
    proof = verify_evidence_chain(({'event_type': 'A'}, {'event_type': 'B'}))
    assert proof['ok'] is True
    assert len(proof['chain']) == 2
    memo = assemble_actuarial_memo({'data': 'x'}, {'data': ('EXP-1',)})
    assert memo['ok'] is True


def test_model_validation_blocks_unvalidated_models():
    failed = model_validation_gate({'model_id': 'M1'}, {'validation_id': 'V1', 'reviewer_independent': False, 'status': 'passed', 'expires_on': '2027-01-01', 'backtest_ok': True})
    assert failed['ok'] is False
    assert failed['blocks_activation'] is True


def test_routes_release_implementation_and_package_smoke_include_standalone_app():
    routes = api_route_contracts()
    assert routes['ok'] is True
    assert 'GET /actuarial-pricing-reserving/app' in routes['routes']
    assert standalone_route_contracts()['ok'] is True
    evidence = build_release_evidence()
    assert evidence['ok'] is True
    assert evidence['single_pbc_app']['ok'] is True
    contract = implementation_contract()
    assert contract['single_pbc_app']['ok'] is True
    assert standalone_smoke_test()['ok'] is True
    assert smoke_test()['ok'] is True
    assert composed_agent_contribution()['standalone_app']['pbc'] == 'actuarial_pricing_reserving'

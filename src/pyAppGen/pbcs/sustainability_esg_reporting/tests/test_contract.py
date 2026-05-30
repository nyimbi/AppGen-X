from pyAppGen.pbcs.sustainability_esg_reporting import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.sustainability_esg_reporting.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.sustainability_esg_reporting.config import (
    compile_rule,
    evaluate_rule,
    governance_smoke_test,
    parameter_manifest,
    rule_manifest,
)
from pyAppGen.pbcs.sustainability_esg_reporting.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.sustainability_esg_reporting.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.sustainability_esg_reporting.release_evidence import (
    build_release_evidence,
    pbc_agent_audit,
    pbc_capability_audit,
    pbc_generation_smoke_audit,
    pbc_implementation_release_audit,
    pbc_package_audit,
    pbc_source_artifact_contract,
    pbc_specification_audit,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.sustainability_esg_reporting.routes import api_route_contracts, dispatch_route, validate_api_route_contracts
from pyAppGen.pbcs.sustainability_esg_reporting.schema_contract import build_schema_contract
from pyAppGen.pbcs.sustainability_esg_reporting.service_contract import build_service_contract
from pyAppGen.pbcs.sustainability_esg_reporting.services import service_operation_contracts
from pyAppGen.pbcs.sustainability_esg_reporting.slice_app import build_standalone_app, build_runtime_capabilities, slice_app_smoke_test
from pyAppGen.pbcs.sustainability_esg_reporting.ui import sustainability_esg_reporting_render_workbench, sustainability_esg_reporting_ui_contract


def test_generated_schema_service_and_release_evidence():
    schema = build_schema_contract()
    service = build_service_contract()
    release = build_release_evidence()
    readiness = release_readiness_manifest()
    validation = validate_release_evidence()

    assert schema['ok'] is True
    assert len(schema['owned_tables']) >= 24
    assert service['ok'] is True
    assert 'define_esg_metric' in service['command_methods']
    assert release['ok'] is True
    assert readiness['ok'] is True
    assert validation['ok'] is True
    assert pbc_source_artifact_contract()['ok'] is True
    assert pbc_package_audit()['ok'] is True
    assert pbc_specification_audit()['ok'] is True
    assert pbc_agent_audit()['ok'] is True
    assert pbc_implementation_release_audit()['ok'] is True
    assert pbc_capability_audit()['ok'] is True
    assert pbc_generation_smoke_audit()['ok'] is True


def test_manifest_and_event_contract():
    implementation = implementation_contract()
    event_manifest = event_contract_manifest()
    event_validation = validate_event_contract()

    assert implementation['pbc'] == 'sustainability_esg_reporting'
    assert implementation['advanced_runtime']['ok'] is True
    assert event_manifest['ok'] is True
    assert 'SupplierQualified' in event_manifest['consumed']
    assert 'EmissionsCalculated' in event_manifest['emitted']
    assert event_validation['ok'] is True


def test_end_to_end_esg_reporting_flow_is_executable():
    app = build_standalone_app()
    metric = app.execute_operation(
        'define_esg_metric',
        {
            'tenant': 'tenant-test',
            'code': 'METRIC-GHG',
            'metric_name': 'Gross GHG Emissions',
            'framework': 'ISSB',
            'materiality_score': 0.93,
        },
    )
    app.execute_operation(
        'assess_materiality',
        {
            'tenant': 'tenant-test',
            'metric_id': metric['record']['id'],
            'stakeholders': ('investors', 'employees', 'communities'),
            'materiality_score': 0.93,
        },
    )
    facility = app.execute_operation(
        'register_facility_profile',
        {'tenant': 'tenant-test', 'code': 'FAC-1', 'title': 'Main plant', 'country': 'KE'},
    )
    activity = app.execute_operation(
        'capture_activity_data',
        {
            'tenant': 'tenant-test',
            'facility_id': facility['record']['id'],
            'activity_type': 'diesel',
            'quantity': 250.0,
            'unit': 'liters',
        },
    )
    factor = app.execute_operation(
        'register_emissions_factor',
        {
            'tenant': 'tenant-test',
            'metric_id': metric['record']['id'],
            'factor_value': 2.68,
            'geography': 'KE',
            'year': 2026,
        },
    )
    scope1 = app.execute_operation(
        'calculate_scope1_emissions',
        {
            'tenant': 'tenant-test',
            'activity_record_id': activity['record']['id'],
            'quantity': 250.0,
            'factor_value': 2.68,
        },
    )
    scope2 = app.execute_operation(
        'calculate_scope2_emissions',
        {
            'tenant': 'tenant-test',
            'activity_record_id': activity['record']['id'],
            'quantity': 1250.0,
            'factor_value': 0.42,
            'market_adjustment': 0.85,
        },
    )
    target = app.execute_operation(
        'create_sustainability_target',
        {
            'tenant': 'tenant-test',
            'metric_id': metric['record']['id'],
            'target_value': 100.0,
            'baseline_value': 180.0,
            'target_year': 2030,
        },
    )
    progress = app.execute_operation(
        'measure_target_progress',
        {
            'tenant': 'tenant-test',
            'target_id': target['record']['id'],
            'target_value': 100.0,
            'actual_value': 72.0,
        },
    )
    app.execute_operation(
        'attach_assurance_evidence',
        {'tenant': 'tenant-test', 'metric_id': metric['record']['id'], 'evidence_uri': 's3://evidence/fact-sheet.pdf'},
    )
    packet = app.execute_operation(
        'build_disclosure_packet',
        {
            'tenant': 'tenant-test',
            'metric_id': metric['record']['id'],
            'frameworks': ('ISSB', 'CSRD'),
            'report_type': 'annual',
        },
    )
    board = app.execute_operation(
        'prepare_board_pack',
        {'tenant': 'tenant-test', 'disclosure_packet_id': packet['record']['id'], 'title': 'Q1 ESG Board Pack'},
    )
    filing = app.execute_operation(
        'file_regulator_filing',
        {
            'tenant': 'tenant-test',
            'disclosure_packet_id': packet['record']['id'],
            'regulator': 'SEC',
            'jurisdiction': 'US',
        },
    )
    scenario = app.execute_operation(
        'simulate_climate_scenario',
        {
            'tenant': 'tenant-test',
            'metric_id': metric['record']['id'],
            'baseline_emissions': scope1['co2e_total'] + scope2['co2e_total'],
            'shock_percent': 0.2,
        },
    )
    workbench = app.build_workbench_view(tenant='tenant-test')

    assert metric['ok'] is True
    assert factor['ok'] is True
    assert scope1['co2e_total'] == 670.0
    assert scope2['co2e_total'] == 446.25
    assert progress['progress_percent'] == 0.72
    assert packet['summary']['metrics'] == 1
    assert board['emitted_event'] == 'BoardPackPrepared'
    assert filing['emitted_event'] == 'RegulatorFilingSubmitted'
    assert scenario['stressed_emissions'] == 1339.5
    assert workbench['summary']['metrics_total'] == 1


def test_agent_preview_and_mutation_guards_are_enforced():
    manifest = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan(
        'Update the board pack and regulator filing for renewable claims and supplier evidence.',
        'preview document changes only',
    )
    preview = datastore_crud_plan('update', table='sustainability_esg_reporting_governed_document', payload={'status': 'preview'})
    rejected = datastore_crud_plan('update', table='foreign_table')
    contribution = composed_agent_contribution()

    assert manifest['ok'] is True
    assert chatbot['ok'] is True
    assert document['ok'] is True
    assert document['requires_human_confirmation'] is True
    assert preview['preview_only'] is True
    assert rejected['ok'] is False
    assert contribution['ok'] is True


def test_routes_ui_configuration_and_release_surface_are_coherent():
    routes = api_route_contracts()
    route_validation = validate_api_route_contracts()
    ui_contract = sustainability_esg_reporting_ui_contract()
    workbench = sustainability_esg_reporting_render_workbench({'tenant': 'tenant-ui'})
    route_dispatch = dispatch_route('/sustainability-esg-reporting-workbench', {'tenant': 'tenant-ui', 'limit': 3}, method='GET')
    runtime = build_runtime_capabilities()
    smoke = slice_app_smoke_test()

    assert routes['ok'] is True
    assert route_validation['ok'] is True
    assert ui_contract['ok'] is True
    assert len(ui_contract['forms']) >= 4
    assert len(ui_contract['wizards']) >= 3
    assert len(ui_contract['controls']) >= 4
    assert workbench['ok'] is True
    assert route_dispatch['ok'] is True
    assert runtime['ok'] is True
    assert smoke['ok'] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    compiled = compile_rule(rule_manifest()['rules'][0])
    evaluated = evaluate_rule(compiled, {'materiality_score': 0.6})
    governance = governance_smoke_test()

    assert compiled['ok'] is True
    assert evaluated['allowed'] is True
    assert governance['ok'] is True
    assert parameter_manifest()['ok'] is True


def test_event_handlers_are_idempotent_and_retryable():
    handler = handler_manifest()
    handled = dispatch_event({'event_type': 'SupplierQualified', 'event_id': 'evt-handler-1', 'tenant': 'tenant-events'})
    duplicate = dispatch_event({'event_type': 'SupplierQualified', 'event_id': 'evt-handler-1', 'tenant': 'tenant-events'}, handled['state'])
    rejected = dispatch_event({'event_type': 'Unexpected', 'event_id': 'evt-handler-2', 'tenant': 'tenant-events'}, duplicate['state'])

    assert handler['ok'] is True
    assert handled['ok'] is True
    assert duplicate['duplicate'] is True
    assert rejected['ok'] is False
    assert rejected['dead_letter_table'].endswith('dead_letter_event')


def test_service_surface_and_registration_are_side_effect_free():
    assert package_metadata_manifest()['pbc'] == 'sustainability_esg_reporting'
    assert validate_package_metadata()['ok'] is True
    assert package_discovery_plan()['ok'] is True
    assert package_discovery_plan()['side_effects'] == ()
    assert service_operation_contracts()['ok'] is True

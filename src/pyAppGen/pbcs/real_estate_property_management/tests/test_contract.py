
from pyAppGen.pbcs.real_estate_property_management import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.real_estate_property_management.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.real_estate_property_management.capability_assurance import (
    table_stakes_capability_manifest,
    validate_table_stakes_capability_coverage,
)
from pyAppGen.pbcs.real_estate_property_management.config import governance_smoke_test
from pyAppGen.pbcs.real_estate_property_management.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.real_estate_property_management.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.real_estate_property_management.permissions import permission_manifest
from pyAppGen.pbcs.real_estate_property_management.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.real_estate_property_management.routes import api_route_contracts, dispatch_route, validate_api_route_contracts
from pyAppGen.pbcs.real_estate_property_management.schema_contract import build_schema_contract
from pyAppGen.pbcs.real_estate_property_management.seed_data import seed_plan, validate_seed_data
from pyAppGen.pbcs.real_estate_property_management.service_contract import build_service_contract
from pyAppGen.pbcs.real_estate_property_management.services import (
    RealEstatePropertyManagementService,
    service_operation_contracts,
)
from pyAppGen.pbcs.real_estate_property_management.standalone import (
    PBC_KEY,
    build_demo_state,
    real_estate_property_management_runtime_capabilities,
    real_estate_property_management_verify_owned_table_boundary,
)


def _build_service_fixture():
    service = RealEstatePropertyManagementService()
    assert service.configure_runtime({'database_backend': 'postgresql', 'event_topic': 'pbc.real_estate_property_management.events'})['ok'] is True
    portfolio = service.create_portfolio({'id': 'portfolio-1', 'code': 'PORT-1', 'name': 'Cedar Portfolio'})
    property_record = service.create_property({'id': 'property-1', 'portfolio_id': portfolio['record']['id'], 'code': 'PROP-1', 'name': 'Cedar Heights', 'asset_class': 'multifamily', 'jurisdiction': 'Nairobi'})
    building = service.create_building({'id': 'building-1', 'property_id': property_record['record']['id'], 'code': 'BLDG-1', 'name': 'North Tower'})
    unit_a = service.create_unit({'id': 'unit-a', 'property_id': property_record['record']['id'], 'building_id': building['record']['id'], 'code': 'UNIT-A', 'unit_number': 'A1', 'market_rent': 1500, 'bedrooms': 2, 'bathrooms': 2})
    unit_b = service.create_unit({'id': 'unit-b', 'property_id': property_record['record']['id'], 'building_id': building['record']['id'], 'code': 'UNIT-B', 'unit_number': 'B1', 'market_rent': 1750, 'bedrooms': 2, 'bathrooms': 2})
    tenant = service.record_tenant({'id': 'tenant-1', 'code': 'TEN-1', 'display_name': 'Morgan Lee', 'contact_email': 'morgan@example.com', 'household': ({'display_name': 'Jordan Lee', 'role': 'occupant'}, {'display_name': 'Avery Lee', 'role': 'guarantor'})})
    lease = service.create_lease({'id': 'lease-1', 'property_id': property_record['record']['id'], 'unit_id': unit_a['record']['id'], 'tenant_id': tenant['record']['id'], 'code': 'LEASE-1', 'start_date': '2026-06-01', 'end_date': '2027-05-31', 'base_rent': 1500})
    schedule = service.generate_rent_schedule({'id': 'schedule-1', 'lease_id': lease['record']['id'], 'code': 'RS-1', 'next_due_date': '2026-06-01', 'frequency': 'monthly'})
    deposit = service.record_security_deposit({'id': 'deposit-1', 'lease_id': lease['record']['id'], 'tenant_id': tenant['record']['id'], 'code': 'DEP-1', 'amount': 1500})
    charge = service.post_charge({'id': 'charge-1', 'lease_id': lease['record']['id'], 'tenant_id': tenant['record']['id'], 'charge_type': 'rent', 'code': 'CHG-1', 'amount': 1500, 'due_date': '2026-06-05'})
    cam = service.accrue_cam_recovery({'id': 'cam-1', 'property_id': property_record['record']['id'], 'lease_id': lease['record']['id'], 'code': 'CAM-1', 'estimated_amount': 90})
    maintenance = service.open_maintenance_request({'id': 'maint-1', 'property_id': property_record['record']['id'], 'unit_id': unit_a['record']['id'], 'lease_id': lease['record']['id'], 'code': 'MR-1', 'summary': 'Plumbing leak', 'priority': 'high'})
    inspection = service.create_inspection({'id': 'insp-1', 'property_id': property_record['record']['id'], 'unit_id': unit_a['record']['id'], 'lease_id': lease['record']['id'], 'code': 'INSP-1', 'inspection_type': 'move_in', 'scheduled_for': '2026-06-01', 'result': 'pass'})
    vacancy = service.track_vacancy({'id': 'vac-1', 'property_id': property_record['record']['id'], 'unit_id': unit_b['record']['id'], 'code': 'VAC-1', 'market_ready_date': '2026-06-10'})
    renewal = service.manage_renewal({'id': 'renew-1', 'lease_id': lease['record']['id'], 'unit_id': unit_a['record']['id'], 'code': 'REN-1', 'stage': 'offer_sent', 'offered_rent': 1600, 'expires_on': '2027-03-15'})
    move_event = service.record_move_event({'id': 'move-1', 'lease_id': lease['record']['id'], 'unit_id': unit_a['record']['id'], 'code': 'MOVE-1', 'event_type': 'move_in', 'event_date': '2026-06-01'})
    delinquency = service.escalate_delinquency({'id': 'del-1', 'lease_id': lease['record']['id'], 'tenant_id': tenant['record']['id'], 'code': 'DEL-1', 'days_past_due': 34, 'balance_due': 275, 'stage': 'notice_pending'})
    notice = service.issue_notice({'id': 'notice-1', 'lease_id': lease['record']['id'], 'code': 'NOT-1', 'notice_type': 'pay_or_quit', 'served_on': '2026-07-10', 'service_method': 'email'})
    compliance = service.manage_compliance_case({'id': 'comp-1', 'property_id': property_record['record']['id'], 'code': 'COMP-1', 'title': 'Elevator certification', 'due_date': '2026-08-01', 'severity': 'high'})
    work_order = service.create_vendor_work_order({'id': 'wo-1', 'maintenance_request_id': maintenance['record']['id'], 'property_id': property_record['record']['id'], 'unit_id': unit_a['record']['id'], 'code': 'WO-1', 'vendor_name': 'FixFast', 'scheduled_for': '2026-06-03'})
    owner_report = service.publish_owner_report({'id': 'owner-1', 'property_id': property_record['record']['id'], 'code': 'OWNER-1', 'statement_period': '2026-06'})
    asset = service.capture_asset_performance({'id': 'asset-1', 'property_id': property_record['record']['id'], 'code': 'ASSET-1', 'reporting_period': '2026-06'})
    assistant = service.preview_assistant_document_instruction({'id': 'assistant-1', 'document': 'Lease renewal memo for unit A1 with revised rent.', 'instruction': 'Create a renewal and update the rent schedule preview.'})
    return service, {
        'portfolio': portfolio,
        'property': property_record,
        'building': building,
        'unit_a': unit_a,
        'unit_b': unit_b,
        'tenant': tenant,
        'lease': lease,
        'schedule': schedule,
        'deposit': deposit,
        'charge': charge,
        'cam': cam,
        'maintenance': maintenance,
        'inspection': inspection,
        'vacancy': vacancy,
        'renewal': renewal,
        'move_event': move_event,
        'delinquency': delinquency,
        'notice': notice,
        'compliance': compliance,
        'work_order': work_order,
        'owner_report': owner_report,
        'asset': asset,
        'assistant': assistant,
    }


def test_generated_schema_service_and_release_evidence():
    schema = build_schema_contract()
    service = build_service_contract()
    release = build_release_evidence()
    assert schema['ok'] is True
    assert len(schema['tables']) >= 20
    assert service['ok'] is True
    assert release['ok'] is True
    assert release_readiness_manifest()['ok'] is True
    assert validate_release_evidence()['ok'] is True
    assert api_route_contracts()['ok'] is True
    assert validate_api_route_contracts()['ok'] is True


def test_portfolio_leasing_and_workbench_flow():
    service, results = _build_service_fixture()
    assert all(result['ok'] for result in results.values())
    workbench = service.query_workbench({'property_id': 'property-1'})
    assessment = service.run_advanced_assessment({'focus': 'operations'})
    assert workbench['ok'] is True
    assert workbench['metrics']['occupancy_rate'] == 0.5
    assert workbench['metrics']['open_vacancies'] == 1
    assert workbench['metrics']['open_delinquency_cases'] == 1
    assert workbench['metrics']['pending_notices'] == 1
    assert workbench['owner_reporting'][0]['id'] == 'owner-1'
    assert workbench['asset_performance'][0]['id'] == 'asset-1'
    assert workbench['assistant_previews'][0]['id'] == 'assistant-1'
    assert 'vac-1' in workbench['queues']['vacancies']
    assert assessment['ok'] is True
    assert assessment['recommendations']
    assert assessment['risk_score'] > 0


def test_routes_support_canonical_and_legacy_property_endpoint():
    route1 = dispatch_route('POST /portfolios', {'id': 'portfolio-route', 'code': 'PORT-R', 'name': 'Route Portfolio'})
    assert route1['ok'] is True
    route2 = dispatch_route('POST /propertys', {'id': 'property-route', 'portfolio_id': 'portfolio-route', 'code': 'PROP-R', 'name': 'Route Property', 'asset_class': 'multifamily', 'jurisdiction': 'Nairobi'}, state=route1['state'])
    assert route2['ok'] is True
    assert route2['canonical_route'] == 'POST /properties'
    route3 = dispatch_route('GET /real-estate-property-management-workbench', {'property_id': 'property-route'}, state=route2['state'])
    assert route3['ok'] is True
    assert route3['result']['boards']


def test_agent_previews_and_owned_boundary_controls():
    assert agent_skill_manifest()['ok'] is True
    assert chatbot_interface_contract()['ok'] is True
    assert composed_agent_contribution()['ok'] is True
    plan = document_instruction_plan('Maintenance notice for lease 11 and unit B1', 'Update the notice draft and open a work order preview.')
    assert plan['ok'] is True
    assert any(table.endswith('notice') for table in plan['candidate_tables'])
    assert datastore_crud_plan('create', table=f'{PBC_KEY}_notice')['ok'] is True
    assert datastore_crud_plan('update', table='foreign_table')['ok'] is False
    boundary = real_estate_property_management_verify_owned_table_boundary((f'{PBC_KEY}_lease', 'foreign_table'))
    assert boundary['ok'] is False


def test_registration_governance_eventing_and_seed_hooks():
    assert implementation_contract()['pbc'] == PBC_KEY
    assert package_metadata_manifest()['pbc'] == PBC_KEY
    assert validate_package_metadata()['ok'] is True
    assert package_discovery_plan()['ok'] is True
    assert governance_smoke_test()['ok'] is True
    assert permission_manifest()['ok'] is True
    assert event_contract_manifest()['ok'] is True
    assert validate_event_contract()['ok'] is True
    manifest = handler_manifest()
    assert manifest['ok'] is True
    first = dispatch_event({'event_type': manifest['consumes'][0], 'idempotency_key': 'event-1'})
    second = dispatch_event({'event_type': manifest['consumes'][0], 'idempotency_key': 'event-1'})
    failed = dispatch_event({'event_type': 'Unexpected', 'idempotency_key': 'event-bad'})
    assert first['ok'] is True
    assert second['duplicate'] is True
    assert failed['dead_letter_table'].endswith('dead_letter_event')
    assert seed_plan()['ok'] is True
    assert validate_seed_data()['ok'] is True


def test_runtime_capability_surface_and_demo_state():
    runtime = real_estate_property_management_runtime_capabilities()
    assurance = validate_table_stakes_capability_coverage()
    manifest = table_stakes_capability_manifest()
    demo_state = build_demo_state()
    contracts = service_operation_contracts()
    assert runtime['ok'] is True
    assert runtime['smoke']['ok'] is True
    assert assurance['ok'] is True
    assert manifest['ok'] is True
    assert contracts['ok'] is True
    assert demo_state['records'][f'{PBC_KEY}_owner_statement']


def run_all_tests():
    executed = []
    for name, func in sorted(globals().items()):
        if name.startswith('test_') and callable(func):
            func()
            executed.append(name)
    return executed


if __name__ == '__main__':
    for name in run_all_tests():
        print(name)


def test_manifest_and_event_contract():
    assert implementation_contract()['pbc'] == PBC_KEY
    assert event_contract_manifest()['ok'] is True
    assert validate_event_contract()['ok'] is True


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()['pbc'] == PBC_KEY
    assert validate_package_metadata()['ok'] is True
    assert package_discovery_plan()['ok'] is True
    assert package_discovery_plan()['side_effects'] == ()


def test_service_and_route_surface_are_executable():
    contracts = service_operation_contracts()
    operation_contract = contracts.get('operation_contract')
    assert contracts['ok'] is True
    assert operation_contract
    assert api_route_contracts()['ok'] is True
    assert validate_api_route_contracts()['ok'] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()['ok'] is True
    assert permission_manifest()['ok'] is True
    assert seed_plan()['ok'] is True
    assert validate_seed_data()['ok'] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest['ok'] is True
    first = dispatch_event({'event_type': manifest['consumes'][0], 'idempotency_key': 'idem-real-estate-source-audit'})
    second = dispatch_event({'event_type': manifest['consumes'][0], 'idempotency_key': 'idem-real-estate-source-audit'})
    failed = dispatch_event({'event_type': 'Unexpected', 'idempotency_key': 'bad-real-estate-source-audit'})
    assert first['ok'] is True
    assert second['duplicate'] is True
    assert failed['dead_letter_table'].endswith('dead_letter_event')

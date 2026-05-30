"""Focused standalone one-PBC tests for utility_outage_restoration."""

from pathlib import Path

from .. import agent, models, release_evidence, routes, services, standalone, ui


def test_standalone_store_executes_outage_restoration_flow():
    store = models.UtilityOutageRestorationStandaloneStore()
    try:
        projection = store.register_network_asset_projection(
            {
                'projection_id': 'asset-test',
                'tenant': 'tenant-test',
                'asset_id': 'feeder-11',
                'critical_customers': ({'customer_id': 'hospital-1', 'life_support': True},),
            }
        )
        outage = store.create_outage_incident(
            {
                'outage_id': 'outage-test',
                'tenant': 'tenant-test',
                'incident_number': 'OMS-TEST-1',
                'service_points': ('svc-1', 'svc-2'),
                'critical_customers': ({'customer_id': 'hospital-1', 'life_support': True},),
                'storm_mode_active': True,
            }
        )
        trouble = store.record_trouble_call({'outage_id': 'outage-test', 'caller_name': 'Jordan', 'service_point': 'svc-1', 'critical_customer': True})
        interruption = store.create_device_interruption({'outage_id': 'outage-test', 'device_id': 'breaker-11', 'downstream_device_ids': ('xf-1',)})
        crew = store.dispatch_crew({'outage_id': 'outage-test', 'crew_id': 'crew-11', 'eta_minutes': 30})
        switching = store.author_switching_plan({'outage_id': 'outage-test', 'plan_id': 'plan-test', 'device_id': 'switch-11'})
        safety = store.isolate_safety({'outage_id': 'outage-test', 'hazard_type': 'downed_wire', 'device_id': 'switch-11'})
        assessment = store.record_damage_assessment({'outage_id': 'outage-test', 'asset_id': 'pole-11', 'severity': 4})
        etr = store.calculate_etr({'outage_id': 'outage-test', 'crew_eta_minutes': 30})
        nested = store.open_nested_outage({'parent_outage_id': 'outage-test', 'outage_id': 'outage-test-nested', 'incident_number': 'OMS-TEST-1-N'})
        notification = store.send_customer_notification({'outage_id': 'outage-test', 'channel': 'sms', 'critical_customer_priority': True})
        mutual_aid = store.request_mutual_aid({'outage_id': 'outage-test', 'quantity': 2, 'crew_type': 'tree'})
        governed = store.create_governed_assistance_session({'outage_id': 'outage-test', 'tenant': 'tenant-test', 'goal': 'Recommend storm switching order'})
        storm = store.activate_storm_mode({'outage_id': 'outage-test'})
        verification = store.verify_restoration({'outage_id': 'outage-test', 'verified_by': 'field-supervisor'})
        regulatory = store.compute_regulatory_indices('tenant-test')
        timeline = store.build_timeline('outage-test')
        workbench = store.build_workbench('tenant-test')
        assert all(item['ok'] is True for item in (projection, outage, trouble, interruption, crew, switching, safety, assessment, etr, nested, notification, mutual_aid, governed, storm, verification, regulatory, timeline, workbench))
        assert workbench['critical_customer_queue']
        assert workbench['storm_mode_active'] is True
        assert workbench['nested_outage_count'] >= 1
        assert timeline['event_count'] >= 6
        assert workbench['outbox_count'] >= 5
    finally:
        store.close()


def test_standalone_service_routes_ui_agent_and_release_surface():
    service = services.UtilityOutageRestorationStandaloneService()
    try:
        projection = routes.dispatch_standalone_route(
            'POST',
            '/app/utility-outage-restoration/network-assets',
            {'projection_id': 'asset-route', 'tenant': 'tenant-route', 'asset_id': 'feeder-route'},
            service=service,
        )
        outage = routes.dispatch_standalone_route(
            'POST',
            '/app/utility-outage-restoration/outages',
            {'outage_id': 'outage-route', 'tenant': 'tenant-route', 'incident_number': 'OMS-ROUTE-2', 'critical_customers': ({'customer_id': 'water-plant'},)},
            service=service,
        )
        workbench = routes.dispatch_standalone_route(
            'GET',
            '/app/utility-outage-restoration/workbench',
            {'tenant': 'tenant-route'},
            service=service,
        )
        rendered = ui.utility_outage_restoration_render_standalone_workbench(workbench['result']['result'])
        document_plan = agent.document_instruction_plan('storm damage packet', 'dispatch crew, notify critical customers, and prepare regulatory snapshot')
        crud_plan = agent.datastore_crud_plan('create', 'utility_outage_restoration_outage_incident', {'outage_id': 'outage-route'})
        app_contract = standalone.utility_outage_restoration_standalone_app_contract()
        smoke = standalone.utility_outage_restoration_standalone_app_smoke()
        evidence = release_evidence.build_release_evidence()
        assert projection['ok'] is True
        assert outage['ok'] is True
        assert workbench['ok'] is True
        assert rendered['ok'] is True
        assert app_contract['ok'] is True
        assert smoke['ok'] is True
        assert document_plan['wizard_candidates']
        assert crud_plan['route_candidates']
        assert evidence['documentation']['ok'] is True
        assert evidence['standalone_app']['ok'] is True
        assert evidence['standalone_smoke']['ok'] is True
    finally:
        service.close()


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ('README.md', 'implementation-plan.md', 'implementation-status.md', 'RELEASE_EVIDENCE.md', 'standalone.py'):
        assert (base / name).exists() is True

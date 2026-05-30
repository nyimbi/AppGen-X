"""Standalone one-PBC app composition for the utility_outage_restoration package."""
from __future__ import annotations

from .agent import standalone_agent_workspace_contract
from .models import UtilityOutageRestorationStandaloneStore, standalone_model_contract, standalone_store_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts, standalone_route_smoke_test
from .services import UtilityOutageRestorationStandaloneService, standalone_service_operation_contracts, standalone_service_smoke_test
from .ui import utility_outage_restoration_render_standalone_workbench, utility_outage_restoration_standalone_workbench_blueprint


def utility_outage_restoration_standalone_app_contract() -> dict:
    models = standalone_model_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    ui = utility_outage_restoration_standalone_workbench_blueprint()
    agent = standalone_agent_workspace_contract()
    return {
        'format': 'appgen.utility-outage-restoration-standalone-app.v1',
        'ok': all(item.get('ok') is True for item in (models, services, routes, ui, agent)),
        'pbc': 'utility_outage_restoration',
        'models': models,
        'services': services,
        'routes': routes,
        'ui': ui,
        'agent': agent,
        'side_effects': (),
    }


def utility_outage_restoration_bootstrap_standalone_app(database_path: str = ':memory:') -> dict:
    store = UtilityOutageRestorationStandaloneStore(database_path=database_path)
    service = UtilityOutageRestorationStandaloneService(store)
    return {
        'ok': True,
        'pbc': 'utility_outage_restoration',
        'store': store,
        'service': service,
        'contract': utility_outage_restoration_standalone_app_contract(),
        'side_effects': (),
    }


def utility_outage_restoration_standalone_app_smoke() -> dict:
    bundle = utility_outage_restoration_bootstrap_standalone_app()
    service = bundle['service']
    try:
        projection = dispatch_standalone_route('POST', '/app/utility-outage-restoration/network-assets', {'projection_id': 'asset-app', 'tenant': 'tenant-app', 'asset_id': 'feeder-app'}, service=service)
        outage = dispatch_standalone_route('POST', '/app/utility-outage-restoration/outages', {'outage_id': 'outage-app', 'tenant': 'tenant-app', 'incident_number': 'OMS-APP-1', 'critical_customers': ({'customer_id': 'hospital-app'},), 'storm_mode_active': True}, service=service)
        trouble = dispatch_standalone_route('POST', '/app/utility-outage-restoration/trouble-calls', {'outage_id': 'outage-app', 'caller_name': 'App Customer', 'service_point': 'svc-app', 'critical_customer': True}, service=service)
        crew = dispatch_standalone_route('POST', '/app/utility-outage-restoration/crew-dispatch', {'outage_id': 'outage-app', 'crew_id': 'crew-app', 'eta_minutes': 20}, service=service)
        switching = dispatch_standalone_route('POST', '/app/utility-outage-restoration/switching-plan', {'outage_id': 'outage-app', 'plan_id': 'plan-app', 'device_id': 'switch-app'}, service=service)
        safety = dispatch_standalone_route('POST', '/app/utility-outage-restoration/safety-isolations', {'outage_id': 'outage-app', 'hazard_type': 'downed_wire', 'device_id': 'switch-app'}, service=service)
        assessment = dispatch_standalone_route('POST', '/app/utility-outage-restoration/damage-assessments', {'outage_id': 'outage-app', 'asset_id': 'pole-app', 'severity': 4}, service=service)
        etr = dispatch_standalone_route('POST', '/app/utility-outage-restoration/etr', {'outage_id': 'outage-app', 'crew_eta_minutes': 20}, service=service)
        nested = dispatch_standalone_route('POST', '/app/utility-outage-restoration/nested-outages', {'parent_outage_id': 'outage-app', 'outage_id': 'outage-app-nested', 'incident_number': 'OMS-APP-1-N'}, service=service)
        notification = dispatch_standalone_route('POST', '/app/utility-outage-restoration/customer-notifications', {'outage_id': 'outage-app', 'critical_customer_priority': True}, service=service)
        mutual_aid = dispatch_standalone_route('POST', '/app/utility-outage-restoration/mutual-aid', {'outage_id': 'outage-app', 'quantity': 1}, service=service)
        governed = dispatch_standalone_route('POST', '/app/utility-outage-restoration/governed-assistance', {'outage_id': 'outage-app', 'tenant': 'tenant-app', 'goal': 'Prepare storm mode switching plan'}, service=service)
        storm = dispatch_standalone_route('POST', '/app/utility-outage-restoration/storm-mode', {'outage_id': 'outage-app'}, service=service)
        verification = dispatch_standalone_route('POST', '/app/utility-outage-restoration/restoration-verification', {'outage_id': 'outage-app', 'verified_by': 'dispatcher'}, service=service)
        workbench = dispatch_standalone_route('GET', '/app/utility-outage-restoration/workbench', {'tenant': 'tenant-app'}, service=service)
        rendered = utility_outage_restoration_render_standalone_workbench(workbench['result']['result'])
        regulatory = dispatch_standalone_route('GET', '/app/utility-outage-restoration/regulatory-indices', {'tenant': 'tenant-app'}, service=service)
        timeline = dispatch_standalone_route('GET', '/app/utility-outage-restoration/timeline', {'outage_id': 'outage-app'}, service=service)
        inbound = dispatch_standalone_route('POST', '/app/utility-outage-restoration/events/inbox', {'event_type': 'PolicyChanged', 'idempotency_key': 'policy-app', 'policy_id': 'storm'}, service=service)
        return {
            'ok': bundle['contract']['ok'] and standalone_store_smoke_test()['ok'] and standalone_service_smoke_test()['ok'] and standalone_route_smoke_test()['ok'] and all(item['ok'] for item in (projection, outage, trouble, crew, switching, safety, assessment, etr, nested, notification, mutual_aid, governed, storm, verification, workbench, rendered, regulatory, timeline, inbound)),
            'contract': bundle['contract'],
            'workbench': workbench,
            'rendered': rendered,
            'regulatory': regulatory,
            'timeline': timeline,
            'side_effects': (),
        }
    finally:
        service.close()

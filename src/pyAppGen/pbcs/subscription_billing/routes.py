"""API route contracts for the subscription_billing PBC."""

from .services import SubscriptionBillingService, service_operation_contracts


ROUTES = ({'method': 'POST', 'path': '/api/pbc/subscription_billing/subscriptions', 'handler': 'command_subscriptions', 'permission': 'subscription_billing.command.1'}, {'method': 'POST', 'path': '/api/pbc/subscription_billing/usage', 'handler': 'command_usage', 'permission': 'subscription_billing.command.2'}, {'method': 'POST', 'path': '/api/pbc/subscription_billing/renewals', 'handler': 'command_renewals', 'permission': 'subscription_billing.command.3'}, {'method': 'GET', 'path': '/api/pbc/subscription_billing/subscription-billing-workbench', 'handler': 'query_subscription_billing_workbench', 'permission': 'subscription_billing.query.4'})

ROUTES = ROUTES + (
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/trials', 'handler': 'command_trials', 'permission': 'subscription_billing.subscription'},
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/change-orders', 'handler': 'command_change_orders', 'permission': 'subscription_billing.subscription'},
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/cancellations', 'handler': 'command_cancellations', 'permission': 'subscription_billing.subscription'},
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/addons', 'handler': 'command_addons', 'permission': 'subscription_billing.subscription'},
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/credit-memos', 'handler': 'command_credit_memos', 'permission': 'subscription_billing.invoice'},
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/payment-applications', 'handler': 'command_payment_applications', 'permission': 'subscription_billing.invoice'},
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/entitlements', 'handler': 'command_entitlements', 'permission': 'subscription_billing.entitlement'},
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/revenue-recognition', 'handler': 'command_revenue', 'permission': 'subscription_billing.revenue'},
    {'method': 'POST', 'path': '/api/pbc/subscription_billing/billing-exceptions', 'handler': 'command_billing_exceptions', 'permission': 'subscription_billing.audit'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/subscription_billing/subscriptions', 'handler': 'command_subscriptions', 'permission': 'subscription_billing.command.1', 'operation': 'command_subscriptions', 'operation_kind': 'command', 'owned_tables': ('subscription_billing_subscription', 'subscription_billing_usage_meter', 'subscription_billing_billing_schedule', 'subscription_billing_dunning_notice'), 'read_tables': (), 'emitted_event': 'SubscriptionRenewed', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'subscription_billing:command_subscriptions:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/subscription_billing/usage', 'handler': 'command_usage', 'permission': 'subscription_billing.command.2', 'operation': 'command_usage', 'operation_kind': 'command', 'owned_tables': ('subscription_billing_subscription', 'subscription_billing_usage_meter', 'subscription_billing_billing_schedule', 'subscription_billing_dunning_notice'), 'read_tables': (), 'emitted_event': 'UsageRated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'subscription_billing:command_usage:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/subscription_billing/renewals', 'handler': 'command_renewals', 'permission': 'subscription_billing.command.3', 'operation': 'command_renewals', 'operation_kind': 'command', 'owned_tables': ('subscription_billing_subscription', 'subscription_billing_usage_meter', 'subscription_billing_billing_schedule', 'subscription_billing_dunning_notice'), 'read_tables': (), 'emitted_event': 'InvoiceApproved', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'subscription_billing:command_renewals:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/subscription_billing/subscription-billing-workbench', 'handler': 'query_subscription_billing_workbench', 'permission': 'subscription_billing.query.4', 'operation': 'query_subscription_billing_workbench', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('subscription_billing_subscription', 'subscription_billing_usage_meter', 'subscription_billing_billing_schedule', 'subscription_billing_dunning_notice'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})

API_ROUTE_CONTRACTS = API_ROUTE_CONTRACTS + tuple(
    {
        'method': item['method'],
        'path': item['path'],
        'handler': item['operation'],
        'permission': item['permission'],
        'operation': item['operation'],
        'operation_kind': item['operation_kind'],
        'owned_tables': item['owned_tables'],
        'read_tables': item['read_tables'],
        'emitted_event': item['emitted_event'],
        'event_contract': item['event_contract'],
        'transaction_boundary': item['transaction_boundary'],
        'idempotency_required': True,
        'idempotency_key': f"subscription_billing:{item['operation']}:idempotency_key",
        'shared_table_access': False,
        'stream_engine_picker_visible': False,
    }
    for item in service_operation_contracts()['contracts']
    if item['operation'].startswith('command_')
    and item['operation'] not in {'command_subscriptions', 'command_usage', 'command_renewals'}
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts():
    """Return executable API route contracts with policy and boundary evidence."""
    service_contracts = service_operation_contracts()['contracts']
    operation_index = {item['operation']: item for item in service_contracts}
    contracts = tuple(
        {
            **contract,
            'service_operation': operation_index.get(contract['operation']),
            'route_id': f"{contract['method']} {contract['path']}",
        }
        for contract in API_ROUTE_CONTRACTS
    )
    return {
        'ok': bool(contracts)
        and all(item['event_contract'] == 'AppGen-X' for item in contracts)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in contracts)
        and all(item['stream_engine_picker_visible'] is False for item in contracts)
        and all(item['shared_table_access'] is False for item in contracts),
        'pbc': 'subscription_billing',
        'contracts': contracts,
        'routes': tuple(item['route_id'] for item in contracts),
        'side_effects': (),
    }


def validate_api_route_contracts():
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
    manifest = api_route_contracts()
    contracts = manifest['contracts']
    service_mismatches = tuple(
        item['route_id']
        for item in contracts
        if not item['service_operation']
        or item['service_operation']['method'] != item['method']
        or item['service_operation']['path'] != item['path']
        or item['service_operation']['permission'] != item['permission']
    )
    missing_idempotency = tuple(
        item['route_id']
        for item in contracts
        if item['idempotency_required'] and not item['idempotency_key']
    )
    invalid_table_scope = tuple(
        item['route_id']
        for item in contracts
        for table in item['owned_tables'] + item['read_tables']
        if not table.startswith('subscription_billing_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'subscription_billing',
        'contracts': contracts,
        'service_mismatches': service_mismatches,
        'missing_idempotency': missing_idempotency,
        'invalid_table_scope': invalid_table_scope,
        'side_effects': (),
    }


def dispatch_route(method, path, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    route = next(
        (item for item in ROUTES if item['method'] == method and item['path'] == path),
        None,
    )
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found'}
    service = SubscriptionBillingService()
    handler = getattr(service, route['handler'])
    result = handler(payload or {})
    return {
        'ok': result.get('ok') is True,
        'handled': True,
        'route': route,
        'result': result,
        'side_effects': (),
    }


def smoke_test():
    """Execute the first route and validate the API contract surface."""
    validation = validate_api_route_contracts()
    if not ROUTES:
        return {'ok': False, 'reason': 'no_routes'}
    first = ROUTES[0]
    dispatched = dispatch_route(first['method'], first['path'], {'smoke': True})
    return {
        'ok': validation['ok'] and dispatched['ok'],
        'validation': validation,
        'dispatch': dispatched,
        'side_effects': (),
    }



STANDALONE_ROUTES = (
    {'method':'POST','path':'/app/subscription-billing/demo-workspace','handler':'seed_demo_workspace','permission':'subscription_billing.configure'},
    {'method':'GET','path':'/app/subscription-billing/workbench','handler':'build_workbench','permission':'subscription_billing.audit'},
    {'method':'POST','path':'/app/subscription-billing/subscriptions','handler':'create_subscription','permission':'subscription_billing.subscription'},
    {'method':'POST','path':'/app/subscription-billing/usage','handler':'record_usage','permission':'subscription_billing.usage'},
    {'method':'POST','path':'/app/subscription-billing/invoices','handler':'generate_invoice','permission':'subscription_billing.invoice'},
    {'method':'POST','path':'/app/subscription-billing/payment-applications','handler':'apply_payment_to_invoice','permission':'subscription_billing.invoice'},
    {'method':'POST','path':'/app/subscription-billing/assistant/sessions','handler':'run_agent_skill','permission':'subscription_billing.audit'},
)

def standalone_route_contracts():
    from .services import standalone_service_operation_contracts
    indexed={i['operation']:i for i in standalone_service_operation_contracts()['contracts']}
    contracts=tuple({**r,'operation':r['handler'],'service_operation':indexed[r['handler']],'owned_tables':indexed[r['handler']]['owned_tables'],'read_tables':indexed[r['handler']]['read_tables'],'emitted_event':indexed[r['handler']]['emitted_event'],'event_contract':'AppGen-X','stream_engine_picker_visible':False,'shared_table_access':False,'route_id':f"{r['method']} {r['path']}"} for r in STANDALONE_ROUTES)
    return {'format':'appgen.subscription-billing-standalone-routes.v1','ok':bool(contracts) and all(i['event_contract']=='AppGen-X' for i in contracts) and all(i['shared_table_access'] is False for i in contracts),'pbc':'subscription_billing','routes':tuple(i['route_id'] for i in contracts),'contracts':contracts,'side_effects':()}

def dispatch_standalone_route(method,path,payload=None,*,service=None):
    from .services import SubscriptionBillingStandaloneService
    route=next((i for i in STANDALONE_ROUTES if i['method']==method and i['path']==path),None)
    if route is None: return {'ok':False,'handled':False,'reason':'route_not_found','side_effects':()}
    owned=service is None
    if service is None: service=SubscriptionBillingStandaloneService()
    p=dict(payload or {})
    try:
        h=route['handler']
        if h=='seed_demo_workspace': result=service.seed_demo_workspace(tenant=p.get('tenant','tenant_demo'))
        elif h=='build_workbench': result=service.build_workbench(tenant=p.get('tenant','tenant_demo'))
        elif h=='create_subscription': result=service.create_subscription(p,tenant=p.get('tenant','tenant_demo'))
        elif h=='record_usage': result=service.record_usage(p,tenant=p.get('tenant','tenant_demo'))
        elif h=='generate_invoice': result=service.generate_invoice(p['subscription_id'],p['period'],tenant=p.get('tenant','tenant_demo'))
        elif h=='apply_payment_to_invoice': result=service.apply_payment_to_invoice(p['invoice_id'],p['payment_event_id'],p['amount'],tenant=p.get('tenant','tenant_demo'))
        else: result=service.run_agent_skill(p,tenant=p.get('tenant','tenant_demo'))
        return {'ok':result.get('ok') is True,'handled':True,'route':route,'result':result,'side_effects':()}
    finally:
        if owned: service.close()

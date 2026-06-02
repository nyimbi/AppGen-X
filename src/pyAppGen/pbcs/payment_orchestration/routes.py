"""API route contracts for the payment_orchestration PBC."""

from .services import PaymentOrchestrationService, service_operation_contracts


ROUTES = ({'method': 'POST', 'path': '/api/pbc/payment_orchestration/payment-intents', 'handler': 'command_payment_intents', 'permission': 'payment_orchestration.command.1'}, {'method': 'POST', 'path': '/api/pbc/payment_orchestration/gateway-routes', 'handler': 'command_gateway_routes', 'permission': 'payment_orchestration.command.2'}, {'method': 'POST', 'path': '/api/pbc/payment_orchestration/tokens', 'handler': 'command_tokens', 'permission': 'payment_orchestration.command.3'}, {'method': 'GET', 'path': '/api/pbc/payment_orchestration/payment-orchestration-workbench', 'handler': 'query_payment_orchestration_workbench', 'permission': 'payment_orchestration.query.4'})

ROUTES = ROUTES + (
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/authorizations', 'handler': 'command_authorizations', 'permission': 'payment_orchestration.capture'},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/captures', 'handler': 'command_captures', 'permission': 'payment_orchestration.capture'},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/settlements', 'handler': 'command_settlements', 'permission': 'payment_orchestration.settlement'},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/payouts', 'handler': 'command_payouts', 'permission': 'payment_orchestration.settlement'},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/refunds', 'handler': 'command_refunds', 'permission': 'payment_orchestration.refund'},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/disputes', 'handler': 'command_disputes', 'permission': 'payment_orchestration.dispute'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/payment_orchestration/payment-intents', 'handler': 'command_payment_intents', 'permission': 'payment_orchestration.command.1', 'operation': 'command_payment_intents', 'operation_kind': 'command', 'owned_tables': ('payment_orchestration_payment_gateway', 'payment_orchestration_payment_intent', 'payment_orchestration_payment_token', 'payment_orchestration_fraud_check'), 'read_tables': (), 'emitted_event': 'PaymentCaptured', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'payment_orchestration:command_payment_intents:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/payment_orchestration/gateway-routes', 'handler': 'command_gateway_routes', 'permission': 'payment_orchestration.command.2', 'operation': 'command_gateway_routes', 'operation_kind': 'command', 'owned_tables': ('payment_orchestration_payment_gateway', 'payment_orchestration_payment_intent', 'payment_orchestration_payment_token', 'payment_orchestration_fraud_check'), 'read_tables': (), 'emitted_event': 'PaymentFailed', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'payment_orchestration:command_gateway_routes:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/payment_orchestration/tokens', 'handler': 'command_tokens', 'permission': 'payment_orchestration.command.3', 'operation': 'command_tokens', 'operation_kind': 'command', 'owned_tables': ('payment_orchestration_payment_gateway', 'payment_orchestration_payment_intent', 'payment_orchestration_payment_token', 'payment_orchestration_fraud_check'), 'read_tables': (), 'emitted_event': 'FraudCheckRequested', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'payment_orchestration:command_tokens:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/payment_orchestration/payment-orchestration-workbench', 'handler': 'query_payment_orchestration_workbench', 'permission': 'payment_orchestration.query.4', 'operation': 'query_payment_orchestration_workbench', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('payment_orchestration_payment_gateway', 'payment_orchestration_payment_intent', 'payment_orchestration_payment_token', 'payment_orchestration_fraud_check'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})

API_ROUTE_CONTRACTS = API_ROUTE_CONTRACTS + (
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/authorizations', 'handler': 'command_authorizations', 'permission': 'payment_orchestration.capture', 'operation': 'command_authorizations', 'operation_kind': 'command', 'owned_tables': ('payment_orchestration_payment_authorization', 'payment_orchestration_payment_intent'), 'read_tables': (), 'emitted_event': 'PaymentAuthorized', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'payment_orchestration:command_authorizations:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/captures', 'handler': 'command_captures', 'permission': 'payment_orchestration.capture', 'operation': 'command_captures', 'operation_kind': 'command', 'owned_tables': ('payment_orchestration_payment_authorization', 'payment_orchestration_payment_capture', 'payment_orchestration_payment_settlement'), 'read_tables': (), 'emitted_event': 'PaymentCaptured', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'payment_orchestration:command_captures:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/settlements', 'handler': 'command_settlements', 'permission': 'payment_orchestration.settlement', 'operation': 'command_settlements', 'operation_kind': 'command', 'owned_tables': ('payment_orchestration_payment_settlement', 'payment_orchestration_payment_reconciliation_handoff'), 'read_tables': (), 'emitted_event': 'PaymentSettled', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'payment_orchestration:command_settlements:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/payouts', 'handler': 'command_payouts', 'permission': 'payment_orchestration.settlement', 'operation': 'command_payouts', 'operation_kind': 'command', 'owned_tables': ('payment_orchestration_payment_payout',), 'read_tables': (), 'emitted_event': 'PaymentPayoutScheduled', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'payment_orchestration:command_payouts:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/refunds', 'handler': 'command_refunds', 'permission': 'payment_orchestration.refund', 'operation': 'command_refunds', 'operation_kind': 'command', 'owned_tables': ('payment_orchestration_payment_refund', 'payment_orchestration_payment_reconciliation_handoff'), 'read_tables': (), 'emitted_event': 'PaymentRefunded', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'payment_orchestration:command_refunds:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False},
    {'method': 'POST', 'path': '/api/pbc/payment_orchestration/disputes', 'handler': 'command_disputes', 'permission': 'payment_orchestration.dispute', 'operation': 'command_disputes', 'operation_kind': 'command', 'owned_tables': ('payment_orchestration_payment_dispute', 'payment_orchestration_payment_reconciliation_handoff'), 'read_tables': (), 'emitted_event': 'PaymentDisputeResolved', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'payment_orchestration:command_disputes:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False},
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
        'pbc': 'payment_orchestration',
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
        if not table.startswith('payment_orchestration_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'payment_orchestration',
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
    service = PaymentOrchestrationService()
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
    {'method':'POST','path':'/app/payment-orchestration/demo-workspace','handler':'seed_demo_workspace','permission':'payment_orchestration.configure'},
    {'method':'GET','path':'/app/payment-orchestration/workbench','handler':'build_workbench','permission':'payment_orchestration.audit'},
    {'method':'POST','path':'/app/payment-orchestration/intents','handler':'create_payment_intent','permission':'payment_orchestration.intent'},
    {'method':'POST','path':'/app/payment-orchestration/captures','handler':'capture_payment','permission':'payment_orchestration.capture'},
    {'method':'POST','path':'/app/payment-orchestration/settlements','handler':'settle_payment','permission':'payment_orchestration.settlement'},
    {'method':'POST','path':'/app/payment-orchestration/refunds','handler':'refund_payment','permission':'payment_orchestration.refund'},
    {'method':'POST','path':'/app/payment-orchestration/disputes','handler':'open_dispute','permission':'payment_orchestration.dispute'},
    {'method':'POST','path':'/app/payment-orchestration/proofs','handler':'generate_payment_proof','permission':'payment_orchestration.audit'},
    {'method':'POST','path':'/app/payment-orchestration/assistant/sessions','handler':'run_agent_skill','permission':'payment_orchestration.audit'},
)

def standalone_route_contracts():
    from .services import standalone_service_operation_contracts
    indexed={i['operation']:i for i in standalone_service_operation_contracts()['contracts']}
    contracts=tuple({**r,'operation':r['handler'],'service_operation':indexed[r['handler']],'owned_tables':indexed[r['handler']]['owned_tables'],'read_tables':indexed[r['handler']]['read_tables'],'emitted_event':indexed[r['handler']]['emitted_event'],'event_contract':'AppGen-X','stream_engine_picker_visible':False,'shared_table_access':False,'route_id':f"{r['method']} {r['path']}"} for r in STANDALONE_ROUTES)
    return {'format':'appgen.payment-orchestration-standalone-routes.v1','ok':bool(contracts) and all(i['event_contract']=='AppGen-X' for i in contracts) and all(i['shared_table_access'] is False for i in contracts),'pbc':'payment_orchestration','routes':tuple(i['route_id'] for i in contracts),'contracts':contracts,'side_effects':()}

def dispatch_standalone_route(method,path,payload=None,*,service=None):
    from .services import PaymentOrchestrationStandaloneService
    route=next((i for i in STANDALONE_ROUTES if i['method']==method and i['path']==path),None)
    if route is None: return {'ok':False,'handled':False,'reason':'route_not_found','side_effects':()}
    owned=service is None
    if service is None: service=PaymentOrchestrationStandaloneService()
    p=dict(payload or {})
    try:
        h=route['handler']
        if h=='seed_demo_workspace': result=service.seed_demo_workspace(tenant=p.get('tenant','tenant_demo'))
        elif h=='build_workbench': result=service.build_workbench(tenant=p.get('tenant','tenant_demo'))
        elif h=='create_payment_intent': result=service.create_payment_intent(p,tenant=p.get('tenant','tenant_demo'))
        elif h=='capture_payment': result=service.capture_payment(p['intent_id'],p['amount'],tenant=p.get('tenant','tenant_demo'))
        elif h=='settle_payment': result=service.settle_payment(p['intent_id'],p['settlement_reference'],tenant=p.get('tenant','tenant_demo'))
        elif h=='refund_payment': result=service.refund_payment(p['intent_id'],p['amount'],p['reason'],tenant=p.get('tenant','tenant_demo'))
        elif h=='open_dispute': result=service.open_dispute(p['intent_id'],p['amount'],p['reason'],p.get('evidence',()),tenant=p.get('tenant','tenant_demo'))
        elif h=='generate_payment_proof': result=service.generate_payment_proof(p['intent_id'],p.get('disclosure',('intent_id','amount','currency','status')),tenant=p.get('tenant','tenant_demo'))
        else: result=service.run_agent_skill(p,tenant=p.get('tenant','tenant_demo'))
        return {'ok':result.get('ok') is True,'handled':True,'route':route,'result':result,'side_effects':()}
    finally:
        if owned: service.close()

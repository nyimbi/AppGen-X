"""API route contracts for the cross_border_trade PBC."""

from .services import CrossBorderTradeService, service_operation_contracts


ROUTES = ({'method': 'POST', 'path': '/api/pbc/cross_border_trade/landed-cost', 'handler': 'command_landed_cost', 'permission': 'cross_border_trade.command.1'}, {'method': 'POST', 'path': '/api/pbc/cross_border_trade/export-checks', 'handler': 'command_export_checks', 'permission': 'cross_border_trade.command.2'}, {'method': 'POST', 'path': '/api/pbc/cross_border_trade/declarations', 'handler': 'command_declarations', 'permission': 'cross_border_trade.command.3'}, {'method': 'GET', 'path': '/api/pbc/cross_border_trade/cross-border-trade-workbench', 'handler': 'query_cross_border_trade_workbench', 'permission': 'cross_border_trade.query.4'})

ROUTES = ROUTES + (
    {'method': 'POST', 'path': '/api/pbc/cross_border_trade/denied-party-screenings', 'handler': 'command_denied_party_screenings', 'permission': 'cross_border_trade.screen'},
    {'method': 'POST', 'path': '/api/pbc/cross_border_trade/document-packets', 'handler': 'command_document_packets', 'permission': 'cross_border_trade.declare'},
    {'method': 'POST', 'path': '/api/pbc/cross_border_trade/broker-handoffs', 'handler': 'command_broker_handoffs', 'permission': 'cross_border_trade.declare'},
    {'method': 'POST', 'path': '/api/pbc/cross_border_trade/carrier-handoffs', 'handler': 'command_carrier_handoffs', 'permission': 'cross_border_trade.declare'},
    {'method': 'POST', 'path': '/api/pbc/cross_border_trade/compliance-holds', 'handler': 'command_compliance_holds', 'permission': 'cross_border_trade.declare'},
    {'method': 'POST', 'path': '/api/pbc/cross_border_trade/compliance-holds/resolve', 'handler': 'command_hold_resolutions', 'permission': 'cross_border_trade.declare'},
    {'method': 'POST', 'path': '/api/pbc/cross_border_trade/country-restriction-policies', 'handler': 'command_country_restrictions', 'permission': 'cross_border_trade.configure'},
    {'method': 'POST', 'path': '/api/pbc/cross_border_trade/declaration-releases', 'handler': 'command_declaration_releases', 'permission': 'cross_border_trade.declare'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/cross_border_trade/landed-cost', 'handler': 'command_landed_cost', 'permission': 'cross_border_trade.command.1', 'operation': 'command_landed_cost', 'operation_kind': 'command', 'owned_tables': ('cross_border_trade_hs_classification', 'cross_border_trade_landed_cost_quote', 'cross_border_trade_export_control_check', 'cross_border_trade_customs_declaration'), 'read_tables': (), 'emitted_event': 'CustomsDeclarationPrepared', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'cross_border_trade:command_landed_cost:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/cross_border_trade/export-checks', 'handler': 'command_export_checks', 'permission': 'cross_border_trade.command.2', 'operation': 'command_export_checks', 'operation_kind': 'command', 'owned_tables': ('cross_border_trade_hs_classification', 'cross_border_trade_landed_cost_quote', 'cross_border_trade_export_control_check', 'cross_border_trade_customs_declaration'), 'read_tables': (), 'emitted_event': 'LandedCostCalculated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'cross_border_trade:command_export_checks:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/cross_border_trade/declarations', 'handler': 'command_declarations', 'permission': 'cross_border_trade.command.3', 'operation': 'command_declarations', 'operation_kind': 'command', 'owned_tables': ('cross_border_trade_hs_classification', 'cross_border_trade_landed_cost_quote', 'cross_border_trade_export_control_check', 'cross_border_trade_customs_declaration'), 'read_tables': (), 'emitted_event': 'CustomsDeclarationPrepared', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'cross_border_trade:command_declarations:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/cross_border_trade/cross-border-trade-workbench', 'handler': 'query_cross_border_trade_workbench', 'permission': 'cross_border_trade.query.4', 'operation': 'query_cross_border_trade_workbench', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('cross_border_trade_hs_classification', 'cross_border_trade_landed_cost_quote', 'cross_border_trade_export_control_check', 'cross_border_trade_customs_declaration'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})

API_ROUTE_CONTRACTS = API_ROUTE_CONTRACTS + tuple(
    {
        **contract,
        'idempotency_required': True,
        'idempotency_key': f"cross_border_trade:{contract['operation']}:idempotency_key",
        'shared_table_access': False,
        'stream_engine_picker_visible': False,
    }
    for contract in service_operation_contracts()['contracts']
    if contract['operation'] not in {item['operation'] for item in API_ROUTE_CONTRACTS}
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
        'pbc': 'cross_border_trade',
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
        if not table.startswith('cross_border_trade_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'cross_border_trade',
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
    service = CrossBorderTradeService()
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

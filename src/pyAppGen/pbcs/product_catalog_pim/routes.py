"""API route contracts for the product_catalog_pim PBC."""

from .services import ProductCatalogPimService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/product_catalog_pim/products', 'handler': 'command_products', 'permission': 'product_catalog_pim.command.1'},
    {'method': 'GET', 'path': '/api/pbc/product_catalog_pim/product-read-models', 'handler': 'query_product_read_models', 'permission': 'product_catalog_pim.query.2'},
    {'method': 'POST', 'path': '/api/pbc/product_catalog_pim/prices', 'handler': 'command_prices', 'permission': 'product_catalog_pim.command.3'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/product_catalog_pim/products', 'handler': 'command_products', 'permission': 'product_catalog_pim.command.1', 'operation': 'command_products', 'operation_kind': 'command', 'owned_tables': ('product_catalog_pim_product', 'product_catalog_pim_product_price', 'product_catalog_pim_product_media', 'product_catalog_pim_product_attribute'), 'read_tables': (), 'emitted_event': 'ProductClassified', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'product_catalog_pim:command_products:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/product_catalog_pim/product-read-models', 'handler': 'query_product_read_models', 'permission': 'product_catalog_pim.query.2', 'operation': 'query_product_read_models', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('product_catalog_pim_product', 'product_catalog_pim_product_price', 'product_catalog_pim_product_media', 'product_catalog_pim_product_attribute'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/product_catalog_pim/prices', 'handler': 'command_prices', 'permission': 'product_catalog_pim.command.3', 'operation': 'command_prices', 'operation_kind': 'command', 'owned_tables': ('product_catalog_pim_product', 'product_catalog_pim_product_price', 'product_catalog_pim_product_media', 'product_catalog_pim_product_attribute'), 'read_tables': (), 'emitted_event': 'ForecastUpdated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'product_catalog_pim:command_prices:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'product_catalog_pim',
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
        if not table.startswith('product_catalog_pim_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'product_catalog_pim',
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
    service = ProductCatalogPimService()
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


STANDALONE_ROUTES=(
    {'method':'POST','path':'/app/product-catalog-pim/demo-workspace','handler':'seed_demo_workspace'},
    {'method':'GET','path':'/app/product-catalog-pim/workbench','handler':'build_workbench'},
    {'method':'POST','path':'/app/product-catalog-pim/products','handler':'register_product'},
    {'method':'POST','path':'/app/product-catalog-pim/content','handler':'add_localized_content'},
    {'method':'POST','path':'/app/product-catalog-pim/publications','handler':'publish_product'},
    {'method':'POST','path':'/app/product-catalog-pim/publication-proofs','handler':'generate_publication_proof'},)

def standalone_route_contracts():
    from .services import standalone_service_operation_contracts
    ops={i['operation']:i for i in standalone_service_operation_contracts()['contracts']}; contracts=tuple({**r,'operation':r['handler'],'service_operation':ops.get(r['handler'])} for r in STANDALONE_ROUTES)
    return {'format':'appgen.product-catalog-pim-standalone-routes.v1','ok':all(i['service_operation'] for i in contracts),'pbc':'product_catalog_pim','routes':tuple(f"{i['method']} {i['path']}" for i in contracts),'contracts':contracts,'side_effects':()}

def dispatch_standalone_route(method,path,payload=None,*,service=None):
    from .services import ProductCatalogPimStandaloneService
    route=next((i for i in STANDALONE_ROUTES if i['method']==method and i['path']==path),None)
    if route is None: return {'ok':False,'handled':False,'reason':'route_not_found','side_effects':()}
    own=service is None; service=service or ProductCatalogPimStandaloneService(); data=dict(payload or {})
    try:
        if route['handler']=='seed_demo_workspace': result=service.seed_demo_workspace(tenant=data.get('tenant','tenant_demo'))
        elif route['handler']=='build_workbench': result=service.build_workbench(tenant=data.get('tenant','tenant_demo'))
        elif route['handler']=='register_product': result=service.register_product(data.get('tenant','tenant_demo'),data)
        elif route['handler']=='add_localized_content': result=service.add_localized_content(data.get('tenant','tenant_demo'),data)
        elif route['handler']=='publish_product': result=service.publish_product(data.get('tenant','tenant_demo'),data['product_id'],tuple(data.get('channels',('web',))),tuple(data.get('locales',('en-US',))),data.get('published_by','catalog_manager_1'))
        elif route['handler']=='generate_publication_proof': result=service.generate_publication_proof(data.get('tenant','tenant_demo'),data['product_id'],tuple(data.get('disclosure',('product_id','sku','lifecycle_state','completeness'))))
        else: result={'ok':False,'reason':'handler_not_implemented'}
        return {'ok':result.get('ok') is True,'handled':True,'route':route,'result':{'ok':result.get('ok') is True,'result':result},'side_effects':()}
    finally:
        if own: service.close()

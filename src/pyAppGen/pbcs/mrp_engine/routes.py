"""API route contracts for the mrp_engine PBC."""

from .services import MrpEngineService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/boms', 'handler': 'command_mrp_boms', 'permission': 'mrp_engine.command.1'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/demand-projections', 'handler': 'command_mrp_demand_projections', 'permission': 'mrp_engine.command.2'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/inventory-projections', 'handler': 'command_mrp_inventory_projections', 'permission': 'mrp_engine.command.3'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/runs', 'handler': 'command_mrp_runs', 'permission': 'mrp_engine.command.4'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/runs/{id}/calculate', 'handler': 'command_mrp_runs_id_calculate', 'permission': 'mrp_engine.command.5'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/planned-orders/{id}/release', 'handler': 'command_mrp_planned_orders_id_release', 'permission': 'mrp_engine.command.6'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/events/inbox', 'handler': 'command_mrp_events_inbox', 'permission': 'mrp_engine.command.7'},
    {'method': 'GET', 'path': '/api/pbc/mrp_engine/mrp/workbench', 'handler': 'query_mrp_workbench', 'permission': 'mrp_engine.query.8'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/boms', 'handler': 'command_mrp_boms', 'permission': 'mrp_engine.command.1', 'operation': 'command_mrp_boms', 'operation_kind': 'command', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'BomRegistered', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'mrp_engine:command_mrp_boms:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/demand-projections', 'handler': 'command_mrp_demand_projections', 'permission': 'mrp_engine.command.2', 'operation': 'command_mrp_demand_projections', 'operation_kind': 'command', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'DemandProjectionIngested', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'mrp_engine:command_mrp_demand_projections:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/inventory-projections', 'handler': 'command_mrp_inventory_projections', 'permission': 'mrp_engine.command.3', 'operation': 'command_mrp_inventory_projections', 'operation_kind': 'command', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'InventoryProjectionIngested', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'mrp_engine:command_mrp_inventory_projections:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/runs', 'handler': 'command_mrp_runs', 'permission': 'mrp_engine.command.4', 'operation': 'command_mrp_runs', 'operation_kind': 'command', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'MrpRunStarted', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'mrp_engine:command_mrp_runs:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/runs/{id}/calculate', 'handler': 'command_mrp_runs_id_calculate', 'permission': 'mrp_engine.command.5', 'operation': 'command_mrp_runs_id_calculate', 'operation_kind': 'command', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'MaterialShortageDetected', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'mrp_engine:command_mrp_runs_id_calculate:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/planned-orders/{id}/release', 'handler': 'command_mrp_planned_orders_id_release', 'permission': 'mrp_engine.command.6', 'operation': 'command_mrp_planned_orders_id_release', 'operation_kind': 'command', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'PlannedOrderReleased', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'mrp_engine:command_mrp_planned_orders_id_release:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/events/inbox', 'handler': 'command_mrp_events_inbox', 'permission': 'mrp_engine.command.7', 'operation': 'command_mrp_events_inbox', 'operation_kind': 'command', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'BomRegistered', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'mrp_engine:command_mrp_events_inbox:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/mrp_engine/mrp/workbench', 'handler': 'query_mrp_workbench', 'permission': 'mrp_engine.query.8', 'operation': 'query_mrp_workbench', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'mrp_engine',
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
        if not table.startswith('mrp_engine_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'mrp_engine',
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
    service = MrpEngineService()
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

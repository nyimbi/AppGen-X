"""Standalone one-PBC app composition for the restaurant_operations package."""
from __future__ import annotations

from .agent import standalone_agent_workspace_contract
from .models import RestaurantOperationsStandaloneStore, standalone_model_contract, standalone_store_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import RestaurantOperationsStandaloneService, standalone_service_operation_contracts
from .ui import restaurant_operations_render_standalone_workbench, restaurant_operations_standalone_workbench_blueprint


def restaurant_operations_standalone_app_contract() -> dict:
    models = standalone_model_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    ui = restaurant_operations_standalone_workbench_blueprint()
    agent = standalone_agent_workspace_contract()
    return {
        'format': 'appgen.restaurant-operations-standalone-app.v1',
        'ok': all(item.get('ok') is True for item in (models, services, routes, ui, agent)),
        'pbc': 'restaurant_operations',
        'models': models,
        'services': services,
        'routes': routes,
        'ui': ui,
        'agent': agent,
        'side_effects': (),
    }


def restaurant_operations_bootstrap_standalone_app(database_label: str = 'package-local-memory') -> dict:
    store = RestaurantOperationsStandaloneStore(database_label=database_label)
    service = RestaurantOperationsStandaloneService(store)
    return {
        'ok': True,
        'pbc': 'restaurant_operations',
        'store': store,
        'service': service,
        'contract': restaurant_operations_standalone_app_contract(),
        'side_effects': (),
    }


def restaurant_operations_standalone_app_smoke() -> dict:
    bundle = restaurant_operations_bootstrap_standalone_app()
    service = bundle['service']
    try:
        create_menu = dispatch_standalone_route('POST', '/app/restaurant-operations/menu', {'tenant': 'tenant-standalone', 'menu_item_id': 'shrimp-pasta', 'name': 'Shrimp Pasta', 'base_price': 24.0, 'allergens': ('shellfish', 'gluten'), 'modifier_groups': ({'group': 'protein', 'choices': ('shrimp', 'salmon')},)}, service=service)
        record_recipe = dispatch_standalone_route('POST', '/app/restaurant-operations/recipes', {'tenant': 'tenant-standalone', 'recipe_id': 'shrimp-pasta-recipe', 'menu_item_id': 'shrimp-pasta', 'ingredients': ({'ingredient': 'shrimp', 'quantity': 1, 'unit_cost': 8.0}, {'ingredient': 'pasta', 'quantity': 1, 'unit_cost': 2.5}), 'target_yield': 1}, service=service)
        floor_plan = dispatch_standalone_route('POST', '/app/restaurant-operations/floor-plan', {'tenant': 'tenant-standalone', 'floor_plan_id': 'main', 'tables': ({'table_id': 'T10', 'seats': 4}, {'table_id': 'T11', 'seats': 2})}, service=service)
        reservation = dispatch_standalone_route('POST', '/app/restaurant-operations/reservations', {'tenant': 'tenant-standalone', 'reservation_id': 'res-standalone', 'guest_name': 'Jordan', 'covers': 2, 'floor_plan_id': 'main', 'customer_notes': ('VIP',)}, service=service)
        shift = dispatch_standalone_route('POST', '/app/restaurant-operations/shifts', {'tenant': 'tenant-standalone', 'shift_id': 'shift-standalone', 'scheduled_staff': ({'name': 'Sam', 'role': 'server', 'hours': 8}, {'name': 'Kai', 'role': 'chef', 'hours': 8}), 'readiness_checks': ('station_ready', 'labels_complete')}, service=service)
        prep = dispatch_standalone_route('POST', '/app/restaurant-operations/prep', {'tenant': 'tenant-standalone', 'prep_id': 'prep-standalone', 'station': 'saute', 'par_levels': {'shrimp-pasta': 12}, 'projected_batches': ({'batch_id': 'batch-standalone', 'quantity': 6},), 'ingredients': ({'ingredient': 'shrimp', 'quantity': 12}, {'ingredient': 'pasta', 'quantity': 12})}, service=service)
        order = dispatch_standalone_route('POST', '/app/restaurant-operations/orders', {'tenant': 'tenant-standalone', 'order_id': 'order-standalone', 'channel': 'takeout', 'provider': 'direct', 'items': ({'menu_item_id': 'shrimp-pasta', 'quantity': 2, 'selected_modifiers': ({'name': 'salmon swap', 'price_delta': 4.0},)},), 'guest_count': 2}, service=service)
        kds = dispatch_standalone_route('POST', '/app/restaurant-operations/orders/advance', {'order_id': 'order-standalone', 'next_state': 'firing'}, service=service)
        settlement = dispatch_standalone_route('POST', '/app/restaurant-operations/checks/settle', {'order_id': 'order-standalone', 'splits': ({'seat': 'all', 'amount': 56.0, 'tip': 8.0},), 'tenders': ({'type': 'card', 'amount': 64.0},), 'comps': ({'reason': 'hospitality', 'amount': 4.0},)}, service=service)
        receiving = dispatch_standalone_route('POST', '/app/restaurant-operations/vendor-receipts', {'tenant': 'tenant-standalone', 'receipt_id': 'receipt-standalone', 'vendor': 'Dock Market', 'line_items': ({'ingredient': 'shrimp', 'quantity': 20}, {'ingredient': 'pasta', 'quantity': 20})}, service=service)
        safety = dispatch_standalone_route('POST', '/app/restaurant-operations/safety', {'tenant': 'tenant-standalone', 'log_id': 'safe-standalone', 'station': 'saute', 'check_type': 'holding_temp', 'status': 'pass', 'reading': 63}, service=service)
        incident = dispatch_standalone_route('POST', '/app/restaurant-operations/incidents', {'tenant': 'tenant-standalone', 'incident_id': 'incident-standalone', 'guest_name': 'Jordan', 'severity': 'medium', 'summary': 'takeout delay'}, service=service)
        loyalty = dispatch_standalone_route('POST', '/app/restaurant-operations/loyalty-notes', {'tenant': 'tenant-standalone', 'note_id': 'note-standalone', 'customer_id': 'jord-1', 'loyalty_tier': 'platinum', 'note': 'offer dessert on next visit'}, service=service)
        preview = dispatch_standalone_route('POST', '/app/restaurant-operations/governed-previews', {'tenant': 'tenant-standalone', 'preview_id': 'preview-standalone', 'document': 'Update reservation allergy note and menu modifiers', 'instruction': 'prepare governed CRUD preview'}, service=service)
        workbench = dispatch_standalone_route('GET', '/app/restaurant-operations/workbench', {'tenant': 'tenant-standalone'}, service=service)
        rendered = restaurant_operations_render_standalone_workbench(workbench['result']['result'])
        revenue = dispatch_standalone_route('GET', '/app/restaurant-operations/revenue', {'tenant': 'tenant-standalone'}, service=service)
        governed = dispatch_standalone_route('GET', '/app/restaurant-operations/governed-previews', {'tenant': 'tenant-standalone'}, service=service)
        return {
            'ok': bundle['contract']['ok'] and standalone_store_smoke_test()['ok'] and create_menu['ok'] and record_recipe['ok'] and floor_plan['ok'] and reservation['ok'] and shift['ok'] and prep['ok'] and order['ok'] and kds['ok'] and settlement['ok'] and receiving['ok'] and safety['ok'] and incident['ok'] and loyalty['ok'] and preview['ok'] and workbench['ok'] and rendered['ok'] and revenue['ok'] and governed['ok'],
            'contract': bundle['contract'],
            'workbench': workbench,
            'rendered': rendered,
            'revenue': revenue,
            'governed': governed,
            'side_effects': (),
        }
    finally:
        service.close()

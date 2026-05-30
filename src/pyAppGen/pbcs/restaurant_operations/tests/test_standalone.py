from pyAppGen.pbcs.restaurant_operations.routes import dispatch_standalone_route
from pyAppGen.pbcs.restaurant_operations.services import RestaurantOperationsStandaloneService
from pyAppGen.pbcs.restaurant_operations.standalone import restaurant_operations_bootstrap_standalone_app, restaurant_operations_standalone_app_smoke
from pyAppGen.pbcs.restaurant_operations.ui import restaurant_operations_render_standalone_workbench


def _seed_service(service: RestaurantOperationsStandaloneService) -> None:
    dispatch_standalone_route('POST', '/app/restaurant-operations/menu', {'tenant': 'tenant-standalone-test', 'menu_item_id': 'short-rib', 'name': 'Short Rib', 'base_price': 32.0, 'allergens': ('soy',), 'modifier_groups': ({'group': 'sides', 'choices': ('fries', 'greens')},)}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/recipes', {'tenant': 'tenant-standalone-test', 'recipe_id': 'short-rib-recipe', 'menu_item_id': 'short-rib', 'ingredients': ({'ingredient': 'short_rib', 'quantity': 1, 'unit_cost': 12.0}, {'ingredient': 'sauce', 'quantity': 1, 'unit_cost': 2.0}), 'target_yield': 1}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/floor-plan', {'tenant': 'tenant-standalone-test', 'floor_plan_id': 'main', 'tables': ({'table_id': 'B1', 'seats': 4}, {'table_id': 'B2', 'seats': 2})}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/reservations', {'tenant': 'tenant-standalone-test', 'reservation_id': 'res-1', 'guest_name': 'Priya', 'covers': 4, 'floor_plan_id': 'main', 'customer_notes': ('allergy note',), 'loyalty_tier': 'gold'}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/shifts', {'tenant': 'tenant-standalone-test', 'shift_id': 'shift-1', 'scheduled_staff': ({'name': 'Alex', 'role': 'server', 'hours': 8}, {'name': 'Jo', 'role': 'cook', 'hours': 8}), 'readiness_checks': ('stations_open', 'labels_complete')}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/prep', {'tenant': 'tenant-standalone-test', 'prep_id': 'prep-1', 'station': 'grill', 'par_levels': {'short-rib': 10}, 'projected_batches': ({'batch_id': 'batch-1', 'quantity': 5},), 'ingredients': ({'ingredient': 'short_rib', 'quantity': 10},)}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/orders', {'tenant': 'tenant-standalone-test', 'order_id': 'ord-1', 'channel': 'delivery', 'provider': 'house', 'items': ({'menu_item_id': 'short-rib', 'quantity': 2, 'selected_modifiers': ({'name': 'greens', 'price_delta': 3.0},)},), 'guest_count': 2}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/orders/advance', {'order_id': 'ord-1', 'next_state': 'acknowledged'}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/orders/advance', {'order_id': 'ord-1', 'next_state': 'plated'}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/checks/settle', {'order_id': 'ord-1', 'splits': ({'seat': 'all', 'amount': 70.0, 'tip': 10.0},), 'tenders': ({'type': 'card', 'amount': 80.0},), 'comps': ({'reason': 'vip recovery', 'amount': 5.0},), 'voids': ({'reason': 'remake fries', 'amount': 2.0},)}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/vendor-receipts', {'tenant': 'tenant-standalone-test', 'receipt_id': 'rcv-1', 'vendor': 'Prime Foods', 'line_items': ({'ingredient': 'short_rib', 'quantity': 25}, {'ingredient': 'sauce', 'quantity': 25})}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/safety', {'tenant': 'tenant-standalone-test', 'log_id': 'safe-1', 'station': 'grill', 'check_type': 'cooling', 'status': 'alert', 'reading': 50, 'corrective_action': 'discard'}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/incidents', {'tenant': 'tenant-standalone-test', 'incident_id': 'inc-1', 'guest_name': 'Priya', 'severity': 'high', 'summary': 'allergy concern'}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/loyalty-notes', {'tenant': 'tenant-standalone-test', 'note_id': 'note-1', 'customer_id': 'cust-1', 'loyalty_tier': 'gold', 'note': 'recover with appetiser credit', 'service_recovery_credit': 10.0}, service=service)
    dispatch_standalone_route('POST', '/app/restaurant-operations/governed-previews', {'tenant': 'tenant-standalone-test', 'preview_id': 'preview-1', 'document': 'Adjust reservation allergy note and menu modifier', 'instruction': 'show governed preview'}, service=service)


def test_restaurant_operations_standalone_workbench_and_analytics():
    bundle = restaurant_operations_bootstrap_standalone_app()
    service = bundle['service']
    try:
        _seed_service(service)
        workbench = dispatch_standalone_route('GET', '/app/restaurant-operations/workbench', {'tenant': 'tenant-standalone-test'}, service=service)
        rendered = restaurant_operations_render_standalone_workbench(workbench['result']['result'])
        revenue = dispatch_standalone_route('GET', '/app/restaurant-operations/revenue', {'tenant': 'tenant-standalone-test'}, service=service)
        kds = dispatch_standalone_route('GET', '/app/restaurant-operations/kitchen-display', {'tenant': 'tenant-standalone-test'}, service=service)
        previews = dispatch_standalone_route('GET', '/app/restaurant-operations/governed-previews', {'tenant': 'tenant-standalone-test'}, service=service)
        assert workbench['ok'] is True
        assert rendered['ok'] is True
        assert revenue['result']['result']['metrics']['net_sales'] == 63.0
        assert revenue['result']['result']['metrics']['tips'] == 10.0
        assert 'plated' in kds['result']['result']['lanes']
        assert previews['result']['result']['previews'][0]['requires_human_confirmation'] is True
        assert workbench['result']['result']['inventory_on_hand']['short_rib'] == 25.0
        assert len(workbench['result']['result']['depletion_requests']) >= 2
    finally:
        service.close()


def test_restaurant_operations_standalone_smoke_bundle():
    smoke = restaurant_operations_standalone_app_smoke()
    assert smoke['ok'] is True
    assert smoke['revenue']['result']['result']['metrics']['net_sales'] > 0

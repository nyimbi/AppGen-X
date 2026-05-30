"""Service layer for the restaurant_operations PBC."""
from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
import hashlib

from .domain_depth import (
    DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS,
    DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES,
    execute_domain_operation as execute_domain_depth_operation,
)
from .events import EMITTED as EMITTED_EVENTS
from .models import RestaurantOperationsStandaloneStore, standalone_model_contract

PBC_KEY = 'restaurant_operations'
EVENT_CONTRACT = {
    'outbox_table': f'{PBC_KEY}_appgen_outbox_event',
    'inbox_table': f'{PBC_KEY}_appgen_inbox_event',
    'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
    'event_contract': 'AppGen-X',
}
COMMAND_OPERATIONS = tuple(dict.fromkeys(('command_menu_item', 'configure_runtime', 'set_parameter', 'register_rule') + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)))
QUERY_OPERATIONS = ('query_workbench',)
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES
TICKET_STATES = ('queued', 'acknowledged', 'firing', 'held', 'plated', 'expo_ready', 'handed_off', 'closed')
_STANDALONE_QUERY_MAP = {
    'get_workbench': 'restaurant_operations_service_shift_plan',
    'get_kitchen_display': 'restaurant_operations_order_ticket',
    'get_floor_plan': 'restaurant_operations_floor_plan',
    'get_revenue_analytics': 'restaurant_operations_check_settlement',
    'list_governed_previews': 'restaurant_operations_governed_preview',
}

STANDALONE_OPERATION_CONTRACTS = (
    {'operation': 'create_menu_profile', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/menu', 'handler': 'create_menu_profile', 'permission': 'restaurant_operations.create', 'table': 'restaurant_operations_menu_catalog', 'form': 'MenuEngineeringForm', 'wizard': 'MenuEngineeringWizard', 'emitted_event': 'RestaurantOperationsCreated'},
    {'operation': 'record_recipe_cost', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/recipes', 'handler': 'record_recipe_cost', 'permission': 'restaurant_operations.create', 'table': 'restaurant_operations_recipe_cost_card', 'form': 'RecipeCostCardForm', 'wizard': 'MenuEngineeringWizard', 'emitted_event': 'RestaurantOperationsUpdated'},
    {'operation': 'configure_floor_plan', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/floor-plan', 'handler': 'configure_floor_plan', 'permission': 'restaurant_operations.update', 'table': 'restaurant_operations_floor_plan', 'form': 'FloorPlanDesignerForm', 'wizard': 'ReservationFlowWizard', 'emitted_event': 'RestaurantOperationsUpdated'},
    {'operation': 'book_reservation', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/reservations', 'handler': 'book_reservation', 'permission': 'restaurant_operations.create', 'table': 'restaurant_operations_reservation_waitlist', 'form': 'ReservationWaitlistForm', 'wizard': 'ReservationFlowWizard', 'emitted_event': 'RestaurantOperationsApproved'},
    {'operation': 'open_service_shift', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/shifts', 'handler': 'open_service_shift', 'permission': 'restaurant_operations.update', 'table': 'restaurant_operations_service_shift_plan', 'form': 'ShiftLaunchForm', 'wizard': 'ServiceLaunchWizard', 'emitted_event': 'RestaurantOperationsApproved'},
    {'operation': 'record_prep_plan', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/prep', 'handler': 'record_prep_plan', 'permission': 'restaurant_operations.update', 'table': 'restaurant_operations_inventory_station', 'form': 'PrepParLevelForm', 'wizard': 'ServiceLaunchWizard', 'emitted_event': 'RestaurantOperationsUpdated'},
    {'operation': 'open_order', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/orders', 'handler': 'open_order', 'permission': 'restaurant_operations.create', 'table': 'restaurant_operations_order_ticket', 'form': 'OrderLifecycleForm', 'wizard': 'DeliveryTakeoutWizard', 'emitted_event': 'RestaurantOperationsCreated'},
    {'operation': 'advance_order_lifecycle', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/orders/advance', 'handler': 'advance_order_lifecycle', 'permission': 'restaurant_operations.update', 'table': 'restaurant_operations_order_ticket', 'form': 'OrderLifecycleForm', 'wizard': 'ServiceLaunchWizard', 'emitted_event': 'RestaurantOperationsUpdated'},
    {'operation': 'settle_guest_check', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/checks/settle', 'handler': 'settle_guest_check', 'permission': 'restaurant_operations.approve', 'table': 'restaurant_operations_check_settlement', 'form': 'CheckSettlementForm', 'wizard': 'DiningRoomRecoveryWizard', 'emitted_event': 'RestaurantOperationsApproved'},
    {'operation': 'receive_vendor_delivery', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/vendor-receipts', 'handler': 'receive_vendor_delivery', 'permission': 'restaurant_operations.update', 'table': 'restaurant_operations_vendor_receipt', 'form': 'VendorReceivingForm', 'wizard': 'ServiceLaunchWizard', 'emitted_event': 'RestaurantOperationsUpdated'},
    {'operation': 'log_safety_check', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/safety', 'handler': 'log_safety_check', 'permission': 'restaurant_operations.update', 'table': 'restaurant_operations_safety_log', 'form': 'SafetyLogForm', 'wizard': 'ServiceLaunchWizard', 'emitted_event': 'RestaurantOperationsExceptionOpened'},
    {'operation': 'record_guest_incident', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/incidents', 'handler': 'record_guest_incident', 'permission': 'restaurant_operations.update', 'table': 'restaurant_operations_guest_incident', 'form': 'GuestIncidentForm', 'wizard': 'DiningRoomRecoveryWizard', 'emitted_event': 'RestaurantOperationsExceptionOpened'},
    {'operation': 'capture_loyalty_note', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/loyalty-notes', 'handler': 'capture_loyalty_note', 'permission': 'restaurant_operations.update', 'table': 'restaurant_operations_loyalty_note', 'form': 'LoyaltyGuestNoteForm', 'wizard': 'DiningRoomRecoveryWizard', 'emitted_event': 'RestaurantOperationsUpdated'},
    {'operation': 'preview_governed_document', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/restaurant-operations/governed-previews', 'handler': 'preview_governed_document', 'permission': 'restaurant_operations.approve', 'table': 'restaurant_operations_governed_preview', 'form': 'GovernedPreviewForm', 'wizard': 'GovernedInstructionWizard', 'emitted_event': 'RestaurantOperationsApproved'},
    {'operation': 'get_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/app/restaurant-operations/workbench', 'handler': 'get_workbench', 'permission': 'restaurant_operations.read', 'table': 'restaurant_operations_service_shift_plan', 'form': None, 'wizard': None, 'emitted_event': None},
    {'operation': 'get_kitchen_display', 'operation_kind': 'query', 'method': 'GET', 'path': '/app/restaurant-operations/kitchen-display', 'handler': 'get_kitchen_display', 'permission': 'restaurant_operations.read', 'table': 'restaurant_operations_order_ticket', 'form': None, 'wizard': None, 'emitted_event': None},
    {'operation': 'get_floor_plan', 'operation_kind': 'query', 'method': 'GET', 'path': '/app/restaurant-operations/floor-plan', 'handler': 'get_floor_plan', 'permission': 'restaurant_operations.read', 'table': 'restaurant_operations_floor_plan', 'form': None, 'wizard': None, 'emitted_event': None},
    {'operation': 'get_revenue_analytics', 'operation_kind': 'query', 'method': 'GET', 'path': '/app/restaurant-operations/revenue', 'handler': 'get_revenue_analytics', 'permission': 'restaurant_operations.read', 'table': 'restaurant_operations_check_settlement', 'form': None, 'wizard': None, 'emitted_event': None},
    {'operation': 'list_governed_previews', 'operation_kind': 'query', 'method': 'GET', 'path': '/app/restaurant-operations/governed-previews', 'handler': 'list_governed_previews', 'permission': 'restaurant_operations.read', 'table': 'restaurant_operations_governed_preview', 'form': None, 'wizard': None, 'emitted_event': None},
)


def _operation_contract(name, kind):
    return {
        'operation': name,
        'operation_kind': kind,
        'owned_tables': OWNED_TABLES[:2] if kind == 'command' else (),
        'read_tables': OWNED_TABLES[:2] if kind == 'query' else (),
        'emitted_event': EMITTED_EVENTS[0] if kind == 'command' else None,
        'transaction_boundary': 'owned_datastore_plus_outbox' if kind == 'command' else 'read_only_projection',
    }


def _utcnow() -> str:
    return datetime.now(UTC).isoformat()


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


class RestaurantOperationsService:
    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            plan = execute_domain_depth_operation(name, payload)
            return {
                'ok': plan['ok'],
                'operation': name,
                'operation_kind': 'command',
                'read_only': False,
                'payload': dict(payload),
                'operation_contract': {
                    'operation': name,
                    'operation_kind': 'command',
                    'owned_tables': plan.get('owned_tables', ()),
                    'read_tables': (),
                    'emitted_event': plan.get('emitted_event'),
                    'transaction_boundary': 'owned_datastore_plus_outbox',
                },
                'outbox_table': EVENT_CONTRACT['outbox_table'],
                'emits': (plan.get('emitted_event'),),
                'transaction_boundary': 'owned_datastore_plus_outbox',
                'domain_depth': plan,
                'side_effects': (),
            }
        contract = _operation_contract(name, 'command')
        return {
            'ok': True,
            'operation': name,
            'operation_kind': 'command',
            'read_only': False,
            'payload': dict(payload),
            'operation_contract': contract,
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (contract['emitted_event'],),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'side_effects': (),
        }

    def _query(self, name, payload):
        contract = _operation_contract(name, 'query')
        return {
            'ok': True,
            'operation': name,
            'operation_kind': 'query',
            'read_only': True,
            'payload': dict(payload),
            'operation_contract': contract,
            'outbox_table': None,
            'emits': (),
            'side_effects': (),
        }


def service_operation_manifest():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'service_class': 'RestaurantOperationsService',
        'command_operations': COMMAND_OPERATIONS,
        'query_operations': QUERY_OPERATIONS,
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def service_operation_contracts():
    contracts = tuple(_operation_contract(name, 'command') for name in COMMAND_OPERATIONS) + tuple(_operation_contract(name, 'query') for name in QUERY_OPERATIONS)
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'contracts': contracts,
        'operation_contract': contracts[0],
        'side_effects': (),
    }


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = 'query' if operation in manifest['query_operations'] else 'command'
    return {
        'ok': operation in manifest['query_operations'] + manifest['command_operations'],
        'operation': operation,
        'operation_kind': kind,
        'payload': dict(payload or {}),
        'side_effects': (),
    }


def _ensure_tuple(items):
    if not items:
        return ()
    return tuple(items)


def _sum_amount(values) -> float:
    return round(sum(float(value) for value in values), 2)


class RestaurantOperationsStandaloneService:
    """Executable one-PBC workflow surface for restaurant operations."""

    def __init__(self, store: RestaurantOperationsStandaloneStore | None = None) -> None:
        self.store = store or RestaurantOperationsStandaloneStore()

    def close(self) -> None:
        self.store.close()

    def _contract(self, name: str) -> dict:
        contract = next(item for item in STANDALONE_OPERATION_CONTRACTS if item['operation'] == name)
        table = contract['table']
        return {
            **contract,
            'owned_tables': (table,) if contract['operation_kind'] == 'command' else (),
            'read_tables': () if contract['operation_kind'] == 'command' else (table,),
            'transaction_boundary': 'owned_datastore_plus_outbox' if contract['operation_kind'] == 'command' else 'read_only_projection',
            'event_contract': 'AppGen-X',
            'stream_engine_picker_visible': False,
        }

    def _emit(self, event_type: str, payload: dict, *, source_operation: str) -> dict:
        event = {
            'event_id': _digest((source_operation, payload, len(self.store.state['outbox']))),
            'event_type': event_type,
            'occurred_at': _utcnow(),
            'topic': 'pbc.restaurant_operations.events',
            'payload': deepcopy(payload),
            'source_operation': source_operation,
            'event_contract': 'AppGen-X',
        }
        self.store.append_event('outbox', event)
        return event

    def _respond(self, name: str, payload: dict, result: dict, *, read_only: bool) -> dict:
        contract = self._contract(name)
        emitted_event = result.get('emitted_event')
        return {
            'ok': result.get('ok', True),
            'pbc': PBC_KEY,
            'operation': name,
            'operation_kind': contract['operation_kind'],
            'read_only': read_only,
            'payload': deepcopy(payload),
            'result': result,
            'operation_contract': contract,
            'outbox_table': None if read_only else EVENT_CONTRACT['outbox_table'],
            'emits': () if read_only or emitted_event is None else (emitted_event,),
            'transaction_boundary': contract['transaction_boundary'],
            'side_effects': (),
        }

    def create_menu_profile(self, payload=None):
        payload = dict(payload or {})
        menu_item_id = payload.get('menu_item_id') or payload.get('code') or f"menu-{len(self.store.state['menu_items']) + 1}"
        price = round(float(payload.get('base_price', 0.0)), 2)
        modifiers = tuple(
            {
                'group': group.get('group'),
                'required': bool(group.get('required', False)),
                'choices': tuple(group.get('choices', ())),
                'max_select': int(group.get('max_select', len(group.get('choices', ()) or (1,)))),
            }
            for group in payload.get('modifier_groups', ())
        )
        record = {
            'menu_item_id': menu_item_id,
            'tenant': payload.get('tenant', 'default'),
            'name': payload.get('name', menu_item_id),
            'status': payload.get('status', 'active'),
            'base_price': price,
            'dayparts': tuple(payload.get('dayparts', ('dinner',))),
            'channels': tuple(payload.get('channels', ('dine_in', 'takeout'))),
            'modifiers': modifiers,
            'allergens': tuple(payload.get('allergens', ())),
            'dietary_flags': tuple(payload.get('dietary_flags', ())),
            'recipe_id': payload.get('recipe_id'),
            'course': payload.get('course', 'entree'),
            'loyalty_eligible': bool(payload.get('loyalty_eligible', True)),
        }
        stored = self.store.save('menu_items', menu_item_id, record)
        event = self._emit('RestaurantOperationsCreated', {'menu_item_id': menu_item_id, 'tenant': stored['tenant']}, source_operation='create_menu_profile')
        return self._respond('create_menu_profile', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def record_recipe_cost(self, payload=None):
        payload = dict(payload or {})
        recipe_id = payload.get('recipe_id') or f"recipe-{len(self.store.state['recipes']) + 1}"
        ingredients = tuple(payload.get('ingredients', ()))
        total_cost = round(sum(float(item.get('unit_cost', 0.0)) * float(item.get('quantity', 0.0)) for item in ingredients), 2)
        target_yield = max(float(payload.get('target_yield', 1.0)), 1.0)
        record = {
            'recipe_id': recipe_id,
            'tenant': payload.get('tenant', 'default'),
            'name': payload.get('name', recipe_id),
            'menu_item_id': payload.get('menu_item_id'),
            'ingredients': ingredients,
            'target_yield': target_yield,
            'portion_cost': round(total_cost / target_yield, 2),
            'theoretical_cost': total_cost,
            'cross_contact_controls': tuple(payload.get('cross_contact_controls', ())),
        }
        stored = self.store.save('recipes', recipe_id, record)
        event = self._emit('RestaurantOperationsUpdated', {'recipe_id': recipe_id, 'menu_item_id': stored.get('menu_item_id')}, source_operation='record_recipe_cost')
        return self._respond('record_recipe_cost', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def configure_floor_plan(self, payload=None):
        payload = dict(payload or {})
        floor_plan_id = payload.get('floor_plan_id') or f"floor-{len(self.store.state['floor_plans']) + 1}"
        tables = tuple(
            {
                'table_id': table.get('table_id'),
                'seats': int(table.get('seats', 2)),
                'zone': table.get('zone', 'main'),
                'status': table.get('status', 'open'),
            }
            for table in payload.get('tables', ())
        )
        record = {
            'floor_plan_id': floor_plan_id,
            'tenant': payload.get('tenant', 'default'),
            'room': payload.get('room', 'main-dining'),
            'tables': tables,
            'service_mode': payload.get('service_mode', 'full_service'),
            'seat_count': sum(table['seats'] for table in tables),
        }
        stored = self.store.save('floor_plans', floor_plan_id, record)
        event = self._emit('RestaurantOperationsUpdated', {'floor_plan_id': floor_plan_id, 'seat_count': stored['seat_count']}, source_operation='configure_floor_plan')
        return self._respond('configure_floor_plan', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def book_reservation(self, payload=None):
        payload = dict(payload or {})
        reservation_id = payload.get('reservation_id') or f"reservation-{len(self.store.state['reservations']) + 1}"
        tenant = payload.get('tenant', 'default')
        floor_plan_id = payload.get('floor_plan_id')
        floor_plan = self.store.fetch('floor_plans', floor_plan_id) if floor_plan_id else None
        available_seats = floor_plan['seat_count'] if floor_plan else 0
        covers = int(payload.get('covers', 2))
        waitlist_requested = bool(payload.get('waitlist_requested', False))
        status = 'waitlist' if waitlist_requested or (available_seats and covers > available_seats) else 'confirmed'
        record = {
            'reservation_id': reservation_id,
            'tenant': tenant,
            'guest_name': payload.get('guest_name', 'Walk-in Guest'),
            'covers': covers,
            'requested_at': payload.get('requested_at', _utcnow()),
            'reservation_time': payload.get('reservation_time', _utcnow()),
            'status': status,
            'waitlist_position': int(payload.get('waitlist_position', len(self.store.state['reservations']) + 1 if status == 'waitlist' else 0)),
            'table_assignment': payload.get('table_assignment'),
            'floor_plan_id': floor_plan_id,
            'customer_notes': tuple(payload.get('customer_notes', ())),
            'loyalty_tier': payload.get('loyalty_tier', 'standard'),
            'delivery_takeout_preference': payload.get('delivery_takeout_preference', 'dine_in'),
        }
        stored = self.store.save('reservations', reservation_id, record)
        event_type = 'RestaurantOperationsExceptionOpened' if status == 'waitlist' else 'RestaurantOperationsApproved'
        event = self._emit(event_type, {'reservation_id': reservation_id, 'status': status, 'tenant': tenant}, source_operation='book_reservation')
        return self._respond('book_reservation', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def open_service_shift(self, payload=None):
        payload = dict(payload or {})
        shift_id = payload.get('shift_id') or f"shift-{len(self.store.state['shifts']) + 1}"
        scheduled_staff = tuple(payload.get('scheduled_staff', ()))
        record = {
            'shift_id': shift_id,
            'tenant': payload.get('tenant', 'default'),
            'service_date': payload.get('service_date', _utcnow()[:10]),
            'station': payload.get('station', 'front-of-house'),
            'scheduled_staff': scheduled_staff,
            'labor_hours': round(sum(float(member.get('hours', 0.0)) for member in scheduled_staff), 2),
            'readiness_checks': tuple(payload.get('readiness_checks', ())),
            'status': payload.get('status', 'open'),
        }
        stored = self.store.save('shifts', shift_id, record)
        event = self._emit('RestaurantOperationsApproved', {'shift_id': shift_id, 'labor_hours': stored['labor_hours']}, source_operation='open_service_shift')
        return self._respond('open_service_shift', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def record_prep_plan(self, payload=None):
        payload = dict(payload or {})
        prep_id = payload.get('prep_id') or f"prep-{len(self.store.state['prep_plans']) + 1}"
        ingredients = tuple(payload.get('ingredients', ()))
        projected_batches = tuple(payload.get('projected_batches', ()))
        record = {
            'prep_id': prep_id,
            'tenant': payload.get('tenant', 'default'),
            'station': payload.get('station', 'line-1'),
            'par_levels': dict(payload.get('par_levels', {})),
            'projected_batches': projected_batches,
            'ingredients': ingredients,
            'approved_by': payload.get('approved_by', 'manager'),
            'depletion_policy': payload.get('depletion_policy', 'recipe-driven'),
        }
        stored = self.store.save('prep_plans', prep_id, record)
        event = self._emit('RestaurantOperationsUpdated', {'prep_id': prep_id, 'station': stored['station']}, source_operation='record_prep_plan')
        return self._respond('record_prep_plan', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def _menu_by_id(self, menu_item_id: str | None) -> dict | None:
        if not menu_item_id:
            return None
        return self.store.fetch('menu_items', menu_item_id)

    def _recipe_for_menu(self, menu_item_id: str | None, recipe_id: str | None = None) -> dict | None:
        if recipe_id:
            return self.store.fetch('recipes', recipe_id)
        if not menu_item_id:
            return None
        for recipe in self.store.state['recipes'].values():
            if recipe.get('menu_item_id') == menu_item_id:
                return deepcopy(recipe)
        return None

    def open_order(self, payload=None):
        payload = dict(payload or {})
        order_id = payload.get('order_id') or f"order-{len(self.store.state['orders']) + 1}"
        tenant = payload.get('tenant', 'default')
        items = []
        depletion = []
        for raw_item in payload.get('items', ()):
            item = dict(raw_item)
            menu_item = self._menu_by_id(item.get('menu_item_id'))
            recipe = self._recipe_for_menu(item.get('menu_item_id'), item.get('recipe_id'))
            quantity = int(item.get('quantity', 1))
            base_price = float(item.get('base_price', menu_item.get('base_price', 0.0) if menu_item else 0.0))
            modifier_total = _sum_amount(choice.get('price_delta', 0.0) for choice in item.get('selected_modifiers', ()))
            items.append({
                'menu_item_id': item.get('menu_item_id'),
                'quantity': quantity,
                'course': item.get('course', menu_item.get('course', 'entree') if menu_item else 'entree'),
                'selected_modifiers': tuple(item.get('selected_modifiers', ())),
                'allergens': tuple(item.get('allergens', menu_item.get('allergens', ()) if menu_item else ())),
                'base_price': base_price,
                'modifier_total': modifier_total,
                'line_total': round((base_price + modifier_total) * quantity, 2),
            })
            if recipe:
                for ingredient in recipe.get('ingredients', ()):
                    depletion.append({
                        'ingredient': ingredient.get('ingredient'),
                        'quantity': round(float(ingredient.get('quantity', 0.0)) * quantity, 2),
                        'uom': ingredient.get('uom', 'ea'),
                        'recipe_id': recipe.get('recipe_id'),
                        'order_id': order_id,
                    })
        record = {
            'order_id': order_id,
            'tenant': tenant,
            'channel': payload.get('channel', 'dine_in'),
            'reservation_id': payload.get('reservation_id'),
            'table_assignment': payload.get('table_assignment'),
            'seat_numbers': tuple(payload.get('seat_numbers', ())),
            'guest_count': int(payload.get('guest_count', len(payload.get('seat_numbers', ())) or 1)),
            'items': tuple(items),
            'ticket_state': 'queued',
            'course_status': {'queued': tuple(item['course'] for item in items)},
            'delivery': {
                'provider': payload.get('provider'),
                'promised_time': payload.get('promised_time'),
                'mode': payload.get('channel', 'dine_in'),
            },
            'notes': tuple(payload.get('notes', ())),
            'depletion_requests': tuple(depletion),
        }
        stored = self.store.save('orders', order_id, record)
        self.store.state['depletion_requests'].extend(depletion)
        if stored['channel'] in ('delivery', 'takeout'):
            self.store.save('delivery_orders', order_id, {
                'order_id': order_id,
                'tenant': tenant,
                'channel': stored['channel'],
                'provider': stored['delivery'].get('provider'),
                'promised_time': stored['delivery'].get('promised_time'),
                'handoff_status': 'queued',
            })
        event = self._emit('RestaurantOperationsCreated', {'order_id': order_id, 'channel': stored['channel']}, source_operation='open_order')
        return self._respond('open_order', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def advance_order_lifecycle(self, payload=None):
        payload = dict(payload or {})
        order_id = payload.get('order_id')
        order = self.store.fetch('orders', order_id) if order_id else None
        if not order:
            return self._respond('advance_order_lifecycle', payload, {'ok': False, 'reason': 'order_not_found', 'emitted_event': None}, read_only=False)
        next_state = payload.get('next_state', 'acknowledged')
        if next_state not in TICKET_STATES:
            return self._respond('advance_order_lifecycle', payload, {'ok': False, 'reason': 'invalid_ticket_state', 'emitted_event': None}, read_only=False)
        current_index = TICKET_STATES.index(order['ticket_state'])
        next_index = TICKET_STATES.index(next_state)
        if next_index < current_index and payload.get('override') is not True:
            return self._respond('advance_order_lifecycle', payload, {'ok': False, 'reason': 'out_of_order_transition', 'emitted_event': None}, read_only=False)
        order['ticket_state'] = next_state
        order.setdefault('state_history', []).append({'state': next_state, 'changed_at': _utcnow(), 'actor': payload.get('actor', 'expediter')})
        if next_state == 'handed_off' and order['channel'] in ('delivery', 'takeout'):
            delivery = self.store.fetch('delivery_orders', order_id) or {'order_id': order_id, 'tenant': order['tenant'], 'channel': order['channel']}
            delivery['handoff_status'] = 'handed_off'
            self.store.save('delivery_orders', order_id, delivery)
        stored = self.store.save('orders', order_id, order)
        event_type = 'RestaurantOperationsApproved' if next_state in ('expo_ready', 'handed_off', 'closed') else 'RestaurantOperationsUpdated'
        event = self._emit(event_type, {'order_id': order_id, 'ticket_state': next_state}, source_operation='advance_order_lifecycle')
        return self._respond('advance_order_lifecycle', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def settle_guest_check(self, payload=None):
        payload = dict(payload or {})
        order_id = payload.get('order_id')
        order = self.store.fetch('orders', order_id) if order_id else None
        if not order:
            return self._respond('settle_guest_check', payload, {'ok': False, 'reason': 'order_not_found', 'emitted_event': None}, read_only=False)
        check_id = payload.get('check_id') or f'check-{order_id}'
        subtotal = round(sum(item['line_total'] for item in order['items']), 2)
        comp_total = _sum_amount(entry.get('amount', 0.0) for entry in payload.get('comps', ()))
        void_total = _sum_amount(entry.get('amount', 0.0) for entry in payload.get('voids', ()))
        tip_total = _sum_amount(split.get('tip', 0.0) for split in payload.get('splits', ()))
        tender_total = _sum_amount(tender.get('amount', 0.0) for tender in payload.get('tenders', ()))
        net_sales = round(subtotal - comp_total - void_total, 2)
        record = {
            'check_id': check_id,
            'tenant': order['tenant'],
            'order_id': order_id,
            'subtotal': subtotal,
            'splits': tuple(payload.get('splits', ())),
            'tenders': tuple(payload.get('tenders', ())),
            'tip_total': tip_total,
            'comp_total': comp_total,
            'void_total': void_total,
            'net_sales': net_sales,
            'tender_total': tender_total,
            'balance_due': round(max(net_sales + tip_total - tender_total, 0.0), 2),
            'service_recovery_notes': tuple(payload.get('service_recovery_notes', ())),
        }
        stored = self.store.save('checks', check_id, record)
        event = self._emit('RestaurantOperationsApproved', {'check_id': check_id, 'order_id': order_id, 'net_sales': net_sales}, source_operation='settle_guest_check')
        return self._respond('settle_guest_check', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def receive_vendor_delivery(self, payload=None):
        payload = dict(payload or {})
        receipt_id = payload.get('receipt_id') or f"receipt-{len(self.store.state['vendor_receipts']) + 1}"
        line_items = tuple(payload.get('line_items', ()))
        for item in line_items:
            ingredient = item.get('ingredient')
            current = float(self.store.state['inventory_on_hand'].get(ingredient, 0.0))
            self.store.state['inventory_on_hand'][ingredient] = round(current + float(item.get('quantity', 0.0)), 2)
        record = {
            'receipt_id': receipt_id,
            'tenant': payload.get('tenant', 'default'),
            'vendor': payload.get('vendor', 'primary'),
            'line_items': line_items,
            'received_at': payload.get('received_at', _utcnow()),
            'temperature_checks': tuple(payload.get('temperature_checks', ())),
        }
        stored = self.store.save('vendor_receipts', receipt_id, record)
        event = self._emit('RestaurantOperationsUpdated', {'receipt_id': receipt_id, 'vendor': stored['vendor']}, source_operation='receive_vendor_delivery')
        return self._respond('receive_vendor_delivery', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def log_safety_check(self, payload=None):
        payload = dict(payload or {})
        log_id = payload.get('log_id') or f"safety-{len(self.store.state['safety_logs']) + 1}"
        status = payload.get('status', 'pass')
        record = {
            'log_id': log_id,
            'tenant': payload.get('tenant', 'default'),
            'station': payload.get('station', 'line-1'),
            'check_type': payload.get('check_type', 'temperature'),
            'status': status,
            'reading': payload.get('reading'),
            'corrective_action': payload.get('corrective_action'),
        }
        stored = self.store.save('safety_logs', log_id, record)
        event_type = 'RestaurantOperationsExceptionOpened' if status != 'pass' else 'RestaurantOperationsUpdated'
        event = self._emit(event_type, {'log_id': log_id, 'status': status}, source_operation='log_safety_check')
        return self._respond('log_safety_check', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def record_guest_incident(self, payload=None):
        payload = dict(payload or {})
        incident_id = payload.get('incident_id') or f"incident-{len(self.store.state['incidents']) + 1}"
        record = {
            'incident_id': incident_id,
            'tenant': payload.get('tenant', 'default'),
            'guest_name': payload.get('guest_name', 'unknown'),
            'severity': payload.get('severity', 'medium'),
            'summary': payload.get('summary', 'service incident'),
            'follow_up_owner': payload.get('follow_up_owner', 'manager'),
        }
        stored = self.store.save('incidents', incident_id, record)
        event = self._emit('RestaurantOperationsExceptionOpened', {'incident_id': incident_id, 'severity': stored['severity']}, source_operation='record_guest_incident')
        return self._respond('record_guest_incident', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def capture_loyalty_note(self, payload=None):
        payload = dict(payload or {})
        note_id = payload.get('note_id') or f"note-{len(self.store.state['loyalty_notes']) + 1}"
        record = {
            'note_id': note_id,
            'tenant': payload.get('tenant', 'default'),
            'customer_id': payload.get('customer_id', payload.get('guest_name', 'guest')),
            'loyalty_tier': payload.get('loyalty_tier', 'standard'),
            'note': payload.get('note', ''),
            'service_recovery_credit': round(float(payload.get('service_recovery_credit', 0.0)), 2),
        }
        stored = self.store.save('loyalty_notes', note_id, record)
        event = self._emit('RestaurantOperationsUpdated', {'note_id': note_id, 'customer_id': stored['customer_id']}, source_operation='capture_loyalty_note')
        return self._respond('capture_loyalty_note', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def preview_governed_document(self, payload=None):
        payload = dict(payload or {})
        preview_id = payload.get('preview_id') or f"preview-{len(self.store.state['governed_previews']) + 1}"
        document = str(payload.get('document', ''))
        instruction = str(payload.get('instruction', ''))
        lowered = f'{document} {instruction}'.lower()
        candidate_tables = []
        if 'reservation' in lowered or 'waitlist' in lowered:
            candidate_tables.append('restaurant_operations_reservation_waitlist')
        if 'menu' in lowered or 'modifier' in lowered or 'allergen' in lowered:
            candidate_tables.append('restaurant_operations_menu_catalog')
        if 'recipe' in lowered or 'cost' in lowered or 'ingredient' in lowered:
            candidate_tables.append('restaurant_operations_recipe_cost_card')
        if 'incident' in lowered:
            candidate_tables.append('restaurant_operations_guest_incident')
        if 'safety' in lowered or 'temperature' in lowered:
            candidate_tables.append('restaurant_operations_safety_log')
        if not candidate_tables:
            candidate_tables.append('restaurant_operations_governed_preview')
        record = {
            'preview_id': preview_id,
            'tenant': payload.get('tenant', 'default'),
            'document_digest': _digest((document, instruction)),
            'instruction': instruction,
            'candidate_tables': tuple(dict.fromkeys(candidate_tables)),
            'proposed_action': payload.get('proposed_action', 'create'),
            'requires_human_confirmation': True,
            'preview_status': 'draft',
        }
        stored = self.store.save('governed_previews', preview_id, record)
        event = self._emit('RestaurantOperationsApproved', {'preview_id': preview_id, 'candidate_tables': stored['candidate_tables']}, source_operation='preview_governed_document')
        return self._respond('preview_governed_document', payload, {'ok': True, 'record': stored, 'emitted_event': event['event_type']}, read_only=False)

    def get_floor_plan(self, payload=None):
        payload = dict(payload or {})
        tenant = payload.get('tenant')
        floor_plan_id = payload.get('floor_plan_id')
        plans = self.store.list_bucket('floor_plans', tenant)
        selected = next((plan for plan in plans if plan['floor_plan_id'] == floor_plan_id), plans[0] if plans else None)
        result = {'ok': selected is not None, 'floor_plan': selected, 'seat_count': selected.get('seat_count', 0) if selected else 0}
        return self._respond('get_floor_plan', payload, result, read_only=True)

    def get_kitchen_display(self, payload=None):
        payload = dict(payload or {})
        tenant = payload.get('tenant')
        orders = tuple(order for order in self.store.list_bucket('orders', tenant) if order['ticket_state'] != 'closed')
        lanes = {state: [] for state in TICKET_STATES}
        for order in orders:
            lanes[order['ticket_state']].append({'order_id': order['order_id'], 'channel': order['channel'], 'items': len(order['items'])})
        result = {'ok': True, 'lanes': {state: tuple(entries) for state, entries in lanes.items() if entries}, 'orders': orders}
        return self._respond('get_kitchen_display', payload, result, read_only=True)

    def get_revenue_analytics(self, payload=None):
        payload = dict(payload or {})
        tenant = payload.get('tenant')
        checks = self.store.list_bucket('checks', tenant)
        reservations = self.store.list_bucket('reservations', tenant)
        shifts = self.store.list_bucket('shifts', tenant)
        metrics = {
            'net_sales': round(sum(check.get('net_sales', 0.0) for check in checks), 2),
            'tips': round(sum(check.get('tip_total', 0.0) for check in checks), 2),
            'covers': sum(item.get('covers', item.get('guest_count', 0)) for item in reservations) or sum(order.get('guest_count', 0) for order in self.store.list_bucket('orders', tenant)),
            'avg_check': round(sum(check.get('net_sales', 0.0) for check in checks) / len(checks), 2) if checks else 0.0,
            'labor_hours': round(sum(shift.get('labor_hours', 0.0) for shift in shifts), 2),
            'waste_events': len(self.store.list_bucket('incidents', tenant)),
        }
        return self._respond('get_revenue_analytics', payload, {'ok': True, 'metrics': metrics}, read_only=True)

    def list_governed_previews(self, payload=None):
        payload = dict(payload or {})
        previews = self.store.list_bucket('governed_previews', payload.get('tenant'))
        return self._respond('list_governed_previews', payload, {'ok': True, 'previews': previews}, read_only=True)

    def get_workbench(self, payload=None):
        payload = dict(payload or {})
        tenant = payload.get('tenant')
        reservations = self.store.list_bucket('reservations', tenant)
        orders = self.store.list_bucket('orders', tenant)
        checks = self.store.list_bucket('checks', tenant)
        safety_logs = self.store.list_bucket('safety_logs', tenant)
        incidents = self.store.list_bucket('incidents', tenant)
        loyalty_notes = self.store.list_bucket('loyalty_notes', tenant)
        previews = self.store.list_bucket('governed_previews', tenant)
        analytics = self.get_revenue_analytics({'tenant': tenant})['result']['metrics']
        result = {
            'ok': True,
            'tenant': tenant,
            'summary_cards': (
                {'key': 'reservations', 'value': len(reservations)},
                {'key': 'waitlist', 'value': len(tuple(item for item in reservations if item['status'] == 'waitlist'))},
                {'key': 'open_orders', 'value': len(tuple(item for item in orders if item['ticket_state'] != 'closed'))},
                {'key': 'open_safety_exceptions', 'value': len(tuple(item for item in safety_logs if item['status'] != 'pass'))},
                {'key': 'service_incidents', 'value': len(incidents)},
                {'key': 'governed_previews', 'value': len(previews)},
            ),
            'reservations': reservations,
            'orders': orders,
            'checks': checks,
            'analytics': analytics,
            'loyalty_notes': loyalty_notes,
            'governed_previews': previews,
            'inventory_on_hand': deepcopy(self.store.state['inventory_on_hand']),
            'depletion_requests': tuple(deepcopy(self.store.state['depletion_requests'])),
            'kds': self.get_kitchen_display({'tenant': tenant})['result'],
        }
        return self._respond('get_workbench', payload, result, read_only=True)


def standalone_service_operation_contracts():
    contracts = tuple(
        {
            **item,
            'owned_tables': (item['table'],) if item['operation_kind'] == 'command' else (),
            'read_tables': () if item['operation_kind'] == 'command' else (item['table'],),
            'transaction_boundary': 'owned_datastore_plus_outbox' if item['operation_kind'] == 'command' else 'read_only_projection',
            'event_contract': 'AppGen-X',
            'stream_engine_picker_visible': False,
        }
        for item in STANDALONE_OPERATION_CONTRACTS
    )
    return {
        'format': 'appgen.restaurant-operations-standalone-service-contract.v1',
        'ok': bool(contracts) and all(item['event_contract'] == 'AppGen-X' for item in contracts),
        'pbc': PBC_KEY,
        'contracts': contracts,
        'command_operations': tuple(item['operation'] for item in contracts if item['operation_kind'] == 'command'),
        'query_operations': tuple(item['operation'] for item in contracts if item['operation_kind'] == 'query'),
        'table_keys': standalone_model_contract()['table_keys'],
        'side_effects': (),
    }


def standalone_service_smoke_test() -> dict:
    service = RestaurantOperationsStandaloneService()
    try:
        service.create_menu_profile({'tenant': 'tenant-smoke', 'menu_item_id': 'burger', 'name': 'Burger', 'base_price': 18.0, 'allergens': ('gluten',), 'modifier_groups': ({'group': 'side', 'choices': ('fries', 'salad')},)})
        service.record_recipe_cost({'tenant': 'tenant-smoke', 'recipe_id': 'burger-recipe', 'menu_item_id': 'burger', 'ingredients': ({'ingredient': 'beef_patty', 'quantity': 1, 'unit_cost': 4.5, 'uom': 'ea'}, {'ingredient': 'bun', 'quantity': 1, 'unit_cost': 1.0, 'uom': 'ea'}), 'target_yield': 1})
        service.configure_floor_plan({'tenant': 'tenant-smoke', 'floor_plan_id': 'main', 'tables': ({'table_id': 'T1', 'seats': 4, 'zone': 'main'}, {'table_id': 'T2', 'seats': 2, 'zone': 'patio'})})
        service.book_reservation({'tenant': 'tenant-smoke', 'reservation_id': 'res-1', 'guest_name': 'Ada', 'covers': 3, 'floor_plan_id': 'main', 'customer_notes': ('anniversary',)})
        service.open_service_shift({'tenant': 'tenant-smoke', 'shift_id': 'shift-1', 'scheduled_staff': ({'name': 'Mina', 'role': 'server', 'hours': 8}, {'name': 'Otis', 'role': 'cook', 'hours': 8}), 'readiness_checks': ('labels_complete', 'sanitizer_ready')})
        service.record_prep_plan({'tenant': 'tenant-smoke', 'prep_id': 'prep-1', 'station': 'grill', 'par_levels': {'burger': 20}, 'projected_batches': ({'batch_id': 'batch-1', 'quantity': 10},), 'ingredients': ({'ingredient': 'beef_patty', 'quantity': 10},)})
        service.open_order({'tenant': 'tenant-smoke', 'order_id': 'ord-1', 'channel': 'delivery', 'provider': 'house', 'items': ({'menu_item_id': 'burger', 'quantity': 2, 'selected_modifiers': ({'name': 'fries', 'price_delta': 2.0},)},), 'guest_count': 2})
        service.advance_order_lifecycle({'order_id': 'ord-1', 'next_state': 'acknowledged'})
        service.advance_order_lifecycle({'order_id': 'ord-1', 'next_state': 'firing'})
        service.advance_order_lifecycle({'order_id': 'ord-1', 'next_state': 'plated'})
        service.settle_guest_check({'order_id': 'ord-1', 'splits': ({'seat': 'all', 'amount': 40.0, 'tip': 6.0},), 'tenders': ({'type': 'card', 'amount': 46.0},), 'comps': ({'reason': 'late order', 'amount': 2.0},)})
        service.receive_vendor_delivery({'tenant': 'tenant-smoke', 'receipt_id': 'rcv-1', 'vendor': 'Local Farm', 'line_items': ({'ingredient': 'beef_patty', 'quantity': 24}, {'ingredient': 'bun', 'quantity': 24})})
        service.log_safety_check({'tenant': 'tenant-smoke', 'log_id': 'safe-1', 'station': 'grill', 'check_type': 'holding_temp', 'status': 'alert', 'reading': 48, 'corrective_action': 'discard batch'})
        service.record_guest_incident({'tenant': 'tenant-smoke', 'incident_id': 'inc-1', 'guest_name': 'Ada', 'severity': 'high', 'summary': 'allergen concern'})
        service.capture_loyalty_note({'tenant': 'tenant-smoke', 'note_id': 'note-1', 'customer_id': 'guest-ada', 'loyalty_tier': 'gold', 'note': 'recover with dessert'})
        service.preview_governed_document({'tenant': 'tenant-smoke', 'preview_id': 'preview-1', 'document': 'Update reservation allergy notes and menu allergen labels', 'instruction': 'prepare governed preview'})
        workbench = service.get_workbench({'tenant': 'tenant-smoke'})
        return {
            'ok': workbench['ok'] and workbench['result']['analytics']['net_sales'] >= 0 and bool(workbench['result']['governed_previews']) and bool(workbench['result']['depletion_requests']),
            'workbench': workbench,
            'kitchen_display': service.get_kitchen_display({'tenant': 'tenant-smoke'}),
            'revenue': service.get_revenue_analytics({'tenant': 'tenant-smoke'}),
            'side_effects': (),
        }
    finally:
        service.close()


def smoke_test():
    service = RestaurantOperationsService()
    command = getattr(service, COMMAND_OPERATIONS[0])({'tenant': 'tenant-smoke'})
    query = getattr(service, QUERY_OPERATIONS[0])({'tenant': 'tenant-smoke'})
    return {
        'ok': command['ok'] and query['ok'] and service_operation_contracts()['ok'] and standalone_service_smoke_test()['ok'],
        'command': command,
        'query': query,
        'standalone': standalone_service_smoke_test(),
        'side_effects': (),
    }

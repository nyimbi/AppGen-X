"""Standalone model metadata and state store for restaurant operations."""
from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime

PBC_KEY = 'restaurant_operations'
STANDALONE_TABLE_KEYS = (
    'restaurant_operations_menu_catalog',
    'restaurant_operations_recipe_cost_card',
    'restaurant_operations_floor_plan',
    'restaurant_operations_reservation_waitlist',
    'restaurant_operations_service_shift_plan',
    'restaurant_operations_order_ticket',
    'restaurant_operations_check_settlement',
    'restaurant_operations_inventory_station',
    'restaurant_operations_vendor_receipt',
    'restaurant_operations_safety_log',
    'restaurant_operations_guest_incident',
    'restaurant_operations_delivery_takeout',
    'restaurant_operations_loyalty_note',
    'restaurant_operations_governed_preview',
)
_TABLE_BUCKETS = {
    'restaurant_operations_menu_catalog': 'menu_items',
    'restaurant_operations_recipe_cost_card': 'recipes',
    'restaurant_operations_floor_plan': 'floor_plans',
    'restaurant_operations_reservation_waitlist': 'reservations',
    'restaurant_operations_service_shift_plan': 'shifts',
    'restaurant_operations_order_ticket': 'orders',
    'restaurant_operations_check_settlement': 'checks',
    'restaurant_operations_inventory_station': 'prep_plans',
    'restaurant_operations_vendor_receipt': 'vendor_receipts',
    'restaurant_operations_safety_log': 'safety_logs',
    'restaurant_operations_guest_incident': 'incidents',
    'restaurant_operations_delivery_takeout': 'delivery_orders',
    'restaurant_operations_loyalty_note': 'loyalty_notes',
    'restaurant_operations_governed_preview': 'governed_previews',
}
_FEATURE_COVERAGE = {
    'reservations_waitlist': ('restaurant_operations_reservation_waitlist',),
    'floor_table_seat_plan': ('restaurant_operations_floor_plan', 'restaurant_operations_reservation_waitlist'),
    'menu_recipe_costing': ('restaurant_operations_menu_catalog', 'restaurant_operations_recipe_cost_card'),
    'prep_par_levels': ('restaurant_operations_inventory_station',),
    'service_shifts_labor': ('restaurant_operations_service_shift_plan',),
    'order_lifecycle_kds': ('restaurant_operations_order_ticket',),
    'modifiers_allergens': ('restaurant_operations_menu_catalog', 'restaurant_operations_order_ticket'),
    'checks_splits_tips_tenders': ('restaurant_operations_check_settlement',),
    'comps_voids': ('restaurant_operations_check_settlement', 'restaurant_operations_order_ticket'),
    'inventory_depletion_vendor_receiving': ('restaurant_operations_inventory_station', 'restaurant_operations_vendor_receipt'),
    'health_safety_logs': ('restaurant_operations_safety_log',),
    'guest_incidents': ('restaurant_operations_guest_incident',),
    'delivery_takeout': ('restaurant_operations_delivery_takeout', 'restaurant_operations_order_ticket'),
    'loyalty_customer_notes': ('restaurant_operations_loyalty_note', 'restaurant_operations_reservation_waitlist'),
    'revenue_service_analytics': ('restaurant_operations_check_settlement', 'restaurant_operations_service_shift_plan'),
    'forms_wizards_controls': STANDALONE_TABLE_KEYS,
    'governed_ai_document_instruction_previews': ('restaurant_operations_governed_preview',),
}


def _now() -> str:
    return datetime.now(UTC).isoformat()


def standalone_model_contract() -> dict:
    tables = tuple(
        {
            'table': table,
            'bucket': bucket,
            'owned_by': PBC_KEY,
            'supports_crud_preview': table == 'restaurant_operations_governed_preview',
        }
        for table, bucket in _TABLE_BUCKETS.items()
    )
    return {
        'format': 'appgen.restaurant-operations-standalone-model-contract.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'table_keys': STANDALONE_TABLE_KEYS,
        'tables': tables,
        'feature_coverage': _FEATURE_COVERAGE,
        'database_backends': ('postgresql', 'mysql', 'mariadb'),
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


class RestaurantOperationsStandaloneStore:
    """Small in-memory store used by the standalone package slice."""

    def __init__(self, database_label: str = 'package-local-memory') -> None:
        self.database_label = database_label
        self.state = {
            'configuration': {},
            'parameters': {},
            'rules': {},
            'menu_items': {},
            'recipes': {},
            'floor_plans': {},
            'reservations': {},
            'shifts': {},
            'prep_plans': {},
            'orders': {},
            'checks': {},
            'vendor_receipts': {},
            'safety_logs': {},
            'incidents': {},
            'delivery_orders': {},
            'loyalty_notes': {},
            'governed_previews': {},
            'inventory_on_hand': {},
            'depletion_requests': [],
            'outbox': [],
            'inbox': [],
            'dead_letter': [],
            'idempotency_keys': set(),
            'audit_trail': [],
        }

    def close(self) -> None:
        return None

    def save(self, bucket: str, record_id: str, record: dict) -> dict:
        saved = deepcopy(record)
        saved.setdefault('id', record_id)
        saved.setdefault('created_at', _now())
        saved['updated_at'] = _now()
        self.state[bucket][record_id] = saved
        self.state['audit_trail'].append({'bucket': bucket, 'record_id': record_id, 'updated_at': saved['updated_at']})
        return deepcopy(saved)

    def fetch(self, bucket: str, record_id: str) -> dict | None:
        record = self.state[bucket].get(record_id)
        return deepcopy(record) if record else None

    def list_bucket(self, bucket: str, tenant: str | None = None) -> tuple[dict, ...]:
        records = tuple(deepcopy(item) for item in self.state[bucket].values())
        if tenant is None:
            return records
        return tuple(item for item in records if item.get('tenant') == tenant)

    def append_event(self, bucket: str, record: dict) -> dict:
        event = deepcopy(record)
        self.state[bucket].append(event)
        return deepcopy(event)

    def snapshot(self) -> dict:
        snapshot = deepcopy(self.state)
        snapshot['idempotency_keys'] = tuple(sorted(snapshot['idempotency_keys']))
        return snapshot


def standalone_store_smoke_test() -> dict:
    store = RestaurantOperationsStandaloneStore()
    menu = store.save(
        'menu_items',
        'menu-smoke',
        {
            'tenant': 'tenant-smoke',
            'name': 'Smoke Burger',
            'allergens': ('gluten', 'dairy'),
            'modifiers': ({'group': 'temp', 'choices': ('rare', 'medium')},),
        },
    )
    order = store.save(
        'orders',
        'order-smoke',
        {
            'tenant': 'tenant-smoke',
            'menu_item_ids': ('menu-smoke',),
            'ticket_state': 'queued',
        },
    )
    event = store.append_event(
        'outbox',
        {'event_type': 'RestaurantOperationsCreated', 'topic': 'pbc.restaurant_operations.events'},
    )
    return {
        'ok': menu['id'] == 'menu-smoke' and order['ticket_state'] == 'queued' and event['topic'] == 'pbc.restaurant_operations.events',
        'model_contract': standalone_model_contract(),
        'snapshot': store.snapshot(),
        'side_effects': (),
    }


def model_contracts():
    from .runtime import restaurant_operations_build_schema_contract

    return restaurant_operations_build_schema_contract()['models']

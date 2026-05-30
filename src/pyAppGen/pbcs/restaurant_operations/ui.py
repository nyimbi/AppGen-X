from __future__ import annotations

from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_EDGE_CASES, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, DOMAIN_PARAMETERS, DOMAIN_RULES, domain_capability_surface_contract
from .models import STANDALONE_TABLE_KEYS
from .permissions import PERMISSIONS

PBC_KEY = 'restaurant_operations'
FRAGMENTS = (
    'RestaurantOperationsWorkbench',
    'RestaurantOperationsDetail',
    'RestaurantOperationsAssistantPanel',
    'DiningRoomFloorBoard',
    'KitchenDisplayBoard',
    'CheckSettlementConsole',
    'SafetyAndIncidentBoard',
    'RevenueServiceAnalyticsPanel',
)
FORM_KEYS = (
    'MenuEngineeringForm',
    'RecipeCostCardForm',
    'ReservationWaitlistForm',
    'FloorPlanDesignerForm',
    'ShiftLaunchForm',
    'PrepParLevelForm',
    'OrderLifecycleForm',
    'CheckSettlementForm',
    'VendorReceivingForm',
    'SafetyLogForm',
    'GuestIncidentForm',
    'LoyaltyGuestNoteForm',
    'GovernedPreviewForm',
)
WIZARD_KEYS = (
    'MenuEngineeringWizard',
    'ReservationFlowWizard',
    'ServiceLaunchWizard',
    'DiningRoomRecoveryWizard',
    'DeliveryTakeoutWizard',
    'GovernedInstructionWizard',
)
CONTROL_KEYS = (
    'DiningRoomFloorControl',
    'KitchenDisplayControl',
    'CheckSplitTenderControl',
    'PrepDepletionControl',
    'SafetyIncidentControl',
    'RevenueServiceAnalyticsControl',
    'GovernedPreviewQueueControl',
)


def restaurant_operations_form_contracts() -> dict:
    contracts = (
        {'key': 'MenuEngineeringForm', 'table': 'restaurant_operations_menu_catalog', 'operation': 'create_menu_profile', 'fields': ('menu_item_id', 'tenant', 'name', 'base_price', 'dayparts', 'channels', 'modifier_groups', 'allergens', 'dietary_flags')},
        {'key': 'RecipeCostCardForm', 'table': 'restaurant_operations_recipe_cost_card', 'operation': 'record_recipe_cost', 'fields': ('recipe_id', 'tenant', 'menu_item_id', 'ingredients', 'target_yield', 'cross_contact_controls')},
        {'key': 'ReservationWaitlistForm', 'table': 'restaurant_operations_reservation_waitlist', 'operation': 'book_reservation', 'fields': ('reservation_id', 'tenant', 'guest_name', 'covers', 'reservation_time', 'waitlist_requested', 'table_assignment', 'customer_notes')},
        {'key': 'FloorPlanDesignerForm', 'table': 'restaurant_operations_floor_plan', 'operation': 'configure_floor_plan', 'fields': ('floor_plan_id', 'tenant', 'room', 'tables', 'service_mode')},
        {'key': 'ShiftLaunchForm', 'table': 'restaurant_operations_service_shift_plan', 'operation': 'open_service_shift', 'fields': ('shift_id', 'tenant', 'service_date', 'station', 'scheduled_staff', 'readiness_checks')},
        {'key': 'PrepParLevelForm', 'table': 'restaurant_operations_inventory_station', 'operation': 'record_prep_plan', 'fields': ('prep_id', 'tenant', 'station', 'par_levels', 'projected_batches', 'ingredients')},
        {'key': 'OrderLifecycleForm', 'table': 'restaurant_operations_order_ticket', 'operation': 'open_order', 'fields': ('order_id', 'tenant', 'channel', 'provider', 'reservation_id', 'table_assignment', 'seat_numbers', 'items', 'notes')},
        {'key': 'CheckSettlementForm', 'table': 'restaurant_operations_check_settlement', 'operation': 'settle_guest_check', 'fields': ('check_id', 'order_id', 'splits', 'tenders', 'comps', 'voids', 'service_recovery_notes')},
        {'key': 'VendorReceivingForm', 'table': 'restaurant_operations_vendor_receipt', 'operation': 'receive_vendor_delivery', 'fields': ('receipt_id', 'tenant', 'vendor', 'line_items', 'temperature_checks')},
        {'key': 'SafetyLogForm', 'table': 'restaurant_operations_safety_log', 'operation': 'log_safety_check', 'fields': ('log_id', 'tenant', 'station', 'check_type', 'status', 'reading', 'corrective_action')},
        {'key': 'GuestIncidentForm', 'table': 'restaurant_operations_guest_incident', 'operation': 'record_guest_incident', 'fields': ('incident_id', 'tenant', 'guest_name', 'severity', 'summary', 'follow_up_owner')},
        {'key': 'LoyaltyGuestNoteForm', 'table': 'restaurant_operations_loyalty_note', 'operation': 'capture_loyalty_note', 'fields': ('note_id', 'tenant', 'customer_id', 'loyalty_tier', 'note', 'service_recovery_credit')},
        {'key': 'GovernedPreviewForm', 'table': 'restaurant_operations_governed_preview', 'operation': 'preview_governed_document', 'fields': ('preview_id', 'tenant', 'document', 'instruction', 'proposed_action')},
    )
    return {'format': 'appgen.restaurant-operations-form-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'side_effects': ()}


def restaurant_operations_wizard_contracts() -> dict:
    contracts = (
        {'key': 'MenuEngineeringWizard', 'steps': ('menu_profile', 'recipe_cost', 'allergen_review', 'modifier_review'), 'forms': ('MenuEngineeringForm', 'RecipeCostCardForm'), 'keywords': ('menu', 'modifier', 'allergen', 'recipe', 'cost')},
        {'key': 'ReservationFlowWizard', 'steps': ('floor_plan', 'reservation', 'waitlist', 'guest_note'), 'forms': ('FloorPlanDesignerForm', 'ReservationWaitlistForm', 'LoyaltyGuestNoteForm'), 'keywords': ('reservation', 'waitlist', 'table', 'seat')},
        {'key': 'ServiceLaunchWizard', 'steps': ('shift', 'prep', 'vendor_receiving', 'safety'), 'forms': ('ShiftLaunchForm', 'PrepParLevelForm', 'VendorReceivingForm', 'SafetyLogForm'), 'keywords': ('shift', 'prep', 'par', 'receiving', 'safety')},
        {'key': 'DiningRoomRecoveryWizard', 'steps': ('incident', 'check_settlement', 'loyalty_note'), 'forms': ('GuestIncidentForm', 'CheckSettlementForm', 'LoyaltyGuestNoteForm'), 'keywords': ('comp', 'void', 'incident', 'recovery', 'tip')},
        {'key': 'DeliveryTakeoutWizard', 'steps': ('order', 'kds', 'handoff'), 'forms': ('OrderLifecycleForm', 'CheckSettlementForm'), 'keywords': ('delivery', 'takeout', 'kitchen', 'order')},
        {'key': 'GovernedInstructionWizard', 'steps': ('document_review', 'crud_preview', 'human_confirmation'), 'forms': ('GovernedPreviewForm',), 'keywords': ('document', 'instruction', 'preview', 'crud')},
    )
    return {'format': 'appgen.restaurant-operations-wizard-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'side_effects': ()}


def restaurant_operations_control_catalog() -> dict:
    contracts = (
        {'key': 'DiningRoomFloorControl', 'type': 'floor_map', 'binds_to': ('restaurant_operations_floor_plan', 'restaurant_operations_reservation_waitlist')},
        {'key': 'KitchenDisplayControl', 'type': 'kds', 'binds_to': ('restaurant_operations_order_ticket',)},
        {'key': 'CheckSplitTenderControl', 'type': 'settlement_console', 'binds_to': ('restaurant_operations_check_settlement',)},
        {'key': 'PrepDepletionControl', 'type': 'prep_console', 'binds_to': ('restaurant_operations_inventory_station', 'restaurant_operations_vendor_receipt')},
        {'key': 'SafetyIncidentControl', 'type': 'safety_board', 'binds_to': ('restaurant_operations_safety_log', 'restaurant_operations_guest_incident')},
        {'key': 'RevenueServiceAnalyticsControl', 'type': 'analytics', 'binds_to': ('restaurant_operations_check_settlement', 'restaurant_operations_service_shift_plan')},
        {'key': 'GovernedPreviewQueueControl', 'type': 'preview_queue', 'binds_to': ('restaurant_operations_governed_preview',)},
    )
    return {'format': 'appgen.restaurant-operations-control-catalog.v1', 'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'side_effects': ()}


def restaurant_operations_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'fragments': FRAGMENTS,
        'forms': FORM_KEYS,
        'wizards': WIZARD_KEYS,
        'controls': CONTROL_KEYS,
        'configuration_editor': True,
        'stream_engine_picker_visible': False,
        'action_permissions': PERMISSIONS,
        'full_capability_surface': {
            'operation_actions': DOMAIN_OPERATIONS,
            'rule_editors': DOMAIN_RULES,
            'parameter_editors': DOMAIN_PARAMETERS,
            'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES,
            'table_browsers': DOMAIN_OWNED_TABLES,
            'edge_case_queues': DOMAIN_EDGE_CASES,
            'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS),
            'navigation_sections': ('overview', 'dining_room', 'kitchen', 'settlement', 'safety', 'governed_ai', 'release_evidence'),
            'coverage': surface['coverage'],
        },
        'standalone_surfaces': {
            'table_browsers': STANDALONE_TABLE_KEYS,
            'forms': FORM_KEYS,
            'wizards': WIZARD_KEYS,
            'controls': CONTROL_KEYS,
        },
        'side_effects': (),
    }


def restaurant_operations_standalone_workbench_blueprint() -> dict:
    return {
        'format': 'appgen.restaurant-operations-standalone-workbench-blueprint.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'route': '/app/restaurant-operations/workbench',
        'fragments': FRAGMENTS,
        'forms': restaurant_operations_form_contracts()['contracts'],
        'wizards': restaurant_operations_wizard_contracts()['contracts'],
        'controls': restaurant_operations_control_catalog()['contracts'],
        'side_effects': (),
    }


def restaurant_operations_render_standalone_workbench(snapshot: dict) -> dict:
    analytics = snapshot.get('analytics', {})
    return {
        'format': 'appgen.restaurant-operations-standalone-workbench-render.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'route': '/app/restaurant-operations/workbench',
        'cards': snapshot.get('summary_cards', ()),
        'kds': snapshot.get('kds', {}),
        'analytics': analytics,
        'forms': restaurant_operations_form_contracts()['contracts'],
        'wizards': restaurant_operations_wizard_contracts()['contracts'],
        'controls': restaurant_operations_control_catalog()['contracts'],
        'governed_preview_count': len(snapshot.get('governed_previews', ())),
        'side_effects': (),
    }


def restaurant_operations_render_workbench(workbench: dict | None = None, *, tenant: str = 'default', principal_permissions: tuple[str, ...] | None = None) -> dict:
    contract = restaurant_operations_ui_contract()
    permissions = set(principal_permissions or PERMISSIONS)
    visible_actions = tuple(permission for permission in PERMISSIONS if permission in permissions)
    snapshot = workbench or {'summary_cards': (), 'analytics': {}, 'governed_previews': (), 'kds': {}}
    rendered = restaurant_operations_render_standalone_workbench(snapshot)
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'tenant': tenant,
        'route': '/workbench/pbcs/restaurant_operations',
        'fragments': contract['fragments'],
        'visible_actions': visible_actions,
        'locked_actions': tuple(permission for permission in PERMISSIONS if permission not in permissions),
        'cards': rendered['cards'],
        'controls': rendered['controls'],
        'forms': rendered['forms'],
        'wizards': rendered['wizards'],
        'analytics': rendered['analytics'],
        'governed_preview_count': rendered['governed_preview_count'],
        'side_effects': (),
    }


def smoke_test():
    render = restaurant_operations_render_workbench({'summary_cards': ({'key': 'reservations', 'value': 2},), 'analytics': {'net_sales': 44.0}, 'governed_previews': ({'preview_id': 'pv1'},), 'kds': {'lanes': {'queued': ({'order_id': 'ord1'},)}}})
    return {'ok': restaurant_operations_ui_contract()['ok'] and restaurant_operations_standalone_workbench_blueprint()['ok'] and render['ok'], 'render': render, 'side_effects': ()}

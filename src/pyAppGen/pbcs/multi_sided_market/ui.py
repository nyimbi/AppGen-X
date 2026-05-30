"""Workbench UI contract for the multi_sided_market PBC."""
from .app_surface import single_pbc_multi_sided_market_app_contract

MULTI_SIDED_MARKET_UI_FRAGMENT_KEYS = ('MarketExchangeWorkbench', 'ListingConsole', 'BookingRentalCalendar', 'EscrowSettlementConsole', 'DisputeResolutionBoard')


def multi_sided_market_forms_contract():
    from .app_surface import multi_sided_market_forms_contract as _forms
    return _forms()

def multi_sided_market_wizards_contract():
    from .app_surface import multi_sided_market_wizards_contract as _wizards
    return _wizards()

def multi_sided_market_controls_contract():
    from .app_surface import multi_sided_market_controls_contract as _controls
    return _controls()


def multi_sided_market_ui_contract():
    return {'ok': True, 'pbc': 'multi_sided_market', 'fragments': MULTI_SIDED_MARKET_UI_FRAGMENT_KEYS, 'configuration_editor': {'required_fields': ('MULTI_SIDED_MARKET_DATABASE_URL', 'MULTI_SIDED_MARKET_EVENT_TOPIC', 'MULTI_SIDED_MARKET_RETRY_LIMIT', 'MULTI_SIDED_MARKET_DEFAULT_CURRENCY', 'MULTI_SIDED_MARKET_ESCROW_HOLD_DAYS', 'MULTI_SIDED_MARKET_MAX_RENTAL_DAYS'), 'allowed_database_backends': ('postgresql','mysql','mariadb'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}, 'action_permissions': {'publish_listing': 'multi_sided_market.create', 'reserve_booking': 'multi_sided_market.create', 'start_rental': 'multi_sided_market.approve', 'issue_loan': 'multi_sided_market.approve', 'open_escrow': 'multi_sided_market.settle', 'prepare_settlement': 'multi_sided_market.settle', 'open_dispute': 'multi_sided_market.update'}, 'forms': multi_sided_market_forms_contract()['forms'], 'wizards': multi_sided_market_wizards_contract()['wizards'], 'controls': multi_sided_market_controls_contract()['controls'], 'single_pbc_app': single_pbc_multi_sided_market_app_contract(), 'event_surfaces': {'outbox_status': 'visible', 'inbox_status': 'visible', 'dead_letter_status': 'visible'}, 'workbench_binding_evidence': {'owned_tables': ('multi_sided_market_participant_profile', 'multi_sided_market_marketplace_listing', 'multi_sided_market_listing_asset', 'multi_sided_market_service_offer', 'multi_sided_market_availability_window', 'multi_sided_market_booking_reservation', 'multi_sided_market_rental_contract', 'multi_sided_market_loan_agreement', 'multi_sided_market_barter_offer', 'multi_sided_market_trade_order', 'multi_sided_market_sale_order', 'multi_sided_market_exchange_proposal', 'multi_sided_market_escrow_account', 'multi_sided_market_settlement_instruction', 'multi_sided_market_dispute_case', 'multi_sided_market_reputation_signal', 'multi_sided_market_market_rule', 'multi_sided_market_market_parameter', 'multi_sided_market_schema_extension', 'multi_sided_market_governed_model'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}, 'side_effects': ()}


def multi_sided_market_render_workbench(state=None, *, tenant='default', principal_permissions=()):
    state = state or {}
    contract = multi_sided_market_ui_contract()
    visible_actions = tuple(action for action, permission in contract['action_permissions'].items() if permission in set(principal_permissions))
    return {'format': 'appgen.multi-sided-market-workbench-render.v1', 'ok': True, 'tenant': tenant, 'route': '/workbench/pbcs/multi_sided_market', 'fragments': contract['fragments'], 'visible_actions': visible_actions, 'locked_actions': tuple(action for action in contract['action_permissions'] if action not in visible_actions), 'configuration_bound': True, 'event_outbox_count': len(state.get('outbox', ())), 'binding_evidence': contract['workbench_binding_evidence'], 'forms': contract['forms'], 'wizards': contract['wizards'], 'controls': contract['controls'], 'single_pbc_app': contract['single_pbc_app'], 'side_effects': ()}


def smoke_test():
    rendered = multi_sided_market_render_workbench({'outbox': ()}, principal_permissions=('multi_sided_market.create',))
    contract = multi_sided_market_ui_contract(); return {'ok': contract['ok'] and rendered['ok'] and bool(contract['forms']) and bool(contract['wizards']) and bool(contract['controls']) and contract['single_pbc_app']['ok'], 'contract': contract, 'rendered': rendered, 'side_effects': ()}

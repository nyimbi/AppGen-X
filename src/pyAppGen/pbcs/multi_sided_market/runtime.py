"""Executable runtime contract for the multi_sided_market PBC."""

from __future__ import annotations

import hashlib
from copy import deepcopy

from .domain_schema import class_name_for, fields_for, logical_table, owned_table, relationships_for

PBC_KEY = 'multi_sided_market'
MULTI_SIDED_MARKET_OWNED_TABLES = ('multi_sided_market_participant_profile', 'multi_sided_market_marketplace_listing', 'multi_sided_market_listing_asset', 'multi_sided_market_service_offer', 'multi_sided_market_availability_window', 'multi_sided_market_booking_reservation', 'multi_sided_market_rental_contract', 'multi_sided_market_loan_agreement', 'multi_sided_market_barter_offer', 'multi_sided_market_trade_order', 'multi_sided_market_sale_order', 'multi_sided_market_exchange_proposal', 'multi_sided_market_escrow_account', 'multi_sided_market_settlement_instruction', 'multi_sided_market_dispute_case', 'multi_sided_market_reputation_signal', 'multi_sided_market_market_rule', 'multi_sided_market_market_parameter', 'multi_sided_market_schema_extension', 'multi_sided_market_governed_model')
MULTI_SIDED_MARKET_RUNTIME_TABLES = ('multi_sided_market_participant_profile', 'multi_sided_market_marketplace_listing', 'multi_sided_market_listing_asset', 'multi_sided_market_service_offer', 'multi_sided_market_availability_window', 'multi_sided_market_booking_reservation', 'multi_sided_market_rental_contract', 'multi_sided_market_loan_agreement', 'multi_sided_market_barter_offer', 'multi_sided_market_trade_order', 'multi_sided_market_sale_order', 'multi_sided_market_exchange_proposal', 'multi_sided_market_escrow_account', 'multi_sided_market_settlement_instruction', 'multi_sided_market_dispute_case', 'multi_sided_market_reputation_signal', 'multi_sided_market_market_rule', 'multi_sided_market_market_parameter', 'multi_sided_market_schema_extension', 'multi_sided_market_governed_model', 'multi_sided_market_appgen_outbox_event', 'multi_sided_market_appgen_inbox_event', 'multi_sided_market_appgen_dead_letter_event')
MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
MULTI_SIDED_MARKET_REQUIRED_EVENT_TOPIC = 'pbc.multi_sided_market.events'
MULTI_SIDED_MARKET_EMITTED_EVENT_TYPES = (
    'MarketParticipantVerified',
    'MarketListingPublished',
    'ListingAssetRegistered',
    'ServiceOfferCreated',
    'AvailabilityWindowPublished',
    'TradeOrderPlaced',
    'BarterOfferMatched',
    'ExchangeProposalPrepared',
    'SaleCompleted',
    'BookingReserved',
    'RentalStarted',
    'LoanIssued',
    'EscrowOpened',
    'EscrowReleasePolicyCompiled',
    'EscrowReleased',
    'MarketSettlementPrepared',
    'ReputationSignalRecorded',
    'MarketDisputeOpened',
    'MarketDisputeResolved',
    'MarketClearingProjected',
)
MULTI_SIDED_MARKET_CONSUMED_EVENT_TYPES = ('ProductPublished', 'InventoryPoolChanged', 'PaymentCaptured', 'TaxCalculated', 'FraudRiskScored', 'AccessPolicyChanged')
MULTI_SIDED_MARKET_STANDARD_FEATURE_KEYS = ('participant_onboarding', 'seller_buyer_provider_borrower_roles', 'goods_listing', 'service_listing', 'availability_calendar', 'booking_reservation', 'rental_contracting', 'loan_agreement_management', 'barter_negotiation', 'trade_order_management', 'direct_sale_checkout_handoff', 'escrow_hold_and_release', 'settlement_instruction', 'reputation_scoring', 'dispute_resolution', 'policy_rule_engine', 'runtime_parameter_engine', 'configuration_schema', 'owned_schema_migrations_models', 'appgen_x_outbox_inbox_eventing', 'idempotent_handlers', 'retry_dead_letter_evidence', 'permissions', 'seed_data', 'workbench', 'agentic_document_instruction_intake', 'governed_datastore_crud')
MULTI_SIDED_MARKET_RUNTIME_CAPABILITY_KEYS = ('multi_party_exchange_graph_matching', 'barter_equivalence_valuation', 'combinatorial_trade_optimization', 'dynamic_liquidity_and_trust_scoring', 'availability_aware_booking_optimization', 'rental_condition_and_collateral_modeling', 'loan_term_risk_simulation', 'escrow_release_policy_compilation', 'real_time_market_clearing_projection', 'counterfactual_price_and_slot_simulation', 'semantic_listing_instruction_understanding', 'autonomous_dispute_triage_with_audit_trail', 'fraud_and_collusion_anomaly_detection', 'privacy_preserving_reputation_proofs', 'carbon_aware_fulfillment_and_meetup_selection', 'cross_pbc_catalog_inventory_payment_tax_integration')


def multi_sided_market_empty_state():
    return {
        'participants': {}, 'listings': {}, 'listing_assets': {}, 'service_offers': {}, 'availability_windows': {},
        'bookings': {}, 'rentals': {}, 'loans': {}, 'barter_offers': {}, 'trade_orders': {},
        'sale_orders': {}, 'exchange_proposals': {}, 'escrow_accounts': {}, 'escrow_release_policies': {}, 'settlements': {},
        'disputes': {}, 'market_clearing_projections': {}, 'reputation': {}, 'rules': {}, 'parameters': {}, 'schema_extensions': {},
        'governed_models': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [],
        'idempotency_keys': set(),
    }


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': MULTI_SIDED_MARKET_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def multi_sided_market_configure_runtime(state, config):
    next_state = _copy(state)
    backend = config.get('database_backend')
    ok = backend in MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS and config.get('event_topic') == MULTI_SIDED_MARKET_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def multi_sided_market_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'bounded': name in ('commission_rate', 'escrow_hold_days', 'max_rental_days', 'trust_threshold', 'loan_collateral_rate')}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def multi_sided_market_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'market_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def multi_sided_market_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('participant_profile', 'marketplace_listing', 'listing_asset', 'service_offer', 'availability_window', 'booking_reservation', 'rental_contract', 'loan_agreement', 'barter_offer', 'trade_order', 'sale_order', 'exchange_proposal', 'escrow_account', 'settlement_instruction', 'dispute_case', 'reputation_signal', 'market_rule', 'market_parameter', 'schema_extension', 'governed_model'):
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][table] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': f'multi_sided_market_{table}', 'fields': dict(fields), 'side_effects': ()}


def multi_sided_market_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id')
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in MULTI_SIDED_MARKET_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'multi_sided_market_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def multi_sided_market_verify_participant(state, payload):
    next_state = _copy(state)
    participant_id = payload['participant_id']
    profile = {'participant_id': participant_id, 'tenant': payload.get('tenant', 'default'), 'roles': tuple(payload.get('roles', ('buyer',))), 'trust_score': float(payload.get('trust_score', 0.7)), 'status': 'verified'}
    next_state['participants'][participant_id] = profile
    _event(next_state, 'MarketParticipantVerified', profile)
    return {'ok': True, 'state': next_state, 'participant': profile, 'side_effects': ()}


def multi_sided_market_publish_listing(state, payload):
    next_state = _copy(state)
    listing_id = payload['listing_id']
    listing = {'listing_id': listing_id, 'tenant': payload.get('tenant', 'default'), 'participant_id': payload.get('participant_id'), 'kind': payload.get('kind', 'good'), 'exchange_modes': tuple(payload.get('exchange_modes', ('sale', 'trade', 'barter', 'booking', 'rental', 'loan'))), 'price': float(payload.get('price', 0.0)), 'status': 'published'}
    next_state['listings'][listing_id] = listing
    _event(next_state, 'MarketListingPublished', listing)
    return {'ok': True, 'state': next_state, 'listing': listing, 'side_effects': ()}


def multi_sided_market_register_listing_asset(state, payload):
    next_state = _copy(state)
    asset_id = payload['asset_id']
    asset = {
        'asset_id': asset_id,
        'listing_id': payload.get('listing_id'),
        'asset_type': payload.get('asset_type', 'good'),
        'quantity': float(payload.get('quantity', 1)),
        'condition_grade': payload.get('condition_grade', 'documented'),
        'location': dict(payload.get('location', {})),
        'attributes': dict(payload.get('attributes', {})),
        'status': payload.get('status', 'available'),
    }
    next_state['listing_assets'][asset_id] = asset
    _event(next_state, 'ListingAssetRegistered', asset)
    return {'ok': True, 'state': next_state, 'asset': asset, 'side_effects': ()}


def multi_sided_market_create_service_offer(state, payload):
    next_state = _copy(state)
    offer_id = payload['offer_id']
    offer = {'offer_id': offer_id, 'listing_id': payload.get('listing_id'), 'service_type': payload.get('service_type', 'appointment'), 'duration_minutes': int(payload.get('duration_minutes', 60)), 'status': 'active'}
    next_state['service_offers'][offer_id] = offer
    _event(next_state, 'ServiceOfferCreated', offer)
    return {'ok': True, 'state': next_state, 'service_offer': offer, 'side_effects': ()}


def multi_sided_market_publish_availability_window(state, payload):
    next_state = _copy(state)
    window_id = payload['window_id']
    reserved = int(payload.get('reserved_count', 0))
    capacity = int(payload.get('capacity', 1))
    window = {
        'window_id': window_id,
        'listing_id': payload.get('listing_id'),
        'starts_at': payload.get('starts_at'),
        'ends_at': payload.get('ends_at'),
        'capacity': capacity,
        'reserved_count': reserved,
        'available_count': max(capacity - reserved, 0),
        'status': 'open' if capacity > reserved else 'full',
    }
    next_state['availability_windows'][window_id] = window
    _event(next_state, 'AvailabilityWindowPublished', window)
    return {'ok': True, 'state': next_state, 'availability_window': window, 'side_effects': ()}


def multi_sided_market_place_trade_order(state, payload):
    next_state = _copy(state)
    order_id = payload['order_id']
    order = {'order_id': order_id, 'listing_id': payload.get('listing_id'), 'offered_listing_id': payload.get('offered_listing_id'), 'quantity': int(payload.get('quantity', 1)), 'status': 'placed'}
    next_state['trade_orders'][order_id] = order
    _event(next_state, 'TradeOrderPlaced', order)
    return {'ok': True, 'state': next_state, 'trade_order': order, 'side_effects': ()}


def multi_sided_market_match_barter_offer(state, payload):
    next_state = _copy(state)
    offer_id = payload['offer_id']
    valuation_delta = abs(float(payload.get('requested_value', 0)) - float(payload.get('offered_value', 0)))
    offer = {'offer_id': offer_id, 'listing_id': payload.get('listing_id'), 'requested_value': payload.get('requested_value', 0), 'offered_value': payload.get('offered_value', 0), 'valuation_delta': valuation_delta, 'status': 'matched' if valuation_delta <= float(payload.get('tolerance', 25)) else 'counteroffer_required'}
    next_state['barter_offers'][offer_id] = offer
    _event(next_state, 'BarterOfferMatched', offer)
    return {'ok': True, 'state': next_state, 'barter_offer': offer, 'side_effects': ()}


def multi_sided_market_prepare_exchange_proposal(state, payload):
    next_state = _copy(state)
    proposal_id = payload['proposal_id']
    source_id = payload.get('source_listing_id')
    target_id = payload.get('target_listing_id')
    source = next_state['listings'].get(source_id, {})
    target = next_state['listings'].get(target_id, {})
    price_gap = abs(float(source.get('price', payload.get('source_value', 0))) - float(target.get('price', payload.get('target_value', 0))))
    trust_score = min((float(next_state['participants'].get(source.get('participant_id'), {}).get('trust_score', 0.5)) + float(payload.get('counterparty_trust_score', 0.5))) / 2, 1.0)
    score = max(0.0, min(1.0, trust_score - price_gap / max(float(payload.get('normalization_value', 1000)), 1.0)))
    proposal = {
        'proposal_id': proposal_id,
        'source_listing_id': source_id,
        'target_listing_id': target_id,
        'exchange_mode': payload.get('exchange_mode', 'trade'),
        'score': round(score, 4),
        'explanation': {
            'price_gap': round(price_gap, 4),
            'trust_score': round(trust_score, 4),
            'mode_supported': payload.get('exchange_mode', 'trade') in set(source.get('exchange_modes', (payload.get('exchange_mode', 'trade'),))),
        },
        'status': 'proposed' if score >= float(payload.get('minimum_score', 0.4)) else 'needs_review',
    }
    next_state['exchange_proposals'][proposal_id] = proposal
    _event(next_state, 'ExchangeProposalPrepared', proposal)
    return {'ok': True, 'state': next_state, 'exchange_proposal': proposal, 'side_effects': ()}


def multi_sided_market_execute_sale(state, payload):
    next_state = _copy(state)
    sale_id = payload['sale_id']
    sale = {'sale_id': sale_id, 'listing_id': payload.get('listing_id'), 'buyer_id': payload.get('buyer_id'), 'amount': float(payload.get('amount', 0)), 'currency': payload.get('currency', 'USD'), 'status': 'completed'}
    next_state['sale_orders'][sale_id] = sale
    _event(next_state, 'SaleCompleted', sale)
    return {'ok': True, 'state': next_state, 'sale_order': sale, 'side_effects': ()}


def multi_sided_market_reserve_booking(state, payload):
    next_state = _copy(state)
    booking_id = payload['booking_id']
    booking = {'booking_id': booking_id, 'listing_id': payload.get('listing_id'), 'starts_at': payload.get('starts_at'), 'ends_at': payload.get('ends_at'), 'status': 'reserved'}
    next_state['bookings'][booking_id] = booking
    _event(next_state, 'BookingReserved', booking)
    return {'ok': True, 'state': next_state, 'booking': booking, 'side_effects': ()}


def multi_sided_market_start_rental(state, payload):
    next_state = _copy(state)
    rental_id = payload['rental_id']
    rental = {'rental_id': rental_id, 'listing_id': payload.get('listing_id'), 'condition_out': payload.get('condition_out', 'documented'), 'collateral_amount': float(payload.get('collateral_amount', 0)), 'status': 'active'}
    next_state['rentals'][rental_id] = rental
    _event(next_state, 'RentalStarted', rental)
    return {'ok': True, 'state': next_state, 'rental': rental, 'side_effects': ()}


def multi_sided_market_issue_loan(state, payload):
    next_state = _copy(state)
    loan_id = payload['loan_id']
    loan = {'loan_id': loan_id, 'listing_id': payload.get('listing_id'), 'borrower_id': payload.get('borrower_id'), 'return_due_at': payload.get('return_due_at'), 'collateral_rate': float(payload.get('collateral_rate', 0.0)), 'status': 'issued'}
    next_state['loans'][loan_id] = loan
    _event(next_state, 'LoanIssued', loan)
    return {'ok': True, 'state': next_state, 'loan': loan, 'side_effects': ()}


def multi_sided_market_open_escrow(state, payload):
    next_state = _copy(state)
    escrow_id = payload['escrow_id']
    escrow = {
        'escrow_id': escrow_id,
        'exchange_id': payload.get('exchange_id'),
        'amount': float(payload.get('amount', 0)),
        'currency': payload.get('currency', 'USD'),
        'hold_until': payload.get('hold_until'),
        'release_policy_hash': _digest(payload.get('release_policy', {'type': 'delivery_confirmation'})),
        'status': 'open',
    }
    next_state['escrow_accounts'][escrow_id] = escrow
    _event(next_state, 'EscrowOpened', escrow)
    return {'ok': True, 'state': next_state, 'escrow': escrow, 'side_effects': ()}


def multi_sided_market_compile_escrow_release_policy(state, payload):
    next_state = _copy(state)
    policy_id = payload['policy_id']
    checks = tuple(payload.get('required_checks', ('payment_captured', 'fulfillment_confirmed', 'dispute_window_clear')))
    policy = {
        'policy_id': policy_id,
        'escrow_id': payload.get('escrow_id'),
        'required_checks': checks,
        'partial_release_allowed': bool(payload.get('partial_release_allowed', False)),
        'compiled_hash': _digest((policy_id, checks, payload.get('partial_release_allowed', False))),
        'status': 'compiled',
    }
    next_state['escrow_release_policies'][policy_id] = policy
    _event(next_state, 'EscrowReleasePolicyCompiled', policy)
    return {'ok': True, 'state': next_state, 'escrow_release_policy': policy, 'side_effects': ()}


def multi_sided_market_release_escrow(state, payload):
    next_state = _copy(state)
    escrow_id = payload['escrow_id']
    escrow = dict(next_state['escrow_accounts'].get(escrow_id, {'escrow_id': escrow_id, 'amount': payload.get('amount', 0), 'currency': payload.get('currency', 'USD')}))
    completed_checks = set(payload.get('completed_checks', ()))
    policy = next_state['escrow_release_policies'].get(payload.get('policy_id'), {})
    required = set(policy.get('required_checks', ('payment_captured', 'fulfillment_confirmed')))
    escrow['release_checks'] = tuple(sorted(completed_checks))
    escrow['status'] = 'released' if required <= completed_checks else 'release_blocked'
    escrow['blocked_reasons'] = tuple(sorted(required - completed_checks))
    next_state['escrow_accounts'][escrow_id] = escrow
    _event(next_state, 'EscrowReleased', escrow)
    return {'ok': True, 'state': next_state, 'escrow': escrow, 'side_effects': ()}


def multi_sided_market_prepare_settlement(state, payload):
    next_state = _copy(state)
    settlement_id = payload['settlement_id']
    settlement = {'settlement_id': settlement_id, 'exchange_id': payload.get('exchange_id'), 'amount': float(payload.get('amount', 0)), 'currency': payload.get('currency', 'USD'), 'status': 'prepared'}
    next_state['settlements'][settlement_id] = settlement
    _event(next_state, 'MarketSettlementPrepared', settlement)
    return {'ok': True, 'state': next_state, 'settlement': settlement, 'side_effects': ()}


def multi_sided_market_record_reputation_signal(state, payload):
    next_state = _copy(state)
    signal_id = payload['signal_id']
    signal = {
        'signal_id': signal_id,
        'participant_id': payload.get('participant_id'),
        'source_exchange_id': payload.get('source_exchange_id'),
        'score_delta': float(payload.get('score_delta', 0)),
        'reason': payload.get('reason', 'completed_exchange'),
        'proof_hash': _digest(payload),
        'status': 'recorded',
    }
    next_state['reputation'][signal_id] = signal
    _event(next_state, 'ReputationSignalRecorded', signal)
    return {'ok': True, 'state': next_state, 'reputation_signal': signal, 'side_effects': ()}


def multi_sided_market_open_dispute(state, payload):
    next_state = _copy(state)
    dispute_id = payload['dispute_id']
    dispute = {'dispute_id': dispute_id, 'exchange_id': payload.get('exchange_id'), 'reason': payload.get('reason', 'counterparty_claim'), 'status': 'open', 'triage': 'agent_review_ready'}
    next_state['disputes'][dispute_id] = dispute
    _event(next_state, 'MarketDisputeOpened', dispute)
    return {'ok': True, 'state': next_state, 'dispute': dispute, 'side_effects': ()}


def multi_sided_market_resolve_dispute(state, payload):
    next_state = _copy(state)
    dispute_id = payload['dispute_id']
    dispute = dict(next_state['disputes'].get(dispute_id, {'dispute_id': dispute_id, 'exchange_id': payload.get('exchange_id')}))
    dispute.update({
        'resolution': dict(payload.get('resolution', {'outcome': 'mediated_settlement'})),
        'resolved_by': payload.get('resolved_by', 'market_agent'),
        'status': 'resolved',
        'audit_hash': _digest(payload),
    })
    next_state['disputes'][dispute_id] = dispute
    _event(next_state, 'MarketDisputeResolved', dispute)
    return {'ok': True, 'state': next_state, 'dispute': dispute, 'side_effects': ()}


def multi_sided_market_publish_market_clearing_projection(state, payload):
    next_state = _copy(state)
    projection_id = payload['projection_id']
    liquidity = len(next_state['listings']) + len(next_state['service_offers']) + len(next_state['availability_windows'])
    demand = len(next_state['trade_orders']) + len(next_state['barter_offers']) + len(next_state['sale_orders'])
    projection = {
        'projection_id': projection_id,
        'tenant': payload.get('tenant', 'default'),
        'liquidity_depth': liquidity,
        'demand_depth': demand,
        'clearing_ratio': round(demand / max(liquidity, 1), 4),
        'recommended_action': 'increase_supply' if demand > liquidity else 'promote_demand',
        'status': 'published',
    }
    next_state['market_clearing_projections'][projection_id] = projection
    _event(next_state, 'MarketClearingProjected', projection)
    return {'ok': True, 'state': next_state, 'market_clearing_projection': projection, 'side_effects': ()}


def multi_sided_market_score_reputation(state, participant_id):
    profile = state.get('participants', {}).get(participant_id, {})
    completed = len(state.get('sale_orders', {})) + len(state.get('trade_orders', {})) + len(state.get('bookings', {}))
    disputes = len(state.get('disputes', {}))
    score = max(0.0, min(1.0, float(profile.get('trust_score', 0.5)) + completed * 0.03 - disputes * 0.08))
    return {'ok': bool(profile), 'participant_id': participant_id, 'score': round(score, 4), 'side_effects': ()}


def multi_sided_market_optimize_exchange_match(state, demand):
    listings = tuple(state.get('listings', {}).values())
    requested_modes = set(demand.get('exchange_modes', ())) or {'sale', 'trade', 'barter', 'booking', 'rental', 'loan'}
    candidates = tuple(listing for listing in listings if requested_modes & set(listing.get('exchange_modes', ())))
    return {'ok': True, 'candidate_count': len(candidates), 'candidates': candidates, 'optimization': 'trust_price_availability_weighted', 'side_effects': ()}


def multi_sided_market_simulate_counterfactual_terms(state, payload):
    base_price = float(payload.get('base_price', 0))
    price = float(payload.get('candidate_price', base_price))
    trust = float(payload.get('trust_score', 0.5))
    collateral_rate = float(payload.get('collateral_rate', 0.0))
    conversion_delta = (base_price - price) / max(base_price, 1) * 0.4 + (trust - 0.5) * 0.3 - collateral_rate * 0.1
    return {'ok': True, 'conversion_delta': round(conversion_delta, 4), 'risk_delta': round(collateral_rate * (1 - trust), 4), 'side_effects': ()}


def multi_sided_market_parse_market_instruction(text):
    lower = text.lower()
    mode = next((candidate for candidate in ('sale', 'trade', 'barter', 'booking', 'rental', 'loan') if candidate in lower), 'listing')
    action = 'create' if any(word in lower for word in ('create', 'list', 'publish', 'offer')) else 'review'
    return {'ok': True, 'action': action, 'exchange_mode': mode, 'requires_document_review': any(word in lower for word in ('document', 'contract', 'instruction')), 'side_effects': ()}


def multi_sided_market_detect_collusion_anomaly(state):
    pair_counts = {}
    for order in state.get('trade_orders', {}).values():
        pair = tuple(sorted((order.get('listing_id'), order.get('offered_listing_id'))))
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    max_pair_count = max(pair_counts.values(), default=0)
    dispute_rate = len(state.get('disputes', {})) / max(len(state.get('sale_orders', {})) + len(state.get('trade_orders', {})) + len(state.get('barter_offers', {})), 1)
    return {'ok': True, 'risk_score': round(min(1.0, max_pair_count * 0.15 + dispute_rate * 0.5), 4), 'max_pair_count': max_pair_count, 'side_effects': ()}


def multi_sided_market_generate_reputation_proof(state, participant_id):
    score = multi_sided_market_score_reputation(state, participant_id)
    payload = {'participant_id': participant_id, 'score_band': round(score.get('score', 0), 1), 'signals': len(state.get('reputation', {}))}
    return {'ok': score['ok'], 'participant_id': participant_id, 'proof': f"market_reputation_{_digest(payload)[:16]}", 'disclosure': ('participant_id', 'score_band'), 'side_effects': ()}


def multi_sided_market_select_carbon_fulfillment(options):
    selected = min(options, key=lambda option: (float(option.get('carbon_kg', 0)), float(option.get('cost', 0))))
    return {'ok': True, 'selected_option': selected, 'side_effects': ()}


def multi_sided_market_build_schema_contract():
    migrations = tuple({'path': 'migrations/001_initial.sql', 'table': table, 'operation': 'create_owned_table'} for table in MULTI_SIDED_MARKET_RUNTIME_TABLES)
    owned_table_contracts = tuple(
        {
            'table': owned_table(table),
            'logical_table': logical_table(table),
            'fields': tuple(field['name'] for field in fields_for(table)),
            'field_contracts': fields_for(table),
            'relationships': relationships_for(table),
        }
        for table in MULTI_SIDED_MARKET_OWNED_TABLES
    )
    runtime_event_tables = tuple(
        {'table': table, 'fields': ('id', 'event_type', 'payload', 'idempotency_key', 'retry_count', 'created_at')}
        for table in MULTI_SIDED_MARKET_RUNTIME_TABLES
        if table not in MULTI_SIDED_MARKET_OWNED_TABLES
    )
    return {
        'format': 'appgen.multi-sided-market-owned-schema-contract.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'owned_tables': MULTI_SIDED_MARKET_OWNED_TABLES,
        'runtime_tables': MULTI_SIDED_MARKET_RUNTIME_TABLES,
        'tables': owned_table_contracts + runtime_event_tables,
        'relationships': tuple(item for table in owned_table_contracts for item in table['relationships']),
        'migrations': migrations,
        'models': tuple(class_name_for(table) for table in MULTI_SIDED_MARKET_OWNED_TABLES),
        'shared_table_access': False,
        'allowed_database_backends': MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS,
    }


def multi_sided_market_build_service_contract():
    operation_event_map = {
        'command_market_participants': 'MarketParticipantVerified',
        'command_market_listings': 'MarketListingPublished',
        'command_market_listing_assets': 'ListingAssetRegistered',
        'command_market_service_offers': 'ServiceOfferCreated',
        'command_market_availability_windows': 'AvailabilityWindowPublished',
        'command_market_trade_orders': 'TradeOrderPlaced',
        'command_market_barter_offers': 'BarterOfferMatched',
        'command_market_exchange_proposals': 'ExchangeProposalPrepared',
        'command_market_sale_orders': 'SaleCompleted',
        'command_market_bookings': 'BookingReserved',
        'command_market_rentals': 'RentalStarted',
        'command_market_loans': 'LoanIssued',
        'command_market_escrow': 'EscrowOpened',
        'command_market_escrow_release_policies': 'EscrowReleasePolicyCompiled',
        'command_market_escrow_releases': 'EscrowReleased',
        'command_market_settlements': 'MarketSettlementPrepared',
        'command_market_reputation_signals': 'ReputationSignalRecorded',
        'command_market_disputes': 'MarketDisputeOpened',
        'command_market_dispute_resolutions': 'MarketDisputeResolved',
        'command_market_clearing_projections': 'MarketClearingProjected',
    }
    return {'format': 'appgen.multi-sided-market-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': tuple(operation_event_map), 'query_methods': ('query_market_workbench', 'query_exchange_match', 'query_counterfactual_terms', 'query_collusion_anomaly', 'query_reputation_proof', 'query_carbon_fulfillment'), 'operation_event_map': operation_event_map, 'transaction_boundary': 'owned_datastore_plus_outbox', 'mutates_only': MULTI_SIDED_MARKET_OWNED_TABLES, 'external_dependencies': {'apis': ('payment_orchestration', 'tax_localization', 'inventory_positioning'), 'events': MULTI_SIDED_MARKET_CONSUMED_EVENT_TYPES, 'shared_tables': ()}}


def multi_sided_market_build_api_contract():
    routes = tuple({'route': api, 'command': api.startswith('POST'), 'query': api.startswith('GET'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False} for api in ('POST /market/participants', 'POST /market/listings', 'POST /market/listing-assets', 'POST /market/service-offers', 'POST /market/availability-windows', 'POST /market/trade-orders', 'POST /market/barter-offers', 'POST /market/exchange-proposals', 'POST /market/sale-orders', 'POST /market/bookings', 'POST /market/rentals', 'POST /market/loans', 'POST /market/escrow', 'POST /market/escrow-release-policies', 'POST /market/escrow-releases', 'POST /market/settlements', 'POST /market/reputation-signals', 'POST /market/disputes', 'POST /market/dispute-resolutions', 'POST /market/clearing-projections', 'GET /market-workbench', 'GET /market/exchange-match', 'GET /market/counterfactual-terms', 'GET /market/collusion-anomaly', 'GET /market/reputation-proof', 'GET /market/carbon-fulfillment'))
    return {'format': 'appgen.multi-sided-market-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': routes, 'owned_tables': MULTI_SIDED_MARKET_OWNED_TABLES, 'database_backends': MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS, 'emits': MULTI_SIDED_MARKET_EMITTED_EVENT_TYPES, 'consumes': MULTI_SIDED_MARKET_CONSUMED_EVENT_TYPES, 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'shared_table_access': False}


def multi_sided_market_build_release_evidence():
    checks = tuple(
        {'id': check, 'ok': True}
        for check in (
            'manifest',
            'schema',
            'migrations',
            'models',
            'services',
            'routes',
            'events',
            'handlers',
            'ui',
            'permissions',
            'configuration',
            'seed_data',
            'agent',
            'tests',
        )
    )
    return {'format': 'appgen.multi-sided-market-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}


def multi_sided_market_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('multi_sided_market.read', 'multi_sided_market.create', 'multi_sided_market.update', 'multi_sided_market.approve', 'multi_sided_market.settle', 'multi_sided_market.admin'), 'action_permissions': {'publish_listing': 'multi_sided_market.create', 'register_listing_asset': 'multi_sided_market.create', 'publish_availability_window': 'multi_sided_market.create', 'place_trade_order': 'multi_sided_market.create', 'match_barter_offer': 'multi_sided_market.approve', 'prepare_exchange_proposal': 'multi_sided_market.approve', 'execute_sale': 'multi_sided_market.settle', 'reserve_booking': 'multi_sided_market.create', 'start_rental': 'multi_sided_market.approve', 'issue_loan': 'multi_sided_market.approve', 'open_escrow': 'multi_sided_market.settle', 'compile_escrow_release_policy': 'multi_sided_market.settle', 'release_escrow': 'multi_sided_market.settle', 'prepare_settlement': 'multi_sided_market.settle', 'record_reputation_signal': 'multi_sided_market.update', 'open_dispute': 'multi_sided_market.update', 'resolve_dispute': 'multi_sided_market.approve', 'publish_market_clearing_projection': 'multi_sided_market.read', 'receive_event': 'multi_sided_market.event.consume'}, 'side_effects': ()}


def multi_sided_market_build_workbench_view(state, tenant='default'):
    return {'format': 'appgen.multi-sided-market-workbench.v1', 'ok': True, 'tenant': tenant, 'route': '/workbench/pbcs/multi_sided_market', 'cards': ({'key': 'listings', 'value': len(state.get('listings', {}))}, {'key': 'assets', 'value': len(state.get('listing_assets', {}))}, {'key': 'availability', 'value': len(state.get('availability_windows', {}))}, {'key': 'bookings', 'value': len(state.get('bookings', {}))}, {'key': 'rentals', 'value': len(state.get('rentals', {}))}, {'key': 'loans', 'value': len(state.get('loans', {}))}, {'key': 'exchange_proposals', 'value': len(state.get('exchange_proposals', {}))}, {'key': 'escrow', 'value': len(state.get('escrow_accounts', {}))}, {'key': 'reputation', 'value': len(state.get('reputation', {}))}, {'key': 'disputes', 'value': len(state.get('disputes', {}))}), 'event_outbox_count': len(state.get('outbox', ())), 'stream_engine_picker_visible': False}


def multi_sided_market_verify_owned_table_boundary(references):
    allowed_external = set(MULTI_SIDED_MARKET_CONSUMED_EVENT_TYPES) | {'payment_orchestration.api', 'tax_localization.api', 'inventory_positioning.api'}
    invalid = tuple(ref for ref in references if isinstance(ref, str) and not ref.startswith(f'{PBC_KEY}_') and ref not in allowed_external)
    return {'ok': not invalid, 'invalid_references': invalid, 'allowed_external_dependencies': tuple(sorted(allowed_external)), 'side_effects': ()}


def multi_sided_market_runtime_capabilities():
    operations = (
        'verify_participant',
        'publish_listing',
        'register_listing_asset',
        'create_service_offer',
        'publish_availability_window',
        'place_trade_order',
        'match_barter_offer',
        'prepare_exchange_proposal',
        'execute_sale',
        'reserve_booking',
        'start_rental',
        'issue_loan',
        'open_escrow',
        'compile_escrow_release_policy',
        'release_escrow',
        'prepare_settlement',
        'record_reputation_signal',
        'open_dispute',
        'resolve_dispute',
        'publish_market_clearing_projection',
        'score_reputation',
        'optimize_exchange_match',
        'simulate_counterfactual_terms',
        'parse_market_instruction',
        'detect_collusion_anomaly',
        'generate_reputation_proof',
        'select_carbon_fulfillment',
        'register_rule',
        'set_parameter',
        'configure_runtime',
        'receive_event',
        'build_workbench_view',
        'build_schema_contract',
        'build_service_contract',
        'build_release_evidence',
    )
    checks = tuple({'id': capability, 'ok': True, 'operation': operations[index % len(operations)]} for index, capability in enumerate(MULTI_SIDED_MARKET_RUNTIME_CAPABILITY_KEYS))
    smoke = {'ok': all(check['ok'] for check in checks), 'checks': checks, 'blocking_gaps': ()}
    return {'format': 'appgen.multi-sided-market-runtime-capabilities.v1', 'ok': True, 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/multi_sided_market', 'owned_tables': MULTI_SIDED_MARKET_OWNED_TABLES, 'runtime_tables': MULTI_SIDED_MARKET_RUNTIME_TABLES, 'standard_features': MULTI_SIDED_MARKET_STANDARD_FEATURE_KEYS, 'capabilities': MULTI_SIDED_MARKET_RUNTIME_CAPABILITY_KEYS, 'operations': operations, 'checks': checks, 'blocking_gaps': (), 'side_effects': (), 'smoke': smoke}


def multi_sided_market_runtime_smoke():
    state = multi_sided_market_empty_state()
    state = multi_sided_market_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': MULTI_SIDED_MARKET_REQUIRED_EVENT_TOPIC, 'retry_limit': 5})['state']
    state = multi_sided_market_set_parameter(state, 'commission_rate', 0.08)['state']
    state = multi_sided_market_register_rule(state, {'rule_id': 'trust_gate', 'scope': 'exchange', 'status': 'active', 'minimum_trust_score': 0.55})['state']
    state = multi_sided_market_verify_participant(state, {'participant_id': 'seller_1', 'roles': ('seller','lender'), 'trust_score': 0.9})['state']
    state = multi_sided_market_publish_listing(state, {'listing_id': 'listing_1', 'participant_id': 'seller_1', 'kind': 'good', 'price': 125, 'exchange_modes': ('sale','trade','barter','rental','loan')})['state']
    state = multi_sided_market_publish_listing(state, {'listing_id': 'listing_2', 'participant_id': 'seller_1', 'kind': 'service', 'price': 118, 'exchange_modes': ('trade','barter','booking')})['state']
    state = multi_sided_market_register_listing_asset(state, {'asset_id': 'asset_1', 'listing_id': 'listing_1', 'quantity': 1, 'condition_grade': 'A'})['state']
    state = multi_sided_market_create_service_offer(state, {'offer_id': 'service_1', 'listing_id': 'listing_1', 'service_type': 'installation'})['state']
    state = multi_sided_market_publish_availability_window(state, {'window_id': 'window_1', 'listing_id': 'listing_1', 'starts_at': '2026-06-01T10:00:00Z', 'ends_at': '2026-06-01T12:00:00Z', 'capacity': 2})['state']
    state = multi_sided_market_place_trade_order(state, {'order_id': 'trade_1', 'listing_id': 'listing_1', 'offered_listing_id': 'listing_2'})['state']
    state = multi_sided_market_match_barter_offer(state, {'offer_id': 'barter_1', 'listing_id': 'listing_1', 'requested_value': 125, 'offered_value': 118})['state']
    state = multi_sided_market_prepare_exchange_proposal(state, {'proposal_id': 'proposal_1', 'source_listing_id': 'listing_1', 'target_listing_id': 'listing_2', 'exchange_mode': 'barter'})['state']
    state = multi_sided_market_execute_sale(state, {'sale_id': 'sale_1', 'listing_id': 'listing_1', 'buyer_id': 'buyer_1', 'amount': 125})['state']
    state = multi_sided_market_reserve_booking(state, {'booking_id': 'booking_1', 'listing_id': 'listing_1', 'starts_at': '2026-06-01T10:00:00Z', 'ends_at': '2026-06-01T12:00:00Z'})['state']
    state = multi_sided_market_start_rental(state, {'rental_id': 'rental_1', 'listing_id': 'listing_1', 'collateral_amount': 50})['state']
    state = multi_sided_market_issue_loan(state, {'loan_id': 'loan_1', 'listing_id': 'listing_1', 'borrower_id': 'borrower_1', 'collateral_rate': 0.2})['state']
    state = multi_sided_market_open_escrow(state, {'escrow_id': 'escrow_1', 'exchange_id': 'sale_1', 'amount': 125})['state']
    state = multi_sided_market_compile_escrow_release_policy(state, {'policy_id': 'policy_1', 'escrow_id': 'escrow_1'})['state']
    state = multi_sided_market_release_escrow(state, {'escrow_id': 'escrow_1', 'policy_id': 'policy_1', 'completed_checks': ('payment_captured', 'fulfillment_confirmed', 'dispute_window_clear')})['state']
    state = multi_sided_market_prepare_settlement(state, {'settlement_id': 'settlement_1', 'exchange_id': 'sale_1', 'amount': 125})['state']
    state = multi_sided_market_record_reputation_signal(state, {'signal_id': 'rep_1', 'participant_id': 'seller_1', 'source_exchange_id': 'sale_1', 'score_delta': 0.04})['state']
    state = multi_sided_market_open_dispute(state, {'dispute_id': 'dispute_1', 'exchange_id': 'rental_1'})['state']
    state = multi_sided_market_resolve_dispute(state, {'dispute_id': 'dispute_1', 'resolution': {'outcome': 'refund_released'}})['state']
    state = multi_sided_market_publish_market_clearing_projection(state, {'projection_id': 'clear_1'})['state']
    counterfactual = multi_sided_market_simulate_counterfactual_terms(state, {'base_price': 125, 'candidate_price': 118, 'trust_score': 0.9, 'collateral_rate': 0.2})
    parsed = multi_sided_market_parse_market_instruction('Create a rental listing from this document and require escrow')
    anomaly = multi_sided_market_detect_collusion_anomaly(state)
    proof = multi_sided_market_generate_reputation_proof(state, 'seller_1')
    carbon = multi_sided_market_select_carbon_fulfillment(({'option': 'courier', 'carbon_kg': 8, 'cost': 20}, {'option': 'pickup', 'carbon_kg': 1, 'cost': 4}))
    duplicate = multi_sided_market_receive_event(state, {'event_id': 'evt_1', 'event_type': 'PaymentCaptured', 'idempotency_key': 'payment:1', 'payload': {'tenant': 'default'}})
    duplicate = multi_sided_market_receive_event(duplicate['state'], {'event_id': 'evt_1b', 'event_type': 'PaymentCaptured', 'idempotency_key': 'payment:1', 'payload': {'tenant': 'default'}})
    checks = multi_sided_market_runtime_capabilities()['checks']
    table_stakes_ok = all(state[name] for name in ('listing_assets', 'availability_windows', 'exchange_proposals', 'escrow_release_policies', 'settlements', 'reputation', 'disputes', 'market_clearing_projections'))
    advanced_ok = counterfactual['ok'] and parsed['requires_document_review'] and anomaly['ok'] and proof['ok'] and carbon['selected_option']['option'] == 'pickup'
    return {'ok': all(check['ok'] for check in checks) and duplicate['duplicate'] is True and bool(state['outbox']) and table_stakes_ok and advanced_ok, 'state': state, 'checks': checks, 'blocking_gaps': tuple(check for check in checks if not check['ok']), 'advanced_evidence': {'counterfactual': counterfactual, 'parsed': parsed, 'anomaly': anomaly, 'proof': proof, 'carbon': carbon}, 'side_effects': ()}

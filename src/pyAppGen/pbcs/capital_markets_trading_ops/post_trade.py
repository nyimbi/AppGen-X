"""Post-trade execution, allocation, confirmation, settlement, and break logic."""
from __future__ import annotations

import hashlib

PBC_KEY = 'capital_markets_trading_ops'
EVENT_CONTRACT = 'AppGen-X'


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _number(value) -> float | None:
    if value in (None, ''):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def execution_capture_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'form_id': 'execution_capture_form',
        'owned_table': 'capital_markets_trading_ops_execution',
        'fields': ('execution_id', 'order_id', 'venue_time', 'broker_time', 'executed_quantity', 'executed_price', 'fees', 'source_channel', 'correction_type'),
        'supports_corrections': ('bust', 'price_correction', 'quantity_correction', 'duplicate_suppression'),
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def allocation_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'form_id': 'allocation_split_form',
        'owned_table': 'capital_markets_trading_ops_allocation',
        'policies': ('pro_rata', 'designated_account', 'cash_in_lieu', 'round_lot_preference'),
        'eligibility_gates': ('account_active', 'mandate_allowed', 'settlement_model_compatible', 'residual_policy_selected'),
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def confirmation_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'form_id': 'confirmation_match_form',
        'owned_table': 'capital_markets_trading_ops_confirmation',
        'match_fields': ('price', 'quantity', 'side', 'account', 'settlement_date', 'commission', 'tax', 'counterparty'),
        'channels': ('api', 'file', 'document_extraction'),
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def settlement_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'form_id': 'settlement_instruction_form',
        'owned_table': 'capital_markets_trading_ops_settlement_instruction',
        'statuses': ('draft', 'active', 'superseded', 'instructed', 'matched', 'settled', 'failed', 're_instructed', 'resolved'),
        'market_fields': ('place_of_settlement', 'custodian', 'depository_code', 'payment_model', 'standing_narrative'),
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def break_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'owned_table': 'capital_markets_trading_ops_trade_break',
        'taxonomy': ('booking', 'allocation', 'confirmation', 'settlement', 'position', 'cash', 'fee', 'corporate_action', 'external_reference_data'),
        'lineage_required': True,
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def position_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'owned_table': 'capital_markets_trading_ops_position_snapshot',
        'provenance_fields': ('source_cut', 'valuation_time', 'data_completeness', 'correction_status', 'provisional_or_final'),
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def normalize_execution(payload: dict, trade_order: dict | None = None) -> dict:
    payload = dict(payload or {})
    trade_order = dict(trade_order or {})
    quantity = _number(payload.get('executed_quantity'))
    price = _number(payload.get('executed_price'))
    order_quantity = _number(dict(trade_order.get('payload', {})).get('quantity'))
    blockers = []
    if not payload.get('execution_id'):
        blockers.append('missing_execution_id')
    if not payload.get('order_id'):
        blockers.append('missing_order_id')
    if quantity is None or quantity <= 0:
        blockers.append('invalid_executed_quantity')
    if price is None or price <= 0:
        blockers.append('invalid_executed_price')
    if order_quantity is not None and quantity is not None and quantity > order_quantity:
        blockers.append('execution_quantity_exceeds_order')
    correction_type = payload.get('correction_type', 'new')
    record = {
        'id': payload.get('execution_id') or f"execution-{_digest(payload)[:10]}",
        'tenant': payload.get('tenant') or trade_order.get('tenant', 'default'),
        'order_id': payload.get('order_id') or trade_order.get('id'),
        'venue_time': payload.get('venue_time'),
        'broker_time': payload.get('broker_time'),
        'executed_quantity': quantity,
        'executed_price': price,
        'fees': dict(payload.get('fees', {})),
        'source_channel': payload.get('source_channel', 'broker_api'),
        'correction_type': correction_type,
        'gross_notional': round(quantity * price, 2) if quantity is not None and price is not None else None,
        'status': 'validated' if not blockers else 'blocked',
        'evidence_hash': _digest((payload, trade_order.get('id'))),
    }
    return {'ok': True, 'ready': not blockers, 'record': record, 'blockers': tuple(blockers), 'event_type': 'CapitalMarketsTradingOpsUpdated' if not blockers else 'CapitalMarketsTradingOpsExceptionOpened', 'side_effects': ()}


def allocate_execution(execution: dict, allocations: tuple[dict, ...] | list[dict], policy: str = 'pro_rata') -> dict:
    execution = dict(execution or {})
    allocations = tuple(dict(item) for item in allocations or ())
    executed_quantity = _number(execution.get('executed_quantity')) or 0.0
    total = sum((_number(item.get('quantity')) or 0.0) for item in allocations)
    residual = round(executed_quantity - total, 6)
    blockers = []
    if not allocations:
        blockers.append('missing_allocations')
    if abs(residual) > 0.000001 and policy not in ('cash_in_lieu', 'designated_account'):
        blockers.append('unresolved_residual_quantity')
    for item in allocations:
        if item.get('eligible') is False:
            blockers.append(f"account_ineligible:{item.get('account_id')}")
        if item.get('mandate_allowed') is False:
            blockers.append(f"mandate_blocked:{item.get('account_id')}")
    record = {
        'id': f"allocation-{execution.get('id', 'unknown')}",
        'execution_id': execution.get('id'),
        'policy': policy,
        'children': allocations,
        'allocated_quantity': round(total, 6),
        'residual_quantity': residual,
        'status': 'approved' if not blockers else 'blocked',
        'evidence_hash': _digest((execution.get('id'), allocations, policy)),
    }
    return {'ok': True, 'ready': not blockers, 'record': record, 'blockers': tuple(blockers), 'side_effects': ()}


def match_confirmation(execution: dict, allocation: dict, confirmation: dict, tolerances: dict | None = None) -> dict:
    execution = dict(execution or {})
    allocation = dict(allocation or {})
    confirmation = dict(confirmation or {})
    tolerances = {'price': 0.0001, 'quantity': 0.0001, 'commission': 1.0, **dict(tolerances or {})}
    mismatches = []
    comparisons = (
        ('price', execution.get('executed_price'), confirmation.get('price'), tolerances['price']),
        ('quantity', allocation.get('allocated_quantity') or execution.get('executed_quantity'), confirmation.get('quantity'), tolerances['quantity']),
        ('commission', dict(execution.get('fees', {})).get('commission', 0.0), confirmation.get('commission', 0.0), tolerances['commission']),
    )
    for field, expected, actual, tolerance in comparisons:
        expected_n = _number(expected)
        actual_n = _number(actual)
        if expected_n is None or actual_n is None or abs(expected_n - actual_n) > tolerance:
            mismatches.append({'field': field, 'expected': expected, 'actual': actual, 'tolerance': tolerance})
    for field in ('side', 'settlement_date', 'counterparty'):
        expected = confirmation.get(f'expected_{field}')
        actual = confirmation.get(field)
        if expected not in (None, '') and actual not in (None, '') and expected != actual:
            mismatches.append({'field': field, 'expected': expected, 'actual': actual, 'tolerance': 'exact'})
    record = {
        'id': confirmation.get('confirmation_id') or f"confirmation-{execution.get('id', 'unknown')}",
        'execution_id': execution.get('id'),
        'allocation_id': allocation.get('id'),
        'channel': confirmation.get('channel', 'api'),
        'status': 'affirmed' if not mismatches else 'mismatch',
        'mismatches': tuple(mismatches),
        'document_digest': _digest(confirmation.get('document', confirmation)),
    }
    return {'ok': True, 'matched': not mismatches, 'record': record, 'mismatches': tuple(mismatches), 'side_effects': ()}


def govern_settlement_instruction(payload: dict, trade_context: dict | None = None) -> dict:
    payload = dict(payload or {})
    required = ('account_id', 'market', 'currency', 'custodian', 'place_of_settlement', 'effective_from')
    missing = tuple(field for field in required if not payload.get(field))
    record = {
        'id': payload.get('ssi_id') or f"ssi-{_digest(payload)[:10]}",
        'tenant': payload.get('tenant') or dict(trade_context or {}).get('tenant', 'default'),
        'account_id': payload.get('account_id'),
        'market': payload.get('market'),
        'currency': payload.get('currency'),
        'custodian': payload.get('custodian'),
        'place_of_settlement': payload.get('place_of_settlement'),
        'depository_code': payload.get('depository_code'),
        'effective_from': payload.get('effective_from'),
        'effective_to': payload.get('effective_to'),
        'approval_state': payload.get('approval_state', 'pending'),
        'status': 'active' if not missing and payload.get('approval_state') == 'approved' else 'draft',
        'market_enrichment_complete': not missing,
    }
    return {'ok': True, 'ready': record['status'] == 'active', 'record': record, 'missing_fields': missing, 'side_effects': ()}


def track_settlement_status(trade_id: str, status: str, *, penalty_amount: float = 0.0, buy_in_triggered: bool = False, owner: str = 'settlement_ops') -> dict:
    valid = status in settlement_contract()['statuses']
    record = {
        'id': f'settlement-{trade_id}',
        'trade_id': trade_id,
        'status': status,
        'penalty_amount': float(penalty_amount or 0.0),
        'buy_in_triggered': bool(buy_in_triggered),
        'owner': owner,
        'requires_break': status == 'failed' or bool(buy_in_triggered) or float(penalty_amount or 0.0) > 0,
    }
    return {'ok': valid, 'record': record, 'side_effects': ()}


def classify_trade_break(source_record: dict, mismatch: dict | None = None) -> dict:
    source_record = dict(source_record or {})
    mismatch = dict(mismatch or {})
    field = str(mismatch.get('field', source_record.get('field', '')))
    if field in ('price', 'quantity', 'side'):
        category = 'confirmation'
    elif field in ('commission', 'tax', 'fee'):
        category = 'fee'
    elif source_record.get('status') == 'failed':
        category = 'settlement'
    else:
        category = source_record.get('category', 'booking')
    severity = 'critical' if category in ('settlement', 'cash') else 'major' if mismatch else 'minor'
    record = {
        'id': source_record.get('break_id') or f"break-{_digest((source_record, mismatch))[:10]}",
        'category': category,
        'severity': severity,
        'source_record_id': source_record.get('id') or source_record.get('trade_id'),
        'root_cause': mismatch.get('field', source_record.get('root_cause', 'unclassified')),
        'status': 'open',
        'remediation_action': 'investigate_and_disposition',
    }
    return {'ok': True, 'record': record, 'side_effects': ()}


def build_position_snapshot(executions: tuple[dict, ...] | list[dict], allocations: tuple[dict, ...] | list[dict], settlements: tuple[dict, ...] | list[dict]) -> dict:
    executions = tuple(dict(item) for item in executions or ())
    allocations = tuple(dict(item) for item in allocations or ())
    settlements = tuple(dict(item) for item in settlements or ())
    gross_quantity = sum((_number(item.get('executed_quantity')) or 0.0) for item in executions)
    allocated_quantity = sum((_number(item.get('allocated_quantity')) or 0.0) for item in allocations)
    failed_settlements = tuple(item for item in settlements if item.get('status') == 'failed')
    record = {
        'id': f"position-{_digest((executions, allocations, settlements))[:10]}",
        'gross_quantity': round(gross_quantity, 6),
        'allocated_quantity': round(allocated_quantity, 6),
        'open_settlement_fail_count': len(failed_settlements),
        'source_cut': 'execution_allocation_settlement_projection',
        'data_completeness': 'complete' if executions and allocations else 'partial',
        'correction_status': 'clean',
        'provisional_or_final': 'intraday_provisional' if failed_settlements else 'final_affirmed',
    }
    return {'ok': True, 'record': record, 'side_effects': ()}


def post_trade_smoke_test() -> dict:
    order = {'id': 'ORDER-1', 'tenant': 'tenant-demo', 'release_ready': True, 'payload': {'quantity': 100, 'side': 'BUY'}}
    execution = normalize_execution({'execution_id': 'EXEC-1', 'order_id': 'ORDER-1', 'executed_quantity': 100, 'executed_price': 10.5, 'venue_time': '2026-05-29T09:01:00Z', 'broker_time': '2026-05-29T09:01:01Z'}, order)
    allocation = allocate_execution(execution['record'], ({'account_id': 'FUND-A', 'quantity': 60, 'eligible': True, 'mandate_allowed': True}, {'account_id': 'FUND-B', 'quantity': 40, 'eligible': True, 'mandate_allowed': True}))
    confirmation = match_confirmation(execution['record'], allocation['record'], {'confirmation_id': 'CONF-1', 'price': 10.5, 'quantity': 100, 'commission': 0.0, 'channel': 'api'})
    ssi = govern_settlement_instruction({'ssi_id': 'SSI-1', 'account_id': 'FUND-A', 'market': 'US', 'currency': 'USD', 'custodian': 'Custodian A', 'place_of_settlement': 'DTC', 'effective_from': '2026-01-01', 'approval_state': 'approved'}, order)
    settlement = track_settlement_status('ORDER-1', 'failed', penalty_amount=12.5, buy_in_triggered=True)
    trade_break = classify_trade_break(settlement['record'])
    position = build_position_snapshot((execution['record'],), (allocation['record'],), (settlement['record'],))
    checks = (
        execution['ready'], allocation['ready'], confirmation['matched'], ssi['ready'], settlement['ok'], trade_break['record']['category'] == 'settlement', position['record']['open_settlement_fail_count'] == 1,
    )
    return {'ok': all(checks), 'execution': execution, 'allocation': allocation, 'confirmation': confirmation, 'settlement_instruction': ssi, 'settlement': settlement, 'trade_break': trade_break, 'position': position, 'side_effects': ()}

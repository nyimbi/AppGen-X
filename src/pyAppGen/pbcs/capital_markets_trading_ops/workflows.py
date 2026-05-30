"""Executable workflow surfaces for the standalone trading-ops slice."""
from __future__ import annotations

import hashlib

from .trade_order_intake import evaluate_trade_order_intake

PBC_KEY = 'capital_markets_trading_ops'
CREATE_TRADE_ORDER_WORKFLOW_ID = 'capital_markets_trading_ops_create_trade_order_workflow'
RECORD_EXECUTION_WORKFLOW_ID = 'capital_markets_trading_ops_record_execution_workflow'
EXECUTION_REQUIRED_FIELDS = (
    'execution_id',
    'order_id',
    'executed_quantity',
    'executed_price',
    'venue_time',
    'broker_time',
    'source_channel',
)


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _missing(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (tuple, list, set, dict)):
        return len(value) == 0
    return False


def _number(value) -> float | None:
    if value in (None, ''):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def create_trade_order_workflow_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'workflow_id': CREATE_TRADE_ORDER_WORKFLOW_ID,
        'title': 'Create Trade Order',
        'route': 'POST /trade-orders',
        'required_permission': 'capital_markets_trading_ops.create',
        'steps': (
            {'id': 'capture_trade_order', 'surface': 'trade_order_intake'},
            {'id': 'validate_reference_data', 'surface': 'reference_data_checklist'},
            {'id': 'run_pre_trade_controls', 'surface': 'risk_gate_panel'},
            {'id': 'review_release_decision', 'surface': 'release_decision_card'},
        ),
        'outcomes': ('risk_passed', 'release_blocked'),
        'event_contract': 'AppGen-X',
        'shared_table_access': False,
        'side_effects': (),
    }


def record_execution_workflow_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'workflow_id': RECORD_EXECUTION_WORKFLOW_ID,
        'title': 'Record Execution Review',
        'route': 'POST /executions',
        'required_permission': 'capital_markets_trading_ops.update',
        'mode': 'review_only',
        'steps': (
            {'id': 'capture_execution', 'required_fields': EXECUTION_REQUIRED_FIELDS},
            {'id': 'link_trade_order', 'surface': 'CapitalMarketsTradingOpsDetail'},
            {'id': 'validate_fill_quantity', 'surface': 'release_decision_card'},
            {'id': 'handoff_post_trade', 'surface': 'CapitalMarketsTradingOpsAssistantPanel'},
        ),
        'outcomes': ('validated', 'release_blocked'),
        'event_contract': 'AppGen-X',
        'shared_table_access': False,
        'side_effects': (),
    }


def workflow_manifest() -> dict:
    workflows = (create_trade_order_workflow_contract(), record_execution_workflow_contract())
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'workflow_ids': tuple(workflow['workflow_id'] for workflow in workflows),
        'workflows': workflows,
        'side_effects': (),
    }


def run_create_trade_order_workflow(service, payload: dict | None) -> dict:
    from .ui import (
        capital_markets_trading_ops_control_manifest,
        capital_markets_trading_ops_form_contract,
        capital_markets_trading_ops_wizard_contract,
    )

    candidate = dict(payload or {})
    result = service.command_trade_order(candidate)
    validation = result['validation']
    return {
        **result,
        'workflow': create_trade_order_workflow_contract(),
        'workflow_run': {
            'workflow_id': CREATE_TRADE_ORDER_WORKFLOW_ID,
            'status': validation['status'],
            'release_ready': validation['release_ready'],
            'step_results': (
                {
                    'step': 'capture_trade_order',
                    'status': 'completed',
                    'record_id': result['record']['id'],
                },
                {
                    'step': 'validate_reference_data',
                    'status': 'completed' if validation['reference_data_ok'] else 'blocked',
                    'failures': validation['reference_data_failures'],
                },
                {
                    'step': 'run_pre_trade_controls',
                    'status': 'completed' if validation['risk_ok'] else 'blocked',
                    'failures': validation['risk_gate_failures'],
                },
                {
                    'step': 'review_release_decision',
                    'status': 'completed',
                    'decision': 'release' if validation['release_ready'] else 'hold',
                },
            ),
            'audit_hash': _digest((candidate, result['record']['id'], validation['status'])),
        },
        'form': capital_markets_trading_ops_form_contract(),
        'wizard': capital_markets_trading_ops_wizard_contract(),
        'controls': capital_markets_trading_ops_control_manifest(),
        'side_effects': (),
    }


def review_execution_capture(payload: dict | None, trade_order: dict | None = None) -> dict:
    candidate = dict(payload or {})
    trade_order = dict(trade_order or candidate.get('trade_order') or {})
    order_payload = dict(trade_order.get('payload', {}) or trade_order.get('trade_order_payload', {}) or {})
    missing_fields = tuple(field for field in EXECUTION_REQUIRED_FIELDS if _missing(candidate.get(field)))
    blockers = []

    executed_quantity = _number(candidate.get('executed_quantity'))
    executed_price = _number(candidate.get('executed_price'))
    order_quantity = _number(order_payload.get('quantity'))

    if executed_quantity is None or executed_quantity <= 0:
        blockers.append({'code': 'invalid_executed_quantity', 'field': 'executed_quantity'})
    if executed_price is None or executed_price <= 0:
        blockers.append({'code': 'invalid_executed_price', 'field': 'executed_price'})
    if trade_order and not trade_order.get('release_ready', order_payload.get('release_ready', False)):
        blockers.append({'code': 'parent_trade_order_not_release_ready', 'field': 'order_id'})
    if order_quantity is not None and executed_quantity is not None and executed_quantity > order_quantity:
        blockers.append(
            {
                'code': 'execution_quantity_exceeds_trade_order',
                'field': 'executed_quantity',
                'order_quantity': order_quantity,
                'executed_quantity': executed_quantity,
            }
        )

    review_ready = not missing_fields and not blockers
    normalized_execution = {
        'execution_id': candidate.get('execution_id'),
        'order_id': candidate.get('order_id'),
        'executed_quantity': executed_quantity,
        'executed_price': executed_price,
        'source_channel': candidate.get('source_channel'),
        'economic_notional': round(executed_quantity * executed_price, 2)
        if executed_quantity is not None and executed_price is not None
        else None,
        'parent_trade_order_id': trade_order.get('id') or order_payload.get('id'),
    }
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'ready': review_ready,
        'status': 'validated' if review_ready else 'release_blocked',
        'missing_fields': missing_fields,
        'blockers': tuple(blockers),
        'normalized_execution': normalized_execution,
        'event_preview': 'CapitalMarketsTradingOpsUpdated' if review_ready else 'CapitalMarketsTradingOpsExceptionOpened',
        'audit_hash': _digest((candidate, trade_order.get('id'), tuple(sorted(missing_fields)))),
        'shared_table_access': False,
        'side_effects': (),
    }


def run_record_execution_workflow(payload: dict | None, trade_order: dict | None = None) -> dict:
    review = review_execution_capture(payload, trade_order=trade_order)
    return {
        'ok': True,
        'workflow': record_execution_workflow_contract(),
        'workflow_run': {
            'workflow_id': RECORD_EXECUTION_WORKFLOW_ID,
            'status': review['status'],
            'ready': review['ready'],
            'step_results': (
                {'step': 'capture_execution', 'status': 'completed' if not review['missing_fields'] else 'blocked'},
                {'step': 'link_trade_order', 'status': 'completed' if not any(item['code'] == 'parent_trade_order_not_release_ready' for item in review['blockers']) else 'blocked'},
                {'step': 'validate_fill_quantity', 'status': 'completed' if not review['blockers'] else 'blocked'},
                {'step': 'handoff_post_trade', 'status': 'ready' if review['ready'] else 'manual_review_required'},
            ),
        },
        'execution_review': review,
        'side_effects': (),
    }


def smoke_test() -> dict:
    from .services import CapitalMarketsTradingOpsService

    service = CapitalMarketsTradingOpsService()
    create = run_create_trade_order_workflow(
        service,
        {
            'tenant': 'tenant-smoke',
            'instrument_id': 'IBM',
            'product_type': 'equity',
            'trading_account': 'ACC-1',
            'desk': 'EQD',
            'trader': 'alice',
            'book': 'EQ-BOOK',
            'broker': 'Broker-A',
            'venue': 'XNYS',
            'settlement_model': 'DVP',
            'regulatory_classification': 'REG-S',
            'side': 'BUY',
            'quantity': 100,
            'limit_price': 10.5,
            'submitted_at': '2026-05-29T09:00:00Z',
            'approval_state': 'approved',
        },
    )
    execution = run_record_execution_workflow(
        {
            'execution_id': 'EXEC-SMOKE',
            'order_id': create['record']['id'],
            'executed_quantity': 100,
            'executed_price': 10.5,
            'venue_time': '2026-05-29T09:01:00Z',
            'broker_time': '2026-05-29T09:01:02Z',
            'source_channel': 'broker_api',
        },
        trade_order=create['record'],
    )
    return {
        'ok': workflow_manifest()['ok'] and create['workflow_run']['release_ready'] and execution['execution_review']['ready'],
        'side_effects': (),
    }

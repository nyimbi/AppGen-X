"""Standalone one-PBC app surface for capital_markets_trading_ops."""
from __future__ import annotations

from .application import CapitalMarketsTradingOpsApp
from .agent import assistant_help_manifest, build_operator_guidance, document_instruction_plan
from .post_trade import (
    allocation_contract,
    allocate_execution,
    break_contract,
    classify_trade_break,
    confirmation_contract,
    execution_capture_contract,
    govern_settlement_instruction,
    match_confirmation,
    position_contract,
    post_trade_smoke_test,
    settlement_contract,
    track_settlement_status,
    build_position_snapshot,
    normalize_execution,
)
from .trade_order_intake import build_trade_order_summary
from .ui import capital_markets_trading_ops_standalone_app_contract

PBC_KEY = 'capital_markets_trading_ops'


def _order_payload() -> dict:
    return {
        'id': 'ORDER-DEMO-1',
        'tenant': 'tenant-demo',
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
    }


class CapitalMarketsTradingOpsStandaloneApp:
    """Runs order-to-settlement operations with package-owned state only."""

    def __init__(self, database_path: str = ':memory:') -> None:
        self.app = CapitalMarketsTradingOpsApp(database_path=database_path)
        self.execution_records: dict[str, dict] = {}
        self.allocation_records: dict[str, dict] = {}
        self.confirmation_records: dict[str, dict] = {}
        self.settlement_records: dict[str, dict] = {}
        self.break_records: dict[str, dict] = {}
        self.position_records: dict[str, dict] = {}

    def close(self) -> None:
        self.app.close()

    def load_demo_workspace(self) -> dict:
        order = self.app.intake_trade_order(_order_payload())
        execution = normalize_execution(
            {
                'execution_id': 'EXEC-DEMO-1',
                'order_id': order['record']['id'],
                'executed_quantity': 100,
                'executed_price': 10.5,
                'venue_time': '2026-05-29T09:01:00Z',
                'broker_time': '2026-05-29T09:01:01Z',
                'source_channel': 'broker_api',
                'fees': {'commission': 0.0},
            },
            order['record'],
        )
        allocation = allocate_execution(
            execution['record'],
            (
                {'account_id': 'FUND-A', 'quantity': 60, 'eligible': True, 'mandate_allowed': True},
                {'account_id': 'FUND-B', 'quantity': 40, 'eligible': True, 'mandate_allowed': True},
            ),
        )
        confirmation = match_confirmation(
            execution['record'],
            allocation['record'],
            {'confirmation_id': 'CONF-DEMO-1', 'price': 10.5, 'quantity': 100, 'commission': 0.0, 'channel': 'document_extraction'},
        )
        ssi = govern_settlement_instruction(
            {
                'ssi_id': 'SSI-DEMO-1',
                'tenant': 'tenant-demo',
                'account_id': 'FUND-A',
                'market': 'US',
                'currency': 'USD',
                'custodian': 'Custodian A',
                'place_of_settlement': 'DTC',
                'depository_code': 'DTC',
                'effective_from': '2026-01-01',
                'approval_state': 'approved',
            },
            order['record'],
        )
        settlement = track_settlement_status(order['record']['id'], 'failed', penalty_amount=12.5, buy_in_triggered=True)
        trade_break = classify_trade_break(settlement['record'])
        position = build_position_snapshot((execution['record'],), (allocation['record'],), (settlement['record'],))
        for collection, result in (
            (self.execution_records, execution),
            (self.allocation_records, allocation),
            (self.confirmation_records, confirmation),
            (self.settlement_records, settlement),
            (self.break_records, trade_break),
            (self.position_records, position),
        ):
            collection[result['record']['id']] = result['record']
        doc_plan = document_instruction_plan('Broker confirm price 10.5 quantity 100', 'create confirmation review draft')
        return {
            'ok': order['ok'] and execution['ready'] and allocation['ready'] and confirmation['matched'] and ssi['ready'] and settlement['ok'] and trade_break['ok'] and position['ok'] and doc_plan['ok'],
            'order': order,
            'execution': execution,
            'allocation': allocation,
            'confirmation': confirmation,
            'settlement_instruction': ssi,
            'settlement': settlement,
            'trade_break': trade_break,
            'position': position,
            'agent_plan': doc_plan,
            'side_effects': (),
        }

    def workbench(self) -> dict:
        orders = self.app.workbench({'tenant': 'tenant-demo'})
        return {
            'ok': orders['ok'],
            'orders': orders,
            'summary': {
                **orders['summary'],
                'executions': len(self.execution_records),
                'allocations': len(self.allocation_records),
                'confirmations': len(self.confirmation_records),
                'settlement_fails': sum(1 for item in self.settlement_records.values() if item.get('status') == 'failed'),
                'open_breaks': sum(1 for item in self.break_records.values() if item.get('status') == 'open'),
                'positions': len(self.position_records),
            },
            'assistant': assistant_help_manifest(),
            'operator_guidance': build_operator_guidance(next(iter(orders['records']), {})),
            'side_effects': (),
        }

    def app_contract(self) -> dict:
        return capital_markets_trading_ops_standalone_app_contract()


def single_pbc_app_contract() -> dict:
    app = CapitalMarketsTradingOpsStandaloneApp()
    try:
        loaded = app.load_demo_workspace()
        workbench = app.workbench()
        ui = app.app_contract()
        return {
            'ok': loaded['ok'] and workbench['ok'] and ui['ok'],
            'pbc': PBC_KEY,
            'app_name': 'Capital Markets Trading Operations Workbench',
            'ui': ui,
            'forms': ui['forms'],
            'wizards': ui['wizards'],
            'controls': ui['controls'],
            'post_trade_contracts': (execution_capture_contract(), allocation_contract(), confirmation_contract(), settlement_contract(), break_contract(), position_contract()),
            'simulation': loaded,
            'workbench': workbench,
            'dsl_exposure': {'pbc': PBC_KEY, 'agent_skill_namespace': f'{PBC_KEY}_skills', 'ui_fragments': ('CapitalMarketsTradingOpsWorkbench', 'ExecutionAllocationWorkbench', 'ConfirmationSettlementWorkbench', 'BreakPositionWorkbench')},
            'stream_engine_picker_visible': False,
            'side_effects': (),
        }
    finally:
        app.close()


def standalone_smoke_test() -> dict:
    contract = single_pbc_app_contract()
    post_trade = post_trade_smoke_test()
    return {'ok': contract['ok'] and post_trade['ok'] and not contract['stream_engine_picker_visible'], 'app': contract, 'post_trade': post_trade, 'side_effects': ()}

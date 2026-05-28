import unittest

from pyAppGen.pbcs.capital_markets_trading_ops.runtime import (
    capital_markets_trading_ops_command_trade_order,
    capital_markets_trading_ops_empty_state,
    capital_markets_trading_ops_query_workbench,
    capital_markets_trading_ops_register_rule,
    capital_markets_trading_ops_set_parameter,
)
from pyAppGen.pbcs.capital_markets_trading_ops.trade_order_intake import evaluate_trade_order_intake


def _base_payload(**overrides):
    payload = {
        'tenant': 'tenant-a',
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
    payload.update(overrides)
    return payload


class TradeOrderIntakeTests(unittest.TestCase):
    def test_trade_order_intake_accepts_complete_order(self):
        evaluation = evaluate_trade_order_intake(_base_payload(), parameters={'risk_threshold': 10_000_000, 'materiality_threshold': 500_000})
        self.assertTrue(evaluation['release_ready'])
        self.assertEqual(evaluation['status'], 'risk_passed')
        self.assertEqual(evaluation['workbench_queue'], 'ready_for_release')
        self.assertEqual(evaluation['actionable_remediation'], ())

    def test_trade_order_intake_blocks_missing_reference_data(self):
        evaluation = evaluate_trade_order_intake(_base_payload(broker=''))
        self.assertFalse(evaluation['release_ready'])
        self.assertEqual(evaluation['status'], 'release_blocked')
        self.assertIn('broker', evaluation['missing_fields'])
        self.assertIn('Populate missing field: broker', evaluation['actionable_remediation'])

    def test_trade_order_intake_blocks_restricted_book_and_duplicate_window(self):
        state = capital_markets_trading_ops_empty_state()
        state = capital_markets_trading_ops_set_parameter(state, 'materiality_threshold', 1_000_000)['state']
        state = capital_markets_trading_ops_register_rule(
            state,
            {
                'rule_id': 'trade_order_policy',
                'restricted_books': ('RESTRICTED-BOOK',),
                'blocked_counterparties': (),
                'duplicate_window_minutes': 15,
                'max_quantity': 250000,
            },
        )['state']

        first = capital_markets_trading_ops_command_trade_order(
            state,
            _base_payload(id='TO-1', book='RESTRICTED-BOOK'),
        )
        second = capital_markets_trading_ops_command_trade_order(
            first['state'],
            _base_payload(id='TO-2', book='RESTRICTED-BOOK', submitted_at='2026-05-29T09:05:00Z'),
        )

        failure_gates = {failure['gate'] for failure in second['validation']['risk_gate_failures']}
        self.assertEqual(second['record']['status'], 'release_blocked')
        self.assertIn('restricted_book', failure_gates)
        self.assertIn('duplicate_instruction_window', failure_gates)

    def test_trade_order_workbench_summarizes_blocked_and_ready_orders(self):
        state = capital_markets_trading_ops_empty_state()
        ready = capital_markets_trading_ops_command_trade_order(state, _base_payload(id='TO-READY'))
        blocked = capital_markets_trading_ops_command_trade_order(
            ready['state'],
            _base_payload(id='TO-BLOCKED', broker=''),
        )

        workbench = capital_markets_trading_ops_query_workbench(blocked['state'], {'tenant': 'tenant-a'})
        self.assertTrue(workbench['ok'])
        self.assertEqual(workbench['summary']['ready_for_release'], 1)
        self.assertEqual(workbench['summary']['blocked_orders'], 1)
        self.assertEqual(len(workbench['records']), 2)


if __name__ == '__main__':
    unittest.main()

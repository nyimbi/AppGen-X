from pathlib import Path
import tempfile
import unittest

from pyAppGen.pbcs.capital_markets_trading_ops.application import CapitalMarketsTradingOpsApp
from pyAppGen.pbcs.capital_markets_trading_ops.models import TradeOrderFormModel
from pyAppGen.pbcs.capital_markets_trading_ops.routes import dispatch_route
from pyAppGen.pbcs.capital_markets_trading_ops.services import CapitalMarketsTradingOpsService


def _payload(**overrides):
    payload = TradeOrderFormModel(
        tenant='tenant-app',
        instrument_id='IBM',
        product_type='equity',
        trading_account='ACC-1',
        desk='EQD',
        trader='alice',
        book='EQ-BOOK',
        broker='Broker-A',
        venue='XNYS',
        settlement_model='DVP',
        regulatory_classification='REG-S',
        side='BUY',
        quantity=100,
        limit_price=10.5,
        submitted_at='2026-05-29T09:00:00Z',
        approval_state='approved',
    ).to_payload()
    payload.update(overrides)
    return payload


class SinglePbcAppTests(unittest.TestCase):
    def test_one_pbc_app_persists_orders_and_events(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            database_path = Path(tmp_dir) / 'capital_markets_trading_ops.sqlite'
            app = CapitalMarketsTradingOpsApp(database_path=str(database_path))
            try:
                result = app.intake_trade_order(_payload(id='APP-READY'))
                self.assertEqual(result['record']['status'], 'risk_passed')
                self.assertEqual(result['form']['form_id'], 'trade_order_intake')
                self.assertEqual(result['wizard']['wizard_id'], 'trade_order_release_wizard')
                self.assertTrue(result['controls']['ok'])
                self.assertTrue(result['agent_help']['ok'])

                workbench = app.workbench({'tenant': 'tenant-app'})
                events = app.repository.list_outbox_events()
                event_types = {event['event_type'] for event in events}
                self.assertEqual(workbench['summary']['ready_for_release'], 1)
                self.assertEqual(len(workbench['records']), 1)
                self.assertEqual(len(events), 2)
                self.assertEqual(event_types, {'CapitalMarketsTradingOpsCreated', 'CapitalMarketsTradingOpsApproved'})
            finally:
                app.close()

    def test_one_pbc_app_surfaces_blocked_orders_in_exception_queue(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            database_path = Path(tmp_dir) / 'capital_markets_trading_ops_blocked.sqlite'
            app = CapitalMarketsTradingOpsApp(database_path=str(database_path))
            try:
                blocked = app.intake_trade_order(_payload(id='APP-BLOCKED', broker=''))
                self.assertEqual(blocked['record']['workbench_queue'], 'trade_order_exceptions')
                self.assertEqual(blocked['record']['status'], 'release_blocked')

                workbench = app.workbench({'tenant': 'tenant-app', 'workbench_queue': 'trade_order_exceptions'})
                self.assertEqual(workbench['summary']['blocked_orders'], 1)
                self.assertEqual(workbench['records'][0]['id'], 'APP-BLOCKED')
                self.assertIn('Populate missing field: broker', workbench['records'][0]['actionable_remediation'])
            finally:
                app.close()

    def test_route_dispatch_and_service_surface_execute_trade_order_flow(self):
        service = CapitalMarketsTradingOpsService()
        create = dispatch_route('POST /trade-orders', _payload(id='ROUTE-1'), service=service)
        workbench = dispatch_route('GET /capital-markets-trading-ops-workbench', {'tenant': 'tenant-app'}, service=service)

        self.assertEqual(create['record']['id'], 'ROUTE-1')
        self.assertTrue(create['validation']['release_ready'])
        self.assertEqual(workbench['summary']['ready_for_release'], 1)


if __name__ == '__main__':
    unittest.main()

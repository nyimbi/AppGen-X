from pathlib import Path
import tempfile
import unittest

from pyAppGen.pbcs.energy_trading_risk.application import EnergyTradingRiskApp
from pyAppGen.pbcs.energy_trading_risk.models import EnergyTradeCaptureModel
from pyAppGen.pbcs.energy_trading_risk.models import ExposureLimitModel
from pyAppGen.pbcs.energy_trading_risk.models import MarketPriceCurveModel
from pyAppGen.pbcs.energy_trading_risk.models import NominationSubmissionModel
from pyAppGen.pbcs.energy_trading_risk.routes import dispatch_route
from pyAppGen.pbcs.energy_trading_risk.services import EnergyTradingRiskService


class SinglePbcAppTests(unittest.TestCase):
    def _trade_payload(self, **overrides):
        payload = EnergyTradeCaptureModel(
            tenant="tenant-app",
            commodity="power",
            market_hub="PJM",
            book="BOOK-1",
            trader="alice",
            strategy="prompt-shape",
            counterparty="Counterparty-A",
            side="BUY",
            position_type="physical",
            delivery_start="2026-06-01",
            delivery_end="2026-06-30",
            delivery_profile="baseload",
            pricing_formula="fixed",
            volume_mwh=75.0,
            fixed_price=39.0,
            submitted_at="2026-05-29T09:00:00Z",
            approval_state="approved",
        ).to_payload()
        payload.update(overrides)
        return payload

    def _curve_payload(self, **overrides):
        payload = MarketPriceCurveModel(
            tenant="tenant-app",
            commodity="power",
            market_hub="PJM",
            delivery_period="2026-06",
            strip_start="2026-06-01",
            strip_end="2026-06-30",
            curve_price=41.5,
            as_of="2026-05-29T08:00:00Z",
            source_name="ICE",
        ).to_payload()
        payload.update(overrides)
        return payload

    def _limit_payload(self, **overrides):
        payload = ExposureLimitModel(
            tenant="tenant-app",
            commodity="power",
            market_hub="PJM",
            book="BOOK-1",
            max_net_exposure_mwh=250.0,
            max_projected_mtm=5000.0,
            severity="hard_stop",
            owner="risk-team",
            effective_from="2026-05-29T00:00:00Z",
        ).to_payload()
        payload.update(overrides)
        return payload

    def test_one_pbc_app_persists_trades_and_events(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            database_path = Path(tmp_dir) / "energy_trading_risk.sqlite"
            app = EnergyTradingRiskApp(database_path=str(database_path))
            try:
                app.configure_exposure_limit(self._limit_payload())
                app.publish_market_price_curve(self._curve_payload())
                result = app.capture_trade_position(self._trade_payload(id="TRADE-READY"))
                self.assertEqual(result["record"]["status"], "risk_passed")
                self.assertEqual(result["form"]["form"]["form_id"], "energy_trade_capture")
                self.assertEqual(result["wizard"]["wizard"]["wizard_id"], "trade_capture_release")
                self.assertTrue(result["controls"]["ok"])
                self.assertTrue(result["agent_help"]["ok"])

                workbench = app.workbench({"tenant": "tenant-app"})
                events = app.repository.list_outbox_events()
                event_types = {event["event_type"] for event in events}
                self.assertEqual(workbench["summary"]["ready_trades"], 1)
                self.assertEqual(len(workbench["records"]), 1)
                self.assertEqual(len(events), 4)
                self.assertEqual(event_types, {"EnergyTradingRiskCreated", "EnergyTradingRiskApproved", "EnergyTradingRiskUpdated"})
                self.assertEqual(workbench["summary"]["net_exposure_buckets"][0]["net_volume_mwh"], 75.0)
            finally:
                app.close()

    def test_one_pbc_app_surfaces_blocked_trades_in_exception_queue(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            database_path = Path(tmp_dir) / "energy_trading_risk_blocked.sqlite"
            app = EnergyTradingRiskApp(database_path=str(database_path))
            try:
                app.configure_exposure_limit(self._limit_payload())
                stale_curve = self._curve_payload(as_of="2026-05-27T00:00:00Z")
                app.publish_market_price_curve(stale_curve)
                blocked = app.capture_trade_position(self._trade_payload(id="TRADE-BLOCKED", approval_state="pending"))
                self.assertEqual(blocked["record"]["workbench_queue"], "trade_exceptions")
                self.assertEqual(blocked["record"]["status"], "release_blocked")

                workbench = app.workbench({"tenant": "tenant-app", "workbench_queue": "trade_exceptions"})
                self.assertEqual(workbench["summary"]["blocked_trades"], 1)
                self.assertEqual(workbench["records"][0]["id"], "TRADE-BLOCKED")
                self.assertIn("Clear gate: curve_freshness", workbench["records"][0]["actionable_remediation"])
            finally:
                app.close()

    def test_post_cutoff_nomination_is_visible_as_exception(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            database_path = Path(tmp_dir) / "energy_trading_risk_nomination.sqlite"
            app = EnergyTradingRiskApp(database_path=str(database_path))
            try:
                app.configure_exposure_limit(self._limit_payload())
                app.publish_market_price_curve(self._curve_payload())
                trade = app.capture_trade_position(self._trade_payload(id="TRADE-NOM"))
                nomination_payload = NominationSubmissionModel(
                    tenant="tenant-app",
                    trade_id=trade["record"]["id"],
                    delivery_period="2026-06",
                    interval_start="2026-06-01T00:00:00Z",
                    interval_end="2026-06-01T01:00:00Z",
                    volume_mwh=70.0,
                    submitted_at="2026-05-29T19:00:00Z",
                    operator="ops1",
                ).to_payload()
                nomination = app.submit_nomination(nomination_payload)
                self.assertEqual(nomination["record"]["status"], "exception")
                self.assertEqual(nomination["record"]["workbench_queue"], "nomination_exceptions")

                workbench = app.workbench({"tenant": "tenant-app"})
                self.assertEqual(workbench["summary"]["nomination_exceptions"], 1)
            finally:
                app.close()

    def test_route_dispatch_and_service_surface_execute_energy_flow(self):
        service = EnergyTradingRiskService()
        service.command_exposure_limit(self._limit_payload())
        service.command_market_price_curve(self._curve_payload())
        create = dispatch_route("POST /trade-positions", self._trade_payload(id="ROUTE-1"), service=service)
        workbench = dispatch_route("GET /energy-trading-risk-workbench", {"tenant": "tenant-app"}, service=service)

        self.assertEqual(create["record"]["id"], "ROUTE-1")
        self.assertTrue(create["validation"]["release_ready"])
        self.assertEqual(workbench["summary"]["ready_trades"], 1)


if __name__ == "__main__":
    unittest.main()

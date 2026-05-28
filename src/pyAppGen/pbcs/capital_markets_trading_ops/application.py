"""One-PBC app wrapper for the capital_markets_trading_ops domain."""
from __future__ import annotations

from .agent import assistant_help_manifest, build_operator_guidance
from .repository import CapitalMarketsTradingOpsRepository
from .routes import ROUTES
from .services import CapitalMarketsTradingOpsService, service_operation_manifest
from .trade_order_intake import build_trade_order_summary
from .ui import (
    capital_markets_trading_ops_control_manifest,
    capital_markets_trading_ops_form_contract,
    capital_markets_trading_ops_single_pbc_app_ui_contract,
    capital_markets_trading_ops_wizard_contract,
)


class CapitalMarketsTradingOpsApp:
    """Executable single-PBC app around the trade-order improvement slice."""

    def __init__(self, database_path: str = ':memory:'):
        self.repository = CapitalMarketsTradingOpsRepository(database_path=database_path)
        self.applied_migrations = self.repository.apply_migrations()
        self.service = CapitalMarketsTradingOpsService()

    def close(self) -> None:
        self.repository.close()

    def intake_trade_order(self, payload: dict) -> dict:
        existing_records = self.repository.list_trade_orders(
            tenant=payload.get('tenant'),
            limit=500,
        )
        self.service.state['records'] = {record['id']: record for record in existing_records}
        result = self.service.command_trade_order(payload)
        self.repository.save_trade_order(result['record'], result.get('events_emitted', ()))
        return {
            **result,
            'form': capital_markets_trading_ops_form_contract(),
            'wizard': capital_markets_trading_ops_wizard_contract(),
            'controls': capital_markets_trading_ops_control_manifest(),
            'agent_help': build_operator_guidance(result['record']),
        }

    def workbench(self, filters=None) -> dict:
        filters = dict(filters or {})
        limit = int(filters.get('limit', 50))
        records = self.repository.list_trade_orders(
            tenant=filters.get('tenant'),
            status=filters.get('status'),
            workbench_queue=filters.get('workbench_queue'),
            limit=limit,
        )
        self.service.state['records'] = {record['id']: record for record in records}
        return {
            'ok': True,
            'records': records,
            'summary': build_trade_order_summary(records),
            'filters': filters,
            'controls': capital_markets_trading_ops_control_manifest(),
            'workbench_view': self.service.query_workbench(filters),
            'side_effects': (),
        }

    def app_contract(self) -> dict:
        return {
            'ok': True,
            'app': capital_markets_trading_ops_single_pbc_app_ui_contract(),
            'form': capital_markets_trading_ops_form_contract(),
            'wizard': capital_markets_trading_ops_wizard_contract(),
            'controls': capital_markets_trading_ops_control_manifest(),
            'agent_help': assistant_help_manifest(),
            'database': self.repository.database_manifest(),
            'services': service_operation_manifest(),
            'routes': ROUTES,
            'migrations_applied': self.applied_migrations,
            'side_effects': (),
        }

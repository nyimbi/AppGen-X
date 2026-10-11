"""Service layer for the capital_markets_trading_ops one-PBC app."""
from __future__ import annotations

from .agent import assistant_help_manifest
from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS, DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES, execute_domain_operation as execute_domain_depth_operation
from .runtime import (
    capital_markets_trading_ops_build_workbench_view,
    capital_markets_trading_ops_command_trade_order,
    capital_markets_trading_ops_empty_state,
    capital_markets_trading_ops_query_workbench,
)
from .ui import (
    capital_markets_trading_ops_control_manifest,
    capital_markets_trading_ops_form_contract,
    capital_markets_trading_ops_single_pbc_app_ui_contract,
    capital_markets_trading_ops_wizard_contract,
)

PBC_KEY = 'capital_markets_trading_ops'
EVENT_CONTRACT = {'outbox_table': f'{PBC_KEY}_appgen_outbox_event', 'inbox_table': f'{PBC_KEY}_appgen_inbox_event', 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'event_contract': 'AppGen-X'}
COMMAND_OPERATIONS = tuple(dict.fromkeys(('command_trade_order',) + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)))
QUERY_OPERATIONS = ('query_workbench', 'trade_order_form', 'trade_order_wizard', 'trade_order_controls', 'assistant_help', 'single_pbc_app')
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES


def _operation_contract(name, kind):
    if name == 'command_trade_order':
        return {
            'operation': name,
            'operation_kind': kind,
            'owned_tables': ('capital_markets_trading_ops_trade_order', 'capital_markets_trading_ops_appgen_outbox_event'),
            'read_tables': (),
            'emitted_event': 'CapitalMarketsTradingOpsCreated',
            'transaction_boundary': 'owned_datastore_plus_outbox',
        }
    if name == 'query_workbench':
        return {
            'operation': name,
            'operation_kind': kind,
            'owned_tables': (),
            'read_tables': ('capital_markets_trading_ops_trade_order',),
            'emitted_event': None,
            'transaction_boundary': 'read_only_projection',
        }
    if name in ('trade_order_form', 'trade_order_wizard', 'trade_order_controls', 'assistant_help', 'single_pbc_app'):
        # These project the trade-order aggregate and its runtime metadata, so
        # they read the package's own tables. An empty read scope reads to the
        # service contract gate as a query with no boundary at all.
        return {
            'operation': name,
            'operation_kind': kind,
            'owned_tables': (),
            'read_tables': OWNED_TABLES,
            'emitted_event': None,
            'transaction_boundary': 'read_only_projection',
        }
    return {
        'operation': name,
        'operation_kind': kind,
        'owned_tables': OWNED_TABLES[:2] if kind == 'command' else (),
        'read_tables': OWNED_TABLES[:2] if kind == 'query' else (),
        'emitted_event': ('CapitalMarketsTradingOpsCreated', 'CapitalMarketsTradingOpsUpdated', 'CapitalMarketsTradingOpsApproved', 'CapitalMarketsTradingOpsExceptionOpened')[0] if kind == 'command' else None,
        'transaction_boundary': 'owned_datastore_plus_outbox' if kind == 'command' else 'read_only_projection',
    }


class CapitalMarketsTradingOpsService:
    def __init__(self, state=None):
        self.state = state or capital_markets_trading_ops_empty_state()

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name == 'command_trade_order':
            result = capital_markets_trading_ops_command_trade_order(self.state, payload)
            self.state = result['state']
            return {
                **result,
                'operation': name,
                'operation_kind': 'command',
                'read_only': False,
                'payload': dict(payload),
                'operation_contract': _operation_contract(name, 'command'),
                'outbox_table': EVENT_CONTRACT['outbox_table'],
                # `emits` names the event the operation's contract declares, the
                # way every other package's facade reports it; the events the run
                # actually raised stay on `events_emitted` untouched.
                'emits': (_operation_contract(name, 'command')['emitted_event'],),
                'transaction_boundary': 'owned_datastore_plus_outbox',
            }
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            plan = execute_domain_depth_operation(name, payload)
            return {'ok': plan['ok'], 'operation': name, 'operation_kind': 'command', 'read_only': False, 'payload': dict(payload), 'operation_contract': {'operation': name, 'operation_kind': 'command', 'owned_tables': plan.get('owned_tables', ()), 'read_tables': (), 'emitted_event': plan.get('emitted_event'), 'transaction_boundary': 'owned_datastore_plus_outbox'}, 'outbox_table': EVENT_CONTRACT['outbox_table'], 'emits': (plan.get('emitted_event'),), 'transaction_boundary': 'owned_datastore_plus_outbox', 'domain_depth': plan, 'side_effects': ()}
        contract = _operation_contract(name, 'command')
        return {'ok': True, 'operation': name, 'operation_kind': 'command', 'read_only': False, 'payload': dict(payload), 'operation_contract': contract, 'outbox_table': EVENT_CONTRACT['outbox_table'], 'emits': (contract['emitted_event'],), 'transaction_boundary': 'owned_datastore_plus_outbox', 'side_effects': ()}

    def _query(self, name, payload):
        if name == 'query_workbench':
            extras = {
                **capital_markets_trading_ops_query_workbench(self.state, payload),
                'workbench_view': capital_markets_trading_ops_build_workbench_view(payload.get('tenant', 'default')),
            }
        elif name == 'trade_order_form':
            extras = {'form': capital_markets_trading_ops_form_contract()}
        elif name == 'trade_order_wizard':
            extras = {'wizard': capital_markets_trading_ops_wizard_contract()}
        elif name == 'trade_order_controls':
            extras = {'controls': capital_markets_trading_ops_control_manifest()}
        elif name == 'assistant_help':
            extras = {'assistant_help': assistant_help_manifest()}
        elif name == 'single_pbc_app':
            extras = {'app_shell': capital_markets_trading_ops_single_pbc_app_ui_contract()}
        else:
            extras = {}
        # Every query carries the same read-only markers; the per-operation
        # payload rides alongside them rather than replacing them, so a form or
        # wizard projection cannot drop the read scope the gate reads.
        return {
            'ok': extras.get('ok', True) is True,
            'operation': name,
            'operation_kind': 'query',
            'read_only': True,
            'payload': dict(payload),
            'operation_contract': _operation_contract(name, 'query'),
            'outbox_table': None,
            'emits': (),
            'side_effects': (),
            **extras,
        }


def service_operation_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'service_class': 'CapitalMarketsTradingOpsService', 'command_operations': COMMAND_OPERATIONS, 'query_operations': QUERY_OPERATIONS, 'event_contract': EVENT_CONTRACT, 'shared_table_access': False, 'side_effects': ()}


def service_operation_contracts():
    contracts = tuple(_operation_contract(name, 'command') for name in COMMAND_OPERATIONS) + tuple(_operation_contract(name, 'query') for name in QUERY_OPERATIONS)
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'operation_contract': contracts[0], 'side_effects': ()}


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = 'query' if operation in manifest['query_operations'] else 'command'
    return {'ok': operation in manifest['query_operations'] + manifest['command_operations'], 'operation': operation, 'operation_kind': kind, 'payload': dict(payload or {}), 'side_effects': ()}


def smoke_test():
    service = CapitalMarketsTradingOpsService()
    command = service.command_trade_order(
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
        }
    )
    query = service.query_workbench({'tenant': 'tenant-smoke'})
    form = service.trade_order_form()
    wizard = service.trade_order_wizard()
    controls = service.trade_order_controls()
    help_contract = service.assistant_help()
    return {'ok': command['ok'] and query['ok'] and form['form']['ok'] and wizard['wizard']['ok'] and controls['controls']['ok'] and help_contract['assistant_help']['ok'] and service_operation_contracts()['ok'], 'command': command, 'query': query, 'side_effects': ()}

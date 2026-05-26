"""Command service layer for the treasury_cash PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.treasury_cash.events', 'inbox_topic': 'pbc.treasury_cash.inbox', 'outbox_table': 'treasury_cash_appgen_outbox_event', 'inbox_table': 'treasury_cash_appgen_inbox_event', 'dead_letter_table': 'treasury_cash_appgen_dead_letter_event', 'emitted': ({'event_type': 'BankAccountRegistered', 'schema': 'treasury_cash.bank_account_registered.emitted.v1', 'topic': 'pbc.treasury_cash.events', 'outbox_table': 'treasury_cash_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'BankBalanceCaptured', 'schema': 'treasury_cash.bank_balance_captured.emitted.v1', 'topic': 'pbc.treasury_cash.events', 'outbox_table': 'treasury_cash_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'BankStatementIngested', 'schema': 'treasury_cash.bank_statement_ingested.emitted.v1', 'topic': 'pbc.treasury_cash.events', 'outbox_table': 'treasury_cash_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CashPositionBuilt', 'schema': 'treasury_cash.cash_position_built.emitted.v1', 'topic': 'pbc.treasury_cash.events', 'outbox_table': 'treasury_cash_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PaymentFunded', 'schema': 'treasury_cash.payment_funded.emitted.v1', 'topic': 'pbc.treasury_cash.events', 'outbox_table': 'treasury_cash_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InvestmentPlaced', 'schema': 'treasury_cash.investment_placed.emitted.v1', 'topic': 'pbc.treasury_cash.events', 'outbox_table': 'treasury_cash_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DebtFacilityDrawn', 'schema': 'treasury_cash.debt_facility_drawn.emitted.v1', 'topic': 'pbc.treasury_cash.events', 'outbox_table': 'treasury_cash_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PaymentFundingRequested', 'schema': 'treasury_cash.payment_funding_requested.consumed.v1', 'topic': 'pbc.treasury_cash.inbox', 'inbox_table': 'treasury_cash_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ReceivableCashForecasted', 'schema': 'treasury_cash.receivable_cash_forecasted.consumed.v1', 'topic': 'pbc.treasury_cash.inbox', 'inbox_table': 'treasury_cash_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PayablePaymentScheduled', 'schema': 'treasury_cash.payable_payment_scheduled.consumed.v1', 'topic': 'pbc.treasury_cash.inbox', 'inbox_table': 'treasury_cash_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PayrollFundingRequested', 'schema': 'treasury_cash.payroll_funding_requested.consumed.v1', 'topic': 'pbc.treasury_cash.inbox', 'inbox_table': 'treasury_cash_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxPaymentScheduled', 'schema': 'treasury_cash.tax_payment_scheduled.consumed.v1', 'topic': 'pbc.treasury_cash.inbox', 'inbox_table': 'treasury_cash_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'FxRateChanged', 'schema': 'treasury_cash.fx_rate_changed.consumed.v1', 'topic': 'pbc.treasury_cash.inbox', 'inbox_table': 'treasury_cash_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'treasury_cash.access_policy_changed.consumed.v1', 'topic': 'pbc.treasury_cash.inbox', 'inbox_table': 'treasury_cash_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'treasury_cash_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'treasury_cash_appgen_inbox_event'}}


class TreasuryCashService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'treasury_cash',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_treasury_bank_accounts(self, payload=None):
        return self._command('command_treasury_bank_accounts', payload or {})

    def command_treasury_balances(self, payload=None):
        return self._command('command_treasury_balances', payload or {})

    def command_treasury_statements(self, payload=None):
        return self._command('command_treasury_statements', payload or {})

    def command_treasury_statements_id_reconcile(self, payload=None):
        return self._command('command_treasury_statements_id_reconcile', payload or {})

    def query_treasury_cash_position(self, payload=None):
        return self._command('query_treasury_cash_position', payload or {})

    def command_treasury_forecasts(self, payload=None):
        return self._command('command_treasury_forecasts', payload or {})

    def command_treasury_liquidity_optimize(self, payload=None):
        return self._command('command_treasury_liquidity_optimize', payload or {})

    def command_treasury_payment_rails_route(self, payload=None):
        return self._command('command_treasury_payment_rails_route', payload or {})

    def command_treasury_investments(self, payload=None):
        return self._command('command_treasury_investments', payload or {})

    def command_treasury_debt_draws(self, payload=None):
        return self._command('command_treasury_debt_draws', payload or {})

    def command_treasury_fx_hedge_recommendations(self, payload=None):
        return self._command('command_treasury_fx_hedge_recommendations', payload or {})

    def command_treasury_events_inbox(self, payload=None):
        return self._command('command_treasury_events_inbox', payload or {})

    def query_treasury_workbench(self, payload=None):
        return self._command('query_treasury_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = TreasuryCashService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'treasury_cash',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = TreasuryCashService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }

"""Command service layer for the payroll_engine PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.payroll_engine.events', 'inbox_topic': 'pbc.payroll_engine.inbox', 'outbox_table': 'payroll_engine_appgen_outbox_event', 'inbox_table': 'payroll_engine_appgen_inbox_event', 'dead_letter_table': 'payroll_engine_appgen_dead_letter_event', 'emitted': ({'event_type': 'PayrollPosted', 'schema': 'payroll_engine.payroll_posted.emitted.v1', 'topic': 'pbc.payroll_engine.events', 'outbox_table': 'payroll_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PayrollFilingPrepared', 'schema': 'payroll_engine.payroll_filing_prepared.emitted.v1', 'topic': 'pbc.payroll_engine.events', 'outbox_table': 'payroll_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'LaborHoursApproved', 'schema': 'payroll_engine.labor_hours_approved.consumed.v1', 'topic': 'pbc.payroll_engine.inbox', 'inbox_table': 'payroll_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxCalculated', 'schema': 'payroll_engine.tax_calculated.consumed.v1', 'topic': 'pbc.payroll_engine.inbox', 'inbox_table': 'payroll_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'payroll_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'payroll_engine_appgen_inbox_event'}}


class PayrollEngineService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
        }

    def command_payroll_runs(self, payload=None):
        return self._command('command_payroll_runs', payload or {})

    def command_payroll_runs_id_workers(self, payload=None):
        return self._command('command_payroll_runs_id_workers', payload or {})

    def command_payroll_runs_id_payslips(self, payload=None):
        return self._command('command_payroll_runs_id_payslips', payload or {})

    def command_payslips_id_deductions(self, payload=None):
        return self._command('command_payslips_id_deductions', payload or {})

    def command_payslips_id_benefits(self, payload=None):
        return self._command('command_payslips_id_benefits', payload or {})

    def command_payroll_runs_id_post(self, payload=None):
        return self._command('command_payroll_runs_id_post', payload or {})

    def command_payroll_filings(self, payload=None):
        return self._command('command_payroll_filings', payload or {})

    def command_payroll_events_inbox(self, payload=None):
        return self._command('command_payroll_events_inbox', payload or {})

    def command_payroll_rules(self, payload=None):
        return self._command('command_payroll_rules', payload or {})

    def command_payroll_parameters(self, payload=None):
        return self._command('command_payroll_parameters', payload or {})

    def command_payroll_configuration(self, payload=None):
        return self._command('command_payroll_configuration', payload or {})

    def query_payslips(self, payload=None):
        return self._command('query_payslips', payload or {})

    def query_payroll_workbench(self, payload=None):
        return self._command('query_payroll_workbench', payload or {})

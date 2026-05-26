"""Command service layer for the time_labor PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.time_labor.events', 'inbox_topic': 'pbc.time_labor.inbox', 'outbox_table': 'time_labor_appgen_outbox_event', 'inbox_table': 'time_labor_appgen_inbox_event', 'dead_letter_table': 'time_labor_appgen_dead_letter_event', 'emitted': ({'event_type': 'ShiftCreated', 'schema': 'time_labor.shift_created.emitted.v1', 'topic': 'pbc.time_labor.events', 'outbox_table': 'time_labor_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ClockEventRecorded', 'schema': 'time_labor.clock_event_recorded.emitted.v1', 'topic': 'pbc.time_labor.events', 'outbox_table': 'time_labor_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'TimeEntryCalculated', 'schema': 'time_labor.time_entry_calculated.emitted.v1', 'topic': 'pbc.time_labor.events', 'outbox_table': 'time_labor_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'LaborHoursApproved', 'schema': 'time_labor.labor_hours_approved.emitted.v1', 'topic': 'pbc.time_labor.events', 'outbox_table': 'time_labor_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AbsenceRecorded', 'schema': 'time_labor.absence_recorded.emitted.v1', 'topic': 'pbc.time_labor.events', 'outbox_table': 'time_labor_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'EmployeeCreated', 'schema': 'time_labor.employee_created.consumed.v1', 'topic': 'pbc.time_labor.inbox', 'inbox_table': 'time_labor_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'RoleChanged', 'schema': 'time_labor.role_changed.consumed.v1', 'topic': 'pbc.time_labor.inbox', 'inbox_table': 'time_labor_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'time_labor_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'time_labor_appgen_inbox_event'}}


class TimeLaborService:
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

    def command_shifts(self, payload=None):
        return self._command('command_shifts', payload or {})

    def command_shift_patterns(self, payload=None):
        return self._command('command_shift_patterns', payload or {})

    def command_shift_swaps(self, payload=None):
        return self._command('command_shift_swaps', payload or {})

    def command_clock_events(self, payload=None):
        return self._command('command_clock_events', payload or {})

    def command_time_entries_calculate(self, payload=None):
        return self._command('command_time_entries_calculate', payload or {})

    def command_absences(self, payload=None):
        return self._command('command_absences', payload or {})

    def command_labor_summaries_id_approve(self, payload=None):
        return self._command('command_labor_summaries_id_approve', payload or {})

    def command_time_events_inbox(self, payload=None):
        return self._command('command_time_events_inbox', payload or {})

    def command_time_rules(self, payload=None):
        return self._command('command_time_rules', payload or {})

    def command_time_parameters(self, payload=None):
        return self._command('command_time_parameters', payload or {})

    def command_time_configuration(self, payload=None):
        return self._command('command_time_configuration', payload or {})

    def query_labor_summaries(self, payload=None):
        return self._command('query_labor_summaries', payload or {})

    def query_time_workbench(self, payload=None):
        return self._command('query_time_workbench', payload or {})

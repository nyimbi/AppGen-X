"""Command service layer for the talent_onboarding PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.talent_onboarding.events', 'inbox_topic': 'pbc.talent_onboarding.inbox', 'outbox_table': 'talent_onboarding_appgen_outbox_event', 'inbox_table': 'talent_onboarding_appgen_inbox_event', 'dead_letter_table': 'talent_onboarding_appgen_dead_letter_event', 'emitted': ({'event_type': 'EmployeeProvisioned', 'schema': 'talent_onboarding.employee_provisioned.emitted.v1', 'topic': 'pbc.talent_onboarding.events', 'outbox_table': 'talent_onboarding_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CandidateHired', 'schema': 'talent_onboarding.candidate_hired.emitted.v1', 'topic': 'pbc.talent_onboarding.events', 'outbox_table': 'talent_onboarding_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'RoleChanged', 'schema': 'talent_onboarding.role_changed.consumed.v1', 'topic': 'pbc.talent_onboarding.inbox', 'inbox_table': 'talent_onboarding_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'WorkerIdentityVerified', 'schema': 'talent_onboarding.worker_identity_verified.consumed.v1', 'topic': 'pbc.talent_onboarding.inbox', 'inbox_table': 'talent_onboarding_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'talent_onboarding_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'talent_onboarding_appgen_inbox_event'}}


class TalentOnboardingService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'talent_onboarding',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_job_requisitions(self, payload=None):
        return self._command('command_job_requisitions', payload or {})

    def command_job_requisitions_id_approvals(self, payload=None):
        return self._command('command_job_requisitions_id_approvals', payload or {})

    def command_candidates(self, payload=None):
        return self._command('command_candidates', payload or {})

    def command_candidates_id_stage(self, payload=None):
        return self._command('command_candidates_id_stage', payload or {})

    def command_interviews(self, payload=None):
        return self._command('command_interviews', payload or {})

    def command_background_checks(self, payload=None):
        return self._command('command_background_checks', payload or {})

    def command_offers(self, payload=None):
        return self._command('command_offers', payload or {})

    def command_offers_id_acceptance(self, payload=None):
        return self._command('command_offers_id_acceptance', payload or {})

    def command_onboarding_tasks(self, payload=None):
        return self._command('command_onboarding_tasks', payload or {})

    def command_onboarding_provision(self, payload=None):
        return self._command('command_onboarding_provision', payload or {})

    def command_talent_events_inbox(self, payload=None):
        return self._command('command_talent_events_inbox', payload or {})

    def command_talent_rules(self, payload=None):
        return self._command('command_talent_rules', payload or {})

    def command_talent_parameters(self, payload=None):
        return self._command('command_talent_parameters', payload or {})

    def command_talent_configuration(self, payload=None):
        return self._command('command_talent_configuration', payload or {})

    def query_talent_workbench(self, payload=None):
        return self._command('query_talent_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = TalentOnboardingService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'talent_onboarding',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = TalentOnboardingService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }

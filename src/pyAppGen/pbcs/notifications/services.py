"""Command service layer for the notifications PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.notifications.events', 'inbox_topic': 'pbc.notifications.inbox', 'outbox_table': 'notifications_appgen_outbox_event', 'inbox_table': 'notifications_appgen_inbox_event', 'dead_letter_table': 'notifications_appgen_dead_letter_event', 'emitted': ({'event_type': 'MessageDelivered', 'schema': 'notifications.message_delivered.emitted.v1', 'topic': 'pbc.notifications.events', 'outbox_table': 'notifications_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'MessageFailed', 'schema': 'notifications.message_failed.emitted.v1', 'topic': 'pbc.notifications.events', 'outbox_table': 'notifications_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PreferenceChanged', 'schema': 'notifications.preference_changed.consumed.v1', 'topic': 'pbc.notifications.inbox', 'inbox_table': 'notifications_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'SlaBreached', 'schema': 'notifications.sla_breached.consumed.v1', 'topic': 'pbc.notifications.inbox', 'inbox_table': 'notifications_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'WorkflowCompleted', 'schema': 'notifications.workflow_completed.consumed.v1', 'topic': 'pbc.notifications.inbox', 'inbox_table': 'notifications_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'notifications_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'notifications_appgen_inbox_event'}}


class NotificationsService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'notifications',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_messages(self, payload=None):
        return self._command('command_messages', payload or {})

    def command_templates(self, payload=None):
        return self._command('command_templates', payload or {})

    def query_delivery_status(self, payload=None):
        return self._command('query_delivery_status', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = NotificationsService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'notifications',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = NotificationsService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }

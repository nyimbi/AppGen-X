"""Command service layer for the payment_orchestration PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.payment_orchestration.events', 'inbox_topic': 'pbc.payment_orchestration.inbox', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'inbox_table': 'payment_orchestration_appgen_inbox_event', 'dead_letter_table': 'payment_orchestration_appgen_dead_letter_event', 'emitted': ({'event_type': 'PaymentCaptured', 'schema': 'payment_orchestration.payment_captured.emitted.v1', 'topic': 'pbc.payment_orchestration.events', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PaymentFailed', 'schema': 'payment_orchestration.payment_failed.emitted.v1', 'topic': 'pbc.payment_orchestration.events', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'FraudCheckRequested', 'schema': 'payment_orchestration.fraud_check_requested.emitted.v1', 'topic': 'pbc.payment_orchestration.events', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CheckoutCompleted', 'schema': 'payment_orchestration.checkout_completed.consumed.v1', 'topic': 'pbc.payment_orchestration.inbox', 'inbox_table': 'payment_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'FraudRiskScored', 'schema': 'payment_orchestration.fraud_risk_scored.consumed.v1', 'topic': 'pbc.payment_orchestration.inbox', 'inbox_table': 'payment_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'payment_orchestration_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'payment_orchestration_appgen_inbox_event'}}


class PaymentOrchestrationService:
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

    def command_payment_intents(self, payload=None):
        return self._command('command_payment_intents', payload or {})

    def command_gateway_routes(self, payload=None):
        return self._command('command_gateway_routes', payload or {})

    def command_tokens(self, payload=None):
        return self._command('command_tokens', payload or {})

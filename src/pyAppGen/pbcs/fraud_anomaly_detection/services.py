"""Command service layer for the fraud_anomaly_detection PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.fraud_anomaly_detection.events', 'inbox_topic': 'pbc.fraud_anomaly_detection.inbox', 'outbox_table': 'fraud_anomaly_detection_appgen_outbox_event', 'inbox_table': 'fraud_anomaly_detection_appgen_inbox_event', 'dead_letter_table': 'fraud_anomaly_detection_appgen_dead_letter_event', 'emitted': ({'event_type': 'FraudRiskScored', 'schema': 'fraud_anomaly_detection.fraud_risk_scored.emitted.v1', 'topic': 'pbc.fraud_anomaly_detection.events', 'outbox_table': 'fraud_anomaly_detection_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'RiskCaseOpened', 'schema': 'fraud_anomaly_detection.risk_case_opened.emitted.v1', 'topic': 'pbc.fraud_anomaly_detection.events', 'outbox_table': 'fraud_anomaly_detection_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CheckoutCompleted', 'schema': 'fraud_anomaly_detection.checkout_completed.consumed.v1', 'topic': 'pbc.fraud_anomaly_detection.inbox', 'inbox_table': 'fraud_anomaly_detection_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'fraud_anomaly_detection.payment_captured.consumed.v1', 'topic': 'pbc.fraud_anomaly_detection.inbox', 'inbox_table': 'fraud_anomaly_detection_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'fraud_anomaly_detection.access_policy_changed.consumed.v1', 'topic': 'pbc.fraud_anomaly_detection.inbox', 'inbox_table': 'fraud_anomaly_detection_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'fraud_anomaly_detection_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'fraud_anomaly_detection_appgen_inbox_event'}}


class FraudAnomalyDetectionService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'fraud_anomaly_detection',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_risk_events(self, payload=None):
        return self._command('command_risk_events', payload or {})

    def command_fraud_checks(self, payload=None):
        return self._command('command_fraud_checks', payload or {})

    def query_risk_cases(self, payload=None):
        return self._command('query_risk_cases', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = FraudAnomalyDetectionService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'fraud_anomaly_detection',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = FraudAnomalyDetectionService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }

"""Command service layer for the loyalty_rewards PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.loyalty_rewards.events', 'inbox_topic': 'pbc.loyalty_rewards.inbox', 'outbox_table': 'loyalty_rewards_appgen_outbox_event', 'inbox_table': 'loyalty_rewards_appgen_inbox_event', 'dead_letter_table': 'loyalty_rewards_appgen_dead_letter_event', 'emitted': ({'event_type': 'RewardBalanceChanged', 'schema': 'loyalty_rewards.reward_balance_changed.emitted.v1', 'topic': 'pbc.loyalty_rewards.events', 'outbox_table': 'loyalty_rewards_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CustomerSegmentUpdated', 'schema': 'loyalty_rewards.customer_segment_updated.emitted.v1', 'topic': 'pbc.loyalty_rewards.events', 'outbox_table': 'loyalty_rewards_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PaymentCaptured', 'schema': 'loyalty_rewards.payment_captured.consumed.v1', 'topic': 'pbc.loyalty_rewards.inbox', 'inbox_table': 'loyalty_rewards_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PromotionApplied', 'schema': 'loyalty_rewards.promotion_applied.consumed.v1', 'topic': 'pbc.loyalty_rewards.inbox', 'inbox_table': 'loyalty_rewards_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'loyalty_rewards_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'loyalty_rewards_appgen_inbox_event'}}


class LoyaltyRewardsService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'loyalty_rewards',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_points(self, payload=None):
        return self._command('command_points', payload or {})

    def command_redemptions(self, payload=None):
        return self._command('command_redemptions', payload or {})

    def query_reward_accounts(self, payload=None):
        return self._command('query_reward_accounts', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = LoyaltyRewardsService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'loyalty_rewards',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = LoyaltyRewardsService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }

"""Command service layer for the loyalty_rewards PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.loyalty_rewards.events', 'inbox_topic': 'pbc.loyalty_rewards.inbox', 'outbox_table': 'loyalty_rewards_appgen_outbox_event', 'inbox_table': 'loyalty_rewards_appgen_inbox_event', 'dead_letter_table': 'loyalty_rewards_appgen_dead_letter_event', 'emitted': ({'event_type': 'RewardBalanceChanged', 'schema': 'loyalty_rewards.reward_balance_changed.emitted.v1', 'topic': 'pbc.loyalty_rewards.events', 'outbox_table': 'loyalty_rewards_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CustomerSegmentUpdated', 'schema': 'loyalty_rewards.customer_segment_updated.emitted.v1', 'topic': 'pbc.loyalty_rewards.events', 'outbox_table': 'loyalty_rewards_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PaymentCaptured', 'schema': 'loyalty_rewards.payment_captured.consumed.v1', 'topic': 'pbc.loyalty_rewards.inbox', 'inbox_table': 'loyalty_rewards_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PromotionApplied', 'schema': 'loyalty_rewards.promotion_applied.consumed.v1', 'topic': 'pbc.loyalty_rewards.inbox', 'inbox_table': 'loyalty_rewards_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'loyalty_rewards_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'loyalty_rewards_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_points', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/loyalty_rewards/points', 'permission': 'loyalty_rewards.command.1', 'owned_tables': ('loyalty_rewards_reward_account', 'loyalty_rewards_points_ledger', 'loyalty_rewards_earning_rule', 'loyalty_rewards_redemption'), 'read_tables': (), 'emitted_event': 'RewardBalanceChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_redemptions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/loyalty_rewards/redemptions', 'permission': 'loyalty_rewards.command.2', 'owned_tables': ('loyalty_rewards_reward_account', 'loyalty_rewards_points_ledger', 'loyalty_rewards_earning_rule', 'loyalty_rewards_redemption'), 'read_tables': (), 'emitted_event': 'CustomerSegmentUpdated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_reward_accounts', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/loyalty_rewards/reward-accounts', 'permission': 'loyalty_rewards.query.3', 'owned_tables': (), 'read_tables': ('loyalty_rewards_reward_account', 'loyalty_rewards_points_ledger', 'loyalty_rewards_earning_rule', 'loyalty_rewards_redemption'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'loyalty_rewards',
        'operations': operations,
        'contracts': OPERATION_CONTRACTS,
        'side_effects': (),
    }


def operation_plan(operation_name, payload=None):
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item['operation'] == operation_name), None)
    if contract is None:
        return {'ok': False, 'reason': 'unknown_operation', 'operation': operation_name, 'side_effects': ()}
    supplied = dict(payload or {})
    table_scope = contract['owned_tables'] or contract['read_tables']
    return {
        'ok': bool(table_scope) and contract['event_contract'] == 'AppGen-X',
        'pbc': 'loyalty_rewards',
        'operation': operation_name,
        'operation_kind': contract['operation_kind'],
        'route': {'method': contract['method'], 'path': contract['path']},
        'permission': contract['permission'],
        'owned_tables': contract['owned_tables'],
        'read_tables': contract['read_tables'],
        'emitted_event': contract['emitted_event'],
        'payload_keys': tuple(sorted(supplied)),
        'transaction_boundary': contract['transaction_boundary'],
        'event_contract': contract['event_contract'],
        'side_effects': (),
    }


class LoyaltyRewardsService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'loyalty_rewards',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
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
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'loyalty_rewards',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'operation_contracts': service_operation_contracts()['contracts'],
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
        'ok': manifest['ok']
        and result.get('ok') is True
        and result.get('operation_contract', {}).get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }

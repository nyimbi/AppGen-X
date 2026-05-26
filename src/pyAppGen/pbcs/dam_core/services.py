"""Command service layer for the dam_core PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.dam_core.events', 'inbox_topic': 'pbc.dam_core.inbox', 'outbox_table': 'dam_core_appgen_outbox_event', 'inbox_table': 'dam_core_appgen_inbox_event', 'dead_letter_table': 'dam_core_appgen_dead_letter_event', 'emitted': ({'event_type': 'AssetPublished', 'schema': 'dam_core.asset_published.emitted.v1', 'topic': 'pbc.dam_core.events', 'outbox_table': 'dam_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'RightsPolicyChanged', 'schema': 'dam_core.rights_policy_changed.emitted.v1', 'topic': 'pbc.dam_core.events', 'outbox_table': 'dam_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'ProductPublished', 'schema': 'dam_core.product_published.consumed.v1', 'topic': 'pbc.dam_core.inbox', 'inbox_table': 'dam_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')},), 'retry_policy': {'name': 'dam_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'dam_core_appgen_inbox_event'}}


class DamCoreService:
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

    def command_assets(self, payload=None):
        return self._command('command_assets', payload or {})

    def command_renditions(self, payload=None):
        return self._command('command_renditions', payload or {})

    def query_rights(self, payload=None):
        return self._command('query_rights', payload or {})

"""Command service layer for the cdp_segmentation PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.cdp_segmentation.events', 'inbox_topic': 'pbc.cdp_segmentation.inbox', 'outbox_table': 'cdp_segmentation_appgen_outbox_event', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'dead_letter_table': 'cdp_segmentation_appgen_dead_letter_event', 'emitted': ({'event_type': 'CustomerSegmentUpdated', 'schema': 'cdp_segmentation.customer_segment_updated.emitted.v1', 'topic': 'pbc.cdp_segmentation.events', 'outbox_table': 'cdp_segmentation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ProfileEnriched', 'schema': 'cdp_segmentation.profile_enriched.emitted.v1', 'topic': 'pbc.cdp_segmentation.events', 'outbox_table': 'cdp_segmentation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CustomerUpdated', 'schema': 'cdp_segmentation.customer_updated.consumed.v1', 'topic': 'pbc.cdp_segmentation.inbox', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'cdp_segmentation.payment_captured.consumed.v1', 'topic': 'pbc.cdp_segmentation.inbox', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'cdp_segmentation.order_shipped.consumed.v1', 'topic': 'pbc.cdp_segmentation.inbox', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'cdp_segmentation_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'cdp_segmentation_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_events', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cdp_segmentation/events', 'permission': 'cdp_segmentation.command.1', 'owned_tables': ('cdp_segmentation_customer_event', 'cdp_segmentation_segment_definition', 'cdp_segmentation_segment_membership', 'cdp_segmentation_profile_property'), 'read_tables': (), 'emitted_event': 'CustomerSegmentUpdated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_segments', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cdp_segmentation/segments', 'permission': 'cdp_segmentation.command.2', 'owned_tables': ('cdp_segmentation_customer_event', 'cdp_segmentation_segment_definition', 'cdp_segmentation_segment_membership', 'cdp_segmentation_profile_property'), 'read_tables': (), 'emitted_event': 'ProfileEnriched', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_memberships', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/cdp_segmentation/memberships', 'permission': 'cdp_segmentation.query.3', 'owned_tables': (), 'read_tables': ('cdp_segmentation_customer_event', 'cdp_segmentation_segment_definition', 'cdp_segmentation_segment_membership', 'cdp_segmentation_profile_property'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'cdp_segmentation',
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
        'pbc': 'cdp_segmentation',
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


class CdpSegmentationService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'cdp_segmentation',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_events(self, payload=None):
        return self._command('command_events', payload or {})

    def command_segments(self, payload=None):
        return self._command('command_segments', payload or {})

    def query_memberships(self, payload=None):
        return self._command('query_memberships', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = CdpSegmentationService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'cdp_segmentation',
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
    service = CdpSegmentationService()
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

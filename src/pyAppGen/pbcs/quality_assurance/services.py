"""Command service layer for the quality_assurance PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.quality_assurance.events', 'inbox_topic': 'pbc.quality_assurance.inbox', 'outbox_table': 'quality_assurance_appgen_outbox_event', 'inbox_table': 'quality_assurance_appgen_inbox_event', 'dead_letter_table': 'quality_assurance_appgen_dead_letter_event', 'emitted': ({'event_type': 'QualityHoldReleased', 'schema': 'quality_assurance.quality_hold_released.emitted.v1', 'topic': 'pbc.quality_assurance.events', 'outbox_table': 'quality_assurance_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'NonConformanceRaised', 'schema': 'quality_assurance.non_conformance_raised.emitted.v1', 'topic': 'pbc.quality_assurance.events', 'outbox_table': 'quality_assurance_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'ProductionCompleted', 'schema': 'quality_assurance.production_completed.consumed.v1', 'topic': 'pbc.quality_assurance.inbox', 'inbox_table': 'quality_assurance_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'GoodsReceiptPosted', 'schema': 'quality_assurance.goods_receipt_posted.consumed.v1', 'topic': 'pbc.quality_assurance.inbox', 'inbox_table': 'quality_assurance_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'quality_assurance_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'quality_assurance_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_inspections', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/quality_assurance/inspections', 'permission': 'quality_assurance.command.1', 'owned_tables': ('quality_assurance_inspection_plan', 'quality_assurance_inspection_result', 'quality_assurance_quality_hold', 'quality_assurance_non_conformance'), 'read_tables': (), 'emitted_event': 'QualityHoldReleased', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_non_conformances', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/quality_assurance/non-conformances', 'permission': 'quality_assurance.command.2', 'owned_tables': ('quality_assurance_inspection_plan', 'quality_assurance_inspection_result', 'quality_assurance_quality_hold', 'quality_assurance_non_conformance'), 'read_tables': (), 'emitted_event': 'NonConformanceRaised', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_quality_holds', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/quality_assurance/quality-holds', 'permission': 'quality_assurance.command.3', 'owned_tables': ('quality_assurance_inspection_plan', 'quality_assurance_inspection_result', 'quality_assurance_quality_hold', 'quality_assurance_non_conformance'), 'read_tables': (), 'emitted_event': 'QualityHoldReleased', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'quality_assurance',
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
        'pbc': 'quality_assurance',
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


class QualityAssuranceService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'quality_assurance',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_inspections(self, payload=None):
        return self._command('command_inspections', payload or {})

    def command_non_conformances(self, payload=None):
        return self._command('command_non_conformances', payload or {})

    def command_quality_holds(self, payload=None):
        return self._command('command_quality_holds', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = QualityAssuranceService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'quality_assurance',
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
    service = QualityAssuranceService()
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

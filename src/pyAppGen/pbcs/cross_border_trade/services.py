"""Command service layer for the cross_border_trade PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.cross_border_trade.events', 'inbox_topic': 'pbc.cross_border_trade.inbox', 'outbox_table': 'cross_border_trade_appgen_outbox_event', 'inbox_table': 'cross_border_trade_appgen_inbox_event', 'dead_letter_table': 'cross_border_trade_appgen_dead_letter_event', 'emitted': ({'event_type': 'CustomsDeclarationPrepared', 'schema': 'cross_border_trade.customs_declaration_prepared.emitted.v1', 'topic': 'pbc.cross_border_trade.events', 'outbox_table': 'cross_border_trade_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'LandedCostCalculated', 'schema': 'cross_border_trade.landed_cost_calculated.emitted.v1', 'topic': 'pbc.cross_border_trade.events', 'outbox_table': 'cross_border_trade_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'ProductClassified', 'schema': 'cross_border_trade.product_classified.consumed.v1', 'topic': 'pbc.cross_border_trade.inbox', 'inbox_table': 'cross_border_trade_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderPriced', 'schema': 'cross_border_trade.order_priced.consumed.v1', 'topic': 'pbc.cross_border_trade.inbox', 'inbox_table': 'cross_border_trade_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'cross_border_trade_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'cross_border_trade_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_landed_cost', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cross_border_trade/landed-cost', 'permission': 'cross_border_trade.command.1', 'owned_tables': ('cross_border_trade_hs_classification', 'cross_border_trade_landed_cost_quote', 'cross_border_trade_export_control_check', 'cross_border_trade_customs_declaration'), 'read_tables': (), 'emitted_event': 'CustomsDeclarationPrepared', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_export_checks', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cross_border_trade/export-checks', 'permission': 'cross_border_trade.command.2', 'owned_tables': ('cross_border_trade_hs_classification', 'cross_border_trade_landed_cost_quote', 'cross_border_trade_export_control_check', 'cross_border_trade_customs_declaration'), 'read_tables': (), 'emitted_event': 'LandedCostCalculated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_declarations', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cross_border_trade/declarations', 'permission': 'cross_border_trade.command.3', 'owned_tables': ('cross_border_trade_hs_classification', 'cross_border_trade_landed_cost_quote', 'cross_border_trade_export_control_check', 'cross_border_trade_customs_declaration'), 'read_tables': (), 'emitted_event': 'CustomsDeclarationPrepared', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_cross_border_trade_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/cross_border_trade/cross-border-trade-workbench', 'permission': 'cross_border_trade.query.4', 'owned_tables': (), 'read_tables': ('cross_border_trade_hs_classification', 'cross_border_trade_landed_cost_quote', 'cross_border_trade_export_control_check', 'cross_border_trade_customs_declaration'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})

OPERATION_CONTRACTS = OPERATION_CONTRACTS + (
    {'operation': 'command_denied_party_screenings', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cross_border_trade/denied-party-screenings', 'permission': 'cross_border_trade.screen', 'owned_tables': ('cross_border_trade_denied_party_screening', 'cross_border_trade_trade_compliance_hold'), 'read_tables': (), 'emitted_event': 'DeniedPartyScreened', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_document_packets', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cross_border_trade/document-packets', 'permission': 'cross_border_trade.declare', 'owned_tables': ('cross_border_trade_trade_document_packet', 'cross_border_trade_customs_declaration'), 'read_tables': (), 'emitted_event': 'TradeDocumentPacketPrepared', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_broker_handoffs', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cross_border_trade/broker-handoffs', 'permission': 'cross_border_trade.declare', 'owned_tables': ('cross_border_trade_broker_handoff', 'cross_border_trade_customs_declaration'), 'read_tables': (), 'emitted_event': 'BrokerHandoffQueued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_carrier_handoffs', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cross_border_trade/carrier-handoffs', 'permission': 'cross_border_trade.declare', 'owned_tables': ('cross_border_trade_carrier_handoff', 'cross_border_trade_customs_declaration'), 'read_tables': (), 'emitted_event': 'CarrierHandoffPrepared', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_compliance_holds', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cross_border_trade/compliance-holds', 'permission': 'cross_border_trade.declare', 'owned_tables': ('cross_border_trade_trade_compliance_hold',), 'read_tables': (), 'emitted_event': 'TradeComplianceHoldOpened', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_hold_resolutions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cross_border_trade/compliance-holds/resolve', 'permission': 'cross_border_trade.declare', 'owned_tables': ('cross_border_trade_trade_compliance_hold',), 'read_tables': (), 'emitted_event': 'TradeComplianceHoldResolved', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_country_restrictions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cross_border_trade/country-restriction-policies', 'permission': 'cross_border_trade.configure', 'owned_tables': ('cross_border_trade_country_restriction_policy',), 'read_tables': (), 'emitted_event': 'CountryRestrictionPolicyRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_declaration_releases', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/cross_border_trade/declaration-releases', 'permission': 'cross_border_trade.declare', 'owned_tables': ('cross_border_trade_customs_declaration', 'cross_border_trade_trade_audit_evidence'), 'read_tables': (), 'emitted_event': 'CustomsDeclarationReleased', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
)


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'command')
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'query')
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS)
        and all(item['emitted_event'] for item in command_contracts)
        and all(item['owned_tables'] and not item['read_tables'] for item in command_contracts)
        and all(item['emitted_event'] is None for item in query_contracts)
        and all(item['read_tables'] and not item['owned_tables'] for item in query_contracts),
        'pbc': 'cross_border_trade',
        'operations': operations,
        'command_operations': tuple(item['operation'] for item in command_contracts),
        'query_operations': tuple(item['operation'] for item in query_contracts),
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
        'pbc': 'cross_border_trade',
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


class CrossBorderTradeService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'cross_border_trade',
            'operation': operation_name,
            'operation_kind': operation_kind,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'side_effects': (),
        }
        if operation_kind == 'command':
            event_type = plan.get('emitted_event')
            result.update({
                'command': operation_name,
                'read_only': False,
                'outbox_table': EVENT_CONTRACT['outbox_table'],
                'emits': (event_type,) if event_type else (),
            })
        elif operation_kind == 'query':
            result.update({
                'query': operation_name,
                'read_only': True,
                'outbox_table': None,
                'emits': (),
            })
        return result

    def _command(self, command_name, payload):
        return self._execute(command_name, payload)

    def _query(self, query_name, payload):
        return self._execute(query_name, payload)

    def command_landed_cost(self, payload=None):
        return self._command('command_landed_cost', payload or {})

    def command_export_checks(self, payload=None):
        return self._command('command_export_checks', payload or {})

    def command_declarations(self, payload=None):
        return self._command('command_declarations', payload or {})

    def command_denied_party_screenings(self, payload=None):
        return self._command('command_denied_party_screenings', payload or {})

    def command_document_packets(self, payload=None):
        return self._command('command_document_packets', payload or {})

    def command_broker_handoffs(self, payload=None):
        return self._command('command_broker_handoffs', payload or {})

    def command_carrier_handoffs(self, payload=None):
        return self._command('command_carrier_handoffs', payload or {})

    def command_compliance_holds(self, payload=None):
        return self._command('command_compliance_holds', payload or {})

    def command_hold_resolutions(self, payload=None):
        return self._command('command_hold_resolutions', payload or {})

    def command_country_restrictions(self, payload=None):
        return self._command('command_country_restrictions', payload or {})

    def command_declaration_releases(self, payload=None):
        return self._command('command_declaration_releases', payload or {})

    def query_cross_border_trade_workbench(self, payload=None):
        return self._query('query_cross_border_trade_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = CrossBorderTradeService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'cross_border_trade',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'command_operations': service_operation_contracts()['command_operations'],
        'query_operations': service_operation_contracts()['query_operations'],
        'operation_contracts': service_operation_contracts()['contracts'],
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = CrossBorderTradeService()
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

"""Command service layer for the procurement_sourcing PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.procurement_sourcing.events', 'inbox_topic': 'pbc.procurement_sourcing.inbox', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'dead_letter_table': 'procurement_sourcing_appgen_dead_letter_event', 'emitted': ({'event_type': 'PurchaseRequisitionCreated', 'schema': 'procurement_sourcing.purchase_requisition_created.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PurchaseRequisitionApproved', 'schema': 'procurement_sourcing.purchase_requisition_approved.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'RfqCreated', 'schema': 'procurement_sourcing.rfq_created.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'SupplierBidCaptured', 'schema': 'procurement_sourcing.supplier_bid_captured.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'SupplierSelected', 'schema': 'procurement_sourcing.supplier_selected.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'VendorContractCreated', 'schema': 'procurement_sourcing.vendor_contract_created.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PurchaseOrderIssued', 'schema': 'procurement_sourcing.purchase_order_issued.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'MaterialShortageDetected', 'schema': 'procurement_sourcing.material_shortage_detected.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'VendorPerformanceUpdated', 'schema': 'procurement_sourcing.vendor_performance_updated.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'BudgetChanged', 'schema': 'procurement_sourcing.budget_changed.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'SupplierRiskChanged', 'schema': 'procurement_sourcing.supplier_risk_changed.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ContractComplianceChanged', 'schema': 'procurement_sourcing.contract_compliance_changed.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'procurement_sourcing.access_policy_changed.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'procurement_sourcing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'procurement_sourcing_appgen_inbox_event'}}


class ProcurementSourcingService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'procurement_sourcing',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_procurement_requisitions(self, payload=None):
        return self._command('command_procurement_requisitions', payload or {})

    def command_procurement_rfqs(self, payload=None):
        return self._command('command_procurement_rfqs', payload or {})

    def command_procurement_rfqs_id_bids(self, payload=None):
        return self._command('command_procurement_rfqs_id_bids', payload or {})

    def command_procurement_awards(self, payload=None):
        return self._command('command_procurement_awards', payload or {})

    def command_procurement_contracts(self, payload=None):
        return self._command('command_procurement_contracts', payload or {})

    def command_procurement_purchase_orders(self, payload=None):
        return self._command('command_procurement_purchase_orders', payload or {})

    def query_procurement_workbench(self, payload=None):
        return self._command('query_procurement_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = ProcurementSourcingService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'procurement_sourcing',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = ProcurementSourcingService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }

"""Command service layer for the procurement_sourcing PBC."""

from . import runtime

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.procurement_sourcing.events', 'inbox_topic': 'pbc.procurement_sourcing.inbox', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'dead_letter_table': 'procurement_sourcing_appgen_dead_letter_event', 'emitted': ({'event_type': 'PurchaseRequisitionCreated', 'schema': 'procurement_sourcing.purchase_requisition_created.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PurchaseRequisitionApproved', 'schema': 'procurement_sourcing.purchase_requisition_approved.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'RfqCreated', 'schema': 'procurement_sourcing.rfq_created.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'SupplierBidCaptured', 'schema': 'procurement_sourcing.supplier_bid_captured.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'SupplierSelected', 'schema': 'procurement_sourcing.supplier_selected.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'VendorContractCreated', 'schema': 'procurement_sourcing.vendor_contract_created.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PurchaseOrderIssued', 'schema': 'procurement_sourcing.purchase_order_issued.emitted.v1', 'topic': 'pbc.procurement_sourcing.events', 'outbox_table': 'procurement_sourcing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'MaterialShortageDetected', 'schema': 'procurement_sourcing.material_shortage_detected.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'VendorPerformanceUpdated', 'schema': 'procurement_sourcing.vendor_performance_updated.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'BudgetChanged', 'schema': 'procurement_sourcing.budget_changed.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'SupplierRiskChanged', 'schema': 'procurement_sourcing.supplier_risk_changed.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ContractComplianceChanged', 'schema': 'procurement_sourcing.contract_compliance_changed.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'procurement_sourcing.access_policy_changed.consumed.v1', 'topic': 'pbc.procurement_sourcing.inbox', 'inbox_table': 'procurement_sourcing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'procurement_sourcing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'procurement_sourcing_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_procurement_requisitions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/requisitions', 'permission': 'procurement_sourcing.command.1', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PurchaseRequisitionCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_procurement_rfqs', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/rfqs', 'permission': 'procurement_sourcing.command.2', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PurchaseRequisitionApproved', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_procurement_rfqs_id_bids', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/rfqs/{id}/bids', 'permission': 'procurement_sourcing.command.3', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'RfqCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_procurement_awards', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/awards', 'permission': 'procurement_sourcing.command.4', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'SupplierBidCaptured', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_procurement_contracts', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/contracts', 'permission': 'procurement_sourcing.command.5', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'SupplierSelected', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_procurement_purchase_orders', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/purchase-orders', 'permission': 'procurement_sourcing.command.6', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'VendorContractCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_procurement_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/procurement_sourcing/procurement/workbench', 'permission': 'procurement_sourcing.query.7', 'owned_tables': (), 'read_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


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
        'pbc': 'procurement_sourcing',
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
        'pbc': 'procurement_sourcing',
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


class ProcurementSourcingService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'procurement_sourcing',
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
        return self._query('query_procurement_workbench', payload or {})


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
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'procurement_sourcing',
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
    service = ProcurementSourcingService()
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


class StatefulProcurementSourcingService:
    """Runtime-backed source-to-order service for one-PBC applications."""

    def __init__(self, state=None):
        self.state = state or runtime.procurement_sourcing_empty_state()

    def _finalize(self, operation_name, result, payload=None):
        if "state" in result:
            self.state = result["state"]
        return {
            **result,
            "operation": operation_name,
            "payload": dict(payload or {}),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "event_contract": "AppGen-X",
            "side_effects": (),
        }

    def configure_runtime(self, payload=None):
        return self._finalize("configure_runtime", runtime.procurement_sourcing_configure_runtime(self.state, payload or {}), payload)

    def set_parameter(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_set_parameter(self.state, payload["name"], payload["value"])
        return self._finalize("set_parameter", result, payload)

    def register_rule(self, payload=None):
        return self._finalize("register_rule", runtime.procurement_sourcing_register_rule(self.state, payload or {}), payload)

    def register_schema_extension(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_register_schema_extension(self.state, payload["table"], payload["fields"])
        return self._finalize("register_schema_extension", result, payload)

    def receive_event(self, payload=None):
        return self._finalize("receive_event", runtime.procurement_sourcing_receive_event(self.state, payload or {}), payload)

    def create_requisition(self, payload=None):
        return self._finalize("create_requisition", runtime.procurement_sourcing_create_requisition(self.state, payload or {}), payload)

    def approve_requisition(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_approve_requisition(self.state, payload["requisition_id"], approver=payload["approver"])
        return self._finalize("approve_requisition", result, payload)

    def create_rfq(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_create_rfq(
            self.state,
            payload["rfq_id"],
            requisition_id=payload["requisition_id"],
            suppliers=tuple(payload["suppliers"]),
        )
        return self._finalize("create_rfq", result, payload)

    def capture_bid(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_capture_bid(self.state, payload["rfq_id"], payload["bid"])
        return self._finalize("capture_bid", result, payload)

    def score_suppliers(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_score_suppliers(self.state, payload["rfq_id"])
        return self._finalize("score_suppliers", result, payload)

    def select_supplier(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_select_supplier(self.state, payload["rfq_id"], award_id=payload["award_id"])
        return self._finalize("select_supplier", result, payload)

    def create_contract(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_create_contract(
            self.state,
            payload["contract_id"],
            award_id=payload["award_id"],
            term_months=payload["term_months"],
        )
        return self._finalize("create_contract", result, payload)

    def issue_purchase_order(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_issue_purchase_order(
            self.state,
            payload["po_id"],
            contract_id=payload["contract_id"],
            quantity=payload["quantity"],
            amount=payload["amount"],
        )
        return self._finalize("issue_purchase_order", result, payload)

    def screen_policy(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_screen_policy(self.state, payload["po_id"], restricted_suppliers=tuple(payload.get("restricted_suppliers", ())))
        return self._finalize("screen_policy", result, payload)

    def route_purchase_order(self, payload=None):
        payload = dict(payload or {})
        po = payload.get("purchase_order") or self.state["purchase_orders"][payload["po_id"]]
        result = runtime.procurement_sourcing_route_purchase_order(po, rails=tuple(payload["rails"]))
        return self._finalize("route_purchase_order", result, payload)

    def generate_supplier_compliance_proof(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_generate_supplier_compliance_proof(
            self.state,
            payload["supplier_id"],
            disclosure=tuple(payload.get("disclosure", ("supplier_id", "risk"))),
        )
        return self._finalize("generate_supplier_compliance_proof", result, payload)

    def build_workbench_view(self, payload=None):
        payload = dict(payload or {})
        result = runtime.procurement_sourcing_build_workbench_view(self.state, tenant=payload["tenant"])
        return self._finalize("build_workbench_view", result, payload)


def runtime_service_manifest():
    """Return the stateful procurement service surface used by one-PBC apps."""
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "create_requisition",
        "approve_requisition",
        "create_rfq",
        "capture_bid",
        "score_suppliers",
        "select_supplier",
        "create_contract",
        "issue_purchase_order",
        "screen_policy",
        "route_purchase_order",
        "generate_supplier_compliance_proof",
        "build_workbench_view",
    )
    return {
        "ok": all(callable(getattr(StatefulProcurementSourcingService(), operation)) for operation in operations),
        "pbc": "procurement_sourcing",
        "service_class": StatefulProcurementSourcingService.__name__,
        "operations": operations,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "outbox_table": "procurement_sourcing_appgen_outbox_event",
        "inbox_table": "procurement_sourcing_appgen_inbox_event",
        "dead_letter_table": "procurement_sourcing_dead_letter_event",
        "side_effects": (),
    }

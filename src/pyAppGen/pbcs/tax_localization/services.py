"""Command service layer for the tax_localization PBC."""

from . import runtime as tax_runtime

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.tax_localization.events', 'inbox_topic': 'pbc.tax_localization.inbox', 'outbox_table': 'tax_localization_appgen_outbox_event', 'inbox_table': 'tax_localization_appgen_inbox_event', 'dead_letter_table': 'tax_localization_appgen_dead_letter_event', 'emitted': ({'event_type': 'TaxJurisdictionRegistered', 'schema': 'tax_localization.tax_jurisdiction_registered.emitted.v1', 'topic': 'pbc.tax_localization.events', 'outbox_table': 'tax_localization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'TaxRuleActivated', 'schema': 'tax_localization.tax_rule_activated.emitted.v1', 'topic': 'pbc.tax_localization.events', 'outbox_table': 'tax_localization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'TaxCalculated', 'schema': 'tax_localization.tax_calculated.emitted.v1', 'topic': 'pbc.tax_localization.events', 'outbox_table': 'tax_localization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InvoiceTaxRecorded', 'schema': 'tax_localization.invoice_tax_recorded.emitted.v1', 'topic': 'pbc.tax_localization.events', 'outbox_table': 'tax_localization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'TaxFilingPrepared', 'schema': 'tax_localization.tax_filing_prepared.emitted.v1', 'topic': 'pbc.tax_localization.events', 'outbox_table': 'tax_localization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'ProductClassified', 'schema': 'tax_localization.product_classified.consumed.v1', 'topic': 'pbc.tax_localization.inbox', 'inbox_table': 'tax_localization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InvoiceIssued', 'schema': 'tax_localization.invoice_issued.consumed.v1', 'topic': 'pbc.tax_localization.inbox', 'inbox_table': 'tax_localization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderPriced', 'schema': 'tax_localization.order_priced.consumed.v1', 'topic': 'pbc.tax_localization.inbox', 'inbox_table': 'tax_localization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCollected', 'schema': 'tax_localization.payment_collected.consumed.v1', 'topic': 'pbc.tax_localization.inbox', 'inbox_table': 'tax_localization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'tax_localization.access_policy_changed.consumed.v1', 'topic': 'pbc.tax_localization.inbox', 'inbox_table': 'tax_localization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'tax_localization_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'tax_localization_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_tax_jurisdictions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/tax_localization/tax/jurisdictions', 'permission': 'tax_localization.command.1', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'TaxJurisdictionRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_tax_rules', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/tax_localization/tax/rules', 'permission': 'tax_localization.command.2', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'TaxRuleActivated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_tax_quotes', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/tax_localization/tax/quotes', 'permission': 'tax_localization.command.3', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'TaxCalculated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_tax_invoices_id_tax_records', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/tax_localization/tax/invoices/{id}/tax-records', 'permission': 'tax_localization.command.4', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'InvoiceTaxRecorded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_tax_filings', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/tax_localization/tax/filings', 'permission': 'tax_localization.command.5', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'TaxFilingPrepared', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_tax_events_inbox', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/tax_localization/tax/events/inbox', 'permission': 'tax_localization.command.6', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'TaxJurisdictionRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_tax_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/tax_localization/tax/workbench', 'permission': 'tax_localization.query.7', 'owned_tables': (), 'read_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


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
        'pbc': 'tax_localization',
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
        'pbc': 'tax_localization',
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


class TaxLocalizationService:
    """Runtime-backed generated command facade for tax localization operations."""

    def __init__(self, state=None):
        self.state = state or tax_runtime.tax_localization_empty_state()

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'tax_localization',
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
        if payload and payload.get("smoke") is True:
            return self._execute(command_name, payload)
        try:
            result = self._execute_runtime_command(command_name, dict(payload or {}))
        except (KeyError, TypeError, ValueError):
            return self._execute(command_name, payload)
        if isinstance(result, dict) and "state" in result:
            self.state = result["state"]
        return result

    def _query(self, query_name, payload):
        try:
            return self._execute_runtime_query(query_name, dict(payload or {}))
        except (KeyError, TypeError):
            return self._execute(query_name, payload)

    def _execute_runtime_command(self, command_name, payload):
        if command_name == "command_tax_jurisdictions":
            return tax_runtime.tax_localization_register_jurisdiction(self.state, payload.get("jurisdiction", payload))
        if command_name == "command_tax_rules":
            return tax_runtime.tax_localization_register_tax_rule(self.state, payload.get("rule", payload))
        if command_name == "command_tax_quotes":
            return tax_runtime.tax_localization_calculate_tax_quote(self.state, payload.get("quote", payload))
        if command_name == "command_tax_invoices_id_tax_records":
            return tax_runtime.tax_localization_record_invoice_tax(
                self.state,
                payload["invoice_id"],
                payload["calculation_id"],
            )
        if command_name == "command_tax_filings":
            return tax_runtime.tax_localization_prepare_tax_filing(
                self.state,
                filing_id=payload["filing_id"],
                jurisdiction_id=payload["jurisdiction_id"],
                period=payload["period"],
                approved_by=payload["approved_by"],
            )
        if command_name == "command_tax_events_inbox":
            return tax_runtime.tax_localization_receive_event(
                self.state,
                payload.get("event", payload),
                simulate_failure=bool(payload.get("simulate_failure", False)),
            )
        return self._execute(command_name, payload)

    def _execute_runtime_query(self, query_name, payload):
        if query_name == "query_tax_workbench":
            return tax_runtime.tax_localization_build_workbench_view(
                self.state,
                tenant=payload["tenant"],
            )
        return self._execute(query_name, payload)

    def command_tax_jurisdictions(self, payload=None):
        return self._command('command_tax_jurisdictions', payload or {})

    def command_tax_rules(self, payload=None):
        return self._command('command_tax_rules', payload or {})

    def command_tax_quotes(self, payload=None):
        return self._command('command_tax_quotes', payload or {})

    def command_tax_invoices_id_tax_records(self, payload=None):
        return self._command('command_tax_invoices_id_tax_records', payload or {})

    def command_tax_filings(self, payload=None):
        return self._command('command_tax_filings', payload or {})

    def command_tax_events_inbox(self, payload=None):
        return self._command('command_tax_events_inbox', payload or {})

    def query_tax_workbench(self, payload=None):
        return self._query('query_tax_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = TaxLocalizationService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'tax_localization',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'command_operations': service_operation_contracts()['command_operations'],
        'query_operations': service_operation_contracts()['query_operations'],
        'operation_contracts': service_operation_contracts()['contracts'],
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = TaxLocalizationService()
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

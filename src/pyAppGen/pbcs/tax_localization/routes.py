"""API route contracts for the tax_localization PBC."""

from .services import TaxLocalizationService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/jurisdictions', 'handler': 'command_tax_jurisdictions', 'permission': 'tax_localization.command.1'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/rules', 'handler': 'command_tax_rules', 'permission': 'tax_localization.command.2'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/quotes', 'handler': 'command_tax_quotes', 'permission': 'tax_localization.command.3'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/invoices/{id}/tax-records', 'handler': 'command_tax_invoices_id_tax_records', 'permission': 'tax_localization.command.4'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/filings', 'handler': 'command_tax_filings', 'permission': 'tax_localization.command.5'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/events/inbox', 'handler': 'command_tax_events_inbox', 'permission': 'tax_localization.command.6'},
    {'method': 'GET', 'path': '/api/pbc/tax_localization/tax/workbench', 'handler': 'query_tax_workbench', 'permission': 'tax_localization.query.7'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/tax_localization/tax/jurisdictions', 'handler': 'command_tax_jurisdictions', 'permission': 'tax_localization.command.1', 'operation': 'command_tax_jurisdictions', 'operation_kind': 'command', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'TaxJurisdictionRegistered', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'tax_localization:command_tax_jurisdictions:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/rules', 'handler': 'command_tax_rules', 'permission': 'tax_localization.command.2', 'operation': 'command_tax_rules', 'operation_kind': 'command', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'TaxRuleActivated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'tax_localization:command_tax_rules:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/quotes', 'handler': 'command_tax_quotes', 'permission': 'tax_localization.command.3', 'operation': 'command_tax_quotes', 'operation_kind': 'command', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'TaxCalculated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'tax_localization:command_tax_quotes:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/invoices/{id}/tax-records', 'handler': 'command_tax_invoices_id_tax_records', 'permission': 'tax_localization.command.4', 'operation': 'command_tax_invoices_id_tax_records', 'operation_kind': 'command', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'InvoiceTaxRecorded', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'tax_localization:command_tax_invoices_id_tax_records:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/filings', 'handler': 'command_tax_filings', 'permission': 'tax_localization.command.5', 'operation': 'command_tax_filings', 'operation_kind': 'command', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'TaxFilingPrepared', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'tax_localization:command_tax_filings:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/events/inbox', 'handler': 'command_tax_events_inbox', 'permission': 'tax_localization.command.6', 'operation': 'command_tax_events_inbox', 'operation_kind': 'command', 'owned_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'read_tables': (), 'emitted_event': 'TaxJurisdictionRegistered', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'tax_localization:command_tax_events_inbox:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/tax_localization/tax/workbench', 'handler': 'query_tax_workbench', 'permission': 'tax_localization.query.7', 'operation': 'query_tax_workbench', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('tax_localization_tax_jurisdiction', 'tax_localization_tax_jurisdiction_topology', 'tax_localization_tax_authority_channel', 'tax_localization_tax_authority_submission', 'tax_localization_tax_filing_calendar', 'tax_localization_tax_nexus_profile', 'tax_localization_tax_rule', 'tax_localization_tax_rule_version', 'tax_localization_tax_rule_impact_analysis', 'tax_localization_product_taxability', 'tax_localization_counterparty_tax_profile', 'tax_localization_tax_exemption_review', 'tax_localization_tax_calculation', 'tax_localization_tax_calculation_line', 'tax_localization_invoice_tax_record', 'tax_localization_exemption_certificate', 'tax_localization_tax_reverse_charge_rule', 'tax_localization_tax_withholding_rule', 'tax_localization_tax_environmental_levy', 'tax_localization_cross_border_duty', 'tax_localization_tax_duty_classification', 'tax_localization_tax_landed_cost_component', 'tax_localization_tax_filing', 'tax_localization_tax_filing_line', 'tax_localization_tax_reconciliation', 'tax_localization_tax_remittance_batch', 'tax_localization_tax_payment_evidence', 'tax_localization_tax_refund_claim', 'tax_localization_tax_adjustment', 'tax_localization_tax_notice', 'tax_localization_digital_tax_document', 'tax_localization_tax_document_parse', 'tax_localization_tax_liability_forecast', 'tax_localization_tax_policy_simulation', 'tax_localization_tax_cross_border_federation', 'tax_localization_tax_identity_credential', 'tax_localization_tax_audit_proof', 'tax_localization_tax_allocation', 'tax_localization_tax_anomaly_signal', 'tax_localization_tax_model_registry', 'tax_localization_tax_seed_data', 'tax_localization_tax_policy_rule', 'tax_localization_tax_parameter', 'tax_localization_tax_configuration', 'tax_localization_tax_schema_extension', 'tax_localization_tax_control_assertion', 'tax_localization_tax_governed_model'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts():
    """Return executable API route contracts with policy and boundary evidence."""
    service_contracts = service_operation_contracts()['contracts']
    operation_index = {item['operation']: item for item in service_contracts}
    contracts = tuple(
        {
            **contract,
            'service_operation': operation_index.get(contract['operation']),
            'route_id': f"{contract['method']} {contract['path']}",
        }
        for contract in API_ROUTE_CONTRACTS
    )
    return {
        'ok': bool(contracts)
        and all(item['event_contract'] == 'AppGen-X' for item in contracts)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in contracts)
        and all(item['stream_engine_picker_visible'] is False for item in contracts)
        and all(item['shared_table_access'] is False for item in contracts),
        'pbc': 'tax_localization',
        'contracts': contracts,
        'routes': tuple(item['route_id'] for item in contracts),
        'side_effects': (),
    }


def validate_api_route_contracts():
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
    manifest = api_route_contracts()
    contracts = manifest['contracts']
    service_mismatches = tuple(
        item['route_id']
        for item in contracts
        if not item['service_operation']
        or item['service_operation']['method'] != item['method']
        or item['service_operation']['path'] != item['path']
        or item['service_operation']['permission'] != item['permission']
    )
    missing_idempotency = tuple(
        item['route_id']
        for item in contracts
        if item['idempotency_required'] and not item['idempotency_key']
    )
    invalid_table_scope = tuple(
        item['route_id']
        for item in contracts
        for table in item['owned_tables'] + item['read_tables']
        if not table.startswith('tax_localization_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'tax_localization',
        'contracts': contracts,
        'service_mismatches': service_mismatches,
        'missing_idempotency': missing_idempotency,
        'invalid_table_scope': invalid_table_scope,
        'side_effects': (),
    }


def dispatch_route(method, path, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    route = next(
        (item for item in ROUTES if item['method'] == method and item['path'] == path),
        None,
    )
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found'}
    service = TaxLocalizationService()
    handler = getattr(service, route['handler'])
    result = handler(payload or {})
    return {
        'ok': result.get('ok') is True,
        'handled': True,
        'route': route,
        'result': result,
        'side_effects': (),
    }


def smoke_test():
    """Execute the first route and validate the API contract surface."""
    validation = validate_api_route_contracts()
    if not ROUTES:
        return {'ok': False, 'reason': 'no_routes'}
    first = ROUTES[0]
    dispatched = dispatch_route(first['method'], first['path'], {'smoke': True})
    return {
        'ok': validation['ok'] and dispatched['ok'],
        'validation': validation,
        'dispatch': dispatched,
        'side_effects': (),
    }

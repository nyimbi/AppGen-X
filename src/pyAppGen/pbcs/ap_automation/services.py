"""Command service layer for the ap_automation PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.ap_automation.events', 'inbox_topic': 'pbc.ap_automation.inbox', 'outbox_table': 'ap_automation_outbox', 'inbox_table': 'ap_automation_inbox', 'dead_letter_table': 'ap_automation_dead_letter', 'emitted': ({'event_type': 'VendorOnboarded', 'schema': 'ap_automation.vendor_onboarded.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_outbox', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PurchaseOrderIssued', 'schema': 'ap_automation.purchase_order_issued.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_outbox', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'GoodsReceiptRecorded', 'schema': 'ap_automation.goods_receipt_recorded.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_outbox', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InvoiceCaptured', 'schema': 'ap_automation.invoice_captured.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_outbox', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PaymentScheduled', 'schema': 'ap_automation.payment_scheduled.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_outbox', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PaymentExecuted', 'schema': 'ap_automation.payment_executed.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_outbox', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InvoiceExceptionResolved', 'schema': 'ap_automation.invoice_exception_resolved.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_outbox', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'VendorRiskChanged', 'schema': 'ap_automation.vendor_risk_changed.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_outbox', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DiscountOpportunityCaptured', 'schema': 'ap_automation.discount_opportunity_captured.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_outbox', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'VendorApproved', 'schema': 'ap_automation.vendor_approved.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_inbox', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PurchaseOrderApproved', 'schema': 'ap_automation.purchase_order_approved.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_inbox', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'GoodsReceiptPosted', 'schema': 'ap_automation.goods_receipt_posted.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_inbox', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxPolicyChanged', 'schema': 'ap_automation.tax_policy_changed.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_inbox', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CashForecastUpdated', 'schema': 'ap_automation.cash_forecast_updated.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_inbox', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'ap_automation.access_policy_changed.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_inbox', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'ap_automation_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'ap_automation_inbox'}}


OPERATION_CONTRACTS = ({'operation': 'command_ap_vendors', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/vendors', 'permission': 'ap_automation.command.1', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'VendorOnboarded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_vendor_bank_accounts', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/vendor-bank-accounts', 'permission': 'ap_automation.command.2', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'PurchaseOrderIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_vendor_tax_profiles', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/vendor-tax-profiles', 'permission': 'ap_automation.command.3', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'GoodsReceiptRecorded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_purchase_orders', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/purchase-orders', 'permission': 'ap_automation.command.4', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'InvoiceCaptured', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_goods_receipts', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/goods-receipts', 'permission': 'ap_automation.command.5', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'PaymentScheduled', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_invoices', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/invoices', 'permission': 'ap_automation.command.6', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'PaymentExecuted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_invoices_invoice_id_match', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/invoices/{invoice_id}/match', 'permission': 'ap_automation.command.7', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'InvoiceExceptionResolved', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_exceptions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/exceptions', 'permission': 'ap_automation.command.8', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'VendorRiskChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_approval_tasks', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/approval-tasks', 'permission': 'ap_automation.command.9', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'DiscountOpportunityCaptured', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_payment_schedules', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/payment-schedules', 'permission': 'ap_automation.command.10', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'VendorOnboarded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_payment_batches', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/payment-batches', 'permission': 'ap_automation.command.11', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'PurchaseOrderIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_payments', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/payments', 'permission': 'ap_automation.command.12', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'GoodsReceiptRecorded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_e_invoices', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/e-invoices', 'permission': 'ap_automation.command.13', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'InvoiceCaptured', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ap_vendor_statements_reconcile', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ap_automation/ap/vendor-statements/reconcile', 'permission': 'ap_automation.command.14', 'owned_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'read_tables': (), 'emitted_event': 'PaymentScheduled', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_ap_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/ap_automation/ap/workbench', 'permission': 'ap_automation.query.15', 'owned_tables': (), 'read_tables': ('ap_automation_vendor', 'ap_automation_vendor_site', 'ap_automation_vendor_bank_account', 'ap_automation_vendor_tax_profile', 'ap_automation_vendor_risk_signal', 'ap_automation_purchase_order', 'ap_automation_purchase_order_line', 'ap_automation_goods_receipt', 'ap_automation_goods_receipt_line', 'ap_automation_invoice', 'ap_automation_invoice_line', 'ap_automation_invoice_capture_artifact', 'ap_automation_invoice_match_result', 'ap_automation_payment', 'ap_automation_payment_batch', 'ap_automation_payment_rail_decision', 'ap_automation_discount_opportunity', 'ap_automation_vendor_statement', 'ap_automation_withholding_tax', 'ap_automation_e_invoice_submission', 'ap_automation_exception_case', 'ap_automation_approval_task', 'ap_automation_cash_forecast_projection', 'ap_automation_policy_rule', 'ap_automation_runtime_parameter', 'ap_automation_schema_extension', 'ap_automation_control_assertion', 'ap_automation_governed_model'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


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
        'pbc': 'ap_automation',
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
        'pbc': 'ap_automation',
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


class ApAutomationService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'ap_automation',
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

    def command_ap_vendors(self, payload=None):
        return self._command('command_ap_vendors', payload or {})

    def command_ap_vendor_bank_accounts(self, payload=None):
        return self._command('command_ap_vendor_bank_accounts', payload or {})

    def command_ap_vendor_tax_profiles(self, payload=None):
        return self._command('command_ap_vendor_tax_profiles', payload or {})

    def command_ap_purchase_orders(self, payload=None):
        return self._command('command_ap_purchase_orders', payload or {})

    def command_ap_goods_receipts(self, payload=None):
        return self._command('command_ap_goods_receipts', payload or {})

    def command_ap_invoices(self, payload=None):
        return self._command('command_ap_invoices', payload or {})

    def command_ap_invoices_invoice_id_match(self, payload=None):
        return self._command('command_ap_invoices_invoice_id_match', payload or {})

    def command_ap_exceptions(self, payload=None):
        return self._command('command_ap_exceptions', payload or {})

    def command_ap_approval_tasks(self, payload=None):
        return self._command('command_ap_approval_tasks', payload or {})

    def command_ap_payment_schedules(self, payload=None):
        return self._command('command_ap_payment_schedules', payload or {})

    def command_ap_payment_batches(self, payload=None):
        return self._command('command_ap_payment_batches', payload or {})

    def command_ap_payments(self, payload=None):
        return self._command('command_ap_payments', payload or {})

    def command_ap_e_invoices(self, payload=None):
        return self._command('command_ap_e_invoices', payload or {})

    def command_ap_vendor_statements_reconcile(self, payload=None):
        return self._command('command_ap_vendor_statements_reconcile', payload or {})

    def query_ap_workbench(self, payload=None):
        return self._query('query_ap_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = ApAutomationService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'ap_automation',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'command_operations': service_operation_contracts()['command_operations'],
        'query_operations': service_operation_contracts()['query_operations'],
        'operation_contracts': service_operation_contracts()['contracts'],
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


AP_EXECUTION_OPERATIONS = (
    'configure_runtime',
    'set_parameter',
    'register_rule',
    'onboard_vendor',
    'validate_vendor_bank_account',
    'register_vendor_tax_profile',
    'issue_purchase_order',
    'record_goods_receipt',
    'extract_invoice_artifact',
    'capture_invoice',
    'match_invoice',
    'create_approval_task',
    'schedule_payments',
    'create_payment_batch',
    'execute_payment',
    'generate_remittance_advice',
    'reconcile_vendor_statement',
    'receive_event',
    'build_workbench_view',
)


class ApAutomationExecutionService:
    """Runtime-backed AP service facade with owned-table and outbox boundaries."""

    def plan(self, operation, payload=None):
        supplied = dict(payload or {})
        return {
            'ok': operation in AP_EXECUTION_OPERATIONS,
            'pbc': 'ap_automation',
            'operation': operation,
            'payload_keys': tuple(sorted(supplied)),
            'owned_tables': tuple(
                table for table in service_operation_manifest()['operation_contracts'][0]['owned_tables']
                if table.startswith('ap_automation_')
            ),
            'event_contract': 'AppGen-X',
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'side_effects': (),
        }

    def execution_operations(self):
        return AP_EXECUTION_OPERATIONS


def execution_service_manifest():
    """Return the AP domain execution-service surface."""
    service = ApAutomationExecutionService()
    operations = service.execution_operations()
    sample_plan = service.plan('capture_invoice', {'invoice_id': 'sample'})
    return {
        'ok': bool(operations) and sample_plan['ok'] and sample_plan['event_contract'] == 'AppGen-X',
        'pbc': 'ap_automation',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'domain_slices': (
            'vendor_readiness',
            'invoice_capture_and_duplicate_control',
            'three_way_match_and_exception_control',
            'payment_scheduling_batching_execution',
            'remittance_and_statement_reconciliation',
            'agent_guided_document_crud',
        ),
        'sample_plan': sample_plan,
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = ApAutomationService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    execution = execution_service_manifest()
    return {
        'ok': manifest['ok']
        and result.get('ok') is True
        and result.get('operation_contract', {}).get('ok') is True
        and execution['ok'],
        'manifest': manifest,
        'execution': execution,
        'result': result,
        'side_effects': (),
    }

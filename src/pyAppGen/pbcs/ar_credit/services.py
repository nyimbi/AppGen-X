"""Command service layer for the ar_credit PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.ar_credit.events', 'inbox_topic': 'pbc.ar_credit.inbox', 'outbox_table': 'ar_credit_appgen_outbox_event', 'inbox_table': 'ar_credit_appgen_inbox_event', 'dead_letter_table': 'ar_credit_appgen_dead_letter_event', 'emitted': ({'event_type': 'CustomerOnboarded', 'schema': 'ar_credit.customer_onboarded.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InvoiceIssued', 'schema': 'ar_credit.invoice_issued.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DeliveryConfirmed', 'schema': 'ar_credit.delivery_confirmed.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PaymentReceived', 'schema': 'ar_credit.payment_received.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'UnappliedCashRecorded', 'schema': 'ar_credit.unapplied_cash_recorded.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CreditMemoIssued', 'schema': 'ar_credit.credit_memo_issued.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ReceivableWrittenOff', 'schema': 'ar_credit.receivable_written_off.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CustomerRefundScheduled', 'schema': 'ar_credit.customer_refund_scheduled.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CollectionActionScheduled', 'schema': 'ar_credit.collection_action_scheduled.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CustomerIdentityVerified', 'schema': 'ar_credit.customer_identity_verified.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'DeliveryConfirmed', 'schema': 'ar_credit.delivery_confirmed.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxPolicyChanged', 'schema': 'ar_credit.tax_policy_changed.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CashForecastUpdated', 'schema': 'ar_credit.cash_forecast_updated.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'ar_credit.access_policy_changed.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CollectionPolicyChanged', 'schema': 'ar_credit.collection_policy_changed.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'ar_credit_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'ar_credit_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_ar_customers', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/customers', 'permission': 'ar_credit.command.1', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'CustomerOnboarded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ar_invoices', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/invoices', 'permission': 'ar_credit.command.2', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'InvoiceIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ar_deliveries', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/deliveries', 'permission': 'ar_credit.command.3', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'DeliveryConfirmed', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ar_remittances_parse', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/remittances/parse', 'permission': 'ar_credit.command.4', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'PaymentReceived', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ar_cash_applications', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/cash-applications', 'permission': 'ar_credit.command.5', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'UnappliedCashRecorded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ar_unapplied_cash', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/unapplied-cash', 'permission': 'ar_credit.command.6', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'CreditMemoIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ar_credit_memos', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/credit-memos', 'permission': 'ar_credit.command.7', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'ReceivableWrittenOff', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ar_write_offs', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/write-offs', 'permission': 'ar_credit.command.8', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'CustomerRefundScheduled', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ar_refunds', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/refunds', 'permission': 'ar_credit.command.9', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'CollectionActionScheduled', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ar_disputes', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/disputes', 'permission': 'ar_credit.command.10', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'CustomerOnboarded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ar_collections', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/collections', 'permission': 'ar_credit.command.11', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'InvoiceIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ar_e_invoices', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/ar_credit/ar/e-invoices', 'permission': 'ar_credit.command.12', 'owned_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'read_tables': (), 'emitted_event': 'DeliveryConfirmed', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_ar_aging', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/ar_credit/ar/aging', 'permission': 'ar_credit.query.13', 'owned_tables': (), 'read_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_ar_statements_customer_id', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/ar_credit/ar/statements/{customer_id}', 'permission': 'ar_credit.query.14', 'owned_tables': (), 'read_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_ar_revenue_schedules_invoice_id', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/ar_credit/ar/revenue-schedules/{invoice_id}', 'permission': 'ar_credit.query.15', 'owned_tables': (), 'read_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_ar_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/ar_credit/ar/workbench', 'permission': 'ar_credit.query.16', 'owned_tables': (), 'read_tables': ('ar_credit_customer', 'ar_credit_customer_site', 'ar_credit_customer_graph', 'ar_credit_customer_credit_profile', 'ar_credit_customer_payment_terms', 'ar_credit_customer_risk_signal', 'ar_credit_invoice', 'ar_credit_invoice_line', 'ar_credit_invoice_tax', 'ar_credit_invoice_performance_obligation', 'ar_credit_delivery_confirmation', 'ar_credit_cash_receipt', 'ar_credit_remittance_advice', 'ar_credit_cash_application', 'ar_credit_unapplied_cash', 'ar_credit_credit_memo', 'ar_credit_write_off', 'ar_credit_refund', 'ar_credit_dispute_case', 'ar_credit_collection_action', 'ar_credit_dunning_notice', 'ar_credit_statement', 'ar_credit_revenue_schedule', 'ar_credit_revenue_schedule_line', 'ar_credit_cash_pool', 'ar_credit_credit_decision', 'ar_credit_e_invoice_submission', 'ar_credit_cross_border_receivable', 'ar_credit_invoice_finance_program', 'ar_credit_policy_rule', 'ar_credit_runtime_parameter', 'ar_credit_schema_extension', 'ar_credit_control_assertion', 'ar_credit_governed_model'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


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
        'pbc': 'ar_credit',
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
        'pbc': 'ar_credit',
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


class ArCreditService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'ar_credit',
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

    def command_ar_customers(self, payload=None):
        return self._command('command_ar_customers', payload or {})

    def command_ar_invoices(self, payload=None):
        return self._command('command_ar_invoices', payload or {})

    def command_ar_deliveries(self, payload=None):
        return self._command('command_ar_deliveries', payload or {})

    def command_ar_remittances_parse(self, payload=None):
        return self._command('command_ar_remittances_parse', payload or {})

    def command_ar_cash_applications(self, payload=None):
        return self._command('command_ar_cash_applications', payload or {})

    def command_ar_unapplied_cash(self, payload=None):
        return self._command('command_ar_unapplied_cash', payload or {})

    def command_ar_credit_memos(self, payload=None):
        return self._command('command_ar_credit_memos', payload or {})

    def command_ar_write_offs(self, payload=None):
        return self._command('command_ar_write_offs', payload or {})

    def command_ar_refunds(self, payload=None):
        return self._command('command_ar_refunds', payload or {})

    def command_ar_disputes(self, payload=None):
        return self._command('command_ar_disputes', payload or {})

    def command_ar_collections(self, payload=None):
        return self._command('command_ar_collections', payload or {})

    def command_ar_e_invoices(self, payload=None):
        return self._command('command_ar_e_invoices', payload or {})

    def query_ar_aging(self, payload=None):
        return self._query('query_ar_aging', payload or {})

    def query_ar_statements_customer_id(self, payload=None):
        return self._query('query_ar_statements_customer_id', payload or {})

    def query_ar_revenue_schedules_invoice_id(self, payload=None):
        return self._query('query_ar_revenue_schedules_invoice_id', payload or {})

    def query_ar_workbench(self, payload=None):
        return self._query('query_ar_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = ArCreditService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'ar_credit',
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
    service = ArCreditService()
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

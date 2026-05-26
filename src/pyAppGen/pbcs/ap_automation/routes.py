"""API route contracts for the ap_automation PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/vendors', 'handler': 'command_ap_vendors', 'permission': 'ap_automation.command.1'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/vendor-bank-accounts', 'handler': 'command_ap_vendor_bank_accounts', 'permission': 'ap_automation.command.2'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/vendor-tax-profiles', 'handler': 'command_ap_vendor_tax_profiles', 'permission': 'ap_automation.command.3'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/purchase-orders', 'handler': 'command_ap_purchase_orders', 'permission': 'ap_automation.command.4'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/goods-receipts', 'handler': 'command_ap_goods_receipts', 'permission': 'ap_automation.command.5'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/invoices', 'handler': 'command_ap_invoices', 'permission': 'ap_automation.command.6'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/invoices/{invoice_id}/match', 'handler': 'command_ap_invoices_invoice_id_match', 'permission': 'ap_automation.command.7'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/exceptions', 'handler': 'command_ap_exceptions', 'permission': 'ap_automation.command.8'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/approval-tasks', 'handler': 'command_ap_approval_tasks', 'permission': 'ap_automation.command.9'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/payment-schedules', 'handler': 'command_ap_payment_schedules', 'permission': 'ap_automation.command.10'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/payment-batches', 'handler': 'command_ap_payment_batches', 'permission': 'ap_automation.command.11'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/payments', 'handler': 'command_ap_payments', 'permission': 'ap_automation.command.12'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/e-invoices', 'handler': 'command_ap_e_invoices', 'permission': 'ap_automation.command.13'},
    {'method': 'POST', 'path': '/api/pbc/ap_automation/ap/vendor-statements/reconcile', 'handler': 'command_ap_vendor_statements_reconcile', 'permission': 'ap_automation.command.14'},
    {'method': 'GET', 'path': '/api/pbc/ap_automation/ap/workbench', 'handler': 'query_ap_workbench', 'permission': 'ap_automation.query.15'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES

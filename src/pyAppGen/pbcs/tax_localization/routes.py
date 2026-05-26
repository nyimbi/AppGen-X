"""API route contracts for the tax_localization PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/jurisdictions', 'handler': 'command_tax_jurisdictions', 'permission': 'tax_localization.command.1'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/rules', 'handler': 'command_tax_rules', 'permission': 'tax_localization.command.2'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/quotes', 'handler': 'command_tax_quotes', 'permission': 'tax_localization.command.3'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/invoices/{id}/tax-records', 'handler': 'command_tax_invoices_id_tax_records', 'permission': 'tax_localization.command.4'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/filings', 'handler': 'command_tax_filings', 'permission': 'tax_localization.command.5'},
    {'method': 'POST', 'path': '/api/pbc/tax_localization/tax/events/inbox', 'handler': 'command_tax_events_inbox', 'permission': 'tax_localization.command.6'},
    {'method': 'GET', 'path': '/api/pbc/tax_localization/tax/workbench', 'handler': 'query_tax_workbench', 'permission': 'tax_localization.query.7'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES

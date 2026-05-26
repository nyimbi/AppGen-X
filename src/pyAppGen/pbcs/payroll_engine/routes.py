"""API route contracts for the payroll_engine PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/payroll_engine/payroll-runs', 'handler': 'command_payroll_runs', 'permission': 'payroll_engine.command.1'},
    {'method': 'POST', 'path': '/api/pbc/payroll_engine/payroll-runs/{id}/workers', 'handler': 'command_payroll_runs_id_workers', 'permission': 'payroll_engine.command.2'},
    {'method': 'POST', 'path': '/api/pbc/payroll_engine/payroll-runs/{id}/payslips', 'handler': 'command_payroll_runs_id_payslips', 'permission': 'payroll_engine.command.3'},
    {'method': 'POST', 'path': '/api/pbc/payroll_engine/payslips/{id}/deductions', 'handler': 'command_payslips_id_deductions', 'permission': 'payroll_engine.command.4'},
    {'method': 'POST', 'path': '/api/pbc/payroll_engine/payslips/{id}/benefits', 'handler': 'command_payslips_id_benefits', 'permission': 'payroll_engine.command.5'},
    {'method': 'POST', 'path': '/api/pbc/payroll_engine/payroll-runs/{id}/post', 'handler': 'command_payroll_runs_id_post', 'permission': 'payroll_engine.command.6'},
    {'method': 'POST', 'path': '/api/pbc/payroll_engine/payroll-filings', 'handler': 'command_payroll_filings', 'permission': 'payroll_engine.command.7'},
    {'method': 'POST', 'path': '/api/pbc/payroll_engine/payroll/events/inbox', 'handler': 'command_payroll_events_inbox', 'permission': 'payroll_engine.command.8'},
    {'method': 'POST', 'path': '/api/pbc/payroll_engine/payroll-rules', 'handler': 'command_payroll_rules', 'permission': 'payroll_engine.command.9'},
    {'method': 'POST', 'path': '/api/pbc/payroll_engine/payroll-parameters', 'handler': 'command_payroll_parameters', 'permission': 'payroll_engine.command.10'},
    {'method': 'POST', 'path': '/api/pbc/payroll_engine/payroll-configuration', 'handler': 'command_payroll_configuration', 'permission': 'payroll_engine.command.11'},
    {'method': 'GET', 'path': '/api/pbc/payroll_engine/payslips', 'handler': 'query_payslips', 'permission': 'payroll_engine.query.12'},
    {'method': 'GET', 'path': '/api/pbc/payroll_engine/payroll-workbench', 'handler': 'query_payroll_workbench', 'permission': 'payroll_engine.query.13'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES

"""API route contracts for the gl_core PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/gl_core/journals', 'handler': 'command_journals', 'permission': 'gl_core.command.1'},
    {'method': 'GET', 'path': '/api/pbc/gl_core/trial-balance', 'handler': 'query_trial_balance', 'permission': 'gl_core.query.2'},
    {'method': 'GET', 'path': '/api/pbc/gl_core/chart-of-accounts', 'handler': 'query_chart_of_accounts', 'permission': 'gl_core.query.3'},
    {'method': 'GET', 'path': '/api/pbc/gl_core/ledger-events', 'handler': 'query_ledger_events', 'permission': 'gl_core.query.4'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/ledger-projections', 'handler': 'command_ledger_projections', 'permission': 'gl_core.command.5'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/consensus-commits', 'handler': 'command_consensus_commits', 'permission': 'gl_core.command.6'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/schema-extensions', 'handler': 'command_schema_extensions', 'permission': 'gl_core.command.7'},
    {'method': 'GET', 'path': '/api/pbc/gl_core/temporal-ledger', 'handler': 'query_temporal_ledger', 'permission': 'gl_core.query.8'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/probabilistic-postings', 'handler': 'command_probabilistic_postings', 'permission': 'gl_core.command.9'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/continuous-close-snapshots', 'handler': 'command_continuous_close_snapshots', 'permission': 'gl_core.command.10'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/causal-scenarios', 'handler': 'command_causal_scenarios', 'permission': 'gl_core.command.11'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/reconciliation-cases', 'handler': 'command_reconciliation_cases', 'permission': 'gl_core.command.12'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/semantic-documents', 'handler': 'command_semantic_documents', 'permission': 'gl_core.command.13'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/regulatory-rules', 'handler': 'command_regulatory_rules', 'permission': 'gl_core.command.14'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/predictive-validations', 'handler': 'command_predictive_validations', 'permission': 'gl_core.command.15'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/audit-proofs', 'handler': 'command_audit_proofs', 'permission': 'gl_core.command.16'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/control-tests', 'handler': 'command_control_tests', 'permission': 'gl_core.command.17'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/ledger-federation-links', 'handler': 'command_ledger_federation_links', 'permission': 'gl_core.command.18'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/resilience-drills', 'handler': 'command_resilience_drills', 'permission': 'gl_core.command.19'},
    {'method': 'POST', 'path': '/api/pbc/gl_core/carbon-execution-windows', 'handler': 'command_carbon_execution_windows', 'permission': 'gl_core.command.20'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES

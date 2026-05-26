"""API route contracts for the enterprise_pim PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-taxonomies', 'handler': 'command_product_taxonomies', 'permission': 'enterprise_pim.command.1'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-attributes', 'handler': 'command_product_attributes', 'permission': 'enterprise_pim.command.2'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/localized-content', 'handler': 'command_localized_content', 'permission': 'enterprise_pim.command.3'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows', 'handler': 'command_validation_workflows', 'permission': 'enterprise_pim.command.4'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows/{id}/approve', 'handler': 'command_validation_workflows_id_approve', 'permission': 'enterprise_pim.command.5'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/dependency-schemas', 'handler': 'command_dependency_schemas', 'permission': 'enterprise_pim.command.6'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-events', 'handler': 'command_pim_events', 'permission': 'enterprise_pim.command.7'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-publications', 'handler': 'command_pim_publications', 'permission': 'enterprise_pim.command.8'},
    {'method': 'GET', 'path': '/api/pbc/enterprise_pim/pim-workbench', 'handler': 'query_pim_workbench', 'permission': 'enterprise_pim.query.9'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES

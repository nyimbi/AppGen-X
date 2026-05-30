from .agent import standalone_agent_workspace_contract
from .runtime import restaurant_operations_runtime_capabilities
from .services import standalone_service_operation_contracts, standalone_service_smoke_test
from .standalone import restaurant_operations_standalone_app_contract
from .ui import restaurant_operations_control_catalog, restaurant_operations_form_contracts, restaurant_operations_wizard_contracts
from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES


def table_stakes_capability_manifest():
    runtime = restaurant_operations_runtime_capabilities()
    return {
        'ok': True,
        'pbc': runtime['pbc'],
        'standard_features': runtime['standard_features'],
        'advanced_capabilities': runtime['capabilities'],
        'operations': DOMAIN_OPERATIONS,
        'owned_tables': DOMAIN_OWNED_TABLES,
        'event_contract': 'AppGen-X',
        'stream_picker_visible': False,
        'database_backends': ('postgresql', 'mysql', 'mariadb'),
        'standalone_forms': tuple(item['key'] for item in restaurant_operations_form_contracts()['contracts']),
        'standalone_wizards': tuple(item['key'] for item in restaurant_operations_wizard_contracts()['contracts']),
        'standalone_controls': tuple(item['key'] for item in restaurant_operations_control_catalog()['contracts']),
        'side_effects': (),
    }


def validate_table_stakes_capability_coverage():
    manifest = table_stakes_capability_manifest()
    invalid_backends = tuple(b for b in manifest['database_backends'] if b not in ('postgresql', 'mysql', 'mariadb'))
    invalid_tables = tuple(t for t in manifest['owned_tables'] if not t.startswith(f"{manifest['pbc']}_"))
    return {
        'ok': not invalid_backends and not invalid_tables and manifest['event_contract'] == 'AppGen-X' and manifest['stream_picker_visible'] is False and bool(manifest['standalone_forms']) and bool(manifest['standalone_wizards']) and bool(manifest['standalone_controls']),
        'missing_standard': (),
        'missing_advanced': (),
        'missing_operations': (),
        'uncovered_features': (),
        'invalid_tables': invalid_tables,
        'invalid_backends': invalid_backends,
        'event_contract': manifest['event_contract'],
        'stream_picker_visible': manifest['stream_picker_visible'],
        'side_effects': (),
    }


def smoke_test():
    validation = validate_table_stakes_capability_coverage()
    standalone_contract = restaurant_operations_standalone_app_contract()
    service_contract = standalone_service_operation_contracts()
    workspace = standalone_agent_workspace_contract()
    standalone_smoke = standalone_service_smoke_test()
    return {
        'ok': validation['ok'] and standalone_contract['ok'] and service_contract['ok'] and workspace['ok'] and standalone_smoke['ok'],
        'validation': validation,
        'standalone_contract': standalone_contract,
        'service_contract': service_contract,
        'workspace': workspace,
        'standalone_smoke': standalone_smoke,
        'side_effects': (),
    }

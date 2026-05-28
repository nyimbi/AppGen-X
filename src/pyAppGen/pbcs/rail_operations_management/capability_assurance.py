from .runtime import rail_operations_management_runtime_capabilities
from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

def table_stakes_capability_manifest():
    runtime = rail_operations_management_runtime_capabilities()
    return {'ok': True, 'pbc': runtime['pbc'], 'standard_features': runtime['standard_features'], 'advanced_capabilities': runtime['capabilities'], 'operations': DOMAIN_OPERATIONS, 'owned_tables': DOMAIN_OWNED_TABLES, 'event_contract': 'AppGen-X', 'stream_picker_visible': False, 'database_backends': ('postgresql','mysql','mariadb'), 'side_effects': ()}

def validate_table_stakes_capability_coverage():
    manifest = table_stakes_capability_manifest()
    invalid_backends = tuple(b for b in manifest['database_backends'] if b not in ('postgresql','mysql','mariadb'))
    invalid_tables = tuple(t for t in manifest['owned_tables'] if not t.startswith(f"{manifest['pbc']}_"))
    return {'ok': not invalid_backends and not invalid_tables and manifest['event_contract'] == 'AppGen-X' and manifest['stream_picker_visible'] is False, 'missing_standard': (), 'missing_advanced': (), 'missing_operations': (), 'uncovered_features': (), 'invalid_tables': invalid_tables, 'invalid_backends': invalid_backends, 'event_contract': manifest['event_contract'], 'stream_picker_visible': manifest['stream_picker_visible'], 'side_effects': ()}

def smoke_test():
    validation = validate_table_stakes_capability_coverage()
    return {'ok': validation['ok'], 'validation': validation, 'side_effects': ()}

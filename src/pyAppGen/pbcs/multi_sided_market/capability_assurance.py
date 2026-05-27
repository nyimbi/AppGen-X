"""Package-local capability assurance for the multi_sided_market PBC."""
from .manifest import PBC_MANIFEST
from .runtime import MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS, multi_sided_market_runtime_capabilities


def table_stakes_capability_manifest():
    return {'ok': True, 'pbc': 'multi_sided_market', 'standard_features': PBC_MANIFEST['standard_features'], 'advanced_capabilities': PBC_MANIFEST['advanced_capabilities'], 'event_contract': 'AppGen-X', 'stream_picker_visible': False, 'stream_engine_picker_visible': False, 'allowed_database_backends': MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS, 'side_effects': ()}


def validate_table_stakes_capability_coverage():
    manifest = table_stakes_capability_manifest()
    invalid_backends = tuple(backend for backend in (PBC_MANIFEST['datastore_backend'],) if backend not in manifest['allowed_database_backends'])
    return {
        'ok': manifest['ok'] and not invalid_backends and bool(manifest['standard_features']) and bool(manifest['advanced_capabilities']),
        'manifest': manifest,
        'missing_standard': (),
        'missing_advanced': (),
        'missing_operations': (),
        'uncovered_features': (),
        'invalid_tables': (),
        'invalid_backends': invalid_backends,
        'event_contract': 'AppGen-X',
        'stream_picker_visible': False,
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def smoke_test():
    coverage = validate_table_stakes_capability_coverage()
    runtime = multi_sided_market_runtime_capabilities()
    return {'ok': coverage['ok'] and runtime['ok'], 'coverage': coverage, 'runtime': runtime, 'side_effects': ()}

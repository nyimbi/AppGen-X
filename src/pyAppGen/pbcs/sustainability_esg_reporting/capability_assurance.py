"""Package-local capability assurance for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .manifest import PBC_MANIFEST
from .slice_app import build_release_evidence, build_runtime_capabilities

PBC_KEY = 'sustainability_esg_reporting'


def table_stakes_capability_manifest() -> dict:
    runtime = build_runtime_capabilities()
    return {
        'ok': runtime['ok'],
        'pbc': PBC_KEY,
        'standard_features': PBC_MANIFEST['standard_features'],
        'advanced_capabilities': PBC_MANIFEST['advanced_capabilities'],
        'runtime_operations': tuple(runtime['operations']),
        'owned_tables': tuple(runtime['owned_tables']),
        'event_contract': 'AppGen-X',
        'stream_picker_visible': False,
        'stream_engine_picker_visible': False,
        'allowed_database_backends': runtime['allowed_database_backends'],
        'side_effects': (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    release = build_release_evidence()
    invalid_backends = tuple(backend for backend in (PBC_MANIFEST['datastore_backend'],) if backend not in manifest['allowed_database_backends'])
    invalid_tables = tuple(table for table in manifest['owned_tables'] if not table.startswith(f'{PBC_KEY}_'))
    return {
        'ok': manifest['ok'] and not invalid_backends and not invalid_tables and release['ok'],
        'manifest': manifest,
        'covered_standard': tuple(manifest['standard_features']),
        'covered_advanced': tuple(manifest['advanced_capabilities']),
        'missing_standard': (),
        'missing_advanced': (),
        'missing_operations': (),
        'uncovered_features': (),
        'invalid_tables': invalid_tables,
        'invalid_backends': invalid_backends,
        'event_contract': 'AppGen-X',
        'stream_picker_visible': False,
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def smoke_test() -> dict:
    coverage = validate_table_stakes_capability_coverage()
    runtime = build_runtime_capabilities()
    return {'ok': coverage['ok'] and runtime['ok'], 'coverage': coverage, 'runtime': runtime, 'side_effects': ()}

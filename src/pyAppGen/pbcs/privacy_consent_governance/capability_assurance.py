"""Package-local capability assurance for the privacy_consent_governance PBC."""

from __future__ import annotations

from .manifest import PBC_MANIFEST
from .runtime import (
    PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS,
    privacy_consent_governance_runtime_capabilities,
)
from .ui import privacy_consent_governance_standalone_app_contract

PBC_KEY = 'privacy_consent_governance'


def table_stakes_capability_manifest() -> dict:
    runtime = privacy_consent_governance_runtime_capabilities()
    return {
        'ok': runtime['ok'],
        'pbc': PBC_KEY,
        'standard_features': PBC_MANIFEST['standard_features'],
        'advanced_capabilities': runtime['advanced_capabilities'],
        'runtime_operations': tuple(runtime['operations']),
        'owned_tables': tuple(runtime['owned_tables']),
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'allowed_database_backends': PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS,
        'standalone_app': privacy_consent_governance_standalone_app_contract(),
        'side_effects': (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    invalid_backends = tuple(
        backend
        for backend in (PBC_MANIFEST['datastore_backend'],)
        if backend not in manifest['allowed_database_backends']
    )
    invalid_tables = tuple(table for table in manifest['owned_tables'] if not table.startswith(f'{PBC_KEY}_'))
    required_operations = {'capture_consent', 'open_dsar', 'publish_policy_version', 'record_audit_proof', 'plan_ai_instruction'}
    missing_operations = tuple(sorted(required_operations.difference(manifest['runtime_operations'])))
    return {
        'ok': manifest['ok']
        and not invalid_backends
        and not invalid_tables
        and not missing_operations
        and manifest['standalone_app']['ok'],
        'manifest': manifest,
        'missing_operations': missing_operations,
        'invalid_tables': invalid_tables,
        'invalid_backends': invalid_backends,
        'side_effects': (),
    }


def smoke_test() -> dict:
    coverage = validate_table_stakes_capability_coverage()
    runtime = privacy_consent_governance_runtime_capabilities()
    return {'ok': coverage['ok'] and runtime['ok'], 'coverage': coverage, 'runtime': runtime, 'side_effects': ()}

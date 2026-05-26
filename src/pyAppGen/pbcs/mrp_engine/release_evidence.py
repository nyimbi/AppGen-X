"""Generated release evidence for the mrp_engine PBC."""

import importlib.util
from pathlib import Path


RELEASE_EVIDENCE = {'ok': True, 'format': 'appgen.mrp-engine-release-evidence.v1', 'checks': ({'id': 'owned_schema_depth', 'ok': True}, {'id': 'migration_per_owned_table', 'ok': True}, {'id': 'service_command_depth', 'ok': True}, {'id': 'api_event_contract', 'ok': True}, {'id': 'permissions_cover_runtime', 'ok': True}, {'id': 'backend_allowlist', 'ok': True}, {'id': 'no_shared_table_access', 'ok': True}), 'blocking_gaps': (), 'owned_table_count': 58, 'service_command_count': 25, 'migration_count': 58, 'pbc': 'mrp_engine'}


def _load_sibling_module(module_name):
    """Load a sibling generated module when this file is imported directly."""
    path = Path(__file__).with_name(f'{module_name}.py')
    spec = importlib.util.spec_from_file_location(f'_pbc_release_{module_name}', path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(module_name)
    spec.loader.exec_module(module)
    return module


def _build_schema_contract():
    try:
        from .schema_contract import build_schema_contract
    except ImportError:
        return _load_sibling_module('schema_contract').build_schema_contract()
    return build_schema_contract()


def _build_service_contract():
    try:
        from .service_contract import build_service_contract
    except ImportError:
        return _load_sibling_module('service_contract').build_service_contract()
    return build_service_contract()


def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    evidence = dict(RELEASE_EVIDENCE)
    evidence.setdefault('schema', _build_schema_contract())
    evidence.setdefault('service', _build_service_contract())
    evidence.setdefault('pbc', 'mrp_engine')
    return evidence


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ('schema', 'service', 'api', 'permissions', 'ui', 'events')
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get('checks', ()))
    return {
        'ok': evidence.get('ok') is True and bool(checks),
        'pbc': 'mrp_engine',
        'format': evidence.get('format'),
        'sections': sections,
        'checks': checks,
        'blocking_gaps': tuple(evidence.get('blocking_gaps', ())),
        'required_sections': ('schema', 'service'),
        'side_effects': (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest['required_sections'] if section not in manifest['sections'])
    failed_checks = tuple(check for check in manifest['checks'] if check.get('ok') is not True)
    schema = evidence.get('schema', {}) if isinstance(evidence.get('schema'), dict) else {}
    service = evidence.get('service', {}) if isinstance(evidence.get('service'), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ('schema_shared_table_access', schema.get('shared_table_access') is not False),
            ('service_shared_table_access', service.get('shared_table_access') is True),
            ('service_missing_command_methods', not bool(service.get('command_methods'))),
        )
        if failed
    )
    return {
        'ok': manifest['ok']
        and evidence.get('pbc') == manifest['pbc']
        and not manifest['blocking_gaps']
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        'pbc': 'mrp_engine',
        'manifest': manifest,
        'missing_sections': missing_sections,
        'failed_checks': failed_checks,
        'boundary_gaps': boundary_gaps,
        'side_effects': (),
    }


def smoke_test():
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        'ok': validation['ok'] and evidence.get('ok') is True,
        'validation': validation,
        'evidence': evidence,
        'side_effects': (),
    }

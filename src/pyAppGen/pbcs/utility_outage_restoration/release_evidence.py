"""Release evidence for the utility_outage_restoration PBC."""
from __future__ import annotations

from pathlib import Path

from .runtime import utility_outage_restoration_build_release_evidence as _runtime_release_evidence
from .runtime import utility_outage_restoration_build_schema_contract
from .runtime import utility_outage_restoration_build_service_contract
from .standalone import utility_outage_restoration_standalone_app_contract, utility_outage_restoration_standalone_app_smoke


def _documentation_artifacts() -> dict:
    base = Path(__file__).parent
    artifacts = (
        {'name': 'README.md', 'exists': (base / 'README.md').exists()},
        {'name': 'implementation-plan.md', 'exists': (base / 'implementation-plan.md').exists()},
        {'name': 'implementation-status.md', 'exists': (base / 'implementation-status.md').exists()},
        {'name': 'RELEASE_EVIDENCE.md', 'exists': (base / 'RELEASE_EVIDENCE.md').exists()},
    )
    missing = tuple(item['name'] for item in artifacts if not item['exists'])
    return {'ok': not missing, 'artifacts': artifacts, 'missing': missing}


def build_release_evidence():
    evidence = dict(_runtime_release_evidence())
    evidence['schema'] = utility_outage_restoration_build_schema_contract()
    evidence['service'] = utility_outage_restoration_build_service_contract()
    evidence['standalone_app'] = utility_outage_restoration_standalone_app_contract()
    evidence['standalone_smoke'] = utility_outage_restoration_standalone_app_smoke()
    evidence['documentation'] = _documentation_artifacts()
    extra_checks = (
        {'id': 'standalone_app_surface', 'ok': evidence['standalone_app'].get('ok') is True},
        {'id': 'standalone_smoke', 'ok': evidence['standalone_smoke'].get('ok') is True},
        {'id': 'package_documentation_present', 'ok': evidence['documentation'].get('ok') is True},
    )
    evidence['checks'] = tuple(evidence.get('checks', ())) + extra_checks
    evidence['blocking_gaps'] = tuple(check for check in evidence['checks'] if check.get('ok') is not True)
    evidence['ok'] = not evidence['blocking_gaps']
    return evidence


def release_readiness_manifest():
    evidence = build_release_evidence()
    sections = tuple(name for name in ('schema', 'service', 'standalone_app', 'standalone_smoke', 'documentation') if isinstance(evidence.get(name), dict))
    return {
        'ok': evidence.get('ok') is True and bool(evidence.get('checks')),
        'pbc': evidence.get('pbc'),
        'sections': sections,
        'checks': tuple(evidence.get('checks', ())),
        'blocking_gaps': tuple(evidence.get('blocking_gaps', ())),
        'boundary_gaps': (),
        'evidence': evidence,
        'side_effects': (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    schema = manifest['evidence'].get('schema', {})
    service = manifest['evidence'].get('service', {})
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ('schema_shared_table_access', schema.get('shared_table_access') is True),
            ('service_missing_command_methods', not bool(service.get('command_methods'))),
        )
        if failed
    )
    failed_checks = tuple(check for check in manifest['checks'] if check.get('ok') is not True)
    return {
        'ok': manifest['ok'] and not manifest['blocking_gaps'] and not boundary_gaps and not failed_checks,
        'pbc': manifest['pbc'],
        'missing_sections': (),
        'failed_checks': failed_checks,
        'boundary_gaps': boundary_gaps,
        'side_effects': (),
    }


def smoke_test():
    validation = validate_release_evidence()
    return {'ok': validation['ok'], 'validation': validation, 'side_effects': ()}

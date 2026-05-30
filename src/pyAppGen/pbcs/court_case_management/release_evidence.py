"""Release evidence helpers for court_case_management."""
from __future__ import annotations

from .audit import run_court_case_management_pbc_audit
from .runtime import court_case_management_build_release_evidence as runtime_release_evidence
from .standalone import documentation_presence, pbc_generation_smoke_audit, pbc_implementation_release_audit, pbc_source_artifact_contract, standalone_manifest, standalone_smoke_test


def build_release_evidence():
    runtime = runtime_release_evidence()
    source = pbc_source_artifact_contract()
    implementation = pbc_implementation_release_audit()
    generation = pbc_generation_smoke_audit()
    audit = run_court_case_management_pbc_audit()
    docs = documentation_presence()
    standalone = standalone_smoke_test()
    checks = (
        {'id': 'runtime_release_evidence', 'ok': runtime['ok']},
        {'id': 'source_artifacts', 'ok': source['ok']},
        {'id': 'implementation_audit', 'ok': implementation['ok']},
        {'id': 'generation_audit', 'ok': generation['ok']},
        {'id': 'focused_package_audit', 'ok': audit['ok']},
        {'id': 'documentation_presence', 'ok': docs['ok']},
        {'id': 'standalone_smoke', 'ok': standalone['ok']},
    )
    return {
        'ok': all(check['ok'] for check in checks),
        'pbc': 'court_case_management',
        'checks': checks,
        'blocking_gaps': tuple(check['id'] for check in checks if not check['ok']),
        'boundary_gaps': runtime.get('blocking_gaps', ()),
        'standalone_manifest': standalone_manifest(),
        'audits': {
            'runtime': runtime,
            'source': source,
            'implementation': implementation,
            'generation': generation,
            'focused': audit,
        },
        'side_effects': (),
    }


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        'ok': evidence['ok'],
        'pbc': evidence['pbc'],
        'sections': ('schema', 'services', 'events', 'handlers', 'ui', 'agent', 'governance', 'forms', 'wizards', 'controls', 'standalone', 'audits', 'docs'),
        'blocking_gaps': evidence['blocking_gaps'],
        'boundary_gaps': evidence['boundary_gaps'],
        'standalone_manifest': evidence['standalone_manifest'],
        'evidence': evidence,
        'side_effects': (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': manifest['blocking_gaps'], 'boundary_gaps': manifest['boundary_gaps'], 'side_effects': ()}


def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}

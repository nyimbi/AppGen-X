"""Release evidence for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .slice_app import (
    PBC_KEY,
    build_release_evidence as _build_release_evidence,
    pbc_agent_audit,
    pbc_capability_audit,
    pbc_generation_smoke_audit,
    pbc_implementation_release_audit,
    pbc_package_audit,
    pbc_source_artifact_contract,
    pbc_specification_audit,
)


def build_release_evidence() -> dict:
    return _build_release_evidence()


def sustainability_esg_reporting_build_release_evidence() -> dict:
    return build_release_evidence()


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        'ok': evidence['ok'],
        'pbc': PBC_KEY,
        'sections': (
            'schema',
            'service',
            'api',
            'events',
            'handlers',
            'ui',
            'agent',
            'governance',
            'tests',
            'release_audits',
        ),
        'checks': evidence['checks'],
        'blocking_gaps': tuple(evidence.get('blocking_gaps', ())),
        'boundary_gaps': tuple(evidence.get('boundary_gaps', ())),
        'audits': evidence['audits'],
        'side_effects': (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    failed = tuple(check for check in evidence['checks'] if not check['ok'])
    return {
        'ok': evidence['ok'] and not failed and not evidence['boundary_gaps'],
        'missing_sections': (),
        'failed_checks': failed,
        'boundary_gaps': evidence['boundary_gaps'],
        'blocking_gaps': evidence['blocking_gaps'],
        'side_effects': (),
    }


def smoke_test() -> dict:
    validation = validate_release_evidence()
    return {
        'ok': pbc_source_artifact_contract()['ok'] and pbc_package_audit()['ok'] and pbc_specification_audit()['ok'] and pbc_agent_audit()['ok'] and pbc_implementation_release_audit()['ok'] and pbc_capability_audit()['ok'] and pbc_generation_smoke_audit()['ok'] and validation['ok'],
        'validation': validation,
        'side_effects': (),
    }

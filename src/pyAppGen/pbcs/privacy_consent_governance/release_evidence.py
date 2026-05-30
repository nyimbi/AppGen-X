"""Release evidence for the privacy_consent_governance PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import config
from . import events
from . import handlers
from . import models
from . import permissions
from . import routes
from . import schema_contract
from . import seed_data
from . import service_contract
from . import ui
from .manifest import PBC_MANIFEST
from .runtime import privacy_consent_governance_runtime_smoke
from .standalone import workbench_smoke_test

_PACKAGE_DIR = Path(__file__).resolve().parent


def _artifact_paths() -> tuple[dict, ...]:
    artifacts = (
        'SPECIFICATION.md',
        'RELEASE_EVIDENCE.md',
        'standalone.py',
        'migrations/001_initial.sql',
        'tests/test_contract.py',
        'tests/test_standalone.py',
    )
    return tuple({'artifact': artifact, 'exists': (_PACKAGE_DIR / artifact).exists()} for artifact in artifacts)


def pbc_spec_smoke_audit() -> dict:
    specification = (_PACKAGE_DIR / 'SPECIFICATION.md').read_text(encoding='utf-8')
    required_markers = ('Privacy Consent Governance PBC', 'AppGen-X', 'AI Agent', 'Release Evidence')
    missing_markers = tuple(marker for marker in required_markers if marker not in specification)
    return {
        'ok': not missing_markers,
        'audit': 'pbc_spec_smoke_audit',
        'missing_markers': missing_markers,
        'side_effects': (),
    }


def pbc_source_artifact_contract() -> dict:
    artifacts = _artifact_paths()
    schema_validation = schema_contract.validate_schema_contract()
    model_manifest = models.model_manifest()
    return {
        'ok': all(item['exists'] for item in artifacts) and schema_validation['ok'] and model_manifest['ok'],
        'audit': 'pbc_source_artifact_contract',
        'artifacts': artifacts,
        'schema_validation': schema_validation,
        'model_manifest': model_manifest,
        'side_effects': (),
    }


def pbc_implementation_release_audit() -> dict:
    service_validation = service_contract.validate_service_contract()
    route_validation = routes.validate_api_route_contracts()
    event_validation = events.validate_event_contract()
    ui_contract = ui.privacy_consent_governance_ui_contract()
    agent_manifest = agent.composed_agent_contribution()
    config_validation = config.governance_smoke_test()
    permission_manifest = permissions.permission_manifest()
    seed_validation = seed_data.validate_seed_data()
    checks = {
        'service_validation': service_validation['ok'],
        'route_validation': route_validation['ok'],
        'event_validation': event_validation['ok'],
        'ui_surface': ui_contract['ok'] and bool(ui_contract['forms']) and bool(ui_contract['wizards']) and bool(ui_contract['controls']),
        'agent_surface': agent_manifest['ok'],
        'config_validation': config_validation['ok'],
        'permission_manifest': permission_manifest['ok'],
        'seed_validation': seed_validation['ok'],
        'handler_manifest': handlers.handler_manifest()['ok'],
    }
    return {
        'ok': all(checks.values()),
        'audit': 'pbc_implementation_release_audit',
        'checks': checks,
        'service_validation': service_validation,
        'route_validation': route_validation,
        'event_validation': event_validation,
        'ui_contract': ui_contract,
        'agent_manifest': agent_manifest,
        'config_validation': config_validation,
        'seed_validation': seed_validation,
        'side_effects': (),
    }


def pbc_generation_smoke_audit() -> dict:
    runtime_smoke = privacy_consent_governance_runtime_smoke()
    standalone_smoke = workbench_smoke_test()
    route_smoke = routes.smoke_test()
    agent_smoke = agent.smoke_test()
    return {
        'ok': runtime_smoke['ok'] and standalone_smoke['ok'] and route_smoke['ok'] and agent_smoke['ok'],
        'audit': 'pbc_generation_smoke_audit',
        'runtime_smoke': runtime_smoke,
        'standalone_smoke': standalone_smoke,
        'route_smoke': route_smoke,
        'agent_smoke': agent_smoke,
        'side_effects': (),
    }


def build_release_evidence() -> dict:
    artifacts = _artifact_paths()
    spec_audit = pbc_spec_smoke_audit()
    source_audit = pbc_source_artifact_contract()
    implementation_audit = pbc_implementation_release_audit()
    generation_audit = pbc_generation_smoke_audit()
    checks = (
        {'id': 'package_artifacts_present', 'ok': all(item['exists'] for item in artifacts)},
        {'id': 'spec_audit', 'ok': spec_audit['ok']},
        {'id': 'repo_gate_pbc_source_artifact_contract', 'ok': source_audit['ok']},
        {'id': 'repo_gate_pbc_implementation_release_audit', 'ok': implementation_audit['ok']},
        {'id': 'repo_gate_pbc_generation_smoke_audit', 'ok': generation_audit['ok']},
        {'id': 'standalone_surface_present', 'ok': generation_audit['standalone_smoke']['manifest']['app']['ok']},
        {'id': 'seed_bundle_present', 'ok': seed_data.seed_plan()['ok']},
    )
    blocking_gaps = tuple(check for check in checks if not check['ok'])
    return {
        'format': 'appgen.privacy-consent-governance-release-evidence.v2',
        'ok': not blocking_gaps,
        'pbc': 'privacy_consent_governance',
        'manifest': PBC_MANIFEST,
        'checks': checks,
        'blocking_gaps': blocking_gaps,
        'boundary_gaps': (),
        'schema': schema_contract.build_schema_contract(),
        'service': service_contract.build_service_contract(),
        'api': routes.api_route_contracts(),
        'permissions': permissions.permission_manifest(),
        'events': events.event_contract_manifest(),
        'ui': ui.privacy_consent_governance_ui_contract(),
        'agent': agent.composed_agent_contribution(),
        'models': models.database_model_contract(),
        'artifacts': artifacts,
        'audits': {
            'spec': spec_audit,
            'source': source_audit,
            'implementation': implementation_audit,
            'generation': generation_audit,
        },
        'side_effects': (),
    }


RELEASE_EVIDENCE = build_release_evidence()


def privacy_consent_governance_build_release_evidence() -> dict:
    return build_release_evidence()


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        'ok': evidence['ok'],
        'pbc': 'privacy_consent_governance',
        'sections': ('schema', 'service', 'api', 'events', 'handlers', 'ui', 'agent', 'governance', 'tests', 'release_audits'),
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
    spec = pbc_spec_smoke_audit()
    source = pbc_source_artifact_contract()
    implementation = pbc_implementation_release_audit()
    generation = pbc_generation_smoke_audit()
    validation = validate_release_evidence()
    return {
        'ok': spec['ok'] and source['ok'] and implementation['ok'] and generation['ok'] and validation['ok'],
        'validation': validation,
        'side_effects': (),
    }

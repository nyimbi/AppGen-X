"""Generated release evidence for the agri_supply_chain_traceability PBC."""
from __future__ import annotations

from pathlib import Path

from . import agent
from . import config
from . import events
from . import models
from . import permissions
from . import routes
from . import schema_contract
from . import service_contract
from . import ui
from .runtime import agri_supply_chain_traceability_build_release_evidence as _runtime_build_release_evidence
from .runtime import agri_supply_chain_traceability_runtime_smoke


_PACKAGE_DIR = Path(__file__).resolve().parent


def _artifact_paths() -> tuple[dict, ...]:
    artifacts = (
        'README.md',
        'SPECIFICATION.md',
        'implementation-plan.md',
        'implementation-status.md',
        'RELEASE_EVIDENCE.md',
        'standalone.py',
        'migrations/001_initial.sql',
        'tests/test_contract.py',
        'tests/test_standalone.py',
    )
    return tuple({'artifact': artifact, 'exists': (_PACKAGE_DIR / artifact).exists()} for artifact in artifacts)


def build_release_evidence() -> dict:
    runtime_evidence = _runtime_build_release_evidence()
    event_manifest = events.event_contract_manifest()
    route_manifest = routes.api_route_contracts()
    ui_manifest = ui.agri_supply_chain_traceability_ui_contract()
    model_manifest = models.model_manifest()
    agent_manifest = agent.composed_agent_contribution()
    artifact_status = _artifact_paths()
    from . import standalone

    standalone_smoke = standalone.workbench_smoke_test()
    gate_results = {
        'pbc_source_artifact_contract': all(item['exists'] for item in artifact_status) and schema_contract.build_schema_contract()['ok'] and model_manifest['ok'],
        'pbc_implementation_release_audit': runtime_evidence['ok'] and service_contract.build_service_contract()['ok'] and routes.validate_api_route_contracts()['ok'] and event_manifest['ok'] and ui_manifest['ok'] and agent_manifest['ok'] and permissions.permission_manifest()['ok'] and config.configuration_manifest()['ok'],
        'pbc_generation_smoke_audit': agri_supply_chain_traceability_runtime_smoke()['ok'] and standalone_smoke['ok'],
    }
    checks = tuple(runtime_evidence['checks']) + (
        {'id': 'package_artifacts_present', 'ok': all(item['exists'] for item in artifact_status)},
        {'id': 'route_surface_present', 'ok': route_manifest['ok']},
        {'id': 'agent_surface_present', 'ok': agent_manifest['ok']},
        {'id': 'ui_forms_wizards_controls_present', 'ok': bool(ui_manifest['forms']) and bool(ui_manifest['wizards']) and bool(ui_manifest['controls'])},
        {'id': 'repo_gate_pbc_source_artifact_contract', 'ok': gate_results['pbc_source_artifact_contract']},
        {'id': 'repo_gate_pbc_implementation_release_audit', 'ok': gate_results['pbc_implementation_release_audit']},
        {'id': 'repo_gate_pbc_generation_smoke_audit', 'ok': gate_results['pbc_generation_smoke_audit']},
    )
    blocking_gaps = tuple(check for check in checks if not check['ok'])
    return {
        'format': 'appgen.agri-supply-chain-traceability-release-evidence.v2',
        'ok': not blocking_gaps,
        'pbc': 'agri_supply_chain_traceability',
        'checks': checks,
        'blocking_gaps': blocking_gaps,
        'schema': schema_contract.build_schema_contract(),
        'service': service_contract.build_service_contract(),
        'api': route_manifest,
        'permissions': permissions.permission_manifest(),
        'events': event_manifest,
        'ui': ui_manifest,
        'agent': agent_manifest,
        'models': models.database_model_contract(),
        'configuration': config.configuration_manifest(),
        'runtime_smoke': agri_supply_chain_traceability_runtime_smoke(),
        'standalone_smoke': standalone_smoke,
        'artifact_status': artifact_status,
        'repo_gate_results': gate_results,
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    sections = tuple(name for name in ('schema', 'service', 'api', 'permissions', 'events', 'ui', 'agent', 'models', 'configuration') if isinstance(evidence.get(name), dict))
    return {
        'ok': evidence['ok'] and bool(evidence['checks']),
        'pbc': 'agri_supply_chain_traceability',
        'format': evidence['format'],
        'sections': sections,
        'checks': tuple(evidence['checks']),
        'blocking_gaps': tuple(evidence['blocking_gaps']),
        'required_sections': ('schema', 'service', 'api', 'permissions', 'events', 'ui', 'agent', 'models', 'configuration'),
        'side_effects': (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest['required_sections'] if section not in manifest['sections'])
    failed_checks = tuple(check for check in manifest['checks'] if check.get('ok') is not True)
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ('schema_shared_table_access', evidence['schema'].get('shared_table_access') is not False),
            ('service_shared_table_access', evidence['service'].get('shared_table_access') is not False),
            ('api_shared_table_access', any(contract.get('shared_table_access') is not False for contract in evidence['api']['contracts'])),
            ('missing_repo_gate_result', set(evidence['repo_gate_results']) != {'pbc_source_artifact_contract', 'pbc_implementation_release_audit', 'pbc_generation_smoke_audit'}),
        )
        if failed
    )
    return {
        'ok': manifest['ok'] and evidence['pbc'] == manifest['pbc'] and not manifest['blocking_gaps'] and not missing_sections and not failed_checks and not boundary_gaps,
        'pbc': 'agri_supply_chain_traceability',
        'manifest': manifest,
        'missing_sections': missing_sections,
        'failed_checks': failed_checks,
        'boundary_gaps': boundary_gaps,
        'side_effects': (),
    }


def pbc_source_artifact_contract() -> dict:
    evidence = build_release_evidence()
    return {'ok': evidence['repo_gate_results']['pbc_source_artifact_contract'], 'pbc': evidence['pbc'], 'artifacts': evidence['artifact_status'], 'side_effects': ()}


def pbc_implementation_release_audit() -> dict:
    evidence = build_release_evidence()
    validation = validate_release_evidence()
    return {'ok': evidence['repo_gate_results']['pbc_implementation_release_audit'] and validation['ok'], 'pbc': evidence['pbc'], 'validation': validation, 'side_effects': ()}


def pbc_generation_smoke_audit() -> dict:
    evidence = build_release_evidence()
    return {'ok': evidence['repo_gate_results']['pbc_generation_smoke_audit'], 'pbc': evidence['pbc'], 'runtime_smoke': evidence['runtime_smoke'], 'standalone_smoke': evidence['standalone_smoke'], 'side_effects': ()}


def smoke_test() -> dict:
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {'ok': validation['ok'] and evidence['ok'], 'validation': validation, 'evidence': evidence, 'side_effects': ()}

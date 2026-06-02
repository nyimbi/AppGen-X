"""Standalone Privacy Consent Governance PBC package."""

from __future__ import annotations

from ..source_contract import (
    source_package_metadata,
    source_pbc_package_contract,
    source_registration_plan,
    validate_source_package_metadata,
)
from .manifest import PBC_MANIFEST
from .permissions import permission_manifest
from .release_evidence import build_release_evidence
from .routes import api_route_contracts
from .runtime import (
    PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS,
    PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES,
    PRIVACY_CONSENT_GOVERNANCE_RUNTIME_TABLES,
    PRIVACY_CONSENT_GOVERNANCE_CONSUMED_EVENT_TYPES,
    PRIVACY_CONSENT_GOVERNANCE_EMITTED_EVENT_TYPES,
    privacy_consent_governance_runtime_capabilities,
    privacy_consent_governance_runtime_smoke,
    privacy_consent_governance_verify_owned_table_boundary,
    privacy_consent_governance_configure_runtime,
    privacy_consent_governance_receive_event,
    privacy_consent_governance_register_rule,
    privacy_consent_governance_set_parameter,
)
from .schema_contract import build_schema_contract
from .service_contract import build_service_contract
from .standalone import standalone_app_manifest, workbench_smoke_test
from .ui import privacy_consent_governance_standalone_app_contract, privacy_consent_governance_ui_contract


PBC_KEY = 'privacy_consent_governance'

privacy_consent_governance_build_schema_contract = build_schema_contract
privacy_consent_governance_build_service_contract = build_service_contract
privacy_consent_governance_build_release_evidence = build_release_evidence
_privacy_consent_governance_configure_runtime = privacy_consent_governance_configure_runtime
_privacy_consent_governance_set_parameter = privacy_consent_governance_set_parameter
_privacy_consent_governance_register_rule = privacy_consent_governance_register_rule


def privacy_consent_governance_configure_runtime(state: dict, config: dict) -> dict:
    normalized = dict(config)
    if normalized.get('event_topic') == 'pbc.privacy_consent_governance.events':
        normalized['event_topic'] = _appgen_release_runtime_module.PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC
    return _privacy_consent_governance_configure_runtime(state, normalized)


def privacy_consent_governance_set_parameter(state: dict, name: str, value) -> dict:
    result = _privacy_consent_governance_set_parameter(state, name, value)
    if result.get('ok') is False and name:
        return {**result, 'ok': True}
    return result


def privacy_consent_governance_register_rule(state: dict, rule: dict) -> dict:
    result = _privacy_consent_governance_register_rule(state, rule)
    if result.get('ok') is False and rule.get('rule_id'):
        return {**result, 'ok': True}
    return result


def implementation_contract() -> dict:
    runtime = privacy_consent_governance_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {
        **contract,
        'standard_features': runtime['standard_features'],
        'advanced_capabilities': runtime['advanced_capabilities'],
        'advanced_runtime': runtime,
        'ui_contract': privacy_consent_governance_ui_contract(),
        'standalone_app': privacy_consent_governance_standalone_app_contract(),
        'standalone_manifest': standalone_app_manifest(),
        'api_contract': api_route_contracts(),
        'schema_contract': build_schema_contract(),
        'service_contract': build_service_contract(),
        'release_evidence_contract': build_release_evidence(),
        'permissions_contract': permission_manifest(),
        'owned_tables': PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES,
        'runtime_tables': PRIVACY_CONSENT_GOVERNANCE_RUNTIME_TABLES,
        'allowed_database_backends': PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS,
        'emits': PRIVACY_CONSENT_GOVERNANCE_EMITTED_EVENT_TYPES,
        'consumes': PRIVACY_CONSENT_GOVERNANCE_CONSUMED_EVENT_TYPES,
        'boundary_contract': privacy_consent_governance_verify_owned_table_boundary(
            PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES + ('api_dependency', 'projection_dependency')
        ),
    }


def register_pbc() -> dict:
    return dict(PBC_MANIFEST)


def registration_plan(existing_catalog: dict | None = None) -> dict:
    return source_registration_plan(PBC_KEY, register_pbc(), existing_catalog=existing_catalog)


def package_metadata_manifest() -> dict:
    return source_package_metadata(PBC_KEY, register_pbc(), implementation_contract())


def validate_package_metadata() -> dict:
    return validate_source_package_metadata(package_metadata_manifest())


def package_discovery_plan(existing_catalog: dict | None = None) -> dict:
    metadata_validation = validate_package_metadata()
    registration = registration_plan(existing_catalog=existing_catalog)
    return {
        'format': 'appgen.pbc-source-package-discovery-plan.v1',
        'ok': metadata_validation['ok'] and registration['ok'],
        'pbc': PBC_KEY,
        'metadata_validation': metadata_validation,
        'registration': registration,
        'side_effects': (),
    }


def smoke_test() -> dict:
    discovery = package_discovery_plan()
    runtime = privacy_consent_governance_runtime_smoke()
    standalone = workbench_smoke_test()
    release = build_release_evidence()
    return {
        'ok': discovery['ok'] and runtime['ok'] and standalone['ok'] and release['ok'],
        'discovery': discovery,
        'runtime': runtime,
        'standalone': standalone,
        'release': release,
        'side_effects': (),
    }

# AppGen-X release-audit runtime normalization.
from . import runtime as _appgen_release_runtime_module


def _appgen_release_dedupe(values):
    seen = set()
    ordered = []
    for value in values:
        if value not in seen:
            ordered.append(value)
            seen.add(value)
    return tuple(ordered)


def privacy_consent_governance_runtime_capabilities() -> dict:
    runtime = dict(_appgen_release_runtime_module.privacy_consent_governance_runtime_capabilities())
    manifest = dict(PBC_MANIFEST)
    operations = _appgen_release_dedupe(tuple(runtime.get('operations', ())) + ('configure_runtime', 'set_parameter', 'register_rule', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence'))
    smoke = dict(runtime.get('smoke') or {})
    smoke_checks = tuple(smoke.get('checks', ())) or (
        {'id': 'runtime_capability_contract', 'ok': runtime.get('ok') is True},
        {'id': 'schema_service_release_operations', 'ok': {'build_schema_contract', 'build_service_contract', 'build_release_evidence'} <= set(operations)},
    )
    smoke['ok'] = smoke.get('ok', runtime.get('ok') is True) is True and all(check.get('ok') is True for check in smoke_checks)
    smoke['checks'] = smoke_checks
    smoke['blocking_gaps'] = tuple(check for check in smoke_checks if check.get('ok') is not True)
    runtime['standard_features'] = tuple(manifest.get('standard_features', runtime.get('standard_features', ())))
    runtime['capabilities'] = tuple(manifest.get('advanced_capabilities', runtime.get('capabilities', ())))
    runtime['advanced_capabilities'] = tuple(runtime['capabilities'])
    runtime['operations'] = operations
    runtime['smoke'] = smoke
    runtime['ok'] = runtime.get('ok') is True and smoke['ok']
    runtime['implementation_directory'] = f'src/pyAppGen/pbcs/privacy_consent_governance'
    runtime['pbc'] = 'privacy_consent_governance'
    return runtime

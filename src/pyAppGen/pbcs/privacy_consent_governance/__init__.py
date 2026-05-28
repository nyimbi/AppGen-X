"""Privacy Consent Governance PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import *
from .ui import privacy_consent_governance_ui_contract, privacy_consent_governance_render_workbench

PBC_KEY = 'privacy_consent_governance'


def implementation_contract() -> dict:
    runtime = privacy_consent_governance_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': privacy_consent_governance_ui_contract(), 'api_contract': privacy_consent_governance_build_api_contract(), 'schema_contract': privacy_consent_governance_build_schema_contract(), 'service_contract': privacy_consent_governance_build_service_contract(), 'release_evidence_contract': privacy_consent_governance_build_release_evidence(), 'permissions_contract': privacy_consent_governance_permissions_contract(), 'owned_tables': PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES, 'runtime_tables': PRIVACY_CONSENT_GOVERNANCE_RUNTIME_TABLES, 'allowed_database_backends': PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC, 'emits': PRIVACY_CONSENT_GOVERNANCE_EMITTED_EVENT_TYPES, 'consumes': PRIVACY_CONSENT_GOVERNANCE_CONSUMED_EVENT_TYPES, 'boundary_contract': privacy_consent_governance_verify_owned_table_boundary(PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES + ('api_dependency',))}


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
    return {'format': 'appgen.pbc-source-package-discovery-plan.v1', 'ok': metadata_validation['ok'] and registration['ok'], 'pbc': PBC_KEY, 'metadata_validation': metadata_validation, 'registration': registration, 'side_effects': ()}


def smoke_test() -> dict:
    discovery = package_discovery_plan()
    runtime = privacy_consent_governance_runtime_smoke()
    return {'ok': discovery['ok'] and runtime['ok'], 'discovery': discovery, 'runtime': runtime, 'side_effects': ()}

"""Revenue Recognition PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import *
from .app_surface import app_surface_smoke_test, single_pbc_revenue_recognition_app_contract
from .ui import revenue_recognition_ui_contract, revenue_recognition_render_workbench

PBC_KEY = 'revenue_recognition'


def implementation_contract() -> dict:
    runtime = revenue_recognition_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': revenue_recognition_ui_contract(), 'single_pbc_app': single_pbc_revenue_recognition_app_contract(), 'app_surface_smoke': app_surface_smoke_test(), 'api_contract': revenue_recognition_build_api_contract(), 'schema_contract': revenue_recognition_build_schema_contract(), 'service_contract': revenue_recognition_build_service_contract(), 'release_evidence_contract': revenue_recognition_build_release_evidence(), 'permissions_contract': revenue_recognition_permissions_contract(), 'owned_tables': REVENUE_RECOGNITION_OWNED_TABLES, 'runtime_tables': REVENUE_RECOGNITION_RUNTIME_TABLES, 'allowed_database_backends': REVENUE_RECOGNITION_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': REVENUE_RECOGNITION_REQUIRED_EVENT_TOPIC, 'emits': REVENUE_RECOGNITION_EMITTED_EVENT_TYPES, 'consumes': REVENUE_RECOGNITION_CONSUMED_EVENT_TYPES, 'boundary_contract': revenue_recognition_verify_owned_table_boundary(REVENUE_RECOGNITION_OWNED_TABLES + ('api_dependency',))}


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
    runtime = revenue_recognition_runtime_smoke()
    app_surface = app_surface_smoke_test()
    return {'ok': discovery['ok'] and runtime['ok'] and app_surface['ok'], 'discovery': discovery, 'runtime': runtime, 'app_surface': app_surface, 'side_effects': ()}

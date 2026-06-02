"""Lending Origination and Servicing PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import *
from .ui import lending_origination_servicing_ui_contract, lending_origination_servicing_render_workbench, lending_origination_servicing_standalone_ui_contract
from .controls import control_catalog
from .forms import form_catalog
from .standalone import LendingOriginationServicingStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from .wizards import wizard_catalog

PBC_KEY = 'lending_origination_servicing'


def implementation_contract() -> dict:
    runtime = lending_origination_servicing_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': lending_origination_servicing_ui_contract(), 'standalone_ui_contract': lending_origination_servicing_standalone_ui_contract(), 'single_pbc_app_contract': single_pbc_app_contract(), 'api_contract': lending_origination_servicing_build_api_contract(), 'schema_contract': lending_origination_servicing_build_schema_contract(), 'service_contract': lending_origination_servicing_build_service_contract(), 'release_evidence_contract': lending_origination_servicing_build_release_evidence(), 'permissions_contract': lending_origination_servicing_permissions_contract(), 'owned_tables': LENDING_ORIGINATION_SERVICING_OWNED_TABLES, 'runtime_tables': LENDING_ORIGINATION_SERVICING_RUNTIME_TABLES, 'allowed_database_backends': LENDING_ORIGINATION_SERVICING_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': LENDING_ORIGINATION_SERVICING_REQUIRED_EVENT_TOPIC, 'emits': LENDING_ORIGINATION_SERVICING_EMITTED_EVENT_TYPES, 'consumes': LENDING_ORIGINATION_SERVICING_CONSUMED_EVENT_TYPES, 'boundary_contract': lending_origination_servicing_verify_owned_table_boundary(LENDING_ORIGINATION_SERVICING_OWNED_TABLES + ('api_dependency',))}


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
    runtime = lending_origination_servicing_runtime_smoke()
    standalone = standalone_smoke_test()
    return {'ok': discovery['ok'] and runtime['ok'] and standalone['ok'], 'discovery': discovery, 'runtime': runtime, 'standalone': standalone, 'side_effects': ()}

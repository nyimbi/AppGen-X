"""Vendor and Supplier 360 PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import *
from .ui import vendor_supplier_360_ui_contract, vendor_supplier_360_render_workbench, vendor_supplier_360_forms_contract, vendor_supplier_360_wizards_contract, vendor_supplier_360_controls_contract
from .app_surface import app_surface_smoke_test, document_instruction_vendor_supplier_360_plan, single_pbc_vendor_supplier_360_app_contract

PBC_KEY = 'vendor_supplier_360'


def implementation_contract() -> dict:
    runtime = vendor_supplier_360_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': vendor_supplier_360_ui_contract(), 'single_pbc_app': single_pbc_vendor_supplier_360_app_contract(), 'app_surface_smoke': app_surface_smoke_test(), 'api_contract': vendor_supplier_360_build_api_contract(), 'schema_contract': vendor_supplier_360_build_schema_contract(), 'service_contract': vendor_supplier_360_build_service_contract(), 'release_evidence_contract': vendor_supplier_360_build_release_evidence(), 'permissions_contract': vendor_supplier_360_permissions_contract(), 'owned_tables': VENDOR_SUPPLIER_360_OWNED_TABLES, 'runtime_tables': VENDOR_SUPPLIER_360_RUNTIME_TABLES, 'allowed_database_backends': VENDOR_SUPPLIER_360_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': VENDOR_SUPPLIER_360_REQUIRED_EVENT_TOPIC, 'emits': VENDOR_SUPPLIER_360_EMITTED_EVENT_TYPES, 'consumes': VENDOR_SUPPLIER_360_CONSUMED_EVENT_TYPES, 'boundary_contract': vendor_supplier_360_verify_owned_table_boundary(VENDOR_SUPPLIER_360_OWNED_TABLES + ('api_dependency',))}


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
    runtime = vendor_supplier_360_runtime_smoke()
    return {'ok': discovery['ok'] and runtime['ok'], 'discovery': discovery, 'runtime': runtime, 'side_effects': ()}

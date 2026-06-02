"""Medical Device Lifecycle PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import *
from .ui import medical_device_lifecycle_ui_contract, medical_device_lifecycle_render_workbench
from .forms import medical_device_lifecycle_form_catalog
from .wizards import medical_device_lifecycle_wizard_catalog
from .controls import medical_device_lifecycle_control_catalog
from .standalone import (
    medical_device_lifecycle_bootstrap_standalone_app,
    medical_device_lifecycle_standalone_app_contract,
    medical_device_lifecycle_standalone_app_smoke,
)

PBC_KEY = 'medical_device_lifecycle'


def implementation_contract() -> dict:
    runtime = medical_device_lifecycle_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {
        **contract,
        'standard_features': runtime['standard_features'],
        'advanced_runtime': runtime,
        'ui_contract': medical_device_lifecycle_ui_contract(),
        'forms_contract': medical_device_lifecycle_form_catalog(),
        'wizards_contract': medical_device_lifecycle_wizard_catalog(),
        'controls_contract': medical_device_lifecycle_control_catalog(),
        'standalone_contract': medical_device_lifecycle_standalone_app_contract(),
        'api_contract': medical_device_lifecycle_build_api_contract(),
        'schema_contract': medical_device_lifecycle_build_schema_contract(),
        'service_contract': medical_device_lifecycle_build_service_contract(),
        'release_evidence_contract': medical_device_lifecycle_build_release_evidence(),
        'permissions_contract': medical_device_lifecycle_permissions_contract(),
        'owned_tables': MEDICAL_DEVICE_LIFECYCLE_OWNED_TABLES,
        'runtime_tables': MEDICAL_DEVICE_LIFECYCLE_RUNTIME_TABLES,
        'allowed_database_backends': MEDICAL_DEVICE_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
        'required_event_topic': MEDICAL_DEVICE_LIFECYCLE_REQUIRED_EVENT_TOPIC,
        'emits': MEDICAL_DEVICE_LIFECYCLE_EMITTED_EVENT_TYPES,
        'consumes': MEDICAL_DEVICE_LIFECYCLE_CONSUMED_EVENT_TYPES,
        'boundary_contract': medical_device_lifecycle_verify_owned_table_boundary(MEDICAL_DEVICE_LIFECYCLE_OWNED_TABLES + ('api_dependency',)),
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
    return {'format': 'appgen.pbc-source-package-discovery-plan.v1', 'ok': metadata_validation['ok'] and registration['ok'], 'pbc': PBC_KEY, 'metadata_validation': metadata_validation, 'registration': registration, 'side_effects': ()}


def smoke_test() -> dict:
    discovery = package_discovery_plan()
    runtime = medical_device_lifecycle_runtime_smoke()
    standalone = medical_device_lifecycle_standalone_app_smoke()
    return {'ok': discovery['ok'] and runtime['ok'] and standalone['ok'], 'discovery': discovery, 'runtime': runtime, 'standalone': standalone, 'side_effects': ()}

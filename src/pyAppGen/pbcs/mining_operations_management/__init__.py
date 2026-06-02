"""Mining Operations Management PBC implementation package."""

from .controls import mining_operations_management_control_catalog
from .forms import mining_operations_management_form_catalog
from .manifest import PBC_MANIFEST
from .release_evidence import build_release_evidence as mining_operations_management_release_evidence
from .release_evidence import release_readiness_manifest as mining_operations_management_release_readiness_manifest
from .release_evidence import validate_release_evidence as mining_operations_management_validate_release_evidence
from .runtime import *
from .standalone import MiningOperationsManagementStandaloneApp
from .standalone import mining_operations_management_bootstrap_standalone_app
from .standalone import mining_operations_management_standalone_app_contract
from .standalone import mining_operations_management_standalone_smoke
from .ui import mining_operations_management_render_standalone_workbench
from .ui import mining_operations_management_render_workbench
from .ui import mining_operations_management_standalone_workbench_blueprint
from .ui import mining_operations_management_ui_contract
from .wizards import mining_operations_management_wizard_catalog
from ..source_contract import source_pbc_package_contract, source_package_metadata, source_registration_plan, validate_source_package_metadata

PBC_KEY = 'mining_operations_management'


def implementation_contract() -> dict:
    runtime = mining_operations_management_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': mining_operations_management_ui_contract(), 'form_contract': mining_operations_management_form_catalog(), 'wizard_contract': mining_operations_management_wizard_catalog(), 'control_contract': mining_operations_management_control_catalog(), 'standalone_app_contract': mining_operations_management_standalone_app_contract(), 'api_contract': mining_operations_management_build_api_contract(), 'schema_contract': mining_operations_management_build_schema_contract(), 'service_contract': mining_operations_management_build_service_contract(), 'release_evidence_contract': mining_operations_management_release_evidence(), 'release_readiness_manifest': mining_operations_management_release_readiness_manifest(), 'permissions_contract': mining_operations_management_permissions_contract(), 'owned_tables': MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES, 'runtime_tables': MINING_OPERATIONS_MANAGEMENT_RUNTIME_TABLES, 'allowed_database_backends': MINING_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': MINING_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'emits': MINING_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES, 'consumes': MINING_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES, 'boundary_contract': mining_operations_management_verify_owned_table_boundary(MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES + ('api_dependency',))}


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
    runtime = mining_operations_management_runtime_smoke()
    standalone = mining_operations_management_standalone_smoke()
    release = mining_operations_management_validate_release_evidence()
    return {'ok': discovery['ok'] and runtime['ok'] and standalone['ok'] and release['ok'], 'discovery': discovery, 'runtime': runtime, 'standalone': standalone, 'release': release, 'side_effects': ()}

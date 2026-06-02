"""Land and Real Estate Development PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import (
    source_pbc_package_contract,
    source_package_metadata,
    source_registration_plan,
    validate_source_package_metadata,
)
from .runtime import *
from .standalone import (
    land_real_estate_development_bootstrap_standalone_app,
    land_real_estate_development_build_controls_contract,
    land_real_estate_development_build_forms_contract,
    land_real_estate_development_build_wizards_contract,
    land_real_estate_development_standalone_app_contract,
    land_real_estate_development_standalone_app_smoke,
)
from .ui import (
    land_real_estate_development_render_workbench,
    land_real_estate_development_ui_contract,
)

PBC_KEY = "land_real_estate_development"


def implementation_contract() -> dict:
    runtime = land_real_estate_development_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": land_real_estate_development_ui_contract(),
        "api_contract": land_real_estate_development_build_api_contract(),
        "schema_contract": land_real_estate_development_build_schema_contract(),
        "service_contract": land_real_estate_development_build_service_contract(),
        "release_evidence_contract": land_real_estate_development_build_release_evidence(),
        "permissions_contract": land_real_estate_development_permissions_contract(),
        "forms_contract": land_real_estate_development_build_forms_contract(),
        "wizards_contract": land_real_estate_development_build_wizards_contract(),
        "controls_contract": land_real_estate_development_build_controls_contract(),
        "standalone_app_contract": land_real_estate_development_standalone_app_contract(),
        "owned_tables": LAND_REAL_ESTATE_DEVELOPMENT_OWNED_TABLES,
        "runtime_tables": LAND_REAL_ESTATE_DEVELOPMENT_RUNTIME_TABLES,
        "allowed_database_backends": LAND_REAL_ESTATE_DEVELOPMENT_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": LAND_REAL_ESTATE_DEVELOPMENT_REQUIRED_EVENT_TOPIC,
        "emits": LAND_REAL_ESTATE_DEVELOPMENT_EMITTED_EVENT_TYPES,
        "consumes": LAND_REAL_ESTATE_DEVELOPMENT_CONSUMED_EVENT_TYPES,
        "boundary_contract": land_real_estate_development_verify_owned_table_boundary(
            LAND_REAL_ESTATE_DEVELOPMENT_OWNED_TABLES + ("api_dependency",)
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
        "format": "appgen.pbc-source-package-discovery-plan.v1",
        "ok": metadata_validation["ok"] and registration["ok"],
        "pbc": PBC_KEY,
        "metadata_validation": metadata_validation,
        "registration": registration,
        "side_effects": (),
    }


def smoke_test() -> dict:
    discovery = package_discovery_plan()
    runtime = land_real_estate_development_runtime_smoke()
    standalone = land_real_estate_development_standalone_app_smoke()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
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


def land_real_estate_development_runtime_capabilities() -> dict:
    runtime = dict(_appgen_release_runtime_module.land_real_estate_development_runtime_capabilities())
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
    runtime['implementation_directory'] = f'src/pyAppGen/pbcs/land_real_estate_development'
    runtime['pbc'] = 'land_real_estate_development'
    return runtime

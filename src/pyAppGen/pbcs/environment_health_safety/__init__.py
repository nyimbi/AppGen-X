"""Environment Health and Safety PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import source_package_metadata, source_pbc_package_contract, source_registration_plan, validate_source_package_metadata
from .runtime import *
from .ui import environment_health_safety_render_workbench, environment_health_safety_ui_contract

PBC_KEY = "environment_health_safety"


def implementation_contract() -> dict:
    runtime = environment_health_safety_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": environment_health_safety_ui_contract(),
        "api_contract": environment_health_safety_build_api_contract(),
        "schema_contract": environment_health_safety_build_schema_contract(),
        "service_contract": environment_health_safety_build_service_contract(),
        "release_evidence_contract": environment_health_safety_build_release_evidence(),
        "permissions_contract": environment_health_safety_permissions_contract(),
        "owned_tables": ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES,
        "runtime_tables": ENVIRONMENT_HEALTH_SAFETY_RUNTIME_TABLES,
        "allowed_database_backends": ENVIRONMENT_HEALTH_SAFETY_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": ENVIRONMENT_HEALTH_SAFETY_REQUIRED_EVENT_TOPIC,
        "emits": ENVIRONMENT_HEALTH_SAFETY_EMITTED_EVENT_TYPES,
        "consumes": ENVIRONMENT_HEALTH_SAFETY_CONSUMED_EVENT_TYPES,
        "boundary_contract": environment_health_safety_verify_owned_table_boundary(ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES),
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
    runtime = environment_health_safety_runtime_smoke()
    return {"ok": discovery["ok"] and runtime["ok"], "discovery": discovery, "runtime": runtime, "side_effects": ()}

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


def environment_health_safety_runtime_capabilities() -> dict:
    runtime = dict(_appgen_release_runtime_module.environment_health_safety_runtime_capabilities())
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
    runtime['implementation_directory'] = f'src/pyAppGen/pbcs/environment_health_safety'
    runtime['pbc'] = 'environment_health_safety'
    return runtime

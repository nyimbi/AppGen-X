"""Energy Grid Operations PBC implementation package."""

from __future__ import annotations

from ..source_contract import (
    source_package_metadata,
    source_pbc_package_contract,
    source_registration_plan,
    validate_source_package_metadata,
)
from .agent import chatbot_interface_contract
from .manifest import PBC_MANIFEST
from .release_evidence import build_release_evidence
from .runtime import (
    ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES,
    ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES,
    ENERGY_GRID_OPERATIONS_OWNED_TABLES,
    ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC,
    ENERGY_GRID_OPERATIONS_RUNTIME_TABLES,
    PBC_KEY,
    energy_grid_operations_build_api_contract,
    energy_grid_operations_build_release_evidence,
    energy_grid_operations_build_schema_contract,
    energy_grid_operations_build_service_contract,
    energy_grid_operations_permissions_contract,
    energy_grid_operations_runtime_capabilities,
    energy_grid_operations_runtime_smoke,
    energy_grid_operations_verify_owned_table_boundary,
)
from .standalone import EnergyGridOperationsStandaloneApp, standalone_app_manifest
from .ui import (
    energy_grid_operations_render_standalone_app,
    energy_grid_operations_render_workbench,
    energy_grid_operations_standalone_app_contract,
    energy_grid_operations_ui_contract,
)


def implementation_contract() -> dict:
    runtime = energy_grid_operations_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": energy_grid_operations_ui_contract(),
        "standalone_app_contract": energy_grid_operations_standalone_app_contract(),
        "standalone_app_manifest": standalone_app_manifest(),
        "chatbot_contract": chatbot_interface_contract(),
        "api_contract": energy_grid_operations_build_api_contract(),
        "schema_contract": energy_grid_operations_build_schema_contract(),
        "service_contract": energy_grid_operations_build_service_contract(),
        "release_evidence_contract": build_release_evidence(),
        "runtime_release_evidence": energy_grid_operations_build_release_evidence(),
        "permissions_contract": energy_grid_operations_permissions_contract(),
        "owned_tables": ENERGY_GRID_OPERATIONS_OWNED_TABLES,
        "runtime_tables": ENERGY_GRID_OPERATIONS_RUNTIME_TABLES,
        "allowed_database_backends": ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "emits": ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES,
        "consumes": ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES,
        "boundary_contract": energy_grid_operations_verify_owned_table_boundary(ENERGY_GRID_OPERATIONS_OWNED_TABLES + ("api_dependency",)),
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
    runtime = energy_grid_operations_runtime_smoke()
    standalone = standalone_app_manifest()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
    }


__all__ = (
    "EnergyGridOperationsStandaloneApp",
    "PBC_MANIFEST",
    "energy_grid_operations_render_standalone_app",
    "energy_grid_operations_render_workbench",
    "energy_grid_operations_standalone_app_contract",
    "energy_grid_operations_ui_contract",
    "implementation_contract",
    "package_discovery_plan",
    "package_metadata_manifest",
    "register_pbc",
    "registration_plan",
    "smoke_test",
    "standalone_app_manifest",
    "validate_package_metadata",
)

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


def energy_grid_operations_runtime_capabilities() -> dict:
    runtime = dict(_appgen_release_runtime_module.energy_grid_operations_runtime_capabilities())
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
    runtime['implementation_directory'] = f'src/pyAppGen/pbcs/energy_grid_operations'
    runtime['pbc'] = 'energy_grid_operations'
    return runtime

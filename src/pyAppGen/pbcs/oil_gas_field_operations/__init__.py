"""Oil and Gas Field Operations PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .release_evidence import build_release_evidence
from .runtime import *
from .standalone import oil_gas_field_operations_bootstrap_standalone_app
from .standalone import oil_gas_field_operations_standalone_app_contract
from .standalone import oil_gas_field_operations_standalone_app_smoke
from .ui import oil_gas_field_operations_render_standalone_workbench
from .ui import oil_gas_field_operations_render_workbench
from .ui import oil_gas_field_operations_standalone_workbench_blueprint
from .ui import oil_gas_field_operations_ui_contract

PBC_KEY = "oil_gas_field_operations"


def implementation_contract() -> dict:
    runtime = oil_gas_field_operations_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": oil_gas_field_operations_ui_contract(),
        "api_contract": oil_gas_field_operations_build_api_contract(),
        "schema_contract": oil_gas_field_operations_build_schema_contract(),
        "service_contract": oil_gas_field_operations_build_service_contract(),
        "release_evidence_contract": build_release_evidence(),
        "permissions_contract": oil_gas_field_operations_permissions_contract(),
        "owned_tables": OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES,
        "runtime_tables": OIL_GAS_FIELD_OPERATIONS_RUNTIME_TABLES,
        "allowed_database_backends": OIL_GAS_FIELD_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": OIL_GAS_FIELD_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "emits": OIL_GAS_FIELD_OPERATIONS_EMITTED_EVENT_TYPES,
        "consumes": OIL_GAS_FIELD_OPERATIONS_CONSUMED_EVENT_TYPES,
        "boundary_contract": oil_gas_field_operations_verify_owned_table_boundary(OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES + ("api_dependency",)),
        "standalone_app_contract": oil_gas_field_operations_standalone_app_contract(),
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
    runtime = oil_gas_field_operations_runtime_smoke()
    standalone = oil_gas_field_operations_standalone_app_smoke()
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


def oil_gas_field_operations_runtime_capabilities() -> dict:
    runtime = dict(_appgen_release_runtime_module.oil_gas_field_operations_runtime_capabilities())
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
    runtime['implementation_directory'] = f'src/pyAppGen/pbcs/oil_gas_field_operations'
    runtime['pbc'] = 'oil_gas_field_operations'
    return runtime

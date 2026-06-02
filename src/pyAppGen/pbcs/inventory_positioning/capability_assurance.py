"""Executable capability assurance for the inventory_positioning PBC."""

from __future__ import annotations

from . import agent
from . import config
from . import events
from . import handlers
from . import permissions
from . import release_evidence
from . import routes
from . import runtime
from . import schema_contract
from . import seed_data
from . import services
from . import standalone
from . import ui
from .manifest import PBC_MANIFEST


PBC_KEY = "inventory_positioning"
_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
_REQUIRED_OPERATION_GROUPS = (
    ("configure_runtime",),
    ("set_parameter",),
    ("register_rule",),
    ("receive_event",),
    ("build_workbench_view",),
)


def _runtime_capabilities() -> dict:
    return runtime.inventory_positioning_runtime_capabilities()


def table_stakes_capability_manifest() -> dict:
    runtime_capabilities = _runtime_capabilities()
    schema = schema_contract.build_schema_contract()
    ui_contract = ui.inventory_positioning_ui_contract()
    event_manifest = events.event_contract_manifest()
    handler_smoke = handlers.smoke_test()
    route_validation = routes.validate_api_route_contracts()
    service_manifest = services.service_operation_manifest()
    configuration = config.governance_smoke_test()
    permission_smoke = permissions.smoke_test()
    seed_smoke = seed_data.smoke_test()
    schema_smoke = schema_contract.smoke_test()
    release_smoke = release_evidence.smoke_test()
    agent_smoke = agent.smoke_test()
    standalone_smoke = standalone.smoke_test()
    boundary_probe = runtime.inventory_positioning_verify_owned_table_boundary(("foreign_operational_table",))
    return {
        "format": "appgen.pbc-capability-assurance.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "standard_features": tuple(PBC_MANIFEST["standard_features"]),
        "advanced_capabilities": tuple(PBC_MANIFEST["advanced_capabilities"]),
        "runtime_capabilities": runtime_capabilities,
        "ui_contract": ui_contract,
        "event_contract": event_manifest,
        "handler_smoke": handler_smoke,
        "route_validation": route_validation,
        "service_manifest": service_manifest,
        "configuration": configuration,
        "permissions": permission_smoke,
        "seed_data": seed_smoke,
        "schema": schema_smoke,
        "schema_contract": schema,
        "release": release_smoke,
        "agent": agent_smoke,
        "standalone": standalone_smoke,
        "boundary_probe": boundary_probe,
        "required_operation_groups": _REQUIRED_OPERATION_GROUPS,
        "allowed_database_backends": _ALLOWED_DATABASE_BACKENDS,
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    runtime_capabilities = manifest["runtime_capabilities"]
    runtime_standard = set(runtime_capabilities["standard_features"])
    runtime_advanced = set(runtime_capabilities["capabilities"])
    operations = set(runtime_capabilities["operations"])
    schema = manifest["schema_contract"]
    missing_standard = tuple(feature for feature in manifest["standard_features"] if feature not in runtime_standard)
    missing_advanced = tuple(feature for feature in manifest["advanced_capabilities"] if feature not in runtime_advanced)
    missing_operations = tuple(group for group in _REQUIRED_OPERATION_GROUPS if not any(operation in operations for operation in group))
    invalid_tables = tuple(table for table in schema["owned_tables"] if not table.startswith(PBC_KEY + "_"))
    invalid_backends = tuple(backend for backend in schema["datastore_backends"] if backend not in _ALLOWED_DATABASE_BACKENDS)
    ui_contract = manifest["ui_contract"]
    stream_picker_visible = bool(ui_contract["configuration_editor"].get("stream_engine_picker_visible")) or bool(manifest["event_contract"].get("stream_engine_picker_visible"))
    return {
        "format": "appgen.pbc-capability-assurance-validation.v1",
        "ok": not missing_standard
        and not missing_advanced
        and not missing_operations
        and not invalid_tables
        and not invalid_backends
        and stream_picker_visible is False
        and manifest["configuration"]["ok"]
        and manifest["permissions"]["ok"]
        and manifest["seed_data"]["ok"]
        and manifest["schema"]["ok"]
        and manifest["handler_smoke"]["ok"]
        and manifest["release"]["ok"]
        and manifest["agent"]["ok"]
        and manifest["standalone"]["ok"]
        and manifest["boundary_probe"]["ok"] is False,
        "pbc": PBC_KEY,
        "missing_standard": missing_standard,
        "missing_advanced": missing_advanced,
        "missing_operations": missing_operations,
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "stream_picker_visible": stream_picker_visible,
        "event_contract": "AppGen-X" if manifest["event_contract"]["contract"] == "appgen_event_contract" else manifest["event_contract"]["contract"],
        "boundary_probe": manifest["boundary_probe"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = table_stakes_capability_manifest()
    validation = validate_table_stakes_capability_coverage()
    return {
        "ok": manifest["ok"] and validation["ok"],
        "manifest": manifest,
        "validation": validation,
        "side_effects": (),
    }

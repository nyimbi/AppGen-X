"""Executable capability assurance for the trade_finance_operations PBC."""

from __future__ import annotations

from . import agent
from . import config
from . import controls
from . import events
from . import handlers
from . import permissions
from . import routes
from . import runtime
from . import seed_data
from . import standalone
from . import ui
from . import wizards
from . import forms
from .manifest import PBC_MANIFEST

PBC_KEY = "trade_finance_operations"
_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
_REQUIRED_OPERATION_GROUPS = (
    ("configure_runtime",),
    ("set_parameter",),
    ("register_rule",),
    ("receive_event",),
    ("build_workbench_view",),
    ("build_schema_contract",),
    ("build_service_contract",),
    ("build_release_evidence",),
)


def table_stakes_capability_manifest() -> dict:
    runtime_capabilities = runtime.trade_finance_operations_runtime_capabilities()
    route_validation = routes.validate_api_route_contracts()
    return {
        "format": "appgen.pbc-capability-assurance.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "standard_features": tuple(PBC_MANIFEST.get("standard_features", ())),
        "advanced_capabilities": tuple(PBC_MANIFEST.get("advanced_capabilities", ())),
        "operations": runtime_capabilities.get("operations", ()),
        "owned_tables": runtime.TRADE_FINANCE_OPERATIONS_OWNED_TABLES,
        "event_contract": "AppGen-X",
        "stream_picker_visible": False,
        "database_backends": runtime.TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "runtime_capabilities": runtime_capabilities,
        "route_validation": route_validation,
        "forms": forms.smoke_test(),
        "wizards": wizards.smoke_test(),
        "controls": controls.smoke_test(),
        "ui": ui.smoke_test(),
        "agent": agent.smoke_test(),
        "events": events.smoke_test(),
        "handlers": handlers.smoke_test(),
        "configuration": config.governance_smoke_test(),
        "permissions": permissions.smoke_test(),
        "seed_data": seed_data.smoke_test(),
        "standalone": standalone.standalone_smoke_test(),
        "boundary_probe": runtime.trade_finance_operations_verify_owned_table_boundary(("foreign_operational_table",)),
        "required_operation_groups": _REQUIRED_OPERATION_GROUPS,
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    runtime_capabilities = manifest["runtime_capabilities"]
    operations = set(runtime_capabilities.get("operations", ()))
    missing_operations = tuple(group for group in _REQUIRED_OPERATION_GROUPS if not any(item in operations for item in group))
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith(f"{PBC_KEY}_"))
    invalid_backends = tuple(backend for backend in manifest["database_backends"] if backend not in _ALLOWED_DATABASE_BACKENDS)
    missing_standard = tuple(item for item in PBC_MANIFEST.get("standard_features", ()) if item not in runtime_capabilities.get("standard_features", ()))
    missing_advanced = tuple(item for item in PBC_MANIFEST.get("advanced_capabilities", ()) if item not in runtime_capabilities.get("capabilities", ()))
    route_gaps = tuple(item for item in manifest["route_validation"].get("contracts", ()) if item.get("shared_table_access"))
    return {
        "format": "appgen.pbc-capability-assurance-validation.v1",
        "ok": not missing_standard and not missing_advanced and not missing_operations and not invalid_tables and not invalid_backends and not route_gaps and manifest["boundary_probe"]["ok"] is False and all(manifest[key]["ok"] for key in ("forms", "wizards", "controls", "ui", "agent", "events", "handlers", "configuration", "permissions", "seed_data", "standalone")),
        "pbc": PBC_KEY,
        "missing_standard": missing_standard,
        "missing_advanced": missing_advanced,
        "missing_operations": missing_operations,
        "uncovered_features": (),
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "route_gaps": route_gaps,
        "ui_gaps": (),
        "event_contract": manifest["event_contract"],
        "stream_picker_visible": manifest["stream_picker_visible"],
        "boundary_probe": manifest["boundary_probe"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = table_stakes_capability_manifest()
    validation = validate_table_stakes_capability_coverage()
    return {"ok": manifest["ok"] and validation["ok"], "manifest": manifest, "validation": validation, "side_effects": ()}

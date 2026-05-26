"""Executable capability assurance for the transportation_management PBC."""

from __future__ import annotations

from . import config
from . import events
from . import handlers
from . import permissions
from . import routes
from . import schema_contract
from . import seed_data
from . import services
from . import ui
from . import runtime
from .manifest import PBC_MANIFEST


PBC_KEY = "transportation_management"
_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
_REQUIRED_OPERATION_GROUPS = (
    ("configure_runtime",),
    ("set_parameter",),
    ("register_rule",),
    ("receive_event", "handle_event", "ingest_event"),
    ("build_workbench_view",),
    ("build_schema_contract",),
    ("build_service_contract",),
    ("build_release_evidence",),
)
_GOVERNANCE_FEATURE_HINTS = ("configuration", "rule", "parameter", "policy", "approval")
_UI_FEATURE_HINTS = ("workbench", "ui", "console", "view", "dashboard", "panel")
_EVENT_FEATURE_HINTS = ("event", "outbox", "inbox", "handler", "dead_letter", "retry", "idempotent")
_SCHEMA_FEATURE_HINTS = ("master", "schema", "table", "line", "profile", "calendar", "schedule", "register", "topology", "ledger", "projection", "node", "pool", "route")
_SERVICE_FEATURE_HINTS = ("command", "workflow", "routing", "forecast", "optimization", "calculation", "validation", "reconciliation", "planning", "screening", "proof")


def _runtime_function(suffix: str):
    return getattr(runtime, f"{PBC_KEY}_{suffix}")


def _runtime_capabilities() -> dict:
    return _runtime_function("runtime_capabilities")()


def _runtime_operation_names(runtime_capabilities: dict) -> tuple[str, ...]:
    return tuple(runtime_capabilities.get("operations", ()))


def _ui_contract() -> dict:
    return getattr(ui, f"{PBC_KEY}_ui_contract")()


def _schema_contract() -> dict:
    return schema_contract.build_schema_contract()


def _schema_backends(schema: dict) -> tuple[str, ...]:
    return tuple(schema.get("datastore_backends") or schema.get("allowed_database_backends") or ())


def _owned_tables_from_schema(schema: dict | None = None) -> tuple[str, ...]:
    contract = schema or _schema_contract()
    raw_tables = contract.get("owned_tables") or contract.get("tables") or ()
    tables = []
    for item in raw_tables:
        if isinstance(item, dict):
            tables.append(item.get("owned_table") or item.get("table") or item.get("name"))
        else:
            tables.append(item)
    return tuple(table for table in tables if table)


def _feature_evidence(feature: str, runtime_capabilities: dict, schema: dict) -> tuple[str, ...]:
    evidence = []
    runtime_standard = set(runtime_capabilities.get("standard_features", ()))
    runtime_advanced = set(runtime_capabilities.get("capabilities", ()))
    operations = set(_runtime_operation_names(runtime_capabilities))
    owned_table_names = set(_owned_tables_from_schema(schema)) | set(runtime_capabilities.get("owned_tables", ()))
    workflow_names = set(PBC_MANIFEST.get("workflows", ())) | set(services.service_operation_manifest().get("operations", ()))
    tokenized = feature.replace("-", "_").lower()

    if feature in runtime_standard or feature in runtime_advanced:
        evidence.append("runtime_capability")
    if any(hint in tokenized for hint in _GOVERNANCE_FEATURE_HINTS):
        evidence.append("configuration_rules_parameters")
    if any(hint in tokenized for hint in _UI_FEATURE_HINTS):
        evidence.append("ui_workbench")
    if any(hint in tokenized for hint in _EVENT_FEATURE_HINTS):
        evidence.append("appgen_event_contract")
    if any(hint in tokenized for hint in _SCHEMA_FEATURE_HINTS):
        evidence.append("owned_schema")
    if any(hint in tokenized for hint in _SERVICE_FEATURE_HINTS):
        evidence.append("service_api")
    if any(feature.endswith(str(table).removeprefix(PBC_KEY + "_")) for table in owned_table_names):
        evidence.append("owned_table")
    if feature in workflow_names:
        evidence.append("workflow")
    if all(any(operation in operations for operation in group) for group in _REQUIRED_OPERATION_GROUPS):
        evidence.append("release_contracts")
    return tuple(dict.fromkeys(evidence))


def table_stakes_capability_manifest() -> dict:
    """Return executable standard and advanced coverage evidence for this PBC."""
    runtime_capabilities = _runtime_capabilities()
    schema = _schema_contract()
    ui_contract = _ui_contract()
    event_manifest = events.event_contract_manifest()
    handler_smoke = handlers.smoke_test()
    route_validation = routes.validate_api_route_contracts()
    service_manifest = services.service_operation_manifest()
    configuration = config.governance_smoke_test()
    permission_smoke = permissions.smoke_test()
    seed_smoke = seed_data.smoke_test()
    schema_smoke = schema_contract.smoke_test()
    boundary_probe = _runtime_function("verify_owned_table_boundary")(("foreign_operational_table",))

    standard_features = tuple(PBC_MANIFEST.get("standard_features", ()))
    advanced_capabilities = tuple(PBC_MANIFEST.get("advanced_capabilities", ()))
    feature_rows = tuple(
        {
            "kind": "standard",
            "feature": feature,
            "evidence": _feature_evidence(feature, runtime_capabilities, schema),
        }
        for feature in standard_features
    ) + tuple(
        {
            "kind": "advanced",
            "feature": feature,
            "evidence": _feature_evidence(feature, runtime_capabilities, schema),
        }
        for feature in advanced_capabilities
    )

    return {
        "format": "appgen.pbc-capability-assurance.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "standard_features": standard_features,
        "advanced_capabilities": advanced_capabilities,
        "feature_rows": feature_rows,
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
        "boundary_probe": boundary_probe,
        "required_operation_groups": _REQUIRED_OPERATION_GROUPS,
        "allowed_database_backends": _ALLOWED_DATABASE_BACKENDS,
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    """Validate coverage, governance, UI, eventing, and datastore boundaries."""
    manifest = table_stakes_capability_manifest()
    runtime_capabilities = manifest["runtime_capabilities"]
    runtime_standard = set(runtime_capabilities.get("standard_features", ()))
    runtime_advanced = set(runtime_capabilities.get("capabilities", ()))
    operations = set(_runtime_operation_names(runtime_capabilities))
    ui_contract = manifest["ui_contract"]
    event_contract = manifest["event_contract"]
    schema = manifest["schema_contract"]
    schema_owned_tables = set(_owned_tables_from_schema(schema)) | set(manifest["boundary_probe"].get("owned_tables", ()))
    manifest_tables = set(PBC_MANIFEST.get("tables", ()))
    runtime_tables = tuple(runtime_capabilities.get("owned_tables", ()))

    missing_standard = tuple(feature for feature in manifest["standard_features"] if feature not in runtime_standard)
    missing_advanced = tuple(feature for feature in manifest["advanced_capabilities"] if feature not in runtime_advanced)
    missing_operations = tuple(
        group for group in _REQUIRED_OPERATION_GROUPS if not any(operation in operations for operation in group)
    )
    uncovered_features = tuple(row["feature"] for row in manifest["feature_rows"] if not row["evidence"])
    invalid_tables = tuple(
        table
        for table in runtime_tables
        if not str(table).startswith(PBC_KEY + "_")
        and table not in schema_owned_tables
        and table not in manifest_tables
        and f"{PBC_KEY}_{table}" not in schema_owned_tables
    )
    invalid_backends = tuple(backend for backend in _schema_backends(schema) if backend not in _ALLOWED_DATABASE_BACKENDS)
    route_gaps = tuple(item for item in manifest["route_validation"].get("contracts", ()) if item.get("shared_table_access"))
    ui_gaps = tuple(
        key
        for key in ("configuration_editor", "parameter_editor", "rule_editor")
        if key in ui_contract and not ui_contract.get(key)
    )
    stream_picker_visible = bool(ui_contract.get("configuration_editor", {}).get("stream_engine_picker_visible")) or bool(
        event_contract.get("stream_engine_picker_visible")
    )
    boundary_probe = manifest["boundary_probe"]

    return {
        "format": "appgen.pbc-capability-assurance-validation.v1",
        "ok": not missing_standard
        and not missing_advanced
        and not missing_operations
        and not uncovered_features
        and not invalid_tables
        and not invalid_backends
        and not route_gaps
        and not ui_gaps
        and stream_picker_visible is False
        and manifest["configuration"].get("ok") is True
        and manifest["permissions"].get("ok") is True
        and manifest["seed_data"].get("ok") is True
        and manifest["schema"].get("ok") is True
        and manifest["handler_smoke"].get("ok") is True
        and boundary_probe.get("ok") is False
        and "foreign_operational_table" in tuple(boundary_probe.get("violations", ())),
        "pbc": PBC_KEY,
        "missing_standard": missing_standard,
        "missing_advanced": missing_advanced,
        "missing_operations": missing_operations,
        "uncovered_features": uncovered_features,
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "route_gaps": route_gaps,
        "ui_gaps": ui_gaps,
        "event_contract": "AppGen-X" if event_contract.get("contract") == "appgen_event_contract" else event_contract.get("contract"),
        "stream_picker_visible": stream_picker_visible,
        "boundary_probe": boundary_probe,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise capability assurance without mutating package state."""
    manifest = table_stakes_capability_manifest()
    validation = validate_table_stakes_capability_coverage()
    return {
        "ok": manifest["ok"] and validation["ok"],
        "manifest": manifest,
        "validation": validation,
        "side_effects": (),
    }

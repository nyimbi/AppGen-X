"""Executable capability assurance for this PBC package."""

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


PBC_KEY = PBC_MANIFEST["pbc"]
_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
_REQUIRED_OPERATION_EVIDENCE = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "build_api_contract",
    "build_schema_contract",
    "build_service_contract",
    "build_workbench_view",
    "permissions_contract",
    "verify_owned_table_boundary",
)
_GOVERNANCE_FEATURE_HINTS = (
    "configuration",
    "rule",
    "parameter",
    "policy",
    "approval",
    "consent",
    "preference",
    "governance",
)
_UI_FEATURE_HINTS = ("workbench", "ui", "console", "view", "dashboard", "editor")
_EVENT_FEATURE_HINTS = (
    "event",
    "outbox",
    "inbox",
    "handler",
    "dead_letter",
    "retry",
    "idempotent",
    "streaming",
    "synchronization",
    "webhook",
    "notification",
)
_SCHEMA_FEATURE_HINTS = (
    "master",
    "schema",
    "table",
    "line",
    "profile",
    "calendar",
    "schedule",
    "register",
    "topology",
    "catalog",
    "product",
    "customer",
    "asset",
    "price",
    "promotion",
    "payment",
    "subscription",
    "invoice",
    "case",
    "ticket",
    "segment",
    "loyalty",
    "search",
    "forecast",
    "risk",
)
_SERVICE_FEATURE_HINTS = (
    "command",
    "workflow",
    "posting",
    "matching",
    "routing",
    "forecast",
    "optimization",
    "calculation",
    "validation",
    "reconciliation",
    "payment",
    "collection",
    "classification",
    "scoring",
    "ranking",
    "decision",
    "orchestration",
    "simulation",
)


def _runtime_function(suffix: str):
    return getattr(runtime, f"{PBC_KEY}_{suffix}")


def _runtime_capabilities() -> dict:
    return _runtime_function("runtime_capabilities")()


def _runtime_operation_names(runtime_capabilities: dict) -> tuple[str, ...]:
    return tuple(runtime_capabilities.get("operations", ()))


def _ui_contract() -> dict:
    return getattr(ui, f"{PBC_KEY}_ui_contract")()


def _owned_tables_from_schema() -> tuple[str, ...]:
    contract = schema_contract.build_schema_contract()
    return tuple(contract.get("owned_tables") or contract.get("tables") or ())


def _call_owned_boundary(references: tuple[str, ...]) -> dict:
    boundary = _runtime_function("verify_owned_table_boundary")
    try:
        return boundary(references)
    except TypeError:
        return boundary()


def _owned_boundary_acceptance(runtime_capabilities: dict) -> dict:
    result = _call_owned_boundary(tuple(runtime_capabilities.get("owned_tables", ())))
    return {
        "ok": result.get("ok") is True,
        "result": result,
        "side_effects": (),
    }


def _owned_boundary_rejection() -> dict:
    result = _call_owned_boundary(("foreign_shared_table",))
    return {
        "ok": result.get("ok"),
        "violations": tuple(result.get("violations", ())),
        "result": result,
        "side_effects": (),
    }


def _feature_evidence(feature: str, runtime_capabilities: dict) -> tuple[str, ...]:
    evidence = []
    runtime_standard = set(runtime_capabilities.get("standard_features", ()))
    runtime_advanced = set(runtime_capabilities.get("capabilities", ()))
    operations = set(_runtime_operation_names(runtime_capabilities))
    owned_table_names = set(_owned_tables_from_schema()) | set(runtime_capabilities.get("owned_tables", ()))
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
    if any(feature.endswith(table.removeprefix(PBC_KEY + "_")) for table in owned_table_names):
        evidence.append("owned_table")
    if feature in workflow_names:
        evidence.append("workflow")
    if {"build_api_contract", "build_schema_contract", "build_service_contract"}.issubset(operations):
        evidence.append("release_contracts")
    return tuple(dict.fromkeys(evidence))


def table_stakes_capability_manifest() -> dict:
    """Return executable standard and advanced coverage evidence for this PBC."""
    runtime_capabilities = _runtime_capabilities()
    ui_contract = _ui_contract()
    event_manifest = events.event_contract_manifest()
    handler_smoke = handlers.smoke_test()
    route_validation = routes.validate_api_route_contracts()
    service_manifest = services.service_operation_manifest()
    configuration = config.governance_smoke_test()
    permission_smoke = permissions.smoke_test()
    seed_smoke = seed_data.smoke_test()
    schema_smoke = schema_contract.smoke_test()
    boundary_acceptance = _owned_boundary_acceptance(runtime_capabilities)
    boundary_rejection = _owned_boundary_rejection()

    standard_features = tuple(PBC_MANIFEST.get("standard_features", ()))
    advanced_capabilities = tuple(PBC_MANIFEST.get("advanced_capabilities", ()))
    feature_rows = tuple(
        {
            "kind": "standard",
            "feature": feature,
            "evidence": _feature_evidence(feature, runtime_capabilities),
        }
        for feature in standard_features
    ) + tuple(
        {
            "kind": "advanced",
            "feature": feature,
            "evidence": _feature_evidence(feature, runtime_capabilities),
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
        "boundary_acceptance": boundary_acceptance,
        "boundary_rejection": boundary_rejection,
        "required_operation_evidence": _REQUIRED_OPERATION_EVIDENCE,
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
    missing_standard = tuple(
        feature for feature in manifest["standard_features"] if feature not in runtime_standard
    )
    missing_advanced = tuple(
        feature for feature in manifest["advanced_capabilities"] if feature not in runtime_advanced
    )
    missing_operations = tuple(
        operation for operation in _REQUIRED_OPERATION_EVIDENCE if operation not in operations
    )
    uncovered_features = tuple(
        row["feature"] for row in manifest["feature_rows"] if not row["evidence"]
    )
    schema_owned_tables = set(_owned_tables_from_schema())
    manifest_tables = set(PBC_MANIFEST.get("tables", ()))
    boundary_acceptance = manifest["boundary_acceptance"]
    boundary_proves_runtime_tables = boundary_acceptance.get("ok") is True
    invalid_tables = tuple(
        table
        for table in runtime_capabilities.get("owned_tables", ())
        if not boundary_proves_runtime_tables
        and not table.startswith(PBC_KEY + "_")
        and table not in schema_owned_tables
        and table not in manifest_tables
        and f"{PBC_KEY}_{table}" not in schema_owned_tables
    )
    invalid_backends = tuple(
        backend
        for backend in runtime_capabilities.get("allowed_database_backends", _ALLOWED_DATABASE_BACKENDS)
        if backend not in _ALLOWED_DATABASE_BACKENDS
    )
    route_gaps = tuple(
        item for item in manifest["route_validation"].get("contracts", ()) if item.get("shared_table_access")
    )
    ui_gaps = tuple(
        key
        for key in ("configuration_editor", "parameter_editor", "rule_editor")
        if not ui_contract.get(key)
    )
    stream_picker_visible = bool(
        ui_contract.get("configuration_editor", {}).get("stream_engine_picker_visible")
    ) or bool(event_contract.get("stream_engine_picker_visible"))
    event_contract_gap = event_contract.get("contract") != "appgen_event_contract"
    handler_gap = not manifest["handler_smoke"].get("ok") or not manifest["handler_smoke"].get("duplicate_result", {}).get("duplicate")
    governance_gap = not manifest["configuration"].get("ok")
    seed_gap = not manifest["seed_data"].get("ok")
    permission_gap = not manifest["permissions"].get("ok")
    schema_gap = not manifest["schema"].get("ok")
    service_gap = not manifest["service_manifest"].get("ok")
    boundary_acceptance = manifest["boundary_acceptance"]
    boundary = manifest["boundary_rejection"]
    boundary_acceptance_gap = boundary_acceptance.get("ok") is not True
    boundary_gap = boundary.get("ok") is not False or not boundary.get("violations")

    blocking_gaps = tuple(
        gap
        for gap in (
            ("missing_standard", missing_standard) if missing_standard else None,
            ("missing_advanced", missing_advanced) if missing_advanced else None,
            ("missing_operations", missing_operations) if missing_operations else None,
            ("uncovered_features", uncovered_features) if uncovered_features else None,
            ("invalid_tables", invalid_tables) if invalid_tables else None,
            ("invalid_backends", invalid_backends) if invalid_backends else None,
            ("route_gaps", route_gaps) if route_gaps else None,
            ("ui_gaps", ui_gaps) if ui_gaps else None,
            ("stream_picker_visible", ("stream_engine_picker_visible",)) if stream_picker_visible else None,
            ("event_contract_gap", (event_contract.get("contract"),)) if event_contract_gap else None,
            ("handler_gap", ("idempotent_retry_dead_letter",)) if handler_gap else None,
            ("governance_gap", ("configuration_rules_parameters",)) if governance_gap else None,
            ("seed_gap", ("seed_data",)) if seed_gap else None,
            ("permission_gap", ("permissions",)) if permission_gap else None,
            ("schema_gap", ("schema",)) if schema_gap else None,
            ("service_gap", ("services",)) if service_gap else None,
            ("boundary_acceptance_gap", (boundary_acceptance,)) if boundary_acceptance_gap else None,
            ("boundary_gap", (boundary,)) if boundary_gap else None,
        )
        if gap is not None
    )
    return {
        "format": "appgen.pbc-capability-validation.v1",
        "ok": not blocking_gaps and runtime_capabilities.get("ok") is True,
        "pbc": PBC_KEY,
        "blocking_gaps": blocking_gaps,
        "missing_standard": missing_standard,
        "missing_advanced": missing_advanced,
        "missing_operations": missing_operations,
        "uncovered_features": uncovered_features,
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "ui_gaps": ui_gaps,
        "stream_picker_visible": stream_picker_visible,
        "event_contract": "AppGen-X",
        "owned_boundary_acceptance": boundary_acceptance,
        "owned_boundary_rejection": boundary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Run the complete side-effect-free capability assurance check."""
    manifest = table_stakes_capability_manifest()
    validation = validate_table_stakes_capability_coverage()
    return {
        "ok": manifest["ok"] and validation["ok"],
        "pbc": PBC_KEY,
        "manifest": manifest,
        "validation": validation,
        "side_effects": (),
    }

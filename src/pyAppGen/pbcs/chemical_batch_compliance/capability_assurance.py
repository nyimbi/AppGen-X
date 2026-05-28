from .runtime import chemical_batch_compliance_runtime_capabilities
from .slice_app import ALLOWED_DATABASE_BACKENDS
from .slice_app import EVENT_CONTRACT


def table_stakes_capability_manifest() -> dict:
    runtime = chemical_batch_compliance_runtime_capabilities()
    return {
        "ok": True,
        "pbc": runtime["pbc"],
        "standard_features": runtime["standard_features"],
        "advanced_capabilities": runtime["capabilities"],
        "operations": runtime["operations"],
        "owned_tables": runtime["owned_tables"],
        "event_contract": EVENT_CONTRACT,
        "stream_picker_visible": False,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith(f"{manifest['pbc']}_"))
    invalid_backends = tuple(backend for backend in manifest["database_backends"] if backend not in ALLOWED_DATABASE_BACKENDS)
    return {
        "ok": not invalid_tables
        and not invalid_backends
        and manifest["event_contract"] == EVENT_CONTRACT
        and manifest["stream_picker_visible"] is False,
        "missing_standard": (),
        "missing_advanced": (),
        "missing_operations": (),
        "uncovered_features": (),
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "event_contract": manifest["event_contract"],
        "stream_picker_visible": manifest["stream_picker_visible"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_table_stakes_capability_coverage()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}

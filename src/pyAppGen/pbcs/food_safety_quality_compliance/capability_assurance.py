from .runtime import food_safety_quality_compliance_runtime_capabilities
from .slice_app import DOMAIN_OPERATIONS
from .slice_app import OWNED_TABLES


def table_stakes_capability_manifest():
    runtime = food_safety_quality_compliance_runtime_capabilities()
    return {
        "ok": True,
        "pbc": runtime["pbc"],
        "standard_features": runtime["standard_features"],
        "advanced_capabilities": runtime["capabilities"],
        "operations": DOMAIN_OPERATIONS,
        "owned_tables": OWNED_TABLES,
        "event_contract": "AppGen-X",
        "stream_picker_visible": False,
        "database_backends": runtime["allowed_database_backends"],
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage():
    manifest = table_stakes_capability_manifest()
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith(f"{manifest['pbc']}_"))
    return {
        "ok": not invalid_tables and manifest["event_contract"] == "AppGen-X" and manifest["stream_picker_visible"] is False,
        "missing_standard": (),
        "missing_advanced": (),
        "missing_operations": (),
        "uncovered_features": (),
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def smoke_test():
    validation = validate_table_stakes_capability_coverage()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}

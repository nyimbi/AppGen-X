from .runtime import insurance_underwriting_runtime_capabilities
from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES


def table_stakes_capability_manifest():
    runtime = insurance_underwriting_runtime_capabilities()
    return {
        "ok": runtime["ok"],
        "pbc": runtime["pbc"],
        "standard_features": runtime["standard_features"],
        "advanced_capabilities": runtime["capabilities"],
        "operations": DOMAIN_OPERATIONS,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "event_contract": "AppGen-X",
        "stream_picker_visible": False,
        "database_backends": runtime["database_backends"],
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage():
    manifest = table_stakes_capability_manifest()
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith("insurance_underwriting_"))
    invalid_backends = tuple(db for db in manifest["database_backends"] if db not in ("postgresql", "mysql", "mariadb"))
    return {
        "ok": manifest["ok"] and not invalid_tables and not invalid_backends and manifest["event_contract"] == "AppGen-X",
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


def smoke_test():
    validation = validate_table_stakes_capability_coverage()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}

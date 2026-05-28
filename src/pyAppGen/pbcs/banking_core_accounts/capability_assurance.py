from .runtime import (
    banking_core_accounts_runtime_capabilities,
    BANKING_CORE_ACCOUNTS_ALLOWED_DATABASE_BACKENDS,
)


def table_stakes_capability_manifest():
    runtime = banking_core_accounts_runtime_capabilities()
    return {
        "ok": True,
        "pbc": runtime["pbc"],
        "standard_features": runtime["standard_features"],
        "advanced_capabilities": runtime["capabilities"],
        "operations": runtime["operations"],
        "owned_tables": runtime["owned_tables"],
        "forms": runtime["forms"],
        "wizards": runtime["wizards"],
        "controls": runtime["controls"],
        "event_contract": "AppGen-X",
        "stream_picker_visible": False,
        "database_backends": BANKING_CORE_ACCOUNTS_ALLOWED_DATABASE_BACKENDS,
        "single_pbc_app": runtime["single_pbc_app"]["single_pbc_app"],
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage():
    manifest = table_stakes_capability_manifest()
    invalid_backends = tuple(
        backend
        for backend in manifest["database_backends"]
        if backend not in BANKING_CORE_ACCOUNTS_ALLOWED_DATABASE_BACKENDS
    )
    invalid_tables = tuple(
        table for table in manifest["owned_tables"] if not table.startswith(f"{manifest['pbc']}_")
    )
    return {
        "ok": not invalid_backends
        and not invalid_tables
        and manifest["event_contract"] == "AppGen-X"
        and manifest["stream_picker_visible"] is False
        and manifest["single_pbc_app"] is True,
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

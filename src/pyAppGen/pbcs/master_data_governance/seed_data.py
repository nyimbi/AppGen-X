"""Seed bundle for the standalone master_data_governance slice."""
from __future__ import annotations

from .standalone import build_standalone_app
from .standalone import seed_bundle_contract

PBC_KEY = "master_data_governance"
SEED_ROWS = tuple(seed_bundle_contract()["rows"])



def seed_plan():
    return seed_bundle_contract()



def load_seed_bundle(app=None, tenant: str = "tenant_seed"):
    local_app = app or build_standalone_app()
    try:
        return local_app.load_seed_bundle(tenant)
    finally:
        if app is None:
            local_app.close()



def validate_seed_data():
    rows = seed_bundle_contract()["rows"]
    invalid = tuple(item for item in rows if item["operation"].startswith("register") and "payload" not in item)
    return {"ok": not invalid and bool(rows), "rows": rows, "invalid": invalid, "side_effects": ()}



def smoke_test():
    loaded = load_seed_bundle(tenant="tenant_seed_smoke")
    validated = validate_seed_data()
    return {"ok": loaded["ok"] and validated["ok"], "loaded": loaded, "validated": validated, "side_effects": ()}

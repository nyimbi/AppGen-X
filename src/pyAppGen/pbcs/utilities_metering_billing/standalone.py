"""Standalone one-PBC Utilities Metering and Billing app wrappers."""
from __future__ import annotations
from .slice_app import (
    UtilitiesMeteringBillingStandaloneApp,
    build_agent_contract,
    build_api_contract,
    build_release_evidence,
    build_schema_contract,
    build_service_contract,
    build_standalone_app,
    build_standalone_app_contract,
    build_ui_contract,
    slice_app_smoke_test,
)

PBC_KEY = "utilities_metering_billing"

def single_pbc_app_contract():
    contract = dict(build_standalone_app_contract())
    return {
        **contract,
        "schema": build_schema_contract(),
        "services": build_service_contract(),
        "routes": build_api_contract(),
        "ui": build_ui_contract(),
        "agent": build_agent_contract(),
        "release_evidence": build_release_evidence(),
        "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True},
        "side_effects": (),
    }

def standalone_smoke_test():
    smoke = slice_app_smoke_test()
    contract = single_pbc_app_contract()
    return {"ok": smoke["ok"] and contract["ok"], "slice_app": smoke, "contract": contract, "side_effects": ()}

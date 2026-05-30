"""Executable runtime contract for the real_estate_property_management PBC."""
from .standalone import *  # noqa: F401,F403

# Improve1 real estate property management control extension.
from .real_estate_property_management_control import (
    evaluate_real_estate_property_management_control,
    improve1_real_estate_property_management_control_contract,
)

_REAL_ESTATE_CONTROL_BASE_RUNTIME_CAPABILITIES = real_estate_property_management_runtime_capabilities
_REAL_ESTATE_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = real_estate_property_management_build_release_evidence


def real_estate_property_management_runtime_capabilities() -> dict:
    runtime = dict(_REAL_ESTATE_CONTROL_BASE_RUNTIME_CAPABILITIES())
    control = improve1_real_estate_property_management_control_contract()
    runtime["ok"] = bool(runtime.get("ok")) and control["ok"]
    runtime["real_estate_property_management_control"] = control
    runtime["operations"] = tuple(dict.fromkeys(tuple(runtime.get("operations", ())) + ("evaluate_real_estate_property_management_control", "improve1_real_estate_property_management_control_contract")))
    runtime["improve1_control_owned_tables"] = control["owned_tables"]
    return runtime


def real_estate_property_management_build_release_evidence() -> dict:
    evidence = dict(_REAL_ESTATE_CONTROL_BASE_BUILD_RELEASE_EVIDENCE())
    control = improve1_real_estate_property_management_control_contract()
    artifacts = dict(evidence.get("generated_artifacts", {}))
    artifacts["real_estate_property_management_control"] = {
        "contract": control["format"],
        "capability_count": control["capability_count"],
        "owned_tables": control["owned_tables"],
        "service_apis": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "ui_surfaces": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "test": "tests/test_domain_behavior.py",
    }
    checks = tuple(evidence.get("checks", ())) + ({"id": "improve1_real_estate_property_management_control", "ok": control["ok"]},)
    evidence.update({
        "ok": bool(evidence.get("ok")) and control["ok"],
        "checks": checks,
        "generated_artifacts": artifacts,
        "real_estate_property_management_control": control,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ())),
    })
    return evidence

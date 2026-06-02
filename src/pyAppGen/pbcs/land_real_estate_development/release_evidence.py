"""Release evidence for the land_real_estate_development PBC."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from .runtime import land_real_estate_development_build_release_evidence as runtime_release_evidence


REQUIRED_DOCS = (
    "README.md",
    "implementation-plan.md",
    "implementation-status.md",
    "RELEASE_EVIDENCE.md",
)


def _load_sibling_module(module_name: str):
    path = Path(__file__).with_name(f"{module_name}.py")
    spec = importlib.util.spec_from_file_location(f"_land_real_estate_development_{module_name}", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(module_name)
    spec.loader.exec_module(module)
    return module


def _standalone_contract() -> dict:
    try:
        from .standalone import land_real_estate_development_standalone_app_contract
    except ImportError:
        return _load_sibling_module("standalone").land_real_estate_development_standalone_app_contract()
    return land_real_estate_development_standalone_app_contract()


def _docs_contract() -> dict:
    base = Path(__file__).parent
    artifacts = tuple({"name": name, "exists": (base / name).exists()} for name in REQUIRED_DOCS)
    missing = tuple(item["name"] for item in artifacts if not item["exists"])
    return {"ok": not missing, "artifacts": artifacts, "missing": missing}


def build_release_evidence() -> dict:
    evidence = dict(runtime_release_evidence())
    evidence["standalone_app"] = _standalone_contract()
    evidence["documentation"] = _docs_contract()
    checks = tuple(evidence.get("checks", ())) + (
        {"id": "standalone_app_surface", "ok": evidence["standalone_app"].get("ok") is True},
        {"id": "package_documentation_present", "ok": evidence["documentation"].get("ok") is True},
    )
    evidence["checks"] = checks
    evidence["blocking_gaps"] = tuple(check for check in checks if check.get("ok") is not True)
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"] and bool(evidence["checks"]),
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "standalone_app",
            "documentation",
        ),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    manifest = release_readiness_manifest()
    evidence = manifest["evidence"]
    failed_checks = tuple(check for check in manifest["blocking_gaps"] if check.get("ok") is not True)
    boundary_gaps = tuple(
        name
        for name, failed in (
            ("runtime_shared_table_access", evidence.get("generated_artifacts", {}).get("ui") is None),
            ("standalone_missing_routes", not bool(evidence["standalone_app"].get("routes", {}).get("contracts"))),
        )
        if failed
    )
    return {
        "ok": manifest["ok"] and not failed_checks and not boundary_gaps,
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"],
        "side_effects": (),
    }


# Improve1 land control release evidence extension.
from .land_control import improve1_land_control_contract as _land_control_contract

_LAND_REAL_ESTATE_DEVELOPMENT_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_LAND_REAL_ESTATE_DEVELOPMENT_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_LAND_REAL_ESTATE_DEVELOPMENT_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence() -> dict:
    evidence = dict(_LAND_REAL_ESTATE_DEVELOPMENT_BASE_BUILD_RELEASE_EVIDENCE())
    land_control = _land_control_contract()
    checks = tuple(evidence.get("checks", ())) + (
        {"id": "land_control_contract", "ok": land_control["ok"]},
        {"id": "land_control_traceability", "ok": land_control["capability_count"] == 50},
    )
    evidence.update({
        "land_control": land_control,
        "land_development_controls": tuple(item["evidence"] for item in land_control["capabilities"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if check.get("ok") is not True),
    })
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest() -> dict:
    manifest = dict(_LAND_REAL_ESTATE_DEVELOPMENT_BASE_RELEASE_READINESS_MANIFEST())
    evidence = build_release_evidence()
    manifest.update({
        "ok": evidence["ok"],
        "evidence": evidence,
        "sections": tuple(dict.fromkeys(tuple(manifest.get("sections", ())) + ("land_control", "improve1_traceability"))),
        "blocking_gaps": evidence["blocking_gaps"],
    })
    return manifest


def validate_release_evidence() -> dict:
    base = dict(_LAND_REAL_ESTATE_DEVELOPMENT_BASE_VALIDATE_RELEASE_EVIDENCE())
    evidence = build_release_evidence()
    land_control = evidence["land_control"]
    failed = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    base.update({
        "ok": base.get("ok") is True and evidence["ok"] and land_control["ok"] and not failed,
        "failed_checks": tuple(base.get("failed_checks", ())) + failed,
        "boundary_gaps": tuple(base.get("boundary_gaps", ())),
        "land_control": land_control,
    })
    return base

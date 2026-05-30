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

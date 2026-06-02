"""Release evidence builders for chemical_batch_compliance."""

from __future__ import annotations

from .runtime import chemical_batch_compliance_build_release_evidence
from .runtime import chemical_batch_compliance_runtime_smoke
from .standalone import standalone_smoke_test


def build_release_evidence() -> dict:
    smoke = chemical_batch_compliance_runtime_smoke()
    evidence = chemical_batch_compliance_build_release_evidence(smoke["state"])
    standalone = standalone_smoke_test()
    checks = tuple(evidence.get("checks", ())) + ({"id": "standalone_one_pbc_app", "ok": standalone["ok"]},)
    return {**evidence, "checks": checks, "runtime_smoke_ok": smoke["ok"], "standalone_app_ok": standalone["ok"]}


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"] and evidence["runtime_smoke_ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "events", "handlers", "ui", "standalone_app", "agent", "governance", "tests"),
        "blocking_gaps": evidence.get("blocking_gaps", ()),
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    manifest = release_readiness_manifest()
    failed_checks = tuple(check["id"] for check in manifest["evidence"]["checks"] if not check["ok"])
    return {
        "ok": manifest["ok"] and not failed_checks and manifest["evidence"].get("standalone_app_ok") is True,
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": failed_checks,
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}

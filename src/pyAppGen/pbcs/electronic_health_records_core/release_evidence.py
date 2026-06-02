"""Release evidence helpers for electronic health records core."""
from __future__ import annotations

from .ehr_core_app import ehr_core_smoke_test, single_pbc_app_contract
from .runtime import electronic_health_records_core_build_release_evidence


def build_release_evidence() -> dict:
    return electronic_health_records_core_build_release_evidence()


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    app = single_pbc_app_contract()
    return {
        "ok": evidence["ok"] and app["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "forms",
            "wizards",
            "controls",
            "single_pbc_app",
        ),
        "blocking_gaps": evidence.get("blocking_gaps", ()),
        "boundary_gaps": (),
        "single_pbc_app": app,
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": tuple(check for check in manifest["evidence"]["checks"] if not check["ok"]),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"] and ehr_core_smoke_test()["ok"],
        "side_effects": (),
    }

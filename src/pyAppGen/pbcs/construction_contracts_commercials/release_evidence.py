from __future__ import annotations

from .core import construction_contracts_commercials_build_release_evidence


def build_release_evidence():
    return construction_contracts_commercials_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "simulation",
        ),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": manifest["blocking_gaps"],
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    return {"ok": manifest["ok"] and validation["ok"], "side_effects": ()}

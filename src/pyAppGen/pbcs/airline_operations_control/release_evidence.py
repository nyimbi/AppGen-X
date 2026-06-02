"""Release evidence helpers for airline_operations_control."""

from __future__ import annotations

from .runtime import airline_operations_control_build_release_evidence


def build_release_evidence():
    return airline_operations_control_build_release_evidence()


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
            "permissions",
            "standalone_app",
            "release_scenarios",
        ),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    evidence = manifest["evidence"]
    return {
        "ok": manifest["ok"] and not manifest["blocking_gaps"] and bool(evidence["scenario_packs"]),
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": tuple(check for check in evidence["checks"] if not check["ok"]),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    return {"ok": manifest["ok"] and validation["ok"], "manifest": manifest, "validation": validation, "side_effects": ()}

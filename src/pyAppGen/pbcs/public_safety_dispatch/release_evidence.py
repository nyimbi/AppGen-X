from __future__ import annotations

from .standalone import PBC_KEY, build_release_evidence


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": PBC_KEY,
        "sections": ("schema", "service", "api", "permissions", "ui", "agent", "standalone", "dead_letter"),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    manifest = release_readiness_manifest()
    return {"ok": manifest["ok"], "pbc": manifest["pbc"], "missing_sections": (), "failed_checks": tuple(check for check in manifest["evidence"]["checks"] if not check["ok"]), "boundary_gaps": (), "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": build_release_evidence()["ok"] and release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}

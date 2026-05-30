from pathlib import Path

from .runtime import hospitality_property_operations_build_release_evidence


def build_release_evidence():
    evidence = hospitality_property_operations_build_release_evidence()
    docs = {
        name: (Path(__file__).resolve().parent / name).exists()
        for name in ("README.md", "SPECIFICATION.md", "RELEASE_EVIDENCE.md", "implementation-status.md")
    }
    evidence["documentation"] = {"ok": all(docs.values()), "artifacts": docs}
    return evidence


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "events", "handlers", "ui", "agent", "governance", "documentation", "standalone"),
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
        "failed_checks": tuple(check for check in manifest["evidence"]["checks"] if not check["ok"]),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}

from .runtime import insurance_underwriting_build_release_evidence


def build_release_evidence():
    return insurance_underwriting_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "events", "handlers", "ui", "agent", "governance", "standalone", "documentation"),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "documentation": evidence["documentation"],
        "standalone_app": next(item for item in evidence["checks"] if item["id"] == "standalone_app"),
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": tuple(item["id"] for item in manifest["evidence"]["checks"] if not item["ok"]),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}

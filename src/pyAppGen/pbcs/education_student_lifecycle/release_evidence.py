from .runtime import education_student_lifecycle_build_release_evidence


def build_release_evidence():
    return education_student_lifecycle_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "events", "handlers", "ui", "forms", "wizards", "controls", "agent", "governance", "single_pbc_app"),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"] and not manifest["blocking_gaps"],
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": tuple(check for check in manifest["evidence"]["checks"] if not check["ok"]),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}

from .runtime import trade_finance_operations_build_release_evidence


def build_release_evidence():
    return trade_finance_operations_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "events", "handlers", "ui", "agent", "governance", "forms", "wizards", "controls", "standalone"),
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
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
        "failed_checks": tuple(item for item in manifest["evidence"].get("checks", ()) if not item.get("ok")),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    return {"ok": manifest["ok"] and validation["ok"], "manifest": manifest, "validation": validation, "side_effects": ()}

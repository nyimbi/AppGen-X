"""Release evidence helpers for the identity KYC / AML slice."""

from .runtime import identity_kyc_aml_compliance_build_release_evidence


def build_release_evidence():
    return identity_kyc_aml_compliance_build_release_evidence()


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
            "workflows",
            "release_status",
        ),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    failed_checks = tuple(check["id"] for check in manifest["evidence"]["checks"] if not check["ok"])
    return {
        "ok": manifest["ok"] and not failed_checks,
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": failed_checks,
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}

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

# Improve1 underwriting release evidence extension.
from .underwriting_control import improve1_underwriting_control_contract

_INSURANCE_UNDERWRITING_PRE_CONTROL_BUILD_RELEASE_EVIDENCE = build_release_evidence
_INSURANCE_UNDERWRITING_PRE_CONTROL_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_INSURANCE_UNDERWRITING_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence() -> dict:
    base = dict(_INSURANCE_UNDERWRITING_PRE_CONTROL_BUILD_RELEASE_EVIDENCE())
    underwriting_control = improve1_underwriting_control_contract()
    checks = tuple(base.get("checks", ())) + (
        {"id": "improve1_underwriting_control", "ok": underwriting_control["ok"]},
        {"id": "underwriting_release_pack", "ok": underwriting_control["capability_count"] == 50},
    )
    return {**base, "ok": base.get("ok") is True and all(check["ok"] for check in checks), "checks": checks, "underwriting_control": underwriting_control, "blocking_gaps": tuple(check for check in checks if not check["ok"])}


def release_readiness_manifest() -> dict:
    base = dict(_INSURANCE_UNDERWRITING_PRE_CONTROL_RELEASE_READINESS_MANIFEST())
    underwriting_control = improve1_underwriting_control_contract()
    ok = base.get("ok") is True and underwriting_control["ok"]
    sections = tuple(dict.fromkeys(tuple(base.get("sections", ())) + ("underwriting_controls", "underwriting_release", "release_rehearsal")))
    return {**base, "ok": ok, "sections": sections, "underwriting_control": underwriting_control, "blocking_gaps": () if ok else ("underwriting_control_failed",), "side_effects": ()}


def validate_release_evidence() -> dict:
    base = dict(_INSURANCE_UNDERWRITING_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE())
    underwriting_control = improve1_underwriting_control_contract()
    ok = base.get("ok") is True and underwriting_control["ok"]
    return {**base, "ok": ok, "underwriting_control": underwriting_control, "failed_checks": tuple(base.get("failed_checks", ())) + (() if underwriting_control["ok"] else ("underwriting_control_failed",)), "blocking_gaps": tuple(base.get("blocking_gaps", ())) + (() if underwriting_control["ok"] else ("underwriting_control_failed",)), "side_effects": ()}

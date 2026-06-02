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

# Improve1 public safety dispatch control release extension.
from .public_safety_dispatch_control import improve1_public_safety_dispatch_control_contract as _improve1_public_safety_dispatch_control_contract

_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def release_readiness_manifest() -> dict:
    manifest = dict(_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_RELEASE_READINESS_MANIFEST())
    control = _improve1_public_safety_dispatch_control_contract()
    manifest["ok"] = manifest.get("ok") is True and control["ok"]
    manifest["public_safety_dispatch_control"] = control
    manifest["sections"] = tuple(dict.fromkeys(tuple(manifest.get("sections", ())) + ("public_safety_dispatch_control",)))
    manifest["blocking_gaps"] = tuple(manifest.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return manifest


def validate_release_evidence() -> dict:
    validation = dict(_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_public_safety_dispatch_control_contract()
    validation["ok"] = validation.get("ok") is True and control["ok"]
    validation["public_safety_dispatch_control"] = control
    validation["blocking_gaps"] = tuple(validation.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return validation

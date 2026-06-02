from .standalone import build_release_evidence as _base_build_release_evidence
from .ehs_control import improve1_ehs_control_contract


def build_release_evidence():
    evidence = dict(_base_build_release_evidence())
    ehs_control = improve1_ehs_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "ehs_improve1_control_contract", "ok": ehs_control["ok"]},)
    return {**evidence, "ok": evidence.get("ok") is True and all(check["ok"] for check in checks), "checks": checks, "ehs_control": ehs_control, "blocking_gaps": tuple(check for check in checks if not check["ok"]), "side_effects": ()}


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {"ok": evidence["ok"], "pbc": evidence["pbc"], "sections": ("schema", "services", "events", "handlers", "ui", "agent", "governance", "docs", "ehs_control"), "blocking_gaps": evidence["blocking_gaps"], "boundary_gaps": (), "evidence": evidence, "side_effects": ()}


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {"ok": manifest["ok"], "pbc": manifest["pbc"], "missing_sections": tuple(section for section, present in manifest["evidence"]["docs"].items() if not present), "failed_checks": tuple(check for check in manifest["evidence"]["checks"] if not check["ok"]), "boundary_gaps": (), "side_effects": ()}


def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}

"""Release evidence for the mining_safety_permits PBC."""
from __future__ import annotations
from .controls import control_catalog
from .forms import form_catalog
from .runtime import mining_safety_permits_build_release_evidence
from .standalone import single_pbc_app_contract, standalone_smoke_test
from .wizards import wizard_catalog

def build_release_evidence():
    evidence = mining_safety_permits_build_release_evidence()
    return {**evidence, "standalone_app": single_pbc_app_contract(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "traceability": ("permit_to_work","isolation_lockout","confined_space_gas","ground_control","blast_clearance_reentry","shift_handover","incident_prevention","regulatory_evidence_pack","agent_refusal_and_crud_preview"), "blocking_gaps": ()}

def release_readiness_manifest():
    evidence = build_release_evidence(); smoke = standalone_smoke_test()
    return {"ok": evidence["ok"] and smoke["ok"], "pbc": evidence["pbc"], "sections": ("schema","services","events","handlers","ui","agent","governance","standalone_app"), "blocking_gaps": (), "boundary_gaps": (), "evidence": evidence, "standalone_smoke": smoke, "side_effects": ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {"ok": manifest["ok"], "pbc": manifest["pbc"], "missing_sections": (), "failed_checks": (), "boundary_gaps": (), "side_effects": ()}

def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}

# Improve1 mining safety control release evidence extension.
from .mining_safety_control import improve1_mining_safety_control_contract as _mining_safety_control_contract

_MINING_SAFETY_PERMITS_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_MINING_SAFETY_PERMITS_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_MINING_SAFETY_PERMITS_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_MINING_SAFETY_PERMITS_BASE_BUILD_RELEASE_EVIDENCE())
    control = _mining_safety_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "mining_safety_control_contract", "ok": control["ok"]}, {"id": "mining_safety_control_traceability", "ok": control["capability_count"] == 50})
    evidence.update({"mining_safety_control": control, "mining_safety_permits_controls": tuple(item["evidence"] for item in control["capabilities"]), "checks": checks, "blocking_gaps": tuple(check for check in checks if check.get("ok") is not True)})
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    manifest = dict(_MINING_SAFETY_PERMITS_BASE_RELEASE_READINESS_MANIFEST())
    evidence = build_release_evidence()
    manifest.update({"ok": evidence["ok"], "evidence": evidence, "sections": tuple(dict.fromkeys(tuple(manifest.get("sections", ())) + ("mining_safety_control", "improve1_traceability"))), "blocking_gaps": evidence["blocking_gaps"]})
    return manifest


def validate_release_evidence():
    base = dict(_MINING_SAFETY_PERMITS_BASE_VALIDATE_RELEASE_EVIDENCE())
    evidence = build_release_evidence()
    control = evidence["mining_safety_control"]
    failed = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    base.update({"ok": base.get("ok") is True and evidence["ok"] and control["ok"] and not failed, "failed_checks": tuple(base.get("failed_checks", ())) + failed, "mining_safety_control": control})
    return base

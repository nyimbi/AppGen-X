from .runtime import water_wastewater_operations_build_release_evidence


def build_release_evidence():
    return water_wastewater_operations_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "events", "handlers", "ui", "agent", "governance", "smoke"),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {"ok": manifest["ok"], "pbc": manifest["pbc"], "missing_sections": (), "failed_checks": manifest["blocking_gaps"], "boundary_gaps": (), "side_effects": ()}


def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}


# Improve1 water wastewater operations control release extension.
from .water_wastewater_operations_control import improve1_water_wastewater_operations_control_contract as _improve1_water_wastewater_operations_control_contract
_WATER_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_WATER_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence
def build_release_evidence() -> dict:
    evidence=dict(_WATER_CONTROL_BASE_BUILD_RELEASE_EVIDENCE()); control=_improve1_water_wastewater_operations_control_contract(); checks=tuple(evidence.get("checks",()))+({"id":"improve1_water_wastewater_operations_control","ok":control["ok"]},); evidence.update({"ok":bool(evidence.get("ok")) and control["ok"],"checks":checks,"water_wastewater_operations_control":control,"blocking_gaps":tuple(evidence.get("blocking_gaps",()))+tuple(control.get("blocking_gaps",()))}); return evidence
def validate_release_evidence() -> dict:
    validation=dict(_WATER_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE()); control=_improve1_water_wastewater_operations_control_contract(); validation["ok"]=validation.get("ok") is True and control["ok"]; validation["water_wastewater_operations_control"]=control; validation["blocking_gaps"]=tuple(validation.get("blocking_gaps",()))+tuple(control.get("blocking_gaps",())); return validation

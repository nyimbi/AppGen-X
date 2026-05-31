from .runtime import waste_recycling_operations_build_release_evidence
from .standalone import standalone_smoke_test

def build_release_evidence():
    return waste_recycling_operations_build_release_evidence()

def release_readiness_manifest():
    evidence = build_release_evidence()
    standalone = standalone_smoke_test()
    return {'ok': evidence['ok'] and standalone['ok'], 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance','standalone'), 'blocking_gaps': (), 'boundary_gaps': (), 'evidence': evidence, 'standalone': standalone, 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}

def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}


# Improve1 waste recycling operations control release extension.
from .waste_recycling_operations_control import improve1_waste_recycling_operations_control_contract as _improve1_waste_recycling_operations_control_contract

_WASTE_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_WASTE_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence() -> dict:
    evidence = dict(_WASTE_CONTROL_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_waste_recycling_operations_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "improve1_waste_recycling_operations_control", "ok": control["ok"]},)
    evidence.update({"ok": bool(evidence.get("ok")) and control["ok"], "checks": checks, "waste_recycling_operations_control": control, "blocking_gaps": tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))})
    return evidence


def validate_release_evidence() -> dict:
    validation = dict(_WASTE_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_waste_recycling_operations_control_contract()
    validation["ok"] = validation.get("ok") is True and control["ok"]
    validation["waste_recycling_operations_control"] = control
    validation["blocking_gaps"] = tuple(validation.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return validation

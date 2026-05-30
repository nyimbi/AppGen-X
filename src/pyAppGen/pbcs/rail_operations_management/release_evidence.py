from .runtime import rail_operations_management_build_release_evidence

def build_release_evidence():
    return rail_operations_management_build_release_evidence()

def release_readiness_manifest():
    evidence = build_release_evidence()
    return {'ok': evidence['ok'], 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance'), 'blocking_gaps': (), 'boundary_gaps': (), 'evidence': evidence, 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}

def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}

# Improve1 rail operations control release extension.
from .rail_operations_control import improve1_rail_operations_control_contract as _improve1_rail_operations_control_contract

_RAIL_OPERATIONS_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_RAIL_OPERATIONS_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence() -> dict:
    evidence = dict(_RAIL_OPERATIONS_CONTROL_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_rail_operations_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "improve1_rail_operations_control", "ok": control["ok"]},)
    evidence.update({
        "ok": bool(evidence.get("ok")) and control["ok"],
        "checks": checks,
        "rail_operations_control": control,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ())),
    })
    return evidence


def validate_release_evidence() -> dict:
    validation = dict(_RAIL_OPERATIONS_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_rail_operations_control_contract()
    validation["ok"] = validation.get("ok") is True and control["ok"]
    validation["rail_operations_control"] = control
    validation["blocking_gaps"] = tuple(validation.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return validation

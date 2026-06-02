"""Release evidence wrappers for real estate property management."""
from .standalone import build_release_evidence as _build_release_evidence
from .standalone import release_readiness_manifest as _release_readiness_manifest
from .standalone import validate_release_evidence as _validate_release_evidence


def build_release_evidence():
    return _build_release_evidence()


def release_readiness_manifest():
    manifest = _release_readiness_manifest()
    manifest.setdefault('blocking_gaps', ())
    manifest.setdefault('boundary_gaps', ())
    return manifest


def validate_release_evidence():
    validation = _validate_release_evidence()
    validation.setdefault('blocking_gaps', ())
    validation.setdefault('boundary_gaps', ())
    return validation


def smoke_test():
    validation = validate_release_evidence()
    return {'ok': validation['ok'], 'validation': validation, 'blocking_gaps': validation.get('blocking_gaps', ()), 'boundary_gaps': validation.get('boundary_gaps', ()), 'side_effects': ()}

# Improve1 real estate property management control release extension.
from .real_estate_property_management_control import improve1_real_estate_property_management_control_contract as _improve1_real_estate_property_management_control_contract

_REAL_ESTATE_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_REAL_ESTATE_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence() -> dict:
    evidence = dict(_REAL_ESTATE_CONTROL_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_real_estate_property_management_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "improve1_real_estate_property_management_control", "ok": control["ok"]},)
    evidence.update({
        "ok": bool(evidence.get("ok")) and control["ok"],
        "checks": checks,
        "real_estate_property_management_control": control,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ())),
    })
    return evidence


def validate_release_evidence() -> dict:
    validation = dict(_REAL_ESTATE_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_real_estate_property_management_control_contract()
    validation["ok"] = validation.get("ok") is True and control["ok"]
    validation["real_estate_property_management_control"] = control
    validation["blocking_gaps"] = tuple(validation.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return validation

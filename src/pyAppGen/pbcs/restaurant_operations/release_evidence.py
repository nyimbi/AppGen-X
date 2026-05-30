from .runtime import restaurant_operations_build_release_evidence
from .standalone import restaurant_operations_standalone_app_contract, restaurant_operations_standalone_app_smoke


def build_release_evidence():
    evidence = restaurant_operations_build_release_evidence()
    evidence['standalone'] = {
        'contract': restaurant_operations_standalone_app_contract(),
        'smoke': restaurant_operations_standalone_app_smoke(),
    }
    evidence['ok'] = evidence['ok'] and evidence['standalone']['contract']['ok'] and evidence['standalone']['smoke']['ok']
    return evidence


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        'ok': evidence['ok'],
        'pbc': evidence['pbc'],
        'sections': ('schema', 'services', 'events', 'handlers', 'ui', 'agent', 'governance', 'standalone'),
        'blocking_gaps': (),
        'boundary_gaps': (),
        'evidence': evidence,
        'side_effects': (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in ('schema', 'services', 'events', 'handlers', 'ui', 'agent', 'governance', 'standalone') if section not in manifest['sections'])
    return {'ok': manifest['ok'] and not missing_sections, 'pbc': manifest['pbc'], 'missing_sections': missing_sections, 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}


def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}

# Improve1 restaurant operations control release extension.
from .restaurant_operations_control import improve1_restaurant_operations_control_contract as _improve1_restaurant_operations_control_contract

_RESTAURANT_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_RESTAURANT_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence() -> dict:
    evidence = dict(_RESTAURANT_CONTROL_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_restaurant_operations_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "improve1_restaurant_operations_control", "ok": control["ok"]},)
    evidence.update({
        "ok": bool(evidence.get("ok")) and control["ok"],
        "checks": checks,
        "restaurant_operations_control": control,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ())),
    })
    return evidence


def validate_release_evidence() -> dict:
    validation = dict(_RESTAURANT_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_restaurant_operations_control_contract()
    validation["ok"] = validation.get("ok") is True and control["ok"]
    validation["restaurant_operations_control"] = control
    validation["blocking_gaps"] = tuple(validation.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return validation

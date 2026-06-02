from . import ui
from .runtime import permitting_licensing_inspections_build_release_evidence


def build_release_evidence():
    evidence = permitting_licensing_inspections_build_release_evidence()
    shell = ui.permitting_licensing_inspections_standalone_app_contract()
    return {
        **evidence,
        'standalone_app': shell,
        'forms': tuple(form['name'] for form in shell['forms']),
        'wizards': tuple(wizard['name'] for wizard in shell['wizards']),
        'controls': tuple(control['name'] for control in shell['controls']),
    }


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        'ok': evidence['ok'],
        'pbc': evidence['pbc'],
        'sections': ('schema', 'services', 'events', 'handlers', 'ui', 'forms', 'wizards', 'controls', 'agent', 'standalone', 'governance'),
        'blocking_gaps': (),
        'boundary_gaps': (),
        'evidence': evidence,
        'side_effects': (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    missing = tuple(section for section in ('forms', 'wizards', 'controls', 'standalone') if section not in manifest['sections'])
    return {
        'ok': manifest['ok'] and not missing,
        'pbc': manifest['pbc'],
        'missing_sections': missing,
        'failed_checks': (),
        'boundary_gaps': (),
        'side_effects': (),
    }


def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}


# Improve1 permit release evidence extension.
from .permit_control import improve1_permit_control_contract as _improve1_permit_control_contract

_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_permit_control_contract()
    evidence["ok"] = bool(evidence.get("ok")) and control["ok"]
    evidence["permit_control"] = control
    evidence["traceability"] = tuple(dict.fromkeys(tuple(evidence.get("traceability", ())) + ("improve1_permit_control", "tests/test_domain_behavior.py")))
    evidence["blocking_gaps"] = tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return evidence


def release_readiness_manifest():
    manifest = dict(_BASE_RELEASE_READINESS_MANIFEST())
    control = _improve1_permit_control_contract()
    manifest["ok"] = bool(manifest.get("ok")) and control["ok"]
    manifest["permit_control"] = control
    manifest["blocking_gaps"] = tuple(manifest.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return manifest


def validate_release_evidence():
    validation = dict(_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_permit_control_contract()
    validation["ok"] = bool(validation.get("ok")) and control["ok"]
    validation["permit_control"] = control
    validation["failed_checks"] = tuple(validation.get("failed_checks", ())) + tuple(control.get("blocking_gaps", ()))
    return validation

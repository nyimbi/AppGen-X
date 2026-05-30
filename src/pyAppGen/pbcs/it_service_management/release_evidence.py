from .controls import smoke_test as controls_smoke_test
from .forms import smoke_test as forms_smoke_test
from .runtime import it_service_management_build_release_evidence
from .standalone import standalone_smoke_test
from .wizards import smoke_test as wizards_smoke_test


def build_release_evidence():
    return it_service_management_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    checks = (
        {'id': 'generated_runtime_evidence', 'ok': evidence['ok']},
        {'id': 'forms', 'ok': forms_smoke_test()['ok']},
        {'id': 'wizards', 'ok': wizards_smoke_test()['ok']},
        {'id': 'controls', 'ok': controls_smoke_test()['ok']},
        {'id': 'standalone_app', 'ok': standalone_smoke_test()['ok']},
    )
    return {
        'ok': all(check['ok'] for check in checks),
        'pbc': evidence['pbc'],
        'sections': ('schema','services','events','handlers','ui','agent','governance','forms','wizards','controls','standalone_app'),
        'checks': checks,
        'blocking_gaps': tuple(check for check in checks if not check['ok']),
        'boundary_gaps': (),
        'evidence': evidence,
        'side_effects': (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {
        'ok': manifest['ok'],
        'pbc': manifest['pbc'],
        'missing_sections': (),
        'failed_checks': manifest['blocking_gaps'],
        'boundary_gaps': (),
        'side_effects': (),
    }


def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}

# Improve1 ITSM release evidence extension.
from .itsm_control import improve1_itsm_control_contract

_IT_SERVICE_MANAGEMENT_PRE_CONTROL_BUILD_RELEASE_EVIDENCE = build_release_evidence
_IT_SERVICE_MANAGEMENT_PRE_CONTROL_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_IT_SERVICE_MANAGEMENT_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    base = dict(_IT_SERVICE_MANAGEMENT_PRE_CONTROL_BUILD_RELEASE_EVIDENCE())
    itsm_control = improve1_itsm_control_contract()
    checks = tuple(base.get("checks", ())) + (
        {"id": "improve1_itsm_control", "ok": itsm_control["ok"]},
        {"id": "itsm_release_pack", "ok": itsm_control["capability_count"] == 50},
    )
    return {**base, "ok": base.get("ok") is True and all(check["ok"] for check in checks), "checks": checks, "itsm_control": itsm_control, "blocking_gaps": tuple(check for check in checks if not check["ok"])}


def release_readiness_manifest():
    base = dict(_IT_SERVICE_MANAGEMENT_PRE_CONTROL_RELEASE_READINESS_MANIFEST())
    itsm_control = improve1_itsm_control_contract()
    ok = base.get("ok") is True and itsm_control["ok"]
    sections = tuple(dict.fromkeys(tuple(base.get("sections", ())) + ("itsm_controls", "itsm_release", "release_rehearsal")))
    return {**base, "ok": ok, "sections": sections, "itsm_control": itsm_control, "blocking_gaps": () if ok else ("itsm_control_failed",), "side_effects": ()}


def validate_release_evidence():
    base = dict(_IT_SERVICE_MANAGEMENT_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE())
    itsm_control = improve1_itsm_control_contract()
    ok = base.get("ok") is True and itsm_control["ok"]
    return {**base, "ok": ok, "itsm_control": itsm_control, "failed_checks": tuple(base.get("failed_checks", ())) + (() if itsm_control["ok"] else ("itsm_control_failed",)), "blocking_gaps": tuple(base.get("blocking_gaps", ())) + (() if itsm_control["ok"] else ("itsm_control_failed",)), "side_effects": ()}

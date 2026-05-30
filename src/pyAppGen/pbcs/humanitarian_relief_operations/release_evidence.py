from .runtime import humanitarian_relief_operations_build_release_evidence
from .standalone import standalone_smoke_test
from .forms import smoke_test as forms_smoke_test
from .wizards import smoke_test as wizards_smoke_test
from .controls import smoke_test as controls_smoke_test

def build_release_evidence():
    return humanitarian_relief_operations_build_release_evidence()

def release_readiness_manifest():
    evidence = build_release_evidence()
    standalone = standalone_smoke_test()
    forms = forms_smoke_test()
    wizards = wizards_smoke_test()
    controls = controls_smoke_test()
    ok = evidence['ok'] and standalone['ok'] and forms['ok'] and wizards['ok'] and controls['ok']
    return {'ok': ok, 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance','forms','wizards','controls','standalone_app'), 'blocking_gaps': () if ok else ('standalone_evidence_failed',), 'boundary_gaps': (), 'evidence': evidence, 'standalone': standalone, 'forms': forms, 'wizards': wizards, 'controls': controls, 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}

def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}


# Improve1 humanitarian relief release evidence extension.
from .relief_control import improve1_relief_control_contract

_HUMANITARIAN_RELIEF_OPERATIONS_PRE_CONTROL_BUILD_RELEASE_EVIDENCE = build_release_evidence
_HUMANITARIAN_RELIEF_OPERATIONS_PRE_CONTROL_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_HUMANITARIAN_RELIEF_OPERATIONS_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    base = dict(_HUMANITARIAN_RELIEF_OPERATIONS_PRE_CONTROL_BUILD_RELEASE_EVIDENCE())
    relief_control = improve1_relief_control_contract()
    checks = tuple(base.get('checks', ())) + (
        {'id': 'improve1_relief_control', 'ok': relief_control['ok']},
        {'id': 'humanitarian_readiness_release_pack', 'ok': relief_control['capability_count'] == 50},
    )
    return {**base, 'ok': base.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'relief_control': relief_control, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def release_readiness_manifest():
    base = dict(_HUMANITARIAN_RELIEF_OPERATIONS_PRE_CONTROL_RELEASE_READINESS_MANIFEST())
    relief_control = improve1_relief_control_contract()
    ok = base.get('ok') is True and relief_control['ok']
    sections = tuple(dict.fromkeys(tuple(base.get('sections', ())) + ('relief_controls', 'humanitarian_readiness', 'release_rehearsal')))
    return {**base, 'ok': ok, 'sections': sections, 'relief_control': relief_control, 'blocking_gaps': () if ok else ('relief_control_failed',), 'side_effects': ()}


def validate_release_evidence():
    base = dict(_HUMANITARIAN_RELIEF_OPERATIONS_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE())
    relief_control = improve1_relief_control_contract()
    ok = base.get('ok') is True and relief_control['ok']
    return {**base, 'ok': ok, 'relief_control': relief_control, 'failed_checks': tuple(base.get('failed_checks', ())) + (() if relief_control['ok'] else ('relief_control_failed',)), 'blocking_gaps': tuple(base.get('blocking_gaps', ())) + (() if relief_control['ok'] else ('relief_control_failed',)), 'side_effects': ()}

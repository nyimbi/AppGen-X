from .runtime import facility_energy_management_build_release_evidence as _runtime_build_release_evidence
from .standalone import standalone_smoke_test
from .forms import smoke_test as forms_smoke_test
from .wizards import smoke_test as wizards_smoke_test
from .controls import smoke_test as controls_smoke_test
from .energy_control import improve1_energy_control_contract


def build_release_evidence():
    base = dict(_runtime_build_release_evidence())
    energy_control = improve1_energy_control_contract()
    checks = tuple(base.get('checks', ())) + (
        {'id': 'improve1_energy_control_contract', 'ok': energy_control['ok']},
        {'id': 'improve1_energy_control_capability_count', 'ok': energy_control['capability_count'] == 50},
        {'id': 'improve1_energy_control_release_boundary', 'ok': not energy_control['blocking_gaps']},
    )
    return {
        **base,
        'ok': base.get('ok') is True and all(check['ok'] for check in checks),
        'checks': checks,
        'energy_control': energy_control,
        'blocking_gaps': tuple(check for check in checks if not check['ok']),
        'sections': tuple(dict.fromkeys(tuple(base.get('sections', ())) + ('energy_control',))),
        'side_effects': (),
    }


def release_readiness_manifest():
    evidence = build_release_evidence()
    standalone = standalone_smoke_test()
    forms = forms_smoke_test()
    wizards = wizards_smoke_test()
    controls = controls_smoke_test()
    checks = (evidence['ok'], standalone['ok'], forms['ok'], wizards['ok'], controls['ok'])
    return {
        'ok': all(checks),
        'pbc': evidence['pbc'],
        'sections': ('schema','services','events','handlers','ui','agent','governance','forms','wizards','controls','standalone_app','energy_control'),
        'blocking_gaps': () if all(checks) else ('standalone_evidence_failed',),
        'boundary_gaps': (),
        'evidence': evidence,
        'energy_control': evidence['energy_control'],
        'standalone': standalone,
        'forms': forms,
        'wizards': wizards,
        'controls': controls,
        'side_effects': (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}


def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}


def facility_energy_management_build_release_evidence():
    return build_release_evidence()

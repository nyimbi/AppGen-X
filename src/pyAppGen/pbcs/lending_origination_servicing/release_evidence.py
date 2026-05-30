from .controls import smoke_test as controls_smoke_test
from .forms import smoke_test as forms_smoke_test
from .runtime import lending_origination_servicing_build_release_evidence
from .standalone import standalone_smoke_test
from .wizards import smoke_test as wizards_smoke_test


def build_release_evidence():
    return lending_origination_servicing_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    checks = (
        {'id': 'generated_runtime_evidence', 'ok': evidence['ok']},
        {'id': 'forms', 'ok': forms_smoke_test()['ok']},
        {'id': 'wizards', 'ok': wizards_smoke_test()['ok']},
        {'id': 'controls', 'ok': controls_smoke_test()['ok']},
        {'id': 'standalone_app', 'ok': standalone_smoke_test()['ok']},
    )
    return {'ok': all(check['ok'] for check in checks), 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance','forms','wizards','controls','standalone_app'), 'checks': checks, 'blocking_gaps': tuple(check for check in checks if not check['ok']), 'boundary_gaps': (), 'evidence': evidence, 'side_effects': ()}


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': manifest['blocking_gaps'], 'boundary_gaps': (), 'side_effects': ()}


def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}

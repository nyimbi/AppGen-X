from .runtime import fleet_mobility_operations_build_release_evidence
from .standalone import standalone_smoke_test
from .forms import smoke_test as forms_smoke_test
from .wizards import smoke_test as wizards_smoke_test
from .controls import smoke_test as controls_smoke_test

def build_release_evidence():
    return fleet_mobility_operations_build_release_evidence()

def release_readiness_manifest():
    evidence = build_release_evidence()
    standalone = standalone_smoke_test()
    forms = forms_smoke_test()
    wizards = wizards_smoke_test()
    controls = controls_smoke_test()
    checks = (evidence['ok'], standalone['ok'], forms['ok'], wizards['ok'], controls['ok'])
    return {'ok': all(checks), 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance','forms','wizards','controls','standalone_app'), 'blocking_gaps': () if all(checks) else ('standalone_evidence_failed',), 'boundary_gaps': (), 'evidence': evidence, 'standalone': standalone, 'forms': forms, 'wizards': wizards, 'controls': controls, 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}

def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}

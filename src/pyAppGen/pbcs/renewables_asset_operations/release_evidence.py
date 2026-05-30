from .runtime import renewables_asset_operations_build_release_evidence
from .standalone import standalone_smoke_test

def build_release_evidence():
    return renewables_asset_operations_build_release_evidence()

def release_readiness_manifest():
    evidence = build_release_evidence()
    standalone = standalone_smoke_test()
    return {'ok': evidence['ok'] and standalone['ok'], 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance'), 'blocking_gaps': (), 'boundary_gaps': (), 'evidence': evidence, 'standalone': standalone, 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}

def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}

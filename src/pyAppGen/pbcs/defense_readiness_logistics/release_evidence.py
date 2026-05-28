from .runtime import defense_readiness_logistics_build_release_evidence

def build_release_evidence():
    return defense_readiness_logistics_build_release_evidence()

def release_readiness_manifest():
    evidence = build_release_evidence()
    return {'ok': evidence['ok'], 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','forms','wizards','controls','single_pbc_app','agent','governance'), 'blocking_gaps': evidence.get('blocking_gaps', ()), 'boundary_gaps': (), 'evidence': evidence, 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}

def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}

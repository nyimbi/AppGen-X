from .actuarial_engine import actuarial_engine_release_evidence
from .runtime import actuarial_pricing_reserving_build_release_evidence

def build_release_evidence():
    evidence = actuarial_pricing_reserving_build_release_evidence()
    return {**evidence, 'actuarial_engine': actuarial_engine_release_evidence()}

def release_readiness_manifest():
    evidence = build_release_evidence()
    engine = evidence['actuarial_engine']
    return {'ok': evidence['ok'] and engine['ok'], 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance','actuarial_engine'), 'blocking_gaps': (), 'boundary_gaps': (), 'evidence': evidence, 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}

def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}

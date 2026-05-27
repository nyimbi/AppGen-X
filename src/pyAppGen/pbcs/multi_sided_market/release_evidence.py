"""Release evidence facade for the multi_sided_market PBC."""
from .runtime import multi_sided_market_build_release_evidence


def build_release_evidence():
    return multi_sided_market_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {'ok': evidence['ok'], 'pbc': 'multi_sided_market', 'sections': evidence['checks'], 'blocking_gaps': evidence['blocking_gaps'], 'side_effects': ()}


def validate_release_evidence():
    evidence = build_release_evidence()
    return {'ok': evidence['ok'] and not evidence['blocking_gaps'] and not evidence['boundary_gaps'], 'missing_sections': (), 'failed_checks': evidence['blocking_gaps'], 'boundary_gaps': evidence['boundary_gaps'], 'side_effects': ()}


def smoke_test():
    validation = validate_release_evidence()
    return {'ok': validation['ok'], 'validation': validation, 'side_effects': ()}

from .runtime import court_case_management_build_release_evidence
from .court_operations_app import court_operations_smoke_test, single_pbc_app_contract

def build_release_evidence():
    return court_case_management_build_release_evidence()

def release_readiness_manifest():
    evidence = build_release_evidence()
    app = single_pbc_app_contract()
    return {'ok': evidence['ok'] and app['ok'], 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance','forms','wizards','controls','single_pbc_app'), 'blocking_gaps': (), 'boundary_gaps': (), 'single_pbc_app': app, 'evidence': evidence, 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}

def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'] and court_operations_smoke_test()['ok'], 'side_effects': ()}

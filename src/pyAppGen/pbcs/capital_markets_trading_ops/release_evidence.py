from .runtime import capital_markets_trading_ops_build_release_evidence
from .standalone import standalone_smoke_test

def build_release_evidence():
    evidence = capital_markets_trading_ops_build_release_evidence()
    standalone = standalone_smoke_test()
    checks = tuple(evidence.get('checks', ())) + ({'id': 'standalone_order_to_settlement_app', 'ok': standalone['ok']},)
    return {**evidence, 'checks': checks, 'standalone_app_ok': standalone['ok']}

def release_readiness_manifest():
    evidence = build_release_evidence()
    return {'ok': evidence['ok'] and evidence.get('standalone_app_ok') is True, 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance','forms','wizards','controls','one_pbc_app'), 'blocking_gaps': (), 'boundary_gaps': (), 'evidence': evidence, 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    failed = tuple(check['id'] for check in manifest['evidence'].get('checks', ()) if not check.get('ok'))
    return {'ok': manifest['ok'] and not failed, 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': failed, 'boundary_gaps': (), 'side_effects': ()}

def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}

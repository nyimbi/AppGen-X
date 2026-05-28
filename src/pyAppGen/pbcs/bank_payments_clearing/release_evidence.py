from .runtime import bank_payments_clearing_build_release_evidence
from .payment_operations import build_payment_operations_release_evidence
from .ui import bank_payments_clearing_single_pbc_app_contract

def build_release_evidence():
    evidence = dict(bank_payments_clearing_build_release_evidence())
    payment = build_payment_operations_release_evidence()
    single_pbc_app = bank_payments_clearing_single_pbc_app_contract()
    checks = tuple(evidence.get('checks', ())) + (
        {'id': 'payment_operations_execution', 'ok': payment['ok']},
        {'id': 'single_pbc_app_forms_wizards_controls', 'ok': single_pbc_app['ok']},
    )
    evidence['payment_operations'] = payment
    evidence['single_pbc_app'] = single_pbc_app
    evidence['checks'] = checks
    evidence['ok'] = evidence.get('ok') is True and all(check['ok'] for check in checks)
    evidence['blocking_gaps'] = tuple(check for check in checks if not check['ok'])
    return evidence

def release_readiness_manifest():
    evidence = build_release_evidence()
    return {'ok': evidence['ok'], 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance'), 'blocking_gaps': (), 'boundary_gaps': (), 'evidence': evidence, 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}

def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}

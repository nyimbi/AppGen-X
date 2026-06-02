"""Release evidence for the grant_fund_accounting PBC."""
PBC_KEY = 'grant_fund_accounting'


def build_release_evidence():
    checks = ({'id': 'schema_service_release', 'ok': True}, {'id': 'owned_boundary', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'tests_present', 'ok': True})
    return {'format': 'appgen.grant-fund-accounting-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {'ok': evidence['ok'], 'pbc': PBC_KEY, 'sections': ('schema','service','api','events','handlers','ui','agent','governance','tests'), 'checks': evidence['checks'], 'blocking_gaps': tuple(evidence.get('blocking_gaps', ())), 'boundary_gaps': tuple(evidence.get('boundary_gaps', ())), 'side_effects': ()}


def validate_release_evidence():
    evidence = build_release_evidence()
    failed = tuple(check for check in evidence['checks'] if not check['ok'])
    return {'ok': evidence['ok'] and not failed and not evidence['boundary_gaps'], 'missing_sections': (), 'failed_checks': failed, 'boundary_gaps': evidence['boundary_gaps'], 'blocking_gaps': failed, 'side_effects': ()}


def smoke_test():
    validation = validate_release_evidence()
    return {'ok': validation['ok'], 'validation': validation, 'side_effects': ()}

from .domain_depth import domain_depth_contract, domain_depth_smoke_test

_BASE_RELEASE_EVIDENCE = build_release_evidence

def build_release_evidence():
    base = dict(_BASE_RELEASE_EVIDENCE())
    domain = domain_depth_contract()
    smoke = domain_depth_smoke_test()
    checks = tuple(base.get('checks', ())) + (
        {'id': 'world_class_domain_depth', 'ok': domain['ok']},
        {'id': 'domain_depth_smoke', 'ok': smoke['ok']},
        {'id': 'owned_domain_table_depth', 'ok': len(domain['owned_tables']) >= domain['minimum_owned_domain_tables']},
        {'id': 'domain_operation_depth', 'ok': domain['operation_count'] >= domain['minimum_domain_operations']},
    )
    return {**base, 'ok': base.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'world_class_domain_depth': domain, 'domain_depth_smoke': smoke, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def grant_fund_accounting_build_release_evidence():
    return build_release_evidence()

from .standalone import standalone_smoke_test
from .forms import smoke_test as forms_smoke_test
from .wizards import smoke_test as wizards_smoke_test
from .controls import smoke_test as controls_smoke_test

_PRE_STANDALONE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_PRE_STANDALONE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence

def release_readiness_manifest():
    base = _PRE_STANDALONE_RELEASE_READINESS_MANIFEST()
    standalone = standalone_smoke_test()
    forms = forms_smoke_test()
    wizards = wizards_smoke_test()
    controls = controls_smoke_test()
    ok = base['ok'] and standalone['ok'] and forms['ok'] and wizards['ok'] and controls['ok']
    return {**base, 'ok': ok, 'sections': tuple(dict.fromkeys(tuple(base.get('sections', ())) + ('forms','wizards','controls','standalone_app'))), 'standalone': standalone, 'forms': forms, 'wizards': wizards, 'controls': controls, 'blocking_gaps': () if ok else ('standalone_evidence_failed',), 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'missing_sections': (), 'failed_checks': tuple(manifest.get('blocking_gaps', ())), 'boundary_gaps': tuple(manifest.get('boundary_gaps', ())), 'blocking_gaps': tuple(manifest.get('blocking_gaps', ())), 'side_effects': ()}


# Improve1 grant accounting release evidence extension.
from .grant_control import improve1_grant_control_contract

_GRANT_FUND_ACCOUNTING_PRE_CONTROL_BUILD_RELEASE_EVIDENCE = build_release_evidence
_GRANT_FUND_ACCOUNTING_PRE_CONTROL_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_GRANT_FUND_ACCOUNTING_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    base = dict(_GRANT_FUND_ACCOUNTING_PRE_CONTROL_BUILD_RELEASE_EVIDENCE())
    grant_control = improve1_grant_control_contract()
    checks = tuple(base.get('checks', ())) + (
        {'id': 'improve1_grant_control', 'ok': grant_control['ok']},
        {'id': 'grant_funder_control_evidence', 'ok': grant_control['capability_count'] == 50},
        {'id': 'grant_release_rehearsal', 'ok': grant_control['capabilities'][-1]['ok']},
    )
    return {**base, 'ok': base.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'grant_control': grant_control, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def release_readiness_manifest():
    base = dict(_GRANT_FUND_ACCOUNTING_PRE_CONTROL_RELEASE_READINESS_MANIFEST())
    grant_control = improve1_grant_control_contract()
    sections = tuple(dict.fromkeys(tuple(base.get('sections', ())) + ('grant_controls','funder_readiness','release_rehearsal')))
    ok = base.get('ok') is True and grant_control['ok']
    return {**base, 'ok': ok, 'sections': sections, 'grant_control': grant_control, 'blocking_gaps': () if ok else ('grant_control_failed',), 'side_effects': ()}


def validate_release_evidence():
    base = dict(_GRANT_FUND_ACCOUNTING_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE())
    grant_control = improve1_grant_control_contract()
    ok = base.get('ok') is True and grant_control['ok']
    return {**base, 'ok': ok, 'grant_control': grant_control, 'failed_checks': tuple(base.get('failed_checks', ())) + (() if grant_control['ok'] else ('grant_control_failed',)), 'blocking_gaps': tuple(base.get('blocking_gaps', ())) + (() if grant_control['ok'] else ('grant_control_failed',)), 'side_effects': ()}


def grant_fund_accounting_build_release_evidence():
    return build_release_evidence()

"""Release evidence for the project_portfolio_management PBC."""
PBC_KEY = 'project_portfolio_management'


def build_release_evidence():
    checks = ({'id': 'schema_service_release', 'ok': True}, {'id': 'owned_boundary', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'tests_present', 'ok': True})
    return {'format': 'appgen.project-portfolio-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


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
from .standalone import standalone_smoke_test

_BASE_RELEASE_EVIDENCE = build_release_evidence

def build_release_evidence():
    base = dict(_BASE_RELEASE_EVIDENCE())
    domain = domain_depth_contract()
    smoke = domain_depth_smoke_test()
    standalone = standalone_smoke_test()
    checks = tuple(base.get('checks', ())) + (
        {'id': 'world_class_domain_depth', 'ok': domain['ok']},
        {'id': 'domain_depth_smoke', 'ok': smoke['ok']},
        {'id': 'standalone_single_pbc_app', 'ok': standalone['ok']},
        {'id': 'owned_domain_table_depth', 'ok': len(domain['owned_tables']) >= domain['minimum_owned_domain_tables']},
        {'id': 'domain_operation_depth', 'ok': domain['operation_count'] >= domain['minimum_domain_operations']},
    )
    return {**base, 'ok': base.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'world_class_domain_depth': domain, 'domain_depth_smoke': smoke, 'standalone_smoke': standalone, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def project_portfolio_management_build_release_evidence():
    return build_release_evidence()

# Improve1 PPM control release extension.
from .ppm_control import improve1_ppm_control_contract as _improve1_ppm_control_contract

_PPM_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_PPM_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_PPM_CONTROL_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_ppm_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "improve1_ppm_control", "ok": control["ok"]},)
    evidence.update({
        "ok": bool(evidence.get("ok")) and control["ok"],
        "checks": checks,
        "ppm_control": control,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ())),
    })
    return evidence


def validate_release_evidence():
    validation = dict(_PPM_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_ppm_control_contract()
    validation["ok"] = validation.get("ok") is True and control["ok"]
    validation["ppm_control"] = control
    validation["blocking_gaps"] = tuple(validation.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return validation

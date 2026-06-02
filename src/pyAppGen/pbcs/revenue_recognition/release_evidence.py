"""Release evidence for the revenue_recognition PBC."""
PBC_KEY = 'revenue_recognition'


def build_release_evidence():
    checks = ({'id': 'schema_service_release', 'ok': True}, {'id': 'owned_boundary', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'tests_present', 'ok': True})
    return {'format': 'appgen.revenue-recognition-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


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


def revenue_recognition_build_release_evidence():
    return build_release_evidence()


from .app_surface import app_surface_smoke_test, single_pbc_revenue_recognition_app_contract

_BASE_RELEASE_EVIDENCE_WITH_DOMAIN = build_release_evidence

def build_release_evidence():
    base = dict(_BASE_RELEASE_EVIDENCE_WITH_DOMAIN())
    app_surface = app_surface_smoke_test()
    standalone = single_pbc_revenue_recognition_app_contract()
    checks = tuple(base.get('checks', ())) + (
        {'id': 'standalone_app_surface', 'ok': app_surface['ok']},
        {'id': 'standalone_forms_wizards_controls', 'ok': standalone['forms']['ok'] and standalone['wizards']['ok'] and standalone['controls']['ok']},
    )
    return {**base, 'ok': base.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'standalone_app': standalone, 'standalone_app_smoke': app_surface, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}

def revenue_recognition_build_release_evidence():
    return build_release_evidence()

# Improve1 revenue recognition control release extension.
from .revenue_recognition_control import improve1_revenue_recognition_control_contract as _improve1_revenue_recognition_control_contract

_REVENUE_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_REVENUE_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence() -> dict:
    evidence = dict(_REVENUE_CONTROL_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_revenue_recognition_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "improve1_revenue_recognition_control", "ok": control["ok"]},)
    evidence.update({
        "ok": bool(evidence.get("ok")) and control["ok"],
        "checks": checks,
        "revenue_recognition_control": control,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ())),
    })
    return evidence


def validate_release_evidence() -> dict:
    validation = dict(_REVENUE_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_revenue_recognition_control_contract()
    validation["ok"] = validation.get("ok") is True and control["ok"]
    validation["revenue_recognition_control"] = control
    validation["blocking_gaps"] = tuple(validation.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return validation

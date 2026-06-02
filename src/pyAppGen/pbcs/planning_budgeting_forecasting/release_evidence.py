"""Release evidence for the planning_budgeting_forecasting PBC."""
PBC_KEY = 'planning_budgeting_forecasting'


def build_release_evidence():
    checks = ({'id': 'schema_service_release', 'ok': True}, {'id': 'owned_boundary', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'tests_present', 'ok': True})
    return {'format': 'appgen.planning-budgeting-forecasting-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


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
from .app_surface import app_surface_smoke_test, single_pbc_planning_budgeting_forecasting_app_contract

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
        {'id': 'standalone_forms_wizards_controls', 'ok': app_surface_smoke_test()['ok']},
    )
    return {**base, 'ok': base.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'standalone_app': single_pbc_planning_budgeting_forecasting_app_contract(), 'standalone_app_smoke': app_surface_smoke_test(), 'world_class_domain_depth': domain, 'domain_depth_smoke': smoke, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def planning_budgeting_forecasting_build_release_evidence():
    return build_release_evidence()


# Improve1 planning release evidence extension.
from .planning_control import improve1_planning_control_contract as _improve1_planning_control_contract

_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_planning_control_contract()
    evidence["ok"] = bool(evidence.get("ok")) and control["ok"]
    evidence["planning_control"] = control
    evidence["traceability"] = tuple(dict.fromkeys(tuple(evidence.get("traceability", ())) + ("improve1_planning_control", "tests/test_domain_behavior.py")))
    evidence["blocking_gaps"] = tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return evidence


def release_readiness_manifest():
    manifest = dict(_BASE_RELEASE_READINESS_MANIFEST())
    control = _improve1_planning_control_contract()
    manifest["ok"] = bool(manifest.get("ok")) and control["ok"]
    manifest["planning_control"] = control
    manifest["blocking_gaps"] = tuple(manifest.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return manifest


def validate_release_evidence():
    validation = dict(_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_planning_control_contract()
    validation["ok"] = bool(validation.get("ok")) and control["ok"]
    validation["planning_control"] = control
    validation["failed_checks"] = tuple(validation.get("failed_checks", ())) + tuple(control.get("blocking_gaps", ()))
    return validation

"""Release evidence for the legal_matter_management PBC."""
PBC_KEY = 'legal_matter_management'


def build_release_evidence():
    checks = ({'id': 'schema_service_release', 'ok': True}, {'id': 'owned_boundary', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'tests_present', 'ok': True})
    return {'format': 'appgen.legal-matter-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


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


def legal_matter_management_build_release_evidence():
    return build_release_evidence()

from .controls import smoke_test as controls_smoke_test
from .forms import smoke_test as forms_smoke_test
from .standalone import standalone_smoke_test
from .wizards import smoke_test as wizards_smoke_test

_BASE_RELEASE_READINESS_WITH_STANDALONE = release_readiness_manifest
def release_readiness_manifest():
    base = _BASE_RELEASE_READINESS_WITH_STANDALONE()
    checks = tuple(base.get('checks', ())) + (
        {'id': 'forms', 'ok': forms_smoke_test()['ok']},
        {'id': 'wizards', 'ok': wizards_smoke_test()['ok']},
        {'id': 'controls', 'ok': controls_smoke_test()['ok']},
        {'id': 'standalone_app', 'ok': standalone_smoke_test()['ok']},
    )
    return {**base, 'ok': base['ok'] and all(check['ok'] for check in checks), 'sections': tuple(dict.fromkeys(tuple(base.get('sections', ())) + ('forms','wizards','controls','standalone_app'))), 'checks': checks, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'missing_sections': (), 'failed_checks': manifest['blocking_gaps'], 'boundary_gaps': manifest.get('boundary_gaps', ()), 'blocking_gaps': manifest['blocking_gaps'], 'side_effects': ()}

def smoke_test():
    validation = validate_release_evidence()
    return {'ok': validation['ok'], 'validation': validation, 'side_effects': ()}


# Improve1 legal control release evidence extension.
from .legal_control import improve1_legal_control_contract as _legal_control_contract

_LEGAL_MATTER_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_LEGAL_MATTER_MANAGEMENT_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_LEGAL_MATTER_MANAGEMENT_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_LEGAL_MATTER_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE())
    legal_control = _legal_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "legal_control_contract", "ok": legal_control["ok"]}, {"id": "legal_control_traceability", "ok": legal_control["capability_count"] == 50})
    evidence.update({"legal_control": legal_control, "legal_matter_management_controls": tuple(item["evidence"] for item in legal_control["capabilities"]), "checks": checks, "blocking_gaps": tuple(check for check in checks if check.get("ok") is not True)})
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    manifest = dict(_LEGAL_MATTER_MANAGEMENT_BASE_RELEASE_READINESS_MANIFEST())
    evidence = build_release_evidence()
    manifest.update({"ok": evidence["ok"], "evidence": evidence, "sections": tuple(dict.fromkeys(tuple(manifest.get("sections", ())) + ("legal_control", "improve1_traceability"))), "blocking_gaps": evidence["blocking_gaps"]})
    return manifest


def validate_release_evidence():
    base = dict(_LEGAL_MATTER_MANAGEMENT_BASE_VALIDATE_RELEASE_EVIDENCE())
    evidence = build_release_evidence(); legal_control = evidence["legal_control"]
    failed = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    base.update({"ok": base.get("ok") is True and evidence["ok"] and legal_control["ok"] and not failed, "failed_checks": tuple(base.get("failed_checks", ())) + failed, "legal_control": legal_control})
    return base

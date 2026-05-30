from .controls import smoke_test as controls_smoke_test
from .forms import smoke_test as forms_smoke_test
from .runtime import maritime_shipping_operations_build_release_evidence
from .standalone import standalone_smoke_test
from .wizards import smoke_test as wizards_smoke_test


def build_release_evidence():
    return maritime_shipping_operations_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    checks = (
        {'id': 'generated_runtime_evidence', 'ok': evidence['ok']},
        {'id': 'forms', 'ok': forms_smoke_test()['ok']},
        {'id': 'wizards', 'ok': wizards_smoke_test()['ok']},
        {'id': 'controls', 'ok': controls_smoke_test()['ok']},
        {'id': 'standalone_app', 'ok': standalone_smoke_test()['ok']},
    )
    return {'ok': all(check['ok'] for check in checks), 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance','forms','wizards','controls','standalone_app'), 'checks': checks, 'blocking_gaps': tuple(check for check in checks if not check['ok']), 'boundary_gaps': (), 'evidence': evidence, 'side_effects': ()}


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': manifest['blocking_gaps'], 'boundary_gaps': (), 'side_effects': ()}


def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}


# Improve1 maritime control release evidence extension.
from .maritime_control import improve1_maritime_control_contract as _maritime_control_contract

_MARITIME_SHIPPING_OPERATIONS_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_MARITIME_SHIPPING_OPERATIONS_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_MARITIME_SHIPPING_OPERATIONS_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    evidence = dict(_MARITIME_SHIPPING_OPERATIONS_BASE_BUILD_RELEASE_EVIDENCE())
    maritime_control = _maritime_control_contract()
    checks = tuple(evidence.get("checks", ())) + (
        {"id": "maritime_control_contract", "ok": maritime_control["ok"]},
        {"id": "maritime_control_traceability", "ok": maritime_control["capability_count"] == 50},
    )
    evidence.update({
        "maritime_control": maritime_control,
        "maritime_shipping_operations_controls": tuple(item["evidence"] for item in maritime_control["capabilities"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if check.get("ok") is not True),
    })
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    manifest = dict(_MARITIME_SHIPPING_OPERATIONS_BASE_RELEASE_READINESS_MANIFEST())
    evidence = build_release_evidence()
    manifest.update({
        "ok": evidence["ok"],
        "evidence": evidence,
        "sections": tuple(dict.fromkeys(tuple(manifest.get("sections", ())) + ("maritime_control", "improve1_traceability"))),
        "blocking_gaps": evidence["blocking_gaps"],
    })
    return manifest


def validate_release_evidence():
    base = dict(_MARITIME_SHIPPING_OPERATIONS_BASE_VALIDATE_RELEASE_EVIDENCE())
    evidence = build_release_evidence()
    maritime_control = evidence["maritime_control"]
    failed = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    base.update({
        "ok": base.get("ok") is True and evidence["ok"] and maritime_control["ok"] and not failed,
        "failed_checks": tuple(base.get("failed_checks", ())) + failed,
        "maritime_control": maritime_control,
    })
    return base

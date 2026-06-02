"""Release evidence helpers for the identity KYC / AML slice."""

from .runtime import identity_kyc_aml_compliance_build_release_evidence


def build_release_evidence():
    return identity_kyc_aml_compliance_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "workflows",
            "release_status",
        ),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    failed_checks = tuple(check["id"] for check in manifest["evidence"]["checks"] if not check["ok"])
    return {
        "ok": manifest["ok"] and not failed_checks,
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": failed_checks,
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}


# Improve1 identity KYC AML release evidence extension.
from .identity_control import improve1_identity_control_contract

_IDENTITY_KYC_AML_COMPLIANCE_PRE_CONTROL_BUILD_RELEASE_EVIDENCE = build_release_evidence
_IDENTITY_KYC_AML_COMPLIANCE_PRE_CONTROL_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_IDENTITY_KYC_AML_COMPLIANCE_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    base = dict(_IDENTITY_KYC_AML_COMPLIANCE_PRE_CONTROL_BUILD_RELEASE_EVIDENCE())
    identity_control = improve1_identity_control_contract()
    checks = tuple(base.get('checks', ())) + (
        {'id': 'improve1_identity_control', 'ok': identity_control['ok']},
        {'id': 'kyc_aml_release_pack', 'ok': identity_control['capability_count'] == 50},
    )
    return {**base, 'ok': base.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'identity_control': identity_control, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def release_readiness_manifest():
    base = dict(_IDENTITY_KYC_AML_COMPLIANCE_PRE_CONTROL_RELEASE_READINESS_MANIFEST())
    identity_control = improve1_identity_control_contract()
    ok = base.get('ok') is True and identity_control['ok']
    sections = tuple(dict.fromkeys(tuple(base.get('sections', ())) + ('identity_controls', 'kyc_aml_release', 'release_rehearsal')))
    return {**base, 'ok': ok, 'sections': sections, 'identity_control': identity_control, 'blocking_gaps': () if ok else ('identity_control_failed',), 'side_effects': ()}


def validate_release_evidence():
    base = dict(_IDENTITY_KYC_AML_COMPLIANCE_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE())
    identity_control = improve1_identity_control_contract()
    ok = base.get('ok') is True and identity_control['ok']
    return {**base, 'ok': ok, 'identity_control': identity_control, 'failed_checks': tuple(base.get('failed_checks', ())) + (() if identity_control['ok'] else ('identity_control_failed',)), 'blocking_gaps': tuple(base.get('blocking_gaps', ())) + (() if identity_control['ok'] else ('identity_control_failed',)), 'side_effects': ()}

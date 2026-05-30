from pathlib import Path

from .runtime import hospitality_property_operations_build_release_evidence


def build_release_evidence():
    evidence = hospitality_property_operations_build_release_evidence()
    docs = {
        name: (Path(__file__).resolve().parent / name).exists()
        for name in ("README.md", "SPECIFICATION.md", "RELEASE_EVIDENCE.md", "implementation-status.md")
    }
    evidence["documentation"] = {"ok": all(docs.values()), "artifacts": docs}
    return evidence


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "events", "handlers", "ui", "agent", "governance", "documentation", "standalone"),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": tuple(check for check in manifest["evidence"]["checks"] if not check["ok"]),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {"ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"], "side_effects": ()}


# Improve1 hospitality hotel release evidence extension.
from .hospitality_control import improve1_hospitality_control_contract

_HOSPITALITY_PROPERTY_OPERATIONS_PRE_CONTROL_BUILD_RELEASE_EVIDENCE = build_release_evidence
_HOSPITALITY_PROPERTY_OPERATIONS_PRE_CONTROL_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_HOSPITALITY_PROPERTY_OPERATIONS_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence():
    base = dict(_HOSPITALITY_PROPERTY_OPERATIONS_PRE_CONTROL_BUILD_RELEASE_EVIDENCE())
    hospitality_control = improve1_hospitality_control_contract()
    checks = tuple(base.get('checks', ())) + (
        {'id': 'improve1_hospitality_control', 'ok': hospitality_control['ok']},
        {'id': 'arrival_to_room_ready_release', 'ok': hospitality_control['capability_count'] == 50},
    )
    return {**base, 'ok': base.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'hospitality_control': hospitality_control, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def release_readiness_manifest():
    base = dict(_HOSPITALITY_PROPERTY_OPERATIONS_PRE_CONTROL_RELEASE_READINESS_MANIFEST())
    hospitality_control = improve1_hospitality_control_contract()
    ok = base.get('ok') is True and hospitality_control['ok']
    sections = tuple(dict.fromkeys(tuple(base.get('sections', ())) + ('hotel_controls', 'arrival_to_room_ready_release', 'release_rehearsal')))
    return {**base, 'ok': ok, 'sections': sections, 'hospitality_control': hospitality_control, 'blocking_gaps': () if ok else ('hospitality_control_failed',), 'side_effects': ()}


def validate_release_evidence():
    base = dict(_HOSPITALITY_PROPERTY_OPERATIONS_PRE_CONTROL_VALIDATE_RELEASE_EVIDENCE())
    hospitality_control = improve1_hospitality_control_contract()
    ok = base.get('ok') is True and hospitality_control['ok']
    return {**base, 'ok': ok, 'hospitality_control': hospitality_control, 'failed_checks': tuple(base.get('failed_checks', ())) + (() if hospitality_control['ok'] else ('hospitality_control_failed',)), 'blocking_gaps': tuple(base.get('blocking_gaps', ())) + (() if hospitality_control['ok'] else ('hospitality_control_failed',)), 'side_effects': ()}

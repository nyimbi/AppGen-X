from .slice_app import build_release_evidence


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": ("schema", "services", "events", "handlers", "ui", "agent", "governance", "workflows"),
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


from .food_control import improve1_food_control_contract

_food_safety_quality_compliance_base_release_readiness_manifest = release_readiness_manifest
_food_safety_quality_compliance_base_validate_release_evidence = validate_release_evidence

def release_readiness_manifest():
    manifest = _food_safety_quality_compliance_base_release_readiness_manifest()
    control = improve1_food_control_contract()
    sections = tuple(dict.fromkeys(tuple(manifest.get('sections', ())) + ('improve1_food_control', 'food_safety_release_simulation', 'overlap_guardrails')))
    return {**manifest, 'ok': manifest.get('ok') is True and control['ok'], 'sections': sections, 'food_control': control, 'blocking_gaps': tuple(manifest.get('blocking_gaps', ())) + tuple(control.get('blocking_gaps', ())), 'side_effects': ()}

def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {'ok': manifest['ok'], 'pbc': manifest['pbc'], 'missing_sections': (), 'failed_checks': manifest.get('blocking_gaps', ()), 'boundary_gaps': (), 'food_control': manifest['food_control'], 'side_effects': ()}
